"""Dependency injection for the interaction response lifecycle."""

from typing import Annotated

from nonebot.params import Depends

from ..bot import Bot
from ..domains.interaction.lifecycle import (
    InteractionResponder,
    current_interaction_responder,
)
from ..event import ApplicationCommandInteractionEvent


def _invalid_event_or_bot_error() -> ValueError:
    message = "Invalid event or bot"
    return ValueError(message)


def _missing_responder_error() -> ValueError:
    message = (
        "Interaction responder is not available outside interaction handling context"
    )
    return ValueError(message)


def get_command_response(
    event: object,
    bot: object,
) -> InteractionResponder:
    """Return the responder scoped to the currently handled command interaction."""
    if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
        bot, Bot
    ):
        raise _invalid_event_or_bot_error()

    responder = current_interaction_responder.get()
    if responder is None:
        raise _missing_responder_error()
    return responder


CommandResponse = Annotated[InteractionResponder, Depends(get_command_response)]


__all__ = ["CommandResponse", "get_command_response"]
