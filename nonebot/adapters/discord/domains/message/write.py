"""Canonical message.write models."""

from typing import TYPE_CHECKING
from typing_extensions import Required, TypedDict

if TYPE_CHECKING:
    from ..models import (
        AllowedMention,
        Component,
        DirectComponent,
        Embed,
        File,
        MessageReference,
        PollMedia,
    )
    from ...protocol import SnowflakeType

from .._model_support import MessageFlag


class AttachmentSend(TypedDict, total=False):
    """Attachment Send

    see https://discord.com/developers/docs/resources/channel#attachment-object"""

    id: int
    filename: str
    description: str | None


class MessageSend(TypedDict, total=False):
    """Message Send

    see https://discord.com/developers/docs/resources/message#create-message"""

    content: str
    nonce: int | str
    enforce_nonce: bool
    tts: bool
    embeds: "list[Embed]"
    allowed_mentions: "AllowedMention"
    message_reference: "MessageReference"
    components: "list[DirectComponent]"
    sticker_ids: "list[SnowflakeType]"
    files: "list[File]"
    attachments: list[AttachmentSend]
    flags: MessageFlag
    poll: "PollRequest"


class MessageEditParams(TypedDict, total=False):
    """Edit Message Parameters.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/message#edit-message
    """

    content: str | None
    embeds: "list[Embed] | None"
    flags: MessageFlag | None
    allowed_mentions: "AllowedMention | None"
    components: "list[Component] | None"
    files: "list[File]"
    attachments: list[AttachmentSend] | None
    sticker_ids: "list[SnowflakeType]"
    poll: "PollRequest | None"


class PollRequest(TypedDict, total=False):
    """This is the request object used when creating a poll across the
    different endpoints. It is similar but not exactly identical to the
    main poll object. The main difference is that the request has `duration`
    which eventually becomes `expiry`.

    see https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    question: Required["PollMedia"]
    """The question of the poll. Only `text` is supported."""
    answers: Required["list[PollAnswerRequest]"]
    """Each of the answers available in the poll, up to 10"""
    duration: int
    """Number of hours the poll should be open for, up to 32 days. Defaults to 24"""
    allow_multiselect: bool
    """Whether a user can select multiple answers. Defaults to false"""
    layout_type: int
    """The layout type of the poll"""


class PollAnswerRequest(TypedDict, total=False):
    """Poll answer request object.

    see https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    poll_media: Required["PollMedia"]


class BulkDeleteMessagesParams(TypedDict, total=False):
    """Parameters for ``_api_bulk_delete_message``."""

    messages: Required["list[SnowflakeType]"]


__all__ = [
    "AttachmentSend",
    "BulkDeleteMessagesParams",
    "MessageEditParams",
    "MessageSend",
    "PollAnswerRequest",
    "PollRequest",
]
