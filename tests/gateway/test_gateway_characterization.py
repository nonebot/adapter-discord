from typing import cast

from nonebot.adapters.discord.adapter import Adapter
from nonebot.adapters.discord.api.model import Snowflake
from nonebot.adapters.discord.api.types import UNSET
from nonebot.adapters.discord.domains.gateway.factory import (
    EVENT_BINDINGS,
    EVENT_FACTORY,
)
from nonebot.adapters.discord.event import (
    ApplicationCommandAutoCompleteInteractionEvent,
    ApplicationCommandInteractionEvent,
    DirectMessageCreateEvent,
    GuildMessageCreateEvent,
    MessageComponentInteractionEvent,
    ModalSubmitInteractionEvent,
    PingInteractionEvent,
    event_classes,
)
from nonebot.adapters.discord.payload import Dispatch, Opcode
from tests.fake.doubles import DummyAdapter, DummyBot

from nonebot.compat import type_validate_python
from nonebot.drivers import WebSocket
import pytest


def _user_payload() -> dict[str, object]:
    return {
        "id": "3",
        "username": "tester",
        "discriminator": "0",
        "global_name": None,
        "avatar": None,
    }


def _message_payload() -> dict[str, object]:
    return {
        "id": "1",
        "channel_id": "2",
        "author": _user_payload(),
        "content": "current message content",
        "timestamp": "2026-02-14T00:00:00+00:00",
        "edited_timestamp": None,
        "tts": False,
        "mention_everyone": False,
        "mentions": [],
        "mention_roles": [],
        "attachments": [],
        "embeds": [],
        "pinned": False,
        "type": 0,
    }


def _dispatch(event_type: str, data: dict[str, object]) -> Dispatch:
    return type_validate_python(
        Dispatch,
        {"op": Opcode.DISPATCH, "d": data, "s": 1, "t": event_type},
    )


def _interaction_payload(interaction_type: int) -> dict[str, object]:
    return {
        "id": "10",
        "application_id": "11",
        "type": interaction_type,
        "token": "interaction-token",
        "version": 1,
        "attachment_size_limit": 1,
        "authorizing_integration_owners": {},
        "user": _user_payload(),
    }


def test_guild_message_create_keeps_flat_message_fields() -> None:
    payload = _message_payload()
    payload["guild_id"] = "9"

    event = Adapter.payload_to_event(_dispatch("MESSAGE_CREATE", payload))

    assert isinstance(event, GuildMessageCreateEvent)
    assert event.guild_id == Snowflake("9")
    assert isinstance(event.guild_id, Snowflake)
    assert event.id == Snowflake("1")
    assert event.channel_id == Snowflake("2")
    assert event.author.id == Snowflake("3")
    assert event.content == "current message content"


def test_direct_message_create_uses_unset_guild_and_marks_to_me() -> None:
    event = Adapter.payload_to_event(_dispatch("MESSAGE_CREATE", _message_payload()))

    assert isinstance(event, DirectMessageCreateEvent)
    assert event.guild_id is UNSET
    assert event.to_me is True
    assert event.id == Snowflake("1")
    assert event.channel_id == Snowflake("2")
    assert event.author.id == Snowflake("3")
    assert event.content == "current message content"


@pytest.mark.parametrize(
    ("interaction_type", "data", "expected_type"),
    [
        (1, None, PingInteractionEvent),
        (
            2,
            {"id": "20", "name": "command", "type": 1},
            ApplicationCommandInteractionEvent,
        ),
        (
            4,
            {"id": "20", "name": "command", "type": 1},
            ApplicationCommandAutoCompleteInteractionEvent,
        ),
        (
            3,
            {"custom_id": "component", "component_type": 2},
            MessageComponentInteractionEvent,
        ),
        (
            5,
            {"custom_id": "modal", "components": [{"type": 1, "components": []}]},
            ModalSubmitInteractionEvent,
        ),
    ],
)
def test_interaction_create_selects_existing_concrete_event_type(
    interaction_type: int,
    data: dict[str, object] | None,
    expected_type: type[object],
) -> None:
    payload = _interaction_payload(interaction_type)
    if data is not None:
        payload["data"] = data
    if interaction_type == 3:
        payload["message"] = _message_payload()

    event = Adapter.payload_to_event(_dispatch("INTERACTION_CREATE", payload))

    assert isinstance(event, expected_type)


def test_event_classes_is_the_event_binding_projection() -> None:
    assert EVENT_FACTORY.bindings is EVENT_BINDINGS
    assert set(event_classes) == set(EVENT_BINDINGS)
    for event_name, binding in EVENT_BINDINGS.items():
        assert event_classes[event_name] is binding.event_type


@pytest.mark.parametrize(
    "dispatch",
    [
        _dispatch("UNKNOWN_GATEWAY_EVENT", {}),
        _dispatch("MESSAGE_CREATE", {}),
    ],
)
async def test_gateway_loop_logs_and_drops_unparseable_dispatches(
    dispatch: Dispatch,
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    adapter = DummyAdapter()
    bot = DummyBot(adapter)
    logs: list[tuple[str, str]] = []
    handled_events: list[object] = []
    payloads = iter([dispatch])

    stop_message = "stop gateway loop"

    loop_method_name = "_loop"

    def fake_log(level: str, message: str, *_args: object) -> None:
        logs.append((level, message))

    async def receive_payload(_ws: object) -> Dispatch:
        try:
            return next(payloads)
        except StopIteration as error:
            raise RuntimeError(stop_message) from error

    async def handle_event(event: object) -> None:
        handled_events.append(event)

    monkeypatch.setattr("nonebot.adapters.discord.adapter.log", fake_log)
    monkeypatch.setattr(adapter, "receive_payload", receive_payload)
    monkeypatch.setattr(bot, "handle_event", handle_event)

    with pytest.raises(RuntimeError, match="stop gateway loop"):
        await getattr(adapter, loop_method_name)(bot, cast("WebSocket", object()))

    assert handled_events == []
    assert any(
        level == "WARNING" and "Failed to parse event" in message
        for level, message in logs
    )


def test_unknown_gateway_event_type_raises_value_error() -> None:
    with pytest.raises(ValueError, match="UNKNOWN_GATEWAY_EVENT"):
        Adapter.payload_to_event(_dispatch("UNKNOWN_GATEWAY_EVENT", {}))
