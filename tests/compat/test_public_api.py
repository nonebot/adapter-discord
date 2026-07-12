import inspect
import json
from pathlib import Path
import re
from typing import cast

from nonebot.adapters import discord
from nonebot.adapters.discord import (
    DirectMessageCreateEvent,
    GuildMessageCreateEvent,
    Message,
    MessageCreateEvent,
    MessageEvent,
    MessageSegment,
    api,
)
from nonebot.adapters.discord.api import ApiClient, model
from nonebot.adapters.discord.api.model import MessageGet
from nonebot.adapters.discord.commands.matcher import ApplicationCommandMatcher
import nonebot.adapters.discord.message as message_module
from scripts.snapshot_public_api import PublicApiSnapshot, build_snapshot

import pytest

ROOT = Path(__file__).parents[2]
FIXTURE_PATH = ROOT / "tests/fixtures/public_api.json"
LEGACY_REMOVALS = {
    "message": {"parse_message"},
    "application_command_matcher": {
        "send_deferred_response",
        "send_response",
        "send_followup_msg",
    },
}
PRESERVED_MATCHER_HELPERS = {
    "get_response",
    "edit_response",
    "delete_response",
    "get_followup_msg",
    "edit_followup_msg",
    "delete_followup_msg",
}
INTERACTION_LIFECYCLE_EXPORTS = [
    "CommandResponse",
    "InteractionResponder",
    "InteractionStateError",
]


def _fixture() -> PublicApiSnapshot:
    return cast(
        "PublicApiSnapshot",
        json.loads(FIXTURE_PATH.read_text("utf-8")),
    )


def _major_version() -> int:
    pyproject = (ROOT / "pyproject.toml").read_text("utf-8")
    match = re.search(r'^version\s*=\s*"(\d+)\.', pyproject, flags=re.MULTILINE)
    assert match is not None
    return int(match.group(1))


def _model_field_names(model: type[object]) -> set[str]:
    fields = getattr(model, "model_fields", None)
    if fields is None:
        fields = vars(model)["__fields__"]
    return set(fields)


def _assert_runtime_callable(
    target: object, contract: dict[str, object], *, is_classmethod: bool = False
) -> None:
    assert contract["exists"] is True
    assert callable(target)
    if contract["is_async"]:
        assert inspect.iscoroutinefunction(target)

    expected_parameters = contract["parameters"]
    assert isinstance(expected_parameters, list)
    expected_names = [parameter["name"] for parameter in expected_parameters]
    if is_classmethod:
        assert expected_names[0] == "cls"
        expected_names = expected_names[1:]
    assert list(inspect.signature(target).parameters) == expected_names


def test_public_api_fixture_matches_current_ast_contract() -> None:
    fixture = _fixture()
    current = build_snapshot(ROOT)
    assert current["top_level_exports"] == fixture["top_level_exports"]
    assert current["api_exports"] == fixture["api_exports"]
    assert current["model_exports"] == fixture["model_exports"]
    assert current["api_client"] == fixture["api_client"]
    assert current["counts"] == fixture["counts"]
    assert fixture["counts"] == {
        "top_level_exports": 133,
        "api_exports": 378,
        "model_exports": 297,
        "api_client_async_methods": 230,
    }


def test_public_exports_resolve_in_runtime() -> None:
    fixture = _fixture()
    assert list(discord.__all__) == fixture["top_level_exports"]
    assert list(api.__all__) == fixture["api_exports"]
    assert list(model.__all__) == fixture["model_exports"]
    assert all(hasattr(discord, name) for name in discord.__all__)
    assert all(hasattr(api, name) for name in api.__all__)
    assert all(hasattr(model, name) for name in model.__all__)


def test_version_gated_callable_contract() -> None:
    fixture = _fixture()
    current = build_snapshot(ROOT)
    message_contracts = fixture["message"]
    matcher_contracts = fixture["application_command_matcher"]
    assert isinstance(message_contracts, dict)
    assert isinstance(matcher_contracts, dict)

    if _major_version() < 2:
        assert fixture["top_level_exports"][-3:] == INTERACTION_LIFECYCLE_EXPORTS
        assert current["message"] == message_contracts
        assert current["application_command_matcher"] == matcher_contracts
        _assert_runtime_callable(
            message_module.parse_message, message_contracts["parse_message"]
        )
        for name, contract in matcher_contracts.items():
            _assert_runtime_callable(
                getattr(ApplicationCommandMatcher, name), contract, is_classmethod=True
            )
        return

    for section, names in LEGACY_REMOVALS.items():
        actual_contracts = current[section]
        expected_contracts = fixture[section]
        for name, expected in expected_contracts.items():
            if name in names:
                assert actual_contracts[name] == {"exists": False}
            else:
                assert actual_contracts[name] == expected
    assert not hasattr(message_module, "parse_message")
    for name in LEGACY_REMOVALS["application_command_matcher"]:
        assert not hasattr(ApplicationCommandMatcher, name)
    for name in PRESERVED_MATCHER_HELPERS:
        assert callable(getattr(ApplicationCommandMatcher, name))


def test_api_client_fixture_records_230_public_async_methods() -> None:
    fixture = _fixture()
    api_client = fixture["api_client"]
    assert api_client["async_method_count"] == 230
    assert len(api_client["methods"]) == 230
    assert ApiClient.__name__ == "ApiClient"


def test_event_mro_and_flat_message_fields_remain_public() -> None:
    assert GuildMessageCreateEvent.__mro__[:3] == (
        GuildMessageCreateEvent,
        MessageCreateEvent,
        MessageEvent,
    )
    assert issubclass(GuildMessageCreateEvent, MessageEvent)
    assert issubclass(GuildMessageCreateEvent, MessageGet)
    assert issubclass(DirectMessageCreateEvent, MessageEvent)
    assert issubclass(DirectMessageCreateEvent, MessageGet)
    expected_flat_fields = {"id", "channel_id", "author", "content", "guild_id"}
    assert expected_flat_fields <= _model_field_names(GuildMessageCreateEvent)
    assert expected_flat_fields <= _model_field_names(DirectMessageCreateEvent)
    assert "to_me" in _model_field_names(DirectMessageCreateEvent)


def test_message_segment_type_and_data_shape_remains_public() -> None:
    text = MessageSegment.text("hello")
    attachment = MessageSegment.attachment("example.txt", content=b"payload")
    message = Message(text)

    assert text.type == "text"
    assert text.data == {"text": "hello"}
    assert attachment.type == "attachment"
    assert set(attachment.data) == {"attachment", "file", "url", "proxy_url"}
    assert attachment.data["file"].content == b"payload"
    assert message[0].type == "text"


@pytest.mark.parametrize(
    "event_type", [GuildMessageCreateEvent, DirectMessageCreateEvent]
)
def test_message_events_keep_flat_message_model_identity(
    event_type: type[MessageEvent],
) -> None:
    assert issubclass(event_type, MessageGet)
