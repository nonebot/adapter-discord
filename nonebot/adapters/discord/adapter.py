import asyncio
from collections.abc import Callable, Mapping
import contextlib
from functools import lru_cache
import inspect
import json
import sys
from types import UnionType
from typing import Any, cast
from typing_extensions import override

from nonebot.adapters import Adapter as BaseAdapter, Bot as BaseBot

from nonebot.compat import type_validate_json, type_validate_python
from nonebot.drivers import URL, Driver, ForwardDriver, Request, WebSocket
from nonebot.exception import WebSocketClosed
from nonebot.plugin import get_plugin_config
from nonebot.utils import escape_tag

from .api.handle import HandleMixin
from .api.model import GatewayBot, User
from .bot import Bot
from .commands import sync_application_command
from .config import BotInfo, Config
from .event import Event, EventType, MessageEvent, ReadyEvent, event_classes
from .exception import ApiNotAvailable
from .payload import (
    Dispatch,
    Heartbeat,
    HeartbeatAck,
    Hello,
    Identify,
    InvalidSession,
    Payload,
    PayloadType,
    Reconnect,
    Resume,
)
from .utils import decompress_data, log, model_dump

RECONNECT_INTERVAL = 3.0


@lru_cache(maxsize=256)
def _get_handler_params(handler: Callable[..., Any]) -> Mapping[str, inspect.Parameter]:
    """Cache handler signature parameters to avoid repeated introspection."""
    return inspect.signature(handler).parameters


class Adapter(BaseAdapter, HandleMixin):
    @override
    def __init__(self, driver: Driver, **kwargs: Any) -> None:
        super().__init__(driver, **kwargs)
        self.discord_config: Config = get_plugin_config(Config)
        self.tasks: set[asyncio.Task] = set()
        self.base_url: URL = URL(
            f"https://discord.com/api/v{self.discord_config.discord_api_version}",
        )
        self.setup()

    @classmethod
    @override
    def get_name(cls) -> str:
        return "Discord"

    def setup(self) -> None:
        if not isinstance(self.driver, ForwardDriver):
            msg = (
                f"Current driver {self.config.driver} "
                "doesn't support forward connections!"
                "Discord Adapter need a ForwardDriver to work."
            )
            raise RuntimeError(msg)  # noqa: TRY004
        self.on_ready(self.startup)
        self.driver.on_shutdown(self.shutdown)
        self.driver.on_bot_connect(sync_application_command)

    async def startup(self) -> None:
        log("INFO", "Discord Adapter is starting up...")

        log("DEBUG", f"Discord api base url: <y>{escape_tag(str(self.base_url))}</y>")

        for bot_info in self.discord_config.discord_bots:
            self.tasks.add(asyncio.create_task(self.run_bot(bot_info)))

    async def shutdown(self) -> None:
        for task in self.tasks:
            if not task.done():
                task.cancel()

    async def run_bot(self, bot_info: BotInfo) -> None:
        try:
            gateway_info = await self._get_gateway_bot(bot_info)
            ws_url = URL(gateway_info.url)
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Failed to get gateway info.</bg #f8bbd0></r>",
                e,
            )
            return
        remain = (
            gateway_info.session_start_limit
            and gateway_info.session_start_limit.remaining
        )
        if remain and remain <= 0:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Failed to establish connection to Discord "
                "because of session start limit.</bg #f8bbd0></r>\n"
                f"{escape_tag(str(gateway_info))}",
            )
            return

        if bot_info.shard is not None:
            self.tasks.add(
                asyncio.create_task(self._forward_ws(bot_info, ws_url, bot_info.shard)),
            )
            return

        shards = gateway_info.shards or 1
        for i in range(shards):
            self.tasks.add(
                asyncio.create_task(self._forward_ws(bot_info, ws_url, (i, shards))),
            )
            await asyncio.sleep(
                (
                    gateway_info.session_start_limit
                    and gateway_info.session_start_limit.max_concurrency
                )
                or 1,
            )

    async def _get_gateway_bot(self, bot_info: BotInfo) -> GatewayBot:
        headers = {"Authorization": self.get_authorization(bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "gateway/bot",
            timeout=self.discord_config.discord_api_timeout,
            proxy=self.discord_config.discord_proxy,
        )
        resp = await self.request(request)
        if not resp.content:
            msg = "Failed to get gateway info"
            raise ValueError(msg)
        gateway_info = type_validate_json(GatewayBot, resp.content)
        if not gateway_info.url or gateway_info.url.isspace():
            msg = "Failed to get gateway url"
            raise ValueError(msg)
        return gateway_info

    async def _get_bot_user(self, bot_info: BotInfo) -> User:
        headers = {"Authorization": self.get_authorization(bot_info)}
        request = Request(
            method="GET",
            url=self.base_url / "users/@me",
            headers=headers,
            timeout=self.discord_config.discord_api_timeout,
            proxy=self.discord_config.discord_proxy,
        )
        resp = await self.request(request)
        if not resp.content:
            msg = "Failed to get bot user info"
            raise ValueError(msg)
        return type_validate_json(User, resp.content)

    async def _forward_ws(  # noqa: C901
        self,
        bot_info: BotInfo,
        ws_url: URL,
        shard: tuple[int, int],
    ) -> None:
        log("DEBUG", f"Forwarding WebSocket Connection to {escape_tag(str(ws_url))}...")
        headers = {"Authorization": self.get_authorization(bot_info)}
        params = {
            "v": self.discord_config.discord_api_version,
            "encoding": "json",
        }
        if self.discord_config.discord_compress:
            params["compress"] = "zlib-stream"
        request = Request(
            method="GET",
            url=ws_url,
            headers=headers,
            params=params,
            timeout=self.discord_config.discord_api_timeout,
            proxy=self.discord_config.discord_proxy,
        )
        heartbeat_task: asyncio.Task | None = None
        bot: Bot | None = None
        while True:
            try:
                if bot is None:
                    user = await self._get_bot_user(bot_info)
                    bot = Bot(self, str(user.id), bot_info)
                async with self.websocket(request) as ws:
                    log(
                        "DEBUG",
                        "WebSocket Connection to"
                        f" {escape_tag(str(ws_url))} established",
                    )
                    try:
                        # 接收hello事件
                        heartbeat_interval = await self._hello(ws)
                        if not heartbeat_interval:
                            await asyncio.sleep(RECONNECT_INTERVAL)
                            continue

                        if not heartbeat_task:
                            # 发送第一次心跳
                            log("DEBUG", "Waiting for first heartbeat to be send...")
                            # await asyncio.sleep(
                            #     random.random() * heartbeat_interval / 1000.0)  # https://discord.com/developers/docs/topics/gateway#heartbeat-interval
                            await asyncio.sleep(5)
                            await self._heartbeat(ws, bot)
                            await self._heartbeat_ack(ws)

                        # 开启心跳
                        heartbeat_task = asyncio.create_task(
                            self._heartbeat_task(ws, bot, heartbeat_interval),
                        )

                        # 进行identify和resume
                        result = await self._authenticate(bot, ws, shard)
                        if not result:
                            await asyncio.sleep(RECONNECT_INTERVAL)
                            continue

                        # 处理事件
                        await self._loop(bot, ws)
                    except WebSocketClosed as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>WebSocket Closed</bg #f8bbd0></r>",
                            e,
                        )
                    except Exception as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>Error while process data from"
                            f" websocket {escape_tag(str(ws_url))}. Trying to"
                            " reconnect...</bg #f8bbd0></r>",
                            e,
                        )
                    finally:
                        if heartbeat_task:
                            heartbeat_task.cancel()
                            heartbeat_task = None
                        if bot.self_id in self.bots:
                            self.bot_disconnect(bot)

            except Exception as e:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Error while setup websocket to "
                    f"{escape_tag(str(ws_url))}. "
                    "Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )
                await asyncio.sleep(RECONNECT_INTERVAL)

    async def _hello(self, ws: WebSocket) -> int | None:
        """接收并处理服务器的 Hello 事件

        见 https://discord.com/developers/docs/topics/gateway#hello-event
        """
        try:
            payload = await self.receive_payload(ws)
            if isinstance(payload, Hello):
                log("DEBUG", f"Received hello: {payload}")
                return payload.data.heartbeat_interval
            msg = f"Received unexpected payload: {payload!r}"
            raise ValueError(msg)  # noqa: TRY301
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Error while receiving "
                "server hello event</bg #f8bbd0></r>",
                e,
            )

    async def _heartbeat_ack(self, ws: WebSocket) -> None:
        """检查是否收到心跳ACK事件

        见 https://discord.com/developers/docs/topics/gateway#sending-heartbeats"""
        payload = await self.receive_payload(ws)
        if not isinstance(payload, HeartbeatAck):
            await ws.close(1003)  # 除了1000和1001都行

    @staticmethod
    async def _heartbeat(ws: WebSocket, bot: Bot) -> None:
        """心跳"""
        log("TRACE", f"Heartbeat {bot.sequence if bot.has_sequence else ''}")
        payload = type_validate_python(
            Heartbeat,
            {"data": bot.sequence if bot.has_sequence else None},
        )
        with contextlib.suppress(Exception):
            await ws.send(json.dumps(model_dump(payload, by_alias=True)))

    async def _heartbeat_task(
        self, ws: WebSocket, bot: Bot, heartbeat_interval: int
    ) -> None:
        """心跳任务"""
        while True:
            await self._heartbeat(ws, bot)
            await asyncio.sleep(heartbeat_interval / 1000.0)

    async def _authenticate(
        self, bot: Bot, ws: WebSocket, shard: tuple[int, int]
    ) -> bool | None:
        """鉴权连接"""
        if not bot.ready:
            payload = type_validate_python(
                Identify,
                {
                    "data": {
                        "token": self.get_authorization(bot.bot_info),
                        "intents": bot.bot_info.intent.to_int(),
                        "shard": list(shard),
                        "compress": self.discord_config.discord_compress,
                        "properties": {
                            "os": sys.platform,
                            "browser": "NoneBot2",
                            "device": "NoneBot2",
                        },
                    },
                },
            )
        else:
            payload = type_validate_python(
                Resume,
                {
                    "data": {
                        "token": self.get_authorization(bot.bot_info),
                        "session_id": bot.session_id,
                        "seq": bot.sequence,
                    },
                },
            )

        try:
            await ws.send(
                json.dumps(
                    model_dump(
                        payload,
                        by_alias=True,
                        exclude_none=True,
                        omit_unset_values=True,
                    )
                )
            )
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Error while sending "
                + ("Identify" if isinstance(payload, Identify) else "Resume")
                + " event</bg #f8bbd0></r>",
                e,
            )
            return None

        ready_event = None
        if not bot.ready:
            # https://discord.com/developers/docs/topics/gateway#ready-event
            # 鉴权成功之后, 后台会下发一个 Ready Event
            payload = await self.receive_payload(ws)
            if isinstance(payload, HeartbeatAck):
                log(
                    "WARNING", "Received unexpected HeartbeatAck event when identifying"
                )
                payload = await self.receive_payload(ws)
            if not isinstance(payload, Dispatch):
                msg = f"Received unexpected payload: {payload!r}"
                raise ValueError(msg)
            bot.sequence = payload.sequence
            ready_event = self.payload_to_event(payload)
            if not isinstance(ready_event, ReadyEvent):
                msg = f"Received unexpected event: {ready_event!r}"
                raise ValueError(msg)
            ws.request.url = URL(ready_event.resume_gateway_url)
            bot.session_id = ready_event.session_id
            bot.self_info = ready_event.user

        # only connect for single shard
        if bot.self_id not in self.bots:
            self.bot_connect(bot)
            log(
                "INFO",
                f"<y>Bot {escape_tag(bot.self_id)}</y> connected",
            )

        if ready_event:
            task = asyncio.create_task(bot.handle_event(ready_event))
            task.add_done_callback(self.tasks.discard)
            self.tasks.add(task)

        return True

    async def _loop(self, bot: Bot, ws: WebSocket) -> None:
        """接收并处理事件"""
        while True:
            payload = await self.receive_payload(ws)
            log(
                "TRACE",
                f"Received payload: {escape_tag(repr(payload))}",
            )
            if isinstance(payload, Dispatch):
                bot.sequence = payload.sequence
                try:
                    event = self.payload_to_event(payload)
                except Exception as e:
                    log(
                        "WARNING",
                        f"Failed to parse event {escape_tag(repr(payload))}",
                        e,
                    )
                else:
                    if not (
                        isinstance(event, MessageEvent)
                        and event.get_user_id() == bot.self_id
                        and not self.discord_config.discord_handle_self_message
                    ):
                        task = asyncio.create_task(bot.handle_event(event))
                        task.add_done_callback(self.tasks.discard)
                        self.tasks.add(task)
            elif isinstance(payload, Heartbeat):
                # 当接受到心跳payload时, 需要立即发送一次心跳见 https://discord.com/developers/docs/topics/gateway#heartbeat-requests
                await self._heartbeat(ws, bot)

            elif isinstance(payload, HeartbeatAck):
                log("TRACE", "Heartbeat ACK")
                continue
            elif isinstance(payload, Reconnect):
                log(
                    "WARNING",
                    "Received reconnect event from server. Try to reconnect...",
                )
                break
            elif isinstance(payload, InvalidSession):
                bot.clear()
                log(
                    "ERROR",
                    "Received invalid session event from server. Try to reconnect...",
                )
                break
            else:
                log(
                    "WARNING",
                    f"Unknown payload from server: {escape_tag(repr(payload))}",
                )

    @staticmethod
    def get_authorization(bot_info: BotInfo) -> str:
        return f"Bot {bot_info.token}"

    async def receive_payload(self, ws: WebSocket) -> Payload:
        data = await ws.receive()
        data = decompress_data(data, compress=self.discord_config.discord_compress)
        return type_validate_json(cast("type[Payload]", PayloadType), data)

    @classmethod
    def payload_to_event(cls, payload: Dispatch) -> Event:
        EventClass: type[Event] | UnionType | None = event_classes.get(  # noqa: N806
            payload.type, None
        )
        if not EventClass:
            log(
                "WARNING",
                f"Unknown payload type: {payload.type}, detail: {payload!r}",
            )
            event = type_validate_python(Event, payload.data)
            event.__type__ = EventType(payload.type)
            return event
        return type_validate_python(cast("type[Event]", EventClass), payload.data)

    @override
    async def _call_api(self, bot: BaseBot, api: str, **data: Any) -> Any:
        log("DEBUG", f"Calling API <y>{api}</y>")
        api_handler = getattr(self, f"_api_{api}", None)
        if api_handler is None:
            raise ApiNotAvailable
        handler_params = _get_handler_params(api_handler)
        if "bot" in handler_params:
            return await api_handler(bot, **data)
        return await api_handler(**data)
