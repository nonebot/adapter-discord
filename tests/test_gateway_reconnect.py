import asyncio
from collections.abc import AsyncIterator
import json
from typing import Literal, TypedDict

from nonebot.adapters.discord import Adapter, Bot
from nonebot.adapters.discord.config import BotInfo
from nonebot.adapters.discord.event import (
    Event,
    ReadyEvent,
    ResumedEvent,
    UserUpdateEvent,
)

from nonebot.config import Config, Env
from nonebot.drivers import Request, Response
from nonebot.drivers.websockets import Driver
import pytest
from websockets.asyncio.server import ServerConnection, serve


class GatewayPayload(TypedDict):
    op: int
    d: object


async def receive(ws: ServerConnection) -> GatewayPayload:
    return json.loads(await asyncio.wait_for(ws.recv(), timeout=10))


async def authenticate(
    ws: ServerConnection, *, opcode: int, sequence: int | None
) -> GatewayPayload:
    heartbeat: GatewayPayload = {"op": 1, "d": sequence}
    await ws.send(json.dumps({"op": 10, "d": {"heartbeat_interval": 60000}}))
    assert await receive(ws) == heartbeat
    await ws.send('{"op":11}')
    # The periodic heartbeat also sends once when the task starts.
    first, second = await receive(ws), await receive(ws)
    if first == heartbeat:
        first, second = second, first
    assert first["op"] == opcode
    assert second == heartbeat
    return first


def assert_endpoint(ws: ServerConnection, path: str) -> None:
    assert ws.request is not None
    assert ws.request.path == f"{path}?v=10&encoding=json"


@pytest.fixture
async def gateway_adapter(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[Adapter]:
    driver = Driver(Env(), Config())
    monkeypatch.setattr(Driver, "_bot_connection_hook", set())
    monkeypatch.setattr(Driver, "_bot_disconnection_hook", set())
    adapter = Adapter(driver)
    adapter.discord_config.discord_bots = [
        BotInfo(token="test-token", shard=(0, 1))  # noqa: S106
    ]
    yield adapter
    await asyncio.gather(*adapter.tasks, return_exceptions=True)


@pytest.mark.parametrize("resume_result", ["RESUMED", "INVALID_SESSION"])
async def test_gateway_reconnect_waits_for_session_confirmation(
    monkeypatch: pytest.MonkeyPatch,
    gateway_adapter: Adapter,
    resume_result: Literal["RESUMED", "INVALID_SESSION"],
) -> None:
    connections: asyncio.Queue[ServerConnection] = asyncio.Queue()
    events: asyncio.Queue[type[Event]] = asyncio.Queue()
    user = {"id": "123", "username": "testbot", "discriminator": "0000", "avatar": None}
    driver = gateway_adapter.driver

    async def gateway(ws: ServerConnection) -> None:
        connections.put_nowait(ws)
        await ws.wait_closed()

    async def record_event(_bot: Bot, event: Event) -> None:
        events.put_nowait(type(event))

    monkeypatch.setattr(Bot, "handle_event", record_event)
    async with serve(gateway, "127.0.0.1", 0) as server:
        port = server.sockets[0].getsockname()[1]
        gateway_url = f"ws://127.0.0.1:{port}"

        async def request(_adapter: Adapter, setup: Request) -> Response:
            if setup.url.path.endswith("/gateway/bot"):
                return Response(
                    200,
                    content=json.dumps(
                        {
                            "url": f"{gateway_url}/identify",
                            "shards": 1,
                            "session_start_limit": {
                                "total": 1000,
                                "remaining": 999,
                                "reset_after": 86400000,
                                "max_concurrency": 1,
                            },
                        }
                    ),
                )
            assert setup.url.path.endswith("/users/@me")
            return Response(200, content=json.dumps(user))

        monkeypatch.setattr(Adapter, "request", request)
        ready = {
            "op": 0,
            "s": 42,
            "t": "READY",
            "d": {
                "v": 10,
                "user": user,
                "guilds": [],
                "session_id": "original-session",
                "resume_gateway_url": f"{gateway_url}/resume",
                "application": {"id": "123", "flags": 0},
            },
        }

        async with driver._lifespan:  # noqa: SLF001
            initial = await asyncio.wait_for(connections.get(), timeout=10)
            await authenticate(initial, opcode=2, sequence=None)
            await initial.send(json.dumps(ready))
            assert await asyncio.wait_for(events.get(), timeout=10) is ReadyEvent
            assert "123" in driver.bots

            await initial.send('{"op":7,"d":null}')
            await asyncio.wait_for(initial.wait_closed(), timeout=10)
            resumed = await asyncio.wait_for(connections.get(), timeout=10)
            auth = await authenticate(resumed, opcode=6, sequence=42)
            assert auth["d"] == {
                "token": "Bot test-token",
                "session_id": "original-session",
                "seq": 42,
            }

            # Force a round trip while the Gateway is still withholding confirmation.
            await resumed.send('{"op":1,"d":null}')
            assert await receive(resumed) == {"op": 1, "d": 42}
            assert "123" not in driver.bots
            assert initial.close_code not in (None, 1000, 1001)
            assert_endpoint(resumed, "/resume")

            if resume_result == "RESUMED":
                await resumed.send(
                    json.dumps({"op": 0, "t": "USER_UPDATE", "s": 43, "d": user})
                )
                assert (
                    await asyncio.wait_for(events.get(), timeout=10) is UserUpdateEvent
                )
                assert "123" not in driver.bots
                await resumed.send('{"op":0,"t":"RESUMED","s":44,"d":{}}')
                assert await asyncio.wait_for(events.get(), timeout=10) is ResumedEvent
            else:
                await resumed.send('{"op":9,"d":false}')
                fresh = await asyncio.wait_for(connections.get(), timeout=10)
                assert_endpoint(fresh, "/identify")
                await authenticate(fresh, opcode=2, sequence=None)
                assert "123" not in driver.bots
                await fresh.send(json.dumps(ready))
                assert await asyncio.wait_for(events.get(), timeout=10) is ReadyEvent
            assert "123" in driver.bots
