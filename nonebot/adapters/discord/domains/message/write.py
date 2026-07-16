"""Canonical message.write models."""

from typing import TYPE_CHECKING

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

from .._model_support import (
    UNSET,
    BaseModel,
    MessageFlag,
    Missing,
    MissingOrNullable,
    Snowflake,
)


class AttachmentSend(BaseModel):
    """Attachment Send

    see https://discord.com/developers/docs/resources/channel#attachment-object"""

    id: Missing[int] = UNSET
    filename: Missing[str] = UNSET
    description: MissingOrNullable[str] = UNSET


class MessageSend(BaseModel):
    """Message Send

    see https://discord.com/developers/docs/resources/message#create-message"""

    content: Missing[str] = UNSET
    nonce: Missing[int | str] = UNSET
    enforce_nonce: Missing[bool] = UNSET
    tts: Missing[bool] = UNSET
    embeds: Missing[list["Embed"]] = UNSET
    allowed_mentions: Missing["AllowedMention"] = UNSET
    message_reference: Missing["MessageReference"] = UNSET
    components: Missing[list["DirectComponent"]] = UNSET
    sticker_ids: Missing[list[Snowflake]] = UNSET
    files: Missing[list["File"]] = UNSET
    attachments: Missing[list[AttachmentSend]] = UNSET
    flags: Missing[MessageFlag] = UNSET
    poll: Missing["PollRequest"] = UNSET


class MessageEditParams(BaseModel):
    """Edit Message Parameters.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/message#edit-message
    """

    content: MissingOrNullable[str] = UNSET
    embeds: MissingOrNullable[list["Embed"]] = UNSET
    flags: MissingOrNullable[MessageFlag] = UNSET
    allowed_mentions: MissingOrNullable["AllowedMention"] = UNSET
    components: MissingOrNullable[list["Component"]] = UNSET
    files: Missing[list["File"]] = UNSET
    attachments: MissingOrNullable[list[AttachmentSend]] = UNSET
    sticker_ids: Missing[list[Snowflake]] = UNSET
    poll: MissingOrNullable["PollRequest"] = UNSET


class PollRequest(BaseModel):
    """This is the request object used when creating a poll across the
    different endpoints. It is similar but not exactly identical to the
    main poll object. The main difference is that the request has `duration`
    which eventually becomes `expiry`.

    see https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    question: "PollMedia"
    """The question of the poll. Only `text` is supported."""
    answers: list["PollAnswerRequest"]
    """Each of the answers available in the poll, up to 10"""
    duration: Missing[int] = UNSET
    """Number of hours the poll should be open for, up to 32 days. Defaults to 24"""
    allow_multiselect: Missing[bool] = UNSET
    """Whether a user can select multiple answers. Defaults to false"""
    layout_type: Missing[int] = UNSET
    """The layout type of the poll"""


class PollAnswerRequest(BaseModel):
    """Poll answer request object.

    see https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    poll_media: "PollMedia"


__all__ = [
    "AttachmentSend",
    "MessageEditParams",
    "MessageSend",
    "PollAnswerRequest",
    "PollRequest",
]
