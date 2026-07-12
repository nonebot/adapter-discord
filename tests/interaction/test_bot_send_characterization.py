from nonebot.adapters.discord.api.model import (
    InteractionResponse,
)
from nonebot.adapters.discord.api.types import InteractionCallbackType
from nonebot.adapters.discord.event import ApplicationCommandInteractionEvent
from nonebot.adapters.discord.exception import ActionFailed
from tests.fake.doubles import DummyBot

from nonebot.compat import type_validate_python
from nonebot.drivers import Response
import pytest


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


@pytest.mark.asyncio
async def test_bot_send_interaction_callback_success_fetches_original(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bot = DummyBot()
    event = _interaction_event()
    original_message = object()
    calls: list[tuple[str, dict[str, object]]] = []

    async def create_interaction_response(**kwargs: object) -> None:
        calls.append(("callback", kwargs))

    async def get_origin_interaction_response(**kwargs: object) -> object:
        calls.append(("original", kwargs))
        return original_message

    monkeypatch.setattr(bot, "create_interaction_response", create_interaction_response)
    monkeypatch.setattr(
        bot, "get_origin_interaction_response", get_origin_interaction_response
    )

    result = await bot.send(event, "hello")

    assert result is original_message
    assert [name for name, _ in calls] == ["callback", "original"]
    callback = calls[0][1]
    assert callback["interaction_id"] == event.id
    assert callback["interaction_token"] == event.token
    response = callback["response"]
    assert isinstance(response, InteractionResponse)
    assert response.type is InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE
    data = response.data
    assert isinstance(data, dict)
    assert data.get("content") == "hello"
    assert calls[1][1] == {
        "application_id": event.application_id,
        "interaction_token": event.token,
    }


@pytest.mark.asyncio
async def test_bot_send_interaction_callback_action_failed_uses_followup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bot = DummyBot()
    event = _interaction_event()
    followup_message = object()
    calls: list[tuple[str, dict[str, object]]] = []

    async def create_interaction_response(**kwargs: object) -> None:
        calls.append(("callback", kwargs))
        raise ActionFailed(Response(400, content=b'{"code": 40060}'))

    async def create_followup_message(**kwargs: object) -> object:
        calls.append(("followup", kwargs))
        return followup_message

    failure_message = "original response must not be fetched after callback failure"

    async def get_origin_interaction_response(**kwargs: object) -> object:
        del kwargs
        raise AssertionError(failure_message)

    monkeypatch.setattr(bot, "create_interaction_response", create_interaction_response)
    monkeypatch.setattr(bot, "create_followup_message", create_followup_message)
    monkeypatch.setattr(
        bot, "get_origin_interaction_response", get_origin_interaction_response
    )

    result = await bot.send(event, "hello")

    assert result is followup_message
    assert [name for name, _ in calls] == ["callback", "followup"]
    assert calls[1][1]["application_id"] == event.application_id
    assert calls[1][1]["interaction_token"] == event.token
    assert calls[1][1]["content"] == "hello"
