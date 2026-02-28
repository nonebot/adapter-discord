from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ...types import UNSET, AllowedMentionType, MessageFlag, Missing, MissingOrNullable

if TYPE_CHECKING:
    from ..common.embeds import Embed
    from ..common.messages import MessageReference
    from ..http.polls import PollRequest
    from ..interactions.message_components import Component, DirectComponent


class AllowedMention(BaseModel):
    """The allowed mention field allows for more granular control over
    mentions without various hacks to the message
    content. This will always validate against message content to avoid
    phantom pings (e.g. to ping everyone, you must
    still have @everyone in the message content),
    and check against user/bot permissions.

    see https://discord.com/developers/docs/resources/message#allowed-mentions-object"""

    parse: list[AllowedMentionType]
    """An array of allowed mention types to parse from the content."""
    roles: list[Snowflake]
    """Array of role_ids to mention (Max size of 100)"""
    users: list[Snowflake]
    """	Array of user_ids to mention (Max size of 100)"""
    replied_user: bool
    """For replies, whether to mention the author of the message
    being replied to (default false)"""


class File(BaseModel):
    """File payload for multipart upload.

    see https://discord.com/developers/docs/reference#uploading-files
    """

    content: bytes
    filename: str


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
    embeds: Missing[list[Embed]] = UNSET
    allowed_mentions: Missing[AllowedMention] = UNSET
    message_reference: Missing[MessageReference] = UNSET
    components: Missing[list[DirectComponent]] = UNSET
    sticker_ids: Missing[list[Snowflake]] = UNSET
    files: Missing[list[File]] = UNSET
    attachments: Missing[list[AttachmentSend]] = UNSET
    flags: Missing[MessageFlag] = UNSET
    poll: Missing[PollRequest] = UNSET


class MessageEditParams(BaseModel):
    """Edit Message Parameters.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/message#edit-message
    """

    content: MissingOrNullable[str] = UNSET
    embeds: MissingOrNullable[list[Embed]] = UNSET
    flags: MissingOrNullable[MessageFlag] = UNSET
    allowed_mentions: MissingOrNullable[AllowedMention] = UNSET
    components: MissingOrNullable[list[Component]] = UNSET
    files: Missing[list[File]] = UNSET
    attachments: MissingOrNullable[list[AttachmentSend]] = UNSET
    sticker_ids: Missing[list[Snowflake]] = UNSET
    poll: MissingOrNullable[PollRequest] = UNSET
