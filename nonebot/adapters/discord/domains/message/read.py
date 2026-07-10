"""Canonical message.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import (
        ActivityAssets,
        ActivityButtons,
        ActivityEmoji,
        ActivityParty,
        ActivitySecrets,
        ActivityTimestamps,
        Application,
        Channel,
        ChannelMention,
        CountDetails,
        DirectComponent,
        Emoji,
        GuildMember,
        Role,
        Sticker,
        StickerItem,
        User,
    )

from .._model_support import (
    UNSET,
    ActivityFlags,
    ActivityType,
    AllowedMentionType,
    ApplicationIntegrationType,
    AttachmentFlag,
    BaseModel,
    EmbedTypes,
    Field,
    InteractionType,
    Literal,
    MessageActivityType,
    MessageFlag,
    MessageReferenceType,
    MessageType,
    Missing,
    MissingOrNullable,
    Snowflake,
    datetime,
)


class ResolvedData(BaseModel):
    """Resolved Data

    If data for a Member is included,
    data for its corresponding User will also be included.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """

    users: Missing[dict[Snowflake, User]] = UNSET
    """the ids and User objects"""
    members: Missing[dict[Snowflake, GuildMember]] = UNSET
    """the ids and partial Member objects"""
    roles: Missing[dict[Snowflake, Role]] = UNSET
    """the ids and Role objects"""
    channels: Missing[dict[Snowflake, Channel]] = UNSET
    """the ids and partial Channel objects"""
    messages: Missing[dict[Snowflake, MessageGet]] = UNSET
    """the ids and partial Message objects"""
    attachments: Missing[dict[Snowflake, Attachment]] = UNSET
    """the ids and attachment objects"""


class MessageInteraction(BaseModel):
    """Message interaction.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object
    """

    id: Snowflake
    """ID of the interaction"""
    type: InteractionType
    """Type of interaction"""
    name: str
    """Name of the application command, including subcommands and subcommand groups"""
    user: User
    """User who invoked the interaction"""
    member: Missing[GuildMember] = UNSET  # partial member object
    """Member who invoked the interaction in the guild"""


class MessageInteractionMetadata(BaseModel):
    """Message Interaction Metadata

    Metadata about the interaction, including the source of the interaction and relevant server and user IDs.

    see https://discord.com/developers/docs/resources/message#message-interaction-metadata-object
    """

    id: Snowflake
    """ID of the interaction"""
    type: InteractionType
    """Type of interaction"""
    user: User
    """User who triggered the interaction"""
    authorizing_integration_owners: dict[
        ApplicationIntegrationType, Snowflake | Literal[0]
    ]
    """IDs for installation context(s) related to an interaction.
    Details in Authorizing Integration Owners Object"""
    original_response_message_id: Missing[Snowflake] = UNSET
    """ID of the original response message, present only on follow-up messages"""
    interacted_message_id: Missing[Snowflake] = UNSET
    """ID of the message that contained interactive component,
    present only on messages created from component interactions"""
    triggering_interaction_metadata: Missing[MessageInteractionMetadata] = UNSET
    """Metadata for the interaction that was used to open the modal,
    present only on modal submit interactions"""


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


class Embed(BaseModel):
    """Embed

    see https://discord.com/developers/docs/resources/channel#embed-object"""

    title: Missing[str] = UNSET
    type: Missing[EmbedTypes] = UNSET
    description: Missing[str] = UNSET
    url: Missing[str] = UNSET
    timestamp: Missing[datetime.datetime] = UNSET
    color: Missing[int] = UNSET
    footer: Missing[EmbedFooter] = UNSET
    image: Missing[EmbedImage] = UNSET
    thumbnail: Missing[EmbedThumbnail] = UNSET
    video: Missing[EmbedVideo] = UNSET
    provider: Missing[EmbedProvider] = UNSET
    author: Missing[EmbedAuthor] = UNSET
    fields: Missing[list[EmbedField]] = UNSET


class EmbedThumbnail(BaseModel):
    """Embed thumbnail.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-thumbnail-structure
    """

    url: str
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedVideo(BaseModel):
    """Embed video.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-video-structure
    """

    url: Missing[str] = UNSET
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedImage(BaseModel):
    """Embed image.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-image-structure
    """

    url: str
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedProvider(BaseModel):
    """Embed provider.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-provider-structure
    """

    name: Missing[str] = UNSET
    url: Missing[str] = UNSET


class EmbedAuthor(BaseModel):
    """Embed author.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-author-structure
    """

    name: str
    url: Missing[str] = UNSET
    icon_url: Missing[str] = UNSET
    proxy_icon_url: Missing[str] = UNSET


class EmbedFooter(BaseModel):
    """Embed footer.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-footer-structure
    """

    text: str
    icon_url: Missing[str] = UNSET
    proxy_icon_url: Missing[str] = UNSET


class EmbedField(BaseModel):
    """Embed field.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-field-structure
    """

    name: str
    value: str
    inline: Missing[bool] = UNSET


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


class Activity(BaseModel):
    """Activity

    see https://discord.com/developers/docs/topics/gateway-events#activity-object"""

    name: str
    type: ActivityType
    url: MissingOrNullable[str] = UNSET
    created_at: int
    timestamps: Missing[ActivityTimestamps] = UNSET
    application_id: Missing[Snowflake] = UNSET
    details: MissingOrNullable[str] = UNSET
    state: MissingOrNullable[str] = UNSET
    emoji: MissingOrNullable[ActivityEmoji] = UNSET
    party: Missing[ActivityParty] = UNSET
    assets: Missing[ActivityAssets] = UNSET
    secrets: Missing[ActivitySecrets] = UNSET
    instance: Missing[bool] = UNSET
    flags: Missing[ActivityFlags] = UNSET
    buttons: Missing[list[ActivityButtons]] = UNSET


class Poll(BaseModel):
    """The poll object has a lot of levels and nested structures.
    It was also designed to support future extensibility,
    so some fields may appear to be more complex than necessary.

    see https://discord.com/developers/docs/resources/poll#poll-object
    """

    question: PollMedia
    """The question of the poll. Only `text` is supported."""
    answers: list[PollAnswer]
    """Each of the answers available in the poll."""
    expiry: datetime.datetime | None = None
    """The time when the poll ends."""
    allow_multiselect: bool
    """Whether a user can select multiple answers"""
    layout_type: int
    """The layout type of the poll"""
    results: Missing[PollResults] = UNSET
    """The results of the poll"""


class PollAnswer(BaseModel):
    """answer_id: Only sent as part of responses from Discord's API/Gateway.

    see https://discord.com/developers/docs/resources/poll#poll-answer-object
    """

    answer_id: int
    poll_media: PollMedia


class PollMedia(BaseModel):
    """The poll media object is a common object that backs both the question and
    answers. The intention is that it allows us to extensibly add new ways to
    display things in the future. For now, `question` only supports `text`, while
    answers can have an optional `emoji`.

    see https://discord.com/developers/docs/resources/poll#poll-media-object
    """

    text: Missing[str] = UNSET
    emoji: Missing[Emoji] = UNSET  # partial emoji


class PollResults(BaseModel):
    """Poll Results

    see https://discord.com/developers/docs/resources/poll#poll-results-object
    """

    is_finalized: bool
    answer_counts: list[PollAnswerCount]


class PollAnswerCount(BaseModel):
    """Poll Answer Count

    see https://discord.com/developers/docs/resources/poll#poll-results-object-poll-answer-count-object-structure
    """

    id: int
    count: int
    me_voted: bool


class AnswerVoters(BaseModel):
    """get answer voter response

    see https://discord.com/developers/docs/resources/poll#get-answer-voters-response-body
    """

    users: list[User]
    """Users who voted for this answer"""


__all__ = [
    "Activity",
    "AllowedMention",
    "AnswerVoters",
    "Attachment",
    "Embed",
    "EmbedAuthor",
    "EmbedField",
    "EmbedFooter",
    "EmbedImage",
    "EmbedProvider",
    "EmbedThumbnail",
    "EmbedVideo",
    "File",
    "MessageActivity",
    "MessageCall",
    "MessageGet",
    "MessageInteraction",
    "MessageInteractionMetadata",
    "MessageReference",
    "MessageSnapshot",
    "MessageSnapshotMessage",
    "Poll",
    "PollAnswer",
    "PollAnswerCount",
    "PollMedia",
    "PollResults",
    "Reaction",
    "ResolvedData",
    "RoleSubscriptionData",
]
