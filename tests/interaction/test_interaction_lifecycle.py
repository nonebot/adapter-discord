from asyncio import Event, create_task, gather
from contextvars import Token
from typing import cast

from nonebot.adapters.discord.bot import Bot
from nonebot.adapters.discord.domains.interaction.lifecycle import (
    INTERACTION_ALREADY_ACKNOWLEDGED,
    InteractionResponder,
    InteractionState,
    InteractionStateError,
    current_interaction_responder,
)
from nonebot.adapters.discord.domains.models import (
    InteractionCallbackMessage,
    InteractionResponse,
    MessageFlag,
    MessageGet,
)
from nonebot.adapters.discord.event import ApplicationCommandInteractionEvent
from nonebot.adapters.discord.exception import ActionFailed, NetworkError
from tests.fake.doubles import DummyBot

from nonebot.compat import type_validate_python
from nonebot.drivers import Response
import pytest

INTERACTION_TOKEN = InteractionResponder.__name__


def _interaction_event() -> ApplicationCommandInteractionEvent:
    return type_validate_python(
        ApplicationCommandInteractionEvent,
        {
            "id": "10",
            "application_id": "11",
            "type": 2,
            "token": INTERACTION_TOKEN,
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


def _action_failed(code: int) -> ActionFailed:
    return ActionFailed(Response(400, content=f'{{"code": {code}}}'.encode()))


class RecordingBot:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.callback_error: Exception | None = None
        self.original_error: Exception | None = None
        self.patch_error: Exception | None = None
        self.followup_error: Exception | None = None
        self.callback_started: Event | None = None
        self.callback_release: Event | None = None
        self.original = cast("MessageGet", object())
        self.patched = cast("MessageGet", object())
        self.followup = cast("MessageGet", object())

    async def create_interaction_response(self, **kwargs: object) -> None:
        self.calls.append(("callback", kwargs))
        if self.callback_started is not None:
            self.callback_started.set()
        if self.callback_release is not None:
            await self.callback_release.wait()
        if self.callback_error is not None:
            raise self.callback_error

    async def get_origin_interaction_response(self, **kwargs: object) -> MessageGet:
        self.calls.append(("original", kwargs))
        if self.original_error is not None:
            raise self.original_error
        return self.original

    async def edit_origin_interaction_response(self, **kwargs: object) -> MessageGet:
        self.calls.append(("patch", kwargs))
        if self.patch_error is not None:
            raise self.patch_error
        return self.patched

    async def create_followup_message(self, **kwargs: object) -> MessageGet:
        self.calls.append(("followup", kwargs))
        if self.followup_error is not None:
            raise self.followup_error
        return self.followup


def _responder(bot: RecordingBot) -> InteractionResponder:
    return InteractionResponder(
        bot,
        interaction_id=10,
        application_id=11,
        interaction_token=INTERACTION_TOKEN,
    )


@pytest.mark.asyncio
async def test_initial_network_error_marks_state_unknown_before_next_request() -> None:
    bot = RecordingBot()
    bot.callback_error = NetworkError("lost")
    responder = _responder(bot)

    with pytest.raises(NetworkError):
        await responder.respond("one")

    assert responder.state is InteractionState.UNKNOWN
    with pytest.raises(
        InteractionStateError, match="Interaction acknowledgement state is unknown"
    ):
        await responder.respond("two")
    assert [name for name, _ in bot.calls] == ["callback"]


@pytest.mark.asyncio
async def test_explicit_callback_failures_are_retryable_except_already_acknowledged() -> (
    None
):
    bot = RecordingBot()
    responder = _responder(bot)
    bot.callback_error = _action_failed(50035)

    with pytest.raises(ActionFailed):
        await responder.respond("one")
    assert responder.state is InteractionState.NEW

    bot.callback_error = None
    assert await responder.respond("two") is bot.original
    assert responder.state is InteractionState.RESPONDED

    acknowledged_bot = RecordingBot()
    acknowledged_bot.callback_error = _action_failed(INTERACTION_ALREADY_ACKNOWLEDGED)
    acknowledged = _responder(acknowledged_bot)
    with pytest.raises(ActionFailed):
        await acknowledged.respond("one")
    assert acknowledged.state is InteractionState.UNKNOWN


@pytest.mark.asyncio
async def test_original_fetch_failure_keeps_responded_and_deferred_patch_failure_keeps_deferred() -> (
    None
):
    bot = RecordingBot()
    bot.original_error = NetworkError("original unavailable")
    responder = _responder(bot)
    with pytest.raises(NetworkError):
        await responder.respond("one")
    assert responder.state is InteractionState.RESPONDED

    deferred_bot = RecordingBot()
    deferred = _responder(deferred_bot)
    await deferred.defer()
    deferred_bot.patch_error = _action_failed(50035)
    with pytest.raises(ActionFailed):
        await deferred.respond("one")
    assert deferred.state is InteractionState.DEFERRED


@pytest.mark.asyncio
async def test_followup_failure_preserves_acknowledged_state_and_new_operations_reject_locally() -> (
    None
):
    bot = RecordingBot()
    responder = _responder(bot)
    with pytest.raises(
        InteractionStateError, match="Initial interaction response has not completed"
    ):
        await responder.followup("before")

    await responder.defer()
    with pytest.raises(
        InteractionStateError, match="Interaction has already been acknowledged"
    ):
        await responder.defer()

    bot.followup_error = _action_failed(50035)
    with pytest.raises(ActionFailed):
        await responder.followup("after")
    assert responder.state is InteractionState.DEFERRED


@pytest.mark.asyncio
async def test_concurrent_responds_use_one_callback_then_followup() -> None:
    bot = RecordingBot()
    bot.callback_started = Event()
    bot.callback_release = Event()
    responder = _responder(bot)

    first = create_task(responder.respond("first"))
    await bot.callback_started.wait()
    second = create_task(responder.respond("second"))
    bot.callback_release.set()
    first_result, second_result = await gather(first, second)

    assert first_result is bot.original
    assert second_result is bot.followup
    assert [name for name, _ in bot.calls] == ["callback", "original", "followup"]


@pytest.mark.asyncio
async def test_deferred_visibility_inherits_or_rejects_conflicts_and_preserves_other_bits() -> (
    None
):
    bot = RecordingBot()
    responder = _responder(bot)
    await responder.defer(ephemeral=True)

    inherited = await responder.respond("original")
    assert inherited is bot.patched
    patch_flags = bot.calls[-1][1]["flags"]
    assert patch_flags == MessageFlag.EPHEMERAL
    assert await responder.followup("details") is bot.followup
    assert [name for name, _ in bot.calls] == ["callback", "patch", "followup"]

    conflict_bot = RecordingBot()
    conflict = _responder(conflict_bot)
    await conflict.defer(ephemeral=True)
    with pytest.raises(
        InteractionStateError,
        match=r"Original response visibility was fixed by defer\(\)",
    ):
        await conflict.respond("wrong", ephemeral=False)
    with pytest.raises(
        InteractionStateError,
        match=r"Original response visibility was fixed by defer\(\)",
    ):
        await conflict.respond_with_flags("wrong", flags=MessageFlag.SUPPRESS_EMBEDS)

    matching_bot = RecordingBot()
    matching = _responder(matching_bot)
    await matching.defer(ephemeral=True)
    flags = MessageFlag.EPHEMERAL | MessageFlag.SUPPRESS_EMBEDS
    await matching.respond_with_flags("right", flags=flags)
    assert matching_bot.calls[-1][1]["flags"] == flags


@pytest.mark.asyncio
async def test_bot_send_uses_managed_responder_for_all_acknowledged_states(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event = _interaction_event()
    bot = DummyBot()
    calls: list[tuple[str, dict[str, object]]] = []

    async def callback(**kwargs: object) -> None:
        calls.append(("callback", kwargs))

    async def original(**kwargs: object) -> MessageGet:
        calls.append(("original", kwargs))
        return cast("MessageGet", object())

    async def patch(**kwargs: object) -> MessageGet:
        calls.append(("patch", kwargs))
        return cast("MessageGet", object())

    async def followup(**kwargs: object) -> MessageGet:
        calls.append(("followup", kwargs))
        return cast("MessageGet", object())

    monkeypatch.setattr(bot, "create_interaction_response", callback)
    monkeypatch.setattr(bot, "get_origin_interaction_response", original)
    monkeypatch.setattr(bot, "edit_origin_interaction_response", patch)
    monkeypatch.setattr(bot, "create_followup_message", followup)
    responder = InteractionResponder.from_event(bot, event)
    token = current_interaction_responder.set(responder)
    deferred_token: Token[InteractionResponder | None] | None = None
    try:
        initial_flags = MessageFlag.SUPPRESS_EMBEDS | MessageFlag.SUPPRESS_NOTIFICATIONS
        await bot.send(event, "initial", flags=initial_flags)
        response = calls[0][1]["response"]
        assert isinstance(response, InteractionResponse)
        assert isinstance(response.data, InteractionCallbackMessage)
        assert response.data.flags == initial_flags

        deferred = InteractionResponder.from_event(bot, event)
        deferred_token = current_interaction_responder.set(deferred)
        await deferred.defer(ephemeral=True)
        deferred_flags = MessageFlag.EPHEMERAL | MessageFlag.SUPPRESS_NOTIFICATIONS
        await bot.send(event, "edited", flags=deferred_flags)
        assert calls[-1][0] == "patch"
        assert calls[-1][1]["flags"] == deferred_flags

        followup_flags = (
            MessageFlag.SUPPRESS_EMBEDS | MessageFlag.SUPPRESS_NOTIFICATIONS
        )
        await bot.send(event, "followup", flags=followup_flags)
        assert calls[-1][0] == "followup"
        assert calls[-1][1]["flags"] == int(followup_flags)
    finally:
        if deferred_token is not None:
            current_interaction_responder.reset(deferred_token)
        current_interaction_responder.reset(token)


@pytest.mark.asyncio
async def test_bot_send_fallback_warns_only_after_callback_action_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bot = DummyBot()
    event = _interaction_event()

    async def callback(**kwargs: object) -> None:
        del kwargs
        raise _action_failed(INTERACTION_ALREADY_ACKNOWLEDGED)

    async def followup(**kwargs: object) -> MessageGet:
        del kwargs
        return cast("MessageGet", object())

    monkeypatch.setattr(bot, "create_interaction_response", callback)
    monkeypatch.setattr(bot, "create_followup_message", followup)
    with pytest.warns(
        DeprecationWarning,
        match="Automatic interaction followup after ActionFailed is deprecated",
    ):
        await bot.send(event, "fallback")


@pytest.mark.asyncio
async def test_handle_event_scopes_and_resets_responder(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event = _interaction_event()
    bot = DummyBot()
    seen: list[InteractionResponder | None] = []

    async def fake_handle_event(received_bot: Bot, received_event: object) -> None:
        assert received_bot is bot
        assert received_event is event
        seen.append(current_interaction_responder.get())

    monkeypatch.setattr("nonebot.adapters.discord.bot.handle_event", fake_handle_event)
    await bot.handle_event(event)

    assert len(seen) == 1
    assert seen[0] is not None
    assert current_interaction_responder.get() is None
