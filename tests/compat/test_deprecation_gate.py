import json
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Any, cast
import warnings

from nonebot.adapters import MessageTemplate
from nonebot.adapters.discord.commands.matcher import ApplicationCommandMatcher
from nonebot.adapters.discord.domains.interaction.lifecycle import (
    InteractionResponder,
    current_interaction_responder,
)
from nonebot.adapters.discord.event import ApplicationCommandInteractionEvent
from nonebot.adapters.discord.exception import ActionFailed
import nonebot.adapters.discord.message as message_module
from tests.fake.doubles import DummyBot

from nonebot.compat import type_validate_python
from nonebot.drivers import Response
from nonebot.internal.matcher import (
    Matcher,
    current_bot,
    current_event,
    current_matcher,
)
import pytest

ROOT = Path(__file__).parents[2]
DEPRECATIONS_PATH = ROOT / "tests/fixtures/deprecations.json"
MATCHER_CALLABLES = {
    "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_deferred_response": "send_deferred_response",
    "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_response": "send_response",
    "nonebot.adapters.discord.commands.matcher.ApplicationCommandMatcher.send_followup_msg": "send_followup_msg",
}


def _deprecations() -> dict[str, Any]:
    data = json.loads(DEPRECATIONS_PATH.read_text("utf-8"))
    assert data["removal_target"] == "2.0.0"
    assert isinstance(data["callables"], list)
    assert len(data["callables"]) == 4
    assert isinstance(data["legacy_fallback"], dict)
    return data


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


@pytest.mark.skipif(
    _project_major() >= 2, reason="Deprecated helpers are removed in 2.0"
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
async def test_unmanaged_action_failed_fallback_matches_project_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    deprecations = _deprecations()
    legacy_fallback = deprecations["legacy_fallback"]
    assert isinstance(legacy_fallback, dict)
    expected_warning = legacy_fallback["warning"]
    assert isinstance(expected_warning, str)

    bot = DummyBot()
    event = _interaction_event()
    failure = _action_failed()
    followup_result = object()
    followup_calls: list[dict[str, object]] = []

    async def callback(**kwargs: object) -> None:
        del kwargs
        raise failure

    async def followup(**kwargs: object) -> object:
        followup_calls.append(kwargs)
        return followup_result

    monkeypatch.setattr(bot, "create_interaction_response", callback)
    monkeypatch.setattr(bot, "create_followup_message", followup)
    major = _project_major()
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        if major < 2:
            assert await bot.send(event, "fallback") is followup_result
        else:
            with pytest.raises(ActionFailed) as error:
                await bot.send(event, "no fallback")
            assert error.value is failure

    if major < 2:
        _assert_exact_warning(captured, expected_warning)
        assert len(followup_calls) == 1
    else:
        assert captured == []
        assert followup_calls == []
