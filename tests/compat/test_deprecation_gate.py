import json
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Any, cast
import warnings

from nonebot.adapters import MessageTemplate, discord
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
from nonebot.adapters.discord.bot import Bot
from nonebot.adapters.discord.commands.matcher import ApplicationCommandMatcher
from nonebot.adapters.discord.domains.interaction.lifecycle import (
    InteractionResponder,
    current_interaction_responder,
)
from nonebot.adapters.discord.event import ApplicationCommandInteractionEvent
from nonebot.adapters.discord.exception import ActionFailed
import nonebot.adapters.discord.message as message_module
from scripts.snapshot_public_api import PublicApiSnapshot, build_snapshot
from tests.fake.doubles import DummyBot

from nonebot.compat import type_validate_python
from nonebot.drivers import Response
from nonebot.internal.matcher import (
    Matcher,
    current_bot,
    current_event,
    current_matcher,
)
from pydantic import BaseModel
import pytest

ROOT = Path(__file__).parents[2]
DEPRECATIONS_PATH = ROOT / "tests/fixtures/deprecations.json"
PUBLIC_API_PATH = ROOT / "tests/fixtures/public_api.json"
MATCHER_CALLABLES = {
    "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_deferred_response": "send_deferred_response",
    "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_response": "send_response",
    "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_followup_msg": "send_followup_msg",
}
PRESERVED_MATCHER_CRUD = {
    "get_response",
    "edit_response",
    "delete_response",
    "get_followup_msg",
    "edit_followup_msg",
    "delete_followup_msg",
}


def _deprecations() -> dict[str, Any]:
    data = json.loads(DEPRECATIONS_PATH.read_text("utf-8"))
    assert data["removal_target"] == "2.0.0"
    assert isinstance(data["callables"], list)
    assert len(data["callables"]) == 4
    assert isinstance(data["legacy_fallback"], dict)
    return data


def _public_api_fixture() -> PublicApiSnapshot:
    return cast(
        "PublicApiSnapshot",
        json.loads(PUBLIC_API_PATH.read_text("utf-8")),
    )


def _project_major() -> int:
    pyproject = (ROOT / "pyproject.toml").read_text("utf-8")
    project_table = re.search(
        r"(?ms)^\[project\]\s*$\n(?P<body>.*?)(?=^\[|\Z)",
        pyproject,
    )
    assert project_table is not None
    version = re.search(
        r'^version\s*=\s*"(?P<version>\d+(?:\.\d+)*)"\s*$',
        project_table["body"],
        flags=re.MULTILINE,
    )
    assert version is not None
    return int(version["version"].split(".", maxsplit=1)[0])


def _callable_contracts(deprecations: dict[str, Any]) -> dict[str, dict[str, str]]:
    contracts: dict[str, dict[str, str]] = {}
    for contract in deprecations["callables"]:
        assert isinstance(contract, dict)
        name = contract["fully_qualified_name"]
        warning = contract["warning"]
        assert isinstance(name, str)
        assert isinstance(warning, str)
        assert contract["removal_target"] == deprecations["removal_target"]
        contracts[name] = {"warning": warning}

    assert set(contracts) == {
        "nonebot.adapters.discord.message.parse_message",
        *MATCHER_CALLABLES,
    }
    return contracts


def _resolve_callable(name: str) -> object | None:
    if name == "nonebot.adapters.discord.message.parse_message":
        return getattr(message_module, "parse_message", None)
    return getattr(ApplicationCommandMatcher, MATCHER_CALLABLES[name], None)


def _assert_version_gate(
    major: int,
    contracts: dict[str, dict[str, str]],
    *,
    legacy_fallback_present: bool,
) -> None:
    if major < 2:
        for name in contracts:
            assert callable(_resolve_callable(name))
        for name in MATCHER_CALLABLES:
            method = _resolve_callable(name)
            assert getattr(method, "__deprecated__", None) == contracts[name]["warning"]
        assert legacy_fallback_present
        return

    for name in contracts:
        assert _resolve_callable(name) is None
    assert not legacy_fallback_present


def _model_field_names(model: type[BaseModel]) -> set[str]:
    return set(model.model_fields)


def _assert_raw_public_contract(fixture: PublicApiSnapshot) -> None:
    snapshot = build_snapshot(ROOT)
    assert snapshot["top_level_exports"] == fixture["top_level_exports"]
    assert snapshot["api_exports"] == fixture["api_exports"]
    assert snapshot["model_exports"] == fixture["model_exports"]
    assert snapshot["api_client"] == fixture["api_client"]
    assert snapshot["counts"] == fixture["counts"]
    assert list(discord.__all__) == fixture["top_level_exports"]
    assert list(api.__all__) == fixture["api_exports"]
    assert list(model.__all__) == fixture["model_exports"]
    assert all(hasattr(api, name) for name in api.__all__)
    assert ApiClient.__name__ == "ApiClient"

    for method_name in PRESERVED_MATCHER_CRUD:
        assert callable(getattr(ApplicationCommandMatcher, method_name))

    assert GuildMessageCreateEvent.__mro__[:3] == (
        GuildMessageCreateEvent,
        MessageCreateEvent,
        MessageEvent,
    )
    assert issubclass(GuildMessageCreateEvent, MessageGet)
    assert issubclass(DirectMessageCreateEvent, MessageGet)
    flat_fields = {"id", "channel_id", "author", "content", "guild_id"}
    assert flat_fields <= _model_field_names(GuildMessageCreateEvent)
    assert flat_fields <= _model_field_names(DirectMessageCreateEvent)
    assert "to_me" in _model_field_names(DirectMessageCreateEvent)

    text = MessageSegment.text("hello")
    attachment = MessageSegment.attachment("example.txt", content=b"payload")
    assert text.type == "text"
    assert text.data == {"text": "hello"}
    assert attachment.type == "attachment"
    assert set(attachment.data) == {"attachment", "file", "url", "proxy_url"}
    assert attachment.data["file"].content == b"payload"
    assert Message(text)[0].type == "text"


def _interaction_event() -> ApplicationCommandInteractionEvent:
    return type_validate_python(
        ApplicationCommandInteractionEvent,
        {
            "id": "10",
            "application_id": "11",
            "type": 2,
            "token": "interaction-token",
            "version": 1,
            "attachment_size_limit": 1,
            "authorizing_integration_owners": {},
            "user": {
                "id": "3",
                "username": "tester",
                "discriminator": "0",
                "global_name": None,
                "avatar": None,
            },
            "data": {"id": "20", "name": "command", "type": 1},
        },
    )


def _action_failed() -> ActionFailed:
    return ActionFailed(Response(400, content=b'{"code": 40060}'))


def _assert_exact_warning(
    captured: list[warnings.WarningMessage], expected: str
) -> None:
    assert len(captured) == 1
    assert captured[0].category is DeprecationWarning
    assert str(captured[0].message) == expected


def test_current_one_x_gate_keeps_all_deprecated_surfaces() -> None:
    deprecations = _deprecations()
    contracts = _callable_contracts(deprecations)
    legacy_fallback = deprecations["legacy_fallback"]
    assert isinstance(legacy_fallback, dict)
    assert legacy_fallback["removal_target"] == deprecations["removal_target"]
    assert "fully_qualified_name" not in legacy_fallback

    assert _project_major() < 2
    _assert_version_gate(
        _project_major(),
        contracts,
        legacy_fallback_present=True,
    )


@pytest.mark.asyncio
async def test_one_x_deprecation_warnings_are_exact_and_direct(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contracts = _callable_contracts(_deprecations())

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        assert message_module.parse_message("compatibility") == {
            "content": "compatibility"
        }
    _assert_exact_warning(
        captured, contracts["nonebot.adapters.discord.message.parse_message"]["warning"]
    )

    event = _interaction_event()
    bot = DummyBot()
    responder = InteractionResponder.from_event(bot, event)
    calls: list[tuple[str, dict[str, object]]] = []
    followup_result = object()

    async def callback(**kwargs: object) -> None:
        calls.append(("callback", kwargs))

    async def followup(**kwargs: object) -> object:
        calls.append(("followup", kwargs))
        return followup_result

    async def send(cls: type[ApplicationCommandMatcher], message: object) -> object:
        assert cls is ApplicationCommandMatcher
        assert message == "response"
        return followup_result

    monkeypatch.setattr(bot, "create_interaction_response", callback)
    monkeypatch.setattr(bot, "create_followup_message", followup)
    monkeypatch.setattr(ApplicationCommandMatcher, "send", classmethod(send))
    event_token = current_event.set(event)
    bot_token = current_bot.set(bot)
    matcher_token = current_matcher.set(
        cast("Matcher", SimpleNamespace(state={"name": "Ada"}))
    )
    responder_token = current_interaction_responder.set(responder)
    try:
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always", DeprecationWarning)
            assert await ApplicationCommandMatcher.send_deferred_response() is None
        _assert_exact_warning(
            captured,
            contracts[
                "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_deferred_response"
            ]["warning"],
        )

        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always", DeprecationWarning)
            assert (
                await ApplicationCommandMatcher.send_response("response")
                is followup_result
            )
        _assert_exact_warning(
            captured,
            contracts[
                "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_response"
            ]["warning"],
        )

        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always", DeprecationWarning)
            assert (
                await ApplicationCommandMatcher.send_followup_msg(
                    MessageTemplate("followup {name}")
                )
                is followup_result
            )
        _assert_exact_warning(
            captured,
            contracts[
                "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_followup_msg"
            ]["warning"],
        )
    finally:
        current_interaction_responder.reset(responder_token)
        current_matcher.reset(matcher_token)
        current_bot.reset(bot_token)
        current_event.reset(event_token)

    assert [name for name, _ in calls] == ["callback", "followup"]
    assert calls[-1][1]["content"] == "followup Ada"


@pytest.mark.asyncio
async def test_one_x_unmanaged_action_failed_fallback_warns_exactly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    deprecations = _deprecations()
    legacy_fallback = deprecations["legacy_fallback"]
    assert isinstance(legacy_fallback, dict)
    expected_warning = legacy_fallback["warning"]
    assert isinstance(expected_warning, str)

    bot = DummyBot()
    event = _interaction_event()
    followup_result = object()
    followup_calls: list[dict[str, object]] = []

    async def callback(**kwargs: object) -> None:
        del kwargs
        raise _action_failed()

    async def followup(**kwargs: object) -> object:
        followup_calls.append(kwargs)
        return followup_result

    monkeypatch.setattr(bot, "create_interaction_response", callback)
    monkeypatch.setattr(bot, "create_followup_message", followup)
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        assert await bot.send(event, "fallback") is followup_result
    _assert_exact_warning(captured, expected_warning)
    assert len(followup_calls) == 1


@pytest.mark.asyncio
async def test_major_two_removal_gate_uses_temporary_release_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exercise the 2.x assertions without mutating this 1.1.x project's version."""
    contracts = _callable_contracts(_deprecations())
    monkeypatch.delattr(message_module, "parse_message")
    for method_name in MATCHER_CALLABLES.values():
        monkeypatch.delattr(ApplicationCommandMatcher, method_name)

    async def send_without_legacy_fallback(
        self: Bot, event: object, message: object, **params: object
    ) -> object:
        del self, event, message, params
        raise _action_failed()

    monkeypatch.setattr(Bot, "send", send_without_legacy_fallback)
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        with pytest.raises(ActionFailed):
            await DummyBot().send(_interaction_event(), "no fallback")
    assert captured == []

    _assert_version_gate(2, contracts, legacy_fallback_present=False)
    _assert_raw_public_contract(_public_api_fixture())
