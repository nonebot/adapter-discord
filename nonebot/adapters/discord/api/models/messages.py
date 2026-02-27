from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ..types import (
    UNSET,
    AllowedMentionType,
    AttachmentFlag,
    ChannelType,
    MessageActivityType,
    MessageFlag,
    MessageReferenceType,
    MessageType,
    Missing,
    MissingOrNullable,
)

if TYPE_CHECKING:
    from .channels import Channel
    from .embeds import Embed
    from ..model import (
        Application,
        Component,
        DirectComponent,
        Emoji,
        MessageInteraction,
        MessageInteractionMetadata,
        Poll,
        PollRequest,
        ResolvedData,
        Sticker,
        StickerItem,
        User,
    )


class MessageGet(BaseModel):
    """Message

    see https://discord.com/developers/docs/resources/message#message-object"""

    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: datetime.datetime
    edited_timestamp: datetime.datetime | None = Field(...)
    tts: bool
    mention_everyone: bool
    mentions: list[User]
    mention_roles: list[Snowflake]
    mention_channels: Missing[list[ChannelMention]] = UNSET
    attachments: list[Attachment]
    embeds: list[Embed]
    reactions: Missing[list[Reaction]] = UNSET
    nonce: Missing[int | str] = UNSET
    pinned: bool
    webhook_id: Missing[Snowflake] = UNSET
    type: MessageType
    activity: Missing[MessageActivity] = UNSET
    application: Missing[Application] = UNSET
    application_id: Missing[Snowflake] = UNSET
    message_reference: Missing[MessageReference] = UNSET
    flags: Missing[MessageFlag] = UNSET
    message_snapshots: Missing[list[MessageSnapshot]] = UNSET
    referenced_message: MissingOrNullable[MessageGet] = UNSET
    interaction_metadata: Missing[MessageInteractionMetadata] = UNSET
    interaction: Missing[MessageInteraction] = UNSET
    thread: Missing[Channel] = UNSET
    components: Missing[list[DirectComponent]] = UNSET
    sticker_items: Missing[list[StickerItem]] = UNSET
    stickers: Missing[list[Sticker]] = UNSET
    position: Missing[int] = UNSET
    role_subscription_data: Missing[RoleSubscriptionData] = UNSET
    resolved: Missing[ResolvedData] = UNSET
    poll: Missing[Poll] = UNSET
    call: Missing[MessageCall] = UNSET


class MessageActivity(BaseModel):
    """Message activity.

    see https://discord.com/developers/docs/resources/message#message-object-message-activity-structure
    """

    type: MessageActivityType
    party_id: Missing[str] = UNSET


class MessageCall(BaseModel):
    """Information about the call in a private channel.

    see https://discord.com/developers/docs/resources/message#message-call-object
    """

    participants: list[Snowflake]
    ended_timestamp: MissingOrNullable[datetime.datetime] = UNSET


class MessageReference(BaseModel):
    """Message reference.

    see https://discord.com/developers/docs/resources/message#message-reference-object
    """

    type: Missing[MessageReferenceType] = UNSET
    """type of reference."""
    message_id: Missing[Snowflake] = UNSET
    """id of the originating message"""
    channel_id: Missing[Snowflake] = UNSET
    """id of the originating message's channel.
    channel_id is optional when creating a reply,
    but will always be present when receiving an
    event/response that includes this data model."""
    guild_id: Missing[Snowflake] = UNSET
    """id of the originating message's guild"""
    fail_if_not_exists: Missing[bool] = UNSET
    """when sending, whether to error if the referenced
    message doesn't exist instead of sending
    as a normal (non-reply) message, default true"""


class MessageSnapshot(BaseModel):
    """Message Snapshot

    While message snapshots are able to support nested snapshots, we currently limit the depth of nesting to 1.
    see https://discord.com/developers/docs/resources/message#message-snapshot-object
    """

    message: MessageSnapshotMessage


class MessageSnapshotMessage(BaseModel):
    """partial message object for Message Snapshot

    see https://discord.com/developers/docs/resources/message#message-snapshot-object"""

    type: MessageType
    content: str
    embeds: list[Embed]
    attachments: list[Attachment]
    timestamp: datetime.datetime
    edited_timestamp: datetime.datetime | None = Field(...)
    flags: Missing[MessageFlag] = UNSET
    mentions: list[User]
    mention_roles: Missing[list[Snowflake]] = UNSET
    components: Missing[list[DirectComponent]] = UNSET
    sticker_items: Missing[list[StickerItem]] = UNSET
    stickers: Missing[list[Sticker]] = UNSET


class Reaction(BaseModel):
    """Reaction.

    see https://discord.com/developers/docs/resources/message#reaction-object"""

    count: int
    count_details: Missing[CountDetails] = UNSET
    me: bool
    me_burst: Missing[bool] = UNSET
    emoji: Emoji
    burst_colors: Missing[list[str]] = UNSET


class CountDetails(BaseModel):
    """Reaction Count Details

    see https://discord.com/developers/docs/resources/message#reaction-count-details-object
    """

    burst: int
    normal: int


class Attachment(BaseModel):
    """Attachment

    see https://discord.com/developers/docs/resources/message#attachment-object"""

    id: Snowflake
    filename: str
    title: Missing[str] = UNSET
    description: Missing[str] = UNSET
    content_type: Missing[str] = UNSET
    size: int
    url: str
    proxy_url: str
    height: MissingOrNullable[int] = UNSET
    width: MissingOrNullable[int] = UNSET
    ephemeral: Missing[bool] = UNSET
    duration_secs: Missing[float] = UNSET
    waveform: Missing[str] = UNSET
    flags: Missing[AttachmentFlag] = UNSET


class ChannelMention(BaseModel):
    """Channel mention.

    see https://discord.com/developers/docs/resources/message#channel-mention-object"""

    id: str
    guild_id: str
    type: ChannelType
    name: str


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


class RoleSubscriptionData(BaseModel):
    """Role subscription data.

    see https://discord.com/developers/docs/resources/message#role-subscription-data-object
    """

    role_subscription_listing_id: str
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool


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


class WebhookMessageEditParams(BaseModel):
    """Edit Webhook Message Parameters.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/webhook#edit-webhook-message
    """

    content: MissingOrNullable[str] = UNSET
    embeds: MissingOrNullable[list[Embed]] = UNSET
    flags: MissingOrNullable[MessageFlag] = UNSET
    allowed_mentions: MissingOrNullable[AllowedMention] = UNSET
    components: MissingOrNullable[list[Component]] = UNSET
    files: Missing[list[File]] = UNSET
    attachments: MissingOrNullable[list[AttachmentSend]] = UNSET
    poll: MissingOrNullable[PollRequest] = UNSET
