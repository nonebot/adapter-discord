"""Canonical interaction.write models."""

from typing import TYPE_CHECKING
from typing_extensions import Required

from .._model_support import OutboundTypedDict

if TYPE_CHECKING:
    from ..models import (
        AllowedMention,
        ApplicationCommandOptionChoice,
        AttachmentSend,
        Component,
        DirectComponent,
        Embed,
        File,
        PollRequest,
    )

from .._model_support import MessageFlag


class InteractionCallbackMessage(OutboundTypedDict, total=False):
    """Interaction callback message.

    Not all message fields are currently supported.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    tts: bool | None
    """is the response TTS"""
    content: str | None
    """message content"""
    embeds: "list[Embed] | None"
    """supports up to 10 embeds"""
    allowed_mentions: "AllowedMention | None"
    """allowed mentions object"""
    flags: MessageFlag | None
    """message flags combined as a bitfield
    (only SUPPRESS_EMBEDS and EPHEMERAL can be set)"""
    components: "list[Component] | None"
    """message components"""
    attachments: "list[AttachmentSend] | None"
    """attachment objects with filename and description.
    See Uploading Files for details."""
    poll: "PollRequest | None"
    """Details about the poll"""

    files: "list[File] | None"


class CreateFollowupMessageParams(OutboundTypedDict, total=False):
    """Parameters for creating an interaction followup message."""

    content: str | None
    tts: bool | None
    embeds: "list[Embed] | None"
    allowed_mentions: "AllowedMention | None"
    components: "list[DirectComponent] | None"
    files: "list[File] | None"
    attachments: "list[AttachmentSend] | None"
    flags: MessageFlag | None
    poll: "PollRequest | None"


class InteractionCallbackAutocomplete(OutboundTypedDict, total=False):
    """Interaction callback Autocomplete.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: Required["list[ApplicationCommandOptionChoice]"]
    """autocomplete choices (max of 25 choices)"""


class InteractionCallbackModal(OutboundTypedDict, total=False):
    """Interaction callback modal.

    Support for components in modals is currently limited to type 4 (Text Input).

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-modal
    """

    custom_id: Required[str]
    """a developer-defined identifier for the modal, max 100 characters"""
    title: Required[str]
    """the title of the popup modal, max 45 characters"""
    components: Required["list[Component]"]
    """between 1 and 5 (inclusive) components that make up the modal"""


InteractionCallbackData = (
    InteractionCallbackMessage
    | InteractionCallbackAutocomplete
    | InteractionCallbackModal
)

__all__ = [
    "CreateFollowupMessageParams",
    "InteractionCallbackAutocomplete",
    "InteractionCallbackData",
    "InteractionCallbackMessage",
    "InteractionCallbackModal",
]
