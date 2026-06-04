from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Sequence
from datetime import datetime, timezone
import json
from typing_extensions import override

from nonebot.adapters.discord.api import handle
from nonebot.adapters.discord.api.model import (
    AttachmentSend,
    Embed,
    File,
    InteractionCallbackMessage,
    InteractionResponse,
    RecurrenceRule,
    Snowflake,
    User,
)
from nonebot.adapters.discord.api.types import (
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventRecurrenceRuleFrequency,
    InteractionCallbackType,
)
from nonebot.adapters.discord.config import BotInfo
from tests.fake.doubles import DummyAdapter, DummyBot

from nonebot.drivers import URL, Request, Timeout, WebSocket
import pytest


class CapturedRequestError(Exception):
    def __init__(self, request: Request) -> None:
        super().__init__("request captured")
        self.request = request


async def _capture_request(
    monkeypatch: pytest.MonkeyPatch,
    coro: Awaitable[object],
) -> Request:
    async def fake_request(
        _adapter: object, request: Request, *, parse_json: bool = True
    ) -> None:
        del _adapter, parse_json
        raise CapturedRequestError(request)

    monkeypatch.setattr(handle, "_request", fake_request)
    with pytest.raises(CapturedRequestError) as excinfo:
        await coro
    return excinfo.value.request


def _files_to_mapping(
    files: Sequence[tuple[str, tuple[object, object, object | None]]] | None,
) -> dict[str, tuple[object, object, object | None]]:
    assert files is not None
    return dict(files)


def _payload_json_text(
    files: Sequence[tuple[str, tuple[object, object, object | None]]] | None,
) -> str:
    payload_json = _files_to_mapping(files)["payload_json"][1]
    assert isinstance(payload_json, (bytes, str))
    return payload_json.decode() if isinstance(payload_json, bytes) else payload_json


def _assert_transport_datetime(actual: str, expected: datetime) -> None:
    assert datetime.fromisoformat(actual.replace("Z", "+00:00")) == expected


@pytest.mark.asyncio
async def test_create_message_request_uses_transport_payload_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)

    request = await _capture_request(
        monkeypatch,
        adapter._api_create_message(  # noqa: SLF001
            bot,
            channel_id=1,
            embeds=[Embed(timestamp=timestamp)],
            files=[File(content=b"1", filename="a.txt")],
            attachments=[AttachmentSend(filename="a.txt")],
        ),
    )

    assert request.json is None
    payload = json.loads(_payload_json_text(request.files))
    _assert_transport_datetime(payload["embeds"][0]["timestamp"], timestamp)
    assert payload["attachments"][0]["id"] == 0


@pytest.mark.asyncio
async def test_forum_thread_request_keeps_nested_message_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)

    request = await _capture_request(
        monkeypatch,
        adapter._api_start_thread_in_forum_channel(  # noqa: SLF001
            bot,
            channel_id=1,
            name="thread-name",
            embeds=[Embed(timestamp=timestamp)],
            files=[File(content=b"1", filename="a.txt")],
            attachments=[AttachmentSend(filename="a.txt")],
        ),
    )

    assert request.json is None
    payload = json.loads(_payload_json_text(request.files))
    assert payload["name"] == "thread-name"
    _assert_transport_datetime(payload["message"]["embeds"][0]["timestamp"], timestamp)
    assert payload["message"]["attachments"][0]["id"] == 0


@pytest.mark.asyncio
async def test_interaction_response_request_keeps_nested_data_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)
    interaction_token = f"interaction-{timestamp.timestamp()}"

    request = await _capture_request(
        monkeypatch,
        adapter._api_create_interaction_response(  # noqa: SLF001
            bot,
            interaction_id=1,
            interaction_token=interaction_token,
            response=InteractionResponse(
                type=InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                data=InteractionCallbackMessage(
                    embeds=[Embed(timestamp=timestamp)],
                    files=[File(content=b"1", filename="a.txt")],
                    attachments=[AttachmentSend(filename="a.txt")],
                ),
            ),
        ),
    )

    assert request.json is None
    payload = json.loads(_payload_json_text(request.files))
    _assert_transport_datetime(payload["data"]["embeds"][0]["timestamp"], timestamp)
    assert payload["data"]["attachments"][0]["id"] == 0


@pytest.mark.asyncio
async def test_modify_guild_member_request_serializes_datetime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)

    request = await _capture_request(
        monkeypatch,
        adapter._api_modify_guild_member(  # noqa: SLF001
            bot,
            guild_id=1,
            user_id=2,
            communication_disabled_until=timestamp,
        ),
    )

    _assert_transport_datetime(
        request.json["communication_disabled_until"],
        timestamp,
    )


@pytest.mark.asyncio
async def test_modify_current_user_voice_state_request_serializes_datetime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)

    request = await _capture_request(
        monkeypatch,
        adapter._api_modify_current_user_voice_state(  # noqa: SLF001
            bot,
            guild_id=1,
            request_to_speak_timestamp=timestamp,
        ),
    )

    _assert_transport_datetime(
        request.json["request_to_speak_timestamp"],
        timestamp,
    )


@pytest.mark.asyncio
async def test_create_guild_schedule_event_request_serializes_recurrence_rule(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)

    request = await _capture_request(
        monkeypatch,
        adapter._api_create_guild_schedule_event(  # noqa: SLF001
            bot,
            guild_id=1,
            channel_id=Snowflake(1),
            name="standup",
            privacy_level=GuildScheduledEventPrivacyLevel.GUILD_ONLY,
            scheduled_start_time=timestamp,
            entity_type=GuildScheduledEventEntityType.VOICE,
            recurrence_rule=RecurrenceRule(
                start=timestamp,
                frequency=GuildScheduledEventRecurrenceRuleFrequency.WEEKLY,
                interval=1,
            ),
        ),
    )

    _assert_transport_datetime(request.json["scheduled_start_time"], timestamp)
    _assert_transport_datetime(request.json["recurrence_rule"]["start"], timestamp)


@pytest.mark.asyncio
async def test_gateway_heartbeat_uses_transport_json_text() -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    bot.sequence = 42

    class DummyWS(WebSocket):
        def __init__(self) -> None:
            super().__init__(request=Request("GET", "wss://discord.test/gateway"))
            self.sent: list[str] = []
            self._closed = False

        @property
        @override
        def closed(self) -> bool:
            return self._closed

        @override
        async def accept(self) -> None:
            return None

        @override
        async def close(self, code: int = 1000, reason: str = "") -> None:
            del code, reason
            self._closed = True

        @override
        async def receive(self) -> str:
            msg = "receive should not be called in this test"
            raise AssertionError(msg)

        @override
        async def receive_text(self) -> str:
            msg = "receive_text should not be called in this test"
            raise AssertionError(msg)

        @override
        async def receive_bytes(self) -> bytes:
            msg = "receive_bytes should not be called in this test"
            raise AssertionError(msg)

        @override
        async def send_text(self, data: str) -> None:
            self.sent.append(data)

        @override
        async def send_bytes(self, data: bytes) -> None:
            msg = f"unexpected binary payload: {data!r}"
            raise AssertionError(msg)

    ws = DummyWS()
    await adapter._heartbeat(ws, bot)  # noqa: SLF001

    assert ws.sent == ['{"op":1,"d":42}']


@pytest.mark.asyncio
async def test_gateway_websocket_request_does_not_inherit_api_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = DummyAdapter()
    adapter.discord_config.discord_api_timeout = 30.0
    bot_info = BotInfo(token="x" * 10)
    captured_request: Request | None = None

    class StopForwardError(Exception):
        pass

    class StopWebSocket:
        async def __aenter__(self) -> None:
            msg = "websocket request captured"
            raise RuntimeError(msg)

        async def __aexit__(
            self,
            _exc_type: object,
            _exc: object,
            _traceback: object,
        ) -> None:
            return None

    async def fake_get_bot_user(_bot_info: BotInfo) -> User:
        return User(
            id=Snowflake(1),
            username="bot",
            discriminator="0000",
            avatar=None,
        )

    def fake_websocket(request: Request) -> StopWebSocket:
        nonlocal captured_request
        captured_request = request
        return StopWebSocket()

    async def stop_reconnect_sleep(_delay: float) -> None:
        raise StopForwardError

    monkeypatch.setattr(adapter, "_get_bot_user", fake_get_bot_user)
    monkeypatch.setattr(adapter, "websocket", fake_websocket)
    monkeypatch.setattr(asyncio, "sleep", stop_reconnect_sleep)

    with pytest.raises(StopForwardError):
        await adapter._forward_ws(  # noqa: SLF001
            bot_info,
            URL("wss://gateway.discord.gg"),
            (0, 1),
        )

    assert captured_request is not None
    assert isinstance(captured_request.timeout, Timeout)
    assert (
        captured_request.timeout.connect == adapter.discord_config.discord_api_timeout
    )
    assert captured_request.timeout.read is None
    assert captured_request.timeout.close == 10.0
