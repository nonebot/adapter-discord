from typing import Any

from nonebot.adapters.discord.api import ApplicationCommandType
from nonebot.adapters.discord.event import ApplicationCommandInteractionEvent

from nonebot.compat import type_validate_python
import pytest


def _build_base_payload() -> dict[str, Any]:
    return {
        "id": 1,
        "application_id": 2,
        "type": 2,
        "data": {
            "id": 3,
            "name": "issue23_repro",
            "type": ApplicationCommandType.CHAT_INPUT,
        },
        "token": "token",
        "version": 1,
        "authorizing_integration_owners": {"0": "1"},
    }


def _build_user_payload() -> dict[str, Any]:
    return {
        "id": 516240373413183488,
        "username": "scdhh",
        "discriminator": "0",
        "global_name": "scdhh",
        "avatar": None,
    }


def _build_member_payload(*, include_user: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "roles": [],
        "joined_at": "2026-02-12T19:10:40.357000+00:00",
        "flags": 0,
    }
    if include_user:
        payload["user"] = _build_user_payload()
    return payload


def test_interaction_get_user_id_fallback_to_member_user() -> None:
    payload = _build_base_payload()
    payload["member"] = _build_member_payload(include_user=True)

    event = type_validate_python(ApplicationCommandInteractionEvent, payload)

    assert event.get_user_id() == "516240373413183488"


def test_interaction_get_user_id_uses_top_level_user_in_dm() -> None:
    payload = _build_base_payload()
    payload["user"] = _build_user_payload()

    event = type_validate_python(ApplicationCommandInteractionEvent, payload)

    assert event.get_user_id() == "516240373413183488"


def test_interaction_get_user_id_raises_without_user_context() -> None:
    payload = _build_base_payload()
    payload["member"] = _build_member_payload(include_user=False)

    event = type_validate_python(ApplicationCommandInteractionEvent, payload)

    with pytest.raises(ValueError, match="Event has no context!"):
        event.get_user_id()
