"""Canonical interaction.write models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import (
        AllowedMention,
        ApplicationCommandOptionChoice,
        AttachmentSend,
        Component,
        Embed,
        File,
        PollRequest,
    )

from .._model_support import BaseModel, MessageFlag


class InteractionCallbackMessage(BaseModel):
    """Interaction callback message.

    Not all message fields are currently supported.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    tts: bool | None = None
    """is the response TTS"""
    content: str | None = None
    """message content"""
    embeds: list[Embed] | None = None
    """supports up to 10 embeds"""
    allowed_mentions: AllowedMention | None = None
    """allowed mentions object"""
    flags: MessageFlag | None = None
    """message flags combined as a bitfield
    (only SUPPRESS_EMBEDS and EPHEMERAL can be set)"""
    components: list[Component] | None = None
    """message components"""
    attachments: list[AttachmentSend] | None = None
    """attachment objects with filename and description.
    See Uploading Files for details."""
    poll: PollRequest | None = None
    """Details about the poll"""

    files: list[File] | None = None


class InteractionCallbackAutocomplete(BaseModel):
    """Interaction callback Autocomplete.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: list[ApplicationCommandOptionChoice]
    """autocomplete choices (max of 25 choices)"""


class InteractionCallbackModal(BaseModel):
    """Interaction callback modal.

    Support for components in modals is currently limited to type 4 (Text Input).

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-modal
    """

    custom_id: str
    """a developer-defined identifier for the modal, max 100 characters"""
    title: str
    """the title of the popup modal, max 45 characters"""
    components: list[Component]
    """between 1 and 5 (inclusive) components that make up the modal"""


InteractionCallbackData = (
    InteractionCallbackMessage
    | InteractionCallbackAutocomplete
    | InteractionCallbackModal
)

__all__ = [
    "InteractionCallbackAutocomplete",
    "InteractionCallbackData",
    "InteractionCallbackMessage",
    "InteractionCallbackModal",
]
