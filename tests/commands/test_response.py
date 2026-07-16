from types import SimpleNamespace
from typing import cast

from nonebot.adapters import MessageTemplate
from nonebot.adapters.discord.commands.matcher import ApplicationCommandMatcher
from nonebot.adapters.discord.commands.response import get_command_response
from nonebot.adapters.discord.domains.interaction.lifecycle import (
    InteractionResponder,
    current_interaction_responder,
)
from nonebot.adapters.discord.domains.models import (
    InteractionCallbackType,
    InteractionResponse,
    MessageFlag,
)
from nonebot.adapters.discord.event import ApplicationCommandInteractionEvent
from tests.fake.doubles import DummyBot

from nonebot.compat import type_validate_python
from nonebot.internal.matcher import (
    Matcher,
    current_bot,
    current_event,
    current_matcher,
)
import pytest


def _event() -> ApplicationCommandInteractionEvent:
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


def test_command_response_requires_valid_managed_context() -> None:
    event = _event()
    bot = DummyBot()

    with pytest.raises(ValueError, match="Invalid event or bot"):
        get_command_response(event, object())  # type: ignore[arg-type]
    with pytest.raises(
        ValueError,
        match="Interaction responder is not available outside interaction handling context",
    ):
        get_command_response(event, bot)

    responder = InteractionResponder.from_event(bot, event)
    token = current_interaction_responder.set(responder)
    try:
        assert get_command_response(event, bot) is responder
    finally:
        current_interaction_responder.reset(token)


@pytest.mark.asyncio
async def test_deprecated_matcher_adapters_warn_delegate_and_format_templates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event = _event()
    bot = DummyBot()
    calls: list[tuple[str, dict[str, object]]] = []

    async def callback(**kwargs: object) -> None:
        calls.append(("callback", kwargs))

    async def followup(**kwargs: object) -> object:
        calls.append(("followup", kwargs))
        return object()

    monkeypatch.setattr(bot, "create_interaction_response", callback)
    monkeypatch.setattr(bot, "create_followup_message", followup)
    responder = InteractionResponder.from_event(bot, event)
    event_token = current_event.set(event)
    bot_token = current_bot.set(bot)
    matcher_token = current_matcher.set(
        cast("Matcher", SimpleNamespace(state={"name": "Ada"}))
    )
    responder_token = current_interaction_responder.set(responder)
    try:
        with pytest.warns(
            DeprecationWarning,
            match=r"send_deferred_response\(\) is deprecated and will be removed in 2.0; inject CommandResponse and call response.defer\(\)",
        ):
            assert await ApplicationCommandMatcher.send_deferred_response() is None
        assert calls[0][0] == "callback"
        response = calls[0][1]["response"]
        assert isinstance(response, InteractionResponse)
        assert (
            response.type
            is InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
        )

        flags = MessageFlag.EPHEMERAL | MessageFlag.SUPPRESS_NOTIFICATIONS
        with pytest.warns(
            DeprecationWarning,
            match=r"send_followup_msg\(\) is deprecated and will be removed in 2.0; inject CommandResponse and call response.followup\(\)",
        ):
            followup_result = await ApplicationCommandMatcher.send_followup_msg(
                MessageTemplate("hello {name}"), flags=flags
            )
        assert followup_result is not None
        assert calls[-1][0] == "followup"
        assert calls[-1][1]["content"] == "hello Ada"
        assert calls[-1][1]["flags"] == int(flags)

        sent = object()

        async def send(cls: type[ApplicationCommandMatcher], message: object) -> object:
            assert cls is ApplicationCommandMatcher
            assert message == "unchanged"
            return sent

        monkeypatch.setattr(ApplicationCommandMatcher, "send", classmethod(send))
        with pytest.warns(
            DeprecationWarning,
            match=r"send_response\(\) is deprecated and will be removed in 2.0; inject CommandResponse and call response.respond\(\)",
        ):
            assert await ApplicationCommandMatcher.send_response("unchanged") is sent
    finally:
        current_interaction_responder.reset(responder_token)
        current_matcher.reset(matcher_token)
        current_bot.reset(bot_token)
        current_event.reset(event_token)
