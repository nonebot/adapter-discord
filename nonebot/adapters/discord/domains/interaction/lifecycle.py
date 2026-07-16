"""Stateful interaction acknowledgement and response lifecycle."""

from asyncio import Lock
from contextvars import ContextVar
from enum import Enum
from typing import Protocol
from typing_extensions import Unpack

from .conversion import to_followup_message, to_interaction_callback, to_origin_edit
from ...domains.message.conversion import compile_message
from ...domains.models import (
    AllowedMention,
    ExecuteWebhookParams,
    InteractionCallbackMessage,
    InteractionCallbackType,
    InteractionResponse,
    MessageFlag,
    MessageGet,
    WebhookMessageEditParams,
)
from ...event import InteractionCreateEvent
from ...exception import (
    ActionFailed,
    NetworkError,
)
from ...message import Message, MessageSegment
from ...protocol import UNSET, SnowflakeType

INTERACTION_ALREADY_ACKNOWLEDGED = 40060

_UNKNOWN_ACKNOWLEDGEMENT_MESSAGE = "Interaction acknowledgement state is unknown"
_VISIBILITY_FIXED_MESSAGE = "Original response visibility was fixed by defer()"
_ALREADY_ACKNOWLEDGED_MESSAGE = "Interaction has already been acknowledged"
_INITIAL_RESPONSE_INCOMPLETE_MESSAGE = "Initial interaction response has not completed"


class InteractionBot(Protocol):
    """Minimal bot contract required by one interaction lifecycle."""

    async def create_interaction_response(
        self,
        *,
        interaction_id: SnowflakeType,
        interaction_token: str,
        response: InteractionResponse,
        with_response: bool | None = None,
    ) -> InteractionResponse | None: ...

    async def get_origin_interaction_response(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = None,
    ) -> MessageGet: ...

    async def edit_origin_interaction_response(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        **fields: Unpack[WebhookMessageEditParams],
    ) -> MessageGet: ...

    async def create_followup_message(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        **fields: Unpack[ExecuteWebhookParams],
    ) -> MessageGet: ...


class InteractionState(Enum):
    NEW = "new"
    ACKNOWLEDGING = "acknowledging"
    DEFERRED = "deferred"
    RESPONDED = "responded"
    UNKNOWN = "unknown"


class InteractionStateError(RuntimeError):
    """Raised before a request when the interaction lifecycle rejects an operation."""


def _interaction_state_error(message: str) -> InteractionStateError:
    return InteractionStateError(message)


class InteractionResponder:
    """Serialize use of one Discord interaction's initial acknowledgement slot."""

    def __init__(
        self,
        bot: InteractionBot,
        *,
        interaction_id: SnowflakeType,
        application_id: SnowflakeType,
        interaction_token: str,
    ) -> None:
        self._bot = bot
        self._interaction_id = interaction_id
        self._application_id = application_id
        self._interaction_token = interaction_token
        self._lock = Lock()
        self._state = InteractionState.NEW
        self._original_ephemeral = False

    @classmethod
    def from_event(
        cls, bot: InteractionBot, event: InteractionCreateEvent
    ) -> "InteractionResponder":
        return cls(
            bot,
            interaction_id=event.id,
            application_id=event.application_id,
            interaction_token=event.token,
        )

    @property
    def state(self) -> InteractionState:
        """The acknowledged lifecycle state, primarily useful for diagnostics."""
        return self._state

    @staticmethod
    def _convenience_flags(*, ephemeral: bool | None) -> MessageFlag | None:
        if ephemeral is None:
            return None
        return MessageFlag.EPHEMERAL if ephemeral else MessageFlag(0)

    def _raise_if_unknown(self) -> None:
        if self._state is InteractionState.UNKNOWN:
            raise _interaction_state_error(_UNKNOWN_ACKNOWLEDGEMENT_MESSAGE)

    @staticmethod
    def _visibility(flags: MessageFlag) -> bool:
        return bool(flags & MessageFlag.EPHEMERAL)

    def _flags_for_deferred_original(self, flags: MessageFlag | None) -> MessageFlag:
        if flags is None:
            return MessageFlag.EPHEMERAL if self._original_ephemeral else MessageFlag(0)
        if self._visibility(flags) != self._original_ephemeral:
            raise _interaction_state_error(_VISIBILITY_FIXED_MESSAGE)
        return flags

    async def _acknowledge_response(
        self,
        message: str | Message | MessageSegment,
        *,
        flags: MessageFlag | None,
        tts: bool,
        allowed_mentions: AllowedMention | None,
    ) -> MessageGet:
        self._state = InteractionState.ACKNOWLEDGING
        response = InteractionResponse(
            type=InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            data=to_interaction_callback(
                compile_message(message),
                tts=tts,
                allowed_mentions=allowed_mentions,
                flags=flags,
            ),
        )
        try:
            await self._bot.create_interaction_response(
                interaction_id=self._interaction_id,
                interaction_token=self._interaction_token,
                response=response,
            )
        except NetworkError:
            self._state = InteractionState.UNKNOWN
            raise
        except ActionFailed as exc:
            self._state = (
                InteractionState.UNKNOWN
                if exc.code == INTERACTION_ALREADY_ACKNOWLEDGED
                else InteractionState.NEW
            )
            raise

        self._state = InteractionState.RESPONDED
        return await self._bot.get_origin_interaction_response(
            application_id=self._application_id,
            interaction_token=self._interaction_token,
        )

    async def _edit_deferred_original(
        self,
        message: str | Message | MessageSegment,
        *,
        flags: MessageFlag | None,
        tts: bool,
        allowed_mentions: AllowedMention | None,
    ) -> MessageGet:
        del tts
        effective_flags = self._flags_for_deferred_original(flags)
        request = to_origin_edit(
            compile_message(message),
            flags=effective_flags,
            allowed_mentions=(
                allowed_mentions if allowed_mentions is not None else UNSET
            ),
        )
        result = await self._bot.edit_origin_interaction_response(
            application_id=self._application_id,
            interaction_token=self._interaction_token,
            **request,
        )
        self._state = InteractionState.RESPONDED
        return result

    async def _create_followup(
        self,
        message: str | Message | MessageSegment,
        *,
        flags: MessageFlag | None,
        tts: bool,
        allowed_mentions: AllowedMention | None,
    ) -> MessageGet:
        request = to_followup_message(
            compile_message(message),
            tts=tts,
            allowed_mentions=(
                allowed_mentions if allowed_mentions is not None else UNSET
            ),
            flags=flags if flags is not None else UNSET,
        )
        return await self._bot.create_followup_message(
            application_id=self._application_id,
            interaction_token=self._interaction_token,
            **request,
        )

    async def respond(
        self,
        message: str | Message | MessageSegment,
        *,
        ephemeral: bool | None = None,
        tts: bool = False,
        allowed_mentions: AllowedMention | None = None,
    ) -> MessageGet:
        return await self.respond_with_flags(
            message,
            flags=self._convenience_flags(ephemeral=ephemeral),
            tts=tts,
            allowed_mentions=allowed_mentions,
        )

    async def defer(self, *, ephemeral: bool = False) -> None:
        async with self._lock:
            self._raise_if_unknown()
            if self._state is not InteractionState.NEW:
                raise _interaction_state_error(_ALREADY_ACKNOWLEDGED_MESSAGE)

            self._state = InteractionState.ACKNOWLEDGING
            response = InteractionResponse(
                type=InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
                data=(
                    InteractionCallbackMessage(flags=MessageFlag.EPHEMERAL)
                    if ephemeral
                    else UNSET
                ),
            )
            try:
                await self._bot.create_interaction_response(
                    interaction_id=self._interaction_id,
                    interaction_token=self._interaction_token,
                    response=response,
                )
            except NetworkError:
                self._state = InteractionState.UNKNOWN
                raise
            except ActionFailed as exc:
                self._state = (
                    InteractionState.UNKNOWN
                    if exc.code == INTERACTION_ALREADY_ACKNOWLEDGED
                    else InteractionState.NEW
                )
                raise

            self._original_ephemeral = ephemeral
            self._state = InteractionState.DEFERRED

    async def respond_with_flags(
        self,
        message: str | Message | MessageSegment,
        *,
        flags: MessageFlag | None,
        tts: bool = False,
        allowed_mentions: AllowedMention | None = None,
    ) -> MessageGet:
        async with self._lock:
            self._raise_if_unknown()
            if self._state is InteractionState.NEW:
                return await self._acknowledge_response(
                    message,
                    flags=flags,
                    tts=tts,
                    allowed_mentions=allowed_mentions,
                )
            if self._state is InteractionState.DEFERRED:
                return await self._edit_deferred_original(
                    message,
                    flags=flags,
                    tts=tts,
                    allowed_mentions=allowed_mentions,
                )
            if self._state is InteractionState.RESPONDED:
                return await self._create_followup(
                    message,
                    flags=flags,
                    tts=tts,
                    allowed_mentions=allowed_mentions,
                )
            raise _interaction_state_error(_ALREADY_ACKNOWLEDGED_MESSAGE)

    async def followup(
        self,
        message: str | Message | MessageSegment,
        *,
        ephemeral: bool = False,
        tts: bool = False,
        allowed_mentions: AllowedMention | None = None,
    ) -> MessageGet:
        return await self.followup_with_flags(
            message,
            flags=self._convenience_flags(ephemeral=ephemeral),
            tts=tts,
            allowed_mentions=allowed_mentions,
        )

    async def followup_with_flags(
        self,
        message: str | Message | MessageSegment,
        *,
        flags: MessageFlag | None,
        tts: bool = False,
        allowed_mentions: AllowedMention | None = None,
    ) -> MessageGet:
        async with self._lock:
            self._raise_if_unknown()
            if self._state is InteractionState.NEW:
                raise _interaction_state_error(_INITIAL_RESPONSE_INCOMPLETE_MESSAGE)
            if self._state not in {
                InteractionState.DEFERRED,
                InteractionState.RESPONDED,
            }:
                raise _interaction_state_error(_ALREADY_ACKNOWLEDGED_MESSAGE)
            return await self._create_followup(
                message,
                flags=flags,
                tts=tts,
                allowed_mentions=allowed_mentions,
            )


current_interaction_responder: ContextVar[InteractionResponder | None] = ContextVar(
    "current_interaction_responder", default=None
)


__all__ = [
    "INTERACTION_ALREADY_ACKNOWLEDGED",
    "InteractionResponder",
    "InteractionState",
    "InteractionStateError",
    "current_interaction_responder",
]
