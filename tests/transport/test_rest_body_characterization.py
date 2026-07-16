import base64
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
import enum
import inspect
import json
from pathlib import Path
import types
from typing import Annotated, Literal, NoReturn, Union, get_args, get_origin
from typing_extensions import NotRequired, Required, Unpack, is_typeddict

from nonebot.adapters.discord.api.model import File, Snowflake
from nonebot.adapters.discord.api.types import TriggerType
from nonebot.adapters.discord.exception import DiscordAdapterException
from nonebot.adapters.discord.protocol.missing import UnsetType
from tests.fake.doubles import DummyAdapter, DummyBot

from nonebot.drivers import Request
from pydantic import BaseModel
import pytest

FIXTURE = Path(__file__).parent.parent / "fixtures" / "rest_body_characterization.json"
BODY_CONSTRUCTORS = (
    "JsonBody(",
    "PreparedBody(",
    "MultipartBody(",
    "parse_data(",
    "parse_forum_thread_message(",
    "parse_interaction_response(",
)


class CapturedRequestError(DiscordAdapterException):
    def __init__(self, request: Request) -> None:
        super().__init__()
        self.request = request


def _sample(  # noqa: C901, PLR0911, PLR0912
    annotation: object, *, depth: int = 0
) -> object:
    if depth > 8:
        return None
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin in (Annotated, Required, NotRequired):
        return _sample(args[0], depth=depth + 1)
    if origin in (Union, types.UnionType):
        choices = [arg for arg in args if arg not in (type(None), UnsetType)]
        return _sample(choices[0], depth=depth + 1) if choices else None
    if origin is Literal:
        return args[0]
    if origin is list:
        return [_sample(args[0], depth=depth + 1)]
    if origin is dict:
        return {}
    if isinstance(annotation, type) and issubclass(annotation, enum.Enum):
        return next(iter(annotation))
    if annotation is str:
        return "value"
    if annotation is bytes:
        return b"\x89PNG\r\n\x1a\n"
    if annotation is bool:
        return False
    if annotation is int:
        return 1
    if annotation is float:
        return 1.0
    if annotation is datetime:
        return datetime(2026, 1, 1, tzinfo=timezone.utc)
    if annotation is File:
        return File(content=b"x", filename="file.txt")
    if annotation is Snowflake:
        return Snowflake(1)
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        values: dict[str, object] = {}
        fields = annotation.model_fields
        for name, field in fields.items():
            if field.is_required():
                values[name] = _sample(field.annotation, depth=depth + 1)
        return annotation(**values)
    return 1


def _required_kwargs(method: Callable[..., object], bot: DummyBot) -> dict[str, object]:
    kwargs: dict[str, object] = {}
    for name, parameter in inspect.signature(method).parameters.items():
        if name == "bot":
            kwargs[name] = bot
        elif parameter.kind is inspect.Parameter.VAR_KEYWORD:
            unpacked = get_args(parameter.annotation)
            if get_origin(parameter.annotation) is Unpack and unpacked:
                typed_dict = unpacked[0]
                assert is_typeddict(typed_dict)
                for key in getattr(typed_dict, "__required_keys__", frozenset()):
                    kwargs[key] = _sample(typed_dict.__annotations__[key])
        elif parameter.default is inspect.Parameter.empty:
            kwargs[name] = _sample(parameter.annotation)
    return kwargs


def _case_kwargs(  # noqa: C901
    method: Callable[..., object], bot: DummyBot
) -> dict[str, object]:
    kwargs = _required_kwargs(method, bot)
    name = method.__name__
    if any(
        fragment in name
        for fragment in ("create_message", "create_followup_message", "execute_webhook")
    ):
        kwargs["content"] = "value"
    if name == "_api_start_thread_in_forum_channel":
        kwargs["content"] = "value"
    if name in {
        "_api_edit_message",
        "_api_edit_followup_message",
        "_api_edit_origin_interaction_response",
        "_api_edit_webhook_message",
    }:
        kwargs["content"] = "value"
    if name in {
        "_api_create_global_application_command",
        "_api_create_guild_application_command",
    }:
        kwargs["description"] = "value"
    if name.startswith("_api_bulk_overwrite_"):
        kwargs["commands"] = []
    if name == "_api_create_guild_schedule_event":
        kwargs["channel_id"] = 1
    if name == "_api_modify_guild_channel_positions":
        kwargs.update(id=1, position=1, lock_permissions=False, parent_id=None)
    if name == "_api_modify_guild_role_positions":
        kwargs.update(id=1, position=1)
    if name == "_api_bulk_delete_message":
        kwargs["messages"] = [1, 2]
    if name == "_api_create_auto_moderation_rule":
        kwargs["trigger_type"] = TriggerType.SPAM
    if name == "_api_update_application_role_connection_metadata_records":
        kwargs["records"] = []
    return kwargs


async def _capture_request(
    adapter: DummyAdapter,
    coro: Awaitable[object],
) -> Request:
    async def fake_request(setup: Request) -> NoReturn:
        raise CapturedRequestError(setup)

    adapter.request = fake_request
    with pytest.raises(CapturedRequestError) as excinfo:
        await coro
    return excinfo.value.request


def _normalize(value: object) -> object:
    if isinstance(value, bytes):
        return {"bytes": base64.b64encode(value).decode()}
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return repr(value)


def _normalize_request(request: Request) -> dict[str, object]:
    files: list[dict[str, object]] | None = None
    if request.files is not None:
        files = []
        for key, (filename, content, content_type) in request.files:
            item: dict[str, object] = {
                "key": key,
                "filename": _normalize(filename),
                "content_type": content_type,
            }
            if key == "payload_json":
                text = content.decode() if isinstance(content, bytes) else content
                assert isinstance(text, str)
                item["json"] = json.loads(text)
            else:
                item["content"] = _normalize(content)
            files.append(item)
    return {"json": _normalize(request.json), "files": files}


def _body_endpoint_names(adapter: DummyAdapter) -> set[str]:
    names: set[str] = set()
    for name in dir(adapter):
        if not name.startswith("_api_"):
            continue
        method = getattr(adapter, name)
        source = inspect.getsource(method)
        if any(constructor in source for constructor in BODY_CONSTRUCTORS):
            names.add(name)
    return names


@pytest.mark.asyncio
async def test_all_rest_body_endpoints_preserve_wire_contract() -> None:
    expected: dict[str, dict[str, object]] = json.loads(FIXTURE.read_text("utf-8"))
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)

    assert _body_endpoint_names(adapter) == set(expected)
    actual: dict[str, dict[str, object]] = {}
    for name in sorted(expected):
        method = getattr(adapter, name)
        request = await _capture_request(adapter, method(**_case_kwargs(method, bot)))
        actual[name] = _normalize_request(request)

    assert actual == expected


@pytest.mark.asyncio
async def test_rest_body_presence_values_are_not_dropped() -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    request = await _capture_request(
        adapter,
        adapter._api_edit_current_application(  # noqa: SLF001
            bot,
            description="",
            event_webhooks_status=0,
            tags=[],
            integration_types_config={},
            icon=None,
        ),
    )
    assert request.json == {
        "description": "",
        "event_webhooks_status": 0,
        "tags": [],
        "integration_types_config": {},
        "icon": None,
    }


@pytest.mark.asyncio
async def test_create_guild_channel_preserves_legacy_default_null_fields() -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    request = await _capture_request(
        adapter,
        adapter._api_create_guild_channel(  # noqa: SLF001
            bot,
            guild_id=1,
            name="channel",
        ),
    )
    assert request.json == {
        "name": "channel",
        "type": None,
        "topic": None,
        "bitrate": None,
        "user_limit": None,
        "rate_limit_per_user": None,
        "position": None,
        "permission_overwrites": None,
        "parent_id": None,
        "nsfw": None,
        "rtc_region": None,
        "video_quality_mode": None,
        "default_auto_archive_duration": None,
        "default_reaction_emoji": None,
        "available_tags": None,
        "default_sort_order": None,
        "default_forum_layout": None,
        "default_thread_rate_limit_per_user": None,
    }


@pytest.mark.asyncio
async def test_nullable_patch_distinguishes_omitted_and_explicit_none() -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter=adapter)
    omitted = await _capture_request(
        adapter,
        adapter._api_edit_message(bot, channel_id=1, message_id=2, embeds=[]),  # noqa: SLF001
    )
    explicit_null = await _capture_request(
        adapter,
        adapter._api_edit_message(  # noqa: SLF001
            bot,
            channel_id=1,
            message_id=2,
            content=None,
        ),
    )
    assert omitted.json == {"embeds": []}
    assert explicit_null.json == {"content": None}
