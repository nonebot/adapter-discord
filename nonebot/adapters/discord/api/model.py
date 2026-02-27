import datetime
import inspect
import sys
from typing import Literal
import warnings

from nonebot.adapters.discord.api.models.message_components import (
    ActionRow,
    Button,
    Component,
    ComponentEmoji,
    DirectComponent,
    SelectDefaultValue,
    SelectMenu,
    SelectMenuResolved,
    SelectOption,
    TextInput,
)

from nonebot.compat import PYDANTIC_V2
from pydantic import (
    BaseModel,
    Field,
)

from .models.application import (
    Application,
    ApplicationIntegrationTypeConfiguration,
    ApplicationRoleConnectionMetadata,
    InstallParams,
)
from .models.application_commands import (
    AnyCommandOption,
    ApplicationCommand,
    ApplicationCommandBulkOverwriteParams,
    ApplicationCommandCreate,
    ApplicationCommandEditParams,
    ApplicationCommandOption,
    ApplicationCommandOptionChoice,
    ApplicationCommandPermissions,
    AttachmentOption,
    BooleanOption,
    ChannelOption,
    CommandOptionBase,
    GuildApplicationCommandPermissions,
    IntegerOption,
    MentionableOption,
    NumberOption,
    OptionChoice,
    RoleOption,
    StringOption,
    SubCommandGroupOption,
    SubCommandOption,
    UserOption,
)
from .models.audit_log import (
    AuditLog,
    AuditLogChange,
    AuditLogChangeException,
    AuditLogEntry,
    OptionalAuditEntryInfo,
)
from .models.auto_moderation import (
    AutoModerationAction,
    AutoModerationActionMetadata,
    AutoModerationRule,
    CreateAndModifyAutoModerationRuleParams,
    TriggerMetadata,
)
from .models.interactions import (
    ApplicationCommandData,
    ApplicationCommandInteractionDataOption,
    InteractionCallbackAutocomplete,
    InteractionCallbackData,
    InteractionCallbackMessage,
    InteractionCallbackModal,
    InteractionData,
    InteractionGuild,
    InteractionResponse,
    MessageComponentData,
    MessageInteraction,
    MessageInteractionMetadata,
    ModalSubmitData,
    ResolvedData,
)
from .models.snowflake import Snowflake, SnowflakeType
from .types import (
    UNSET,
    ActivityAssetImage,
    ActivityFlags,
    ActivityType,
    AllowedMentionType,
    AnimationType,
    ApplicationFlag,
    ApplicationIntegrationType,
    AttachmentFlag,
    ChannelFlags,
    ChannelType,
    ConnectionServiceType,
    DefaultMessageNotificationLevel,
    EmbedTypes,
    EntitlementType,
    ExplicitContentFilterLevel,
    ForumLayoutTypes,
    GuildFeature,
    GuildMemberFlags,
    GuildNSFWLevel,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventRecurrenceRuleFrequency,
    GuildScheduledEventRecurrenceRuleMonth,
    GuildScheduledEventRecurrenceRuleWeekday,
    GuildScheduledEventStatus,
    IntegrationExpireBehaviors,
    InviteTargetType,
    InviteType,
    LobbyMemberFlags,
    MembershipState,
    MessageActivityType,
    MessageFlag,
    MessageReferenceType,
    MessageType,
    MFALevel,
    Missing,
    MissingOrNullable,
    OnboardingMode,
    OnboardingPromptType,
    OverwriteType,
    PremiumTier,
    PremiumType,
    PresenceStatus,
    RoleFlag,
    SKUFlag,
    SKUType,
    SortOrderTypes,
    StagePrivacyLevel,
    StickerFormatType,
    StickerType,
    SubscriptionStatus,
    SystemChannelFlags,
    TeamMemberRoleType,
    TriggerType,
    UpdatePresenceStatusType,
    UserFlags,
    VerificationLevel,
    VideoQualityMode,
    VisibilityType,
    WebhookType,
)

# Channel
# see https://discord.com/developers/docs/resources/channel


class Channel(BaseModel):
    """Represents a guild or DM channel within Discord.

    see https://discord.com/developers/docs/resources/channel#channel-object"""

    id: Snowflake
    """the id of this channel"""
    type: ChannelType
    """the type of channel"""
    guild_id: Missing[Snowflake] = UNSET
    """the id of the guild (may be missing for some channel objects
    received over gateway guild dispatches)"""
    position: Missing[int] = UNSET
    """sorting position of the channel"""
    permission_overwrites: Missing[list["Overwrite"]] = UNSET
    """explicit permission overwrites for members and roles"""
    name: MissingOrNullable[str] = UNSET
    """the name of the channel (1-100 characters)"""
    topic: MissingOrNullable[str] = UNSET
    """the channel topic (0-4096 characters for GUILD_FORUM channels,
    0-1024 characters for all others)"""
    nsfw: Missing[bool] = UNSET
    """whether the channel is nsfw"""
    last_message_id: MissingOrNullable[Snowflake] = UNSET
    """the id of the last message sent in this channel
    (or thread for GUILD_FORUM channels)
    (may not point to an existing or valid message or thread)"""
    bitrate: Missing[int] = UNSET
    """the bitrate (in bits) of the voice channel"""
    user_limit: Missing[int] = UNSET
    """the user limit of the voice channel"""
    rate_limit_per_user: Missing[int] = UNSET
    """amount of seconds a user has to wait before sending another message (0-21600);
    bots, as well as users with the permission manage_messages or
    manage_channel, are unaffected"""
    recipients: Missing[list["User"]] = UNSET
    """the recipients of the DM"""
    icon: MissingOrNullable[str] = UNSET
    """icon hash of the group DM"""
    owner_id: Missing[Snowflake] = UNSET
    """id of the creator of the group DM or thread"""
    application_id: Missing[Snowflake] = UNSET
    """application id of the group DM creator if it is bot-created"""
    managed: Missing[bool] = UNSET
    """for group DM channels: whether the channel is managed
    by an application via the gdm.join OAuth2 scope"""
    parent_id: MissingOrNullable[Snowflake] = UNSET
    """for guild channels: id of the parent category for a channel
    (each parent category can contain up to 50 channels),
    for threads: id of the text channel this thread was created"""
    last_pin_timestamp: MissingOrNullable[datetime.datetime] = UNSET
    """when the last pinned message was pinned.
    This may be null in events such as GUILD_CREATE when a message is not pinned."""
    rtc_region: MissingOrNullable[str] = UNSET
    """voice region id for the voice channel, automatic when set to null"""
    video_quality_mode: Missing[VideoQualityMode] = UNSET
    """the camera video quality mode of the voice channel, 1 when not present"""
    message_count: Missing[int] = UNSET
    """number of messages (not including the initial message
    or deleted messages) in a thread."""
    member_count: Missing[int] = UNSET
    """an approximate count of users in a thread, stops counting at 50"""
    thread_metadata: Missing["ThreadMetadata"] = UNSET
    """thread-specific fields not needed by other channels"""
    member: Missing["ThreadMember"] = UNSET
    """thread member object for the current user, if they have joined the thread,
    only included on certain API endpoints"""
    default_auto_archive_duration: Missing[int] = UNSET
    """default duration, copied onto newly created threads, in minutes,
    threads will stop showing in the channel list after the specified
    period of inactivity, can be set to: 60, 1440, 4320, 10080"""
    permissions: Missing[str] = UNSET
    """computed permissions for the invoking user in the channel, including overwrites,
    only included when part of the resolved data received on a slash command interaction
    """
    flags: Missing[ChannelFlags] = UNSET
    """channel flags combined as a bitfield"""
    total_message_sent: Missing[int] = UNSET
    """number of messages ever sent in a thread, it's similar to message_count
    on message creation, but will not decrement the number when a message is deleted"""
    available_tags: Missing[list["ForumTag"]] = UNSET
    """the set of tags that can be used in a GUILD_FORUM or a GUILD_MEDIA channel"""
    applied_tags: Missing[list[Snowflake]] = UNSET
    """the IDs of the set of tags that have been applied to a
    thread in a GUILD_FORUM or a GUILD_MEDIA channel"""
    default_reaction_emoji: MissingOrNullable["DefaultReaction"] = UNSET
    """the emoji to show in the add reaction button on a
    thread in a GUILD_FORUM channel"""
    default_thread_rate_limit_per_user: Missing[int] = UNSET
    """the initial rate_limit_per_user to set on newly created threads in a channel.
    this field is copied to the thread at creation time and does not live update."""
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    """the default sort order type used to order posts in GUILD_FORUM channels.
    Defaults to null, which indicates a preferred sort order
    hasn't been set by a channel admin"""
    default_forum_layout: Missing[ForumLayoutTypes] = UNSET
    """the default forum layout view used to display posts in GUILD_FORUM channels.
    Defaults to 0, which indicates a layout view has not been set by a channel admin"""


class MessageGet(BaseModel):
    """Message

    see https://discord.com/developers/docs/resources/message#message-object"""

    id: Snowflake
    channel_id: Snowflake
    author: "User"
    content: str
    timestamp: datetime.datetime
    edited_timestamp: datetime.datetime | None = Field(...)
    tts: bool
    mention_everyone: bool
    mentions: list["User"]
    mention_roles: list[Snowflake]
    mention_channels: Missing[list["ChannelMention"]] = UNSET
    attachments: list["Attachment"]
    embeds: list["Embed"]
    reactions: Missing[list["Reaction"]] = UNSET
    nonce: Missing[int | str] = UNSET
    pinned: bool
    webhook_id: Missing[Snowflake] = UNSET
    type: MessageType
    activity: Missing["MessageActivity"] = UNSET
    application: Missing[Application] = UNSET
    application_id: Missing[Snowflake] = UNSET
    message_reference: Missing["MessageReference"] = UNSET
    flags: Missing[MessageFlag] = UNSET
    message_snapshots: Missing[list["MessageSnapshot"]] = UNSET
    referenced_message: MissingOrNullable["MessageGet"] = UNSET
    interaction_metadata: Missing[MessageInteractionMetadata] = UNSET
    interaction: Missing[MessageInteraction] = UNSET
    thread: Missing[Channel] = UNSET
    components: Missing[list[DirectComponent]] = UNSET
    sticker_items: Missing[list["StickerItem"]] = UNSET
    stickers: Missing[list["Sticker"]] = UNSET
    position: Missing[int] = UNSET
    role_subscription_data: Missing["RoleSubscriptionData"] = UNSET
    resolved: Missing[ResolvedData] = UNSET
    poll: Missing["Poll"] = UNSET
    call: Missing["MessageCall"] = UNSET


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

    message: "MessageSnapshotMessage"


class MessageSnapshotMessage(BaseModel):
    """partial message object for Message Snapshot

    see https://discord.com/developers/docs/resources/message#message-snapshot-object"""

    type: MessageType
    content: str
    embeds: list["Embed"]
    attachments: list["Attachment"]
    timestamp: datetime.datetime
    edited_timestamp: datetime.datetime | None = Field(...)
    flags: Missing[MessageFlag] = UNSET
    mentions: list["User"]
    mention_roles: Missing[list[Snowflake]] = UNSET
    components: Missing[list[DirectComponent]] = UNSET
    sticker_items: Missing[list["StickerItem"]] = UNSET
    stickers: Missing[list["Sticker"]] = UNSET


class FollowedChannel(BaseModel):
    """Followed channel.

    see https://discord.com/developers/docs/resources/channel#followed-channel-object"""

    channel_id: Snowflake
    webhook_id: Snowflake


class Reaction(BaseModel):
    """Reaction.

    see https://discord.com/developers/docs/resources/message#reaction-object"""

    count: int
    count_details: Missing["CountDetails"] = UNSET
    me: bool
    me_burst: Missing[bool] = UNSET
    emoji: "Emoji"
    burst_colors: Missing[list[str]] = UNSET


class CountDetails(BaseModel):
    """Reaction Count Details

    see https://discord.com/developers/docs/resources/message#reaction-count-details-object
    """

    burst: int
    normal: int


class Overwrite(BaseModel):
    """Overwrite.

    see https://discord.com/developers/docs/resources/channel#overwrite-object"""

    id: Snowflake
    type: OverwriteType
    allow: str
    deny: str


class PartialOverwrite(BaseModel):
    """Partial overwrite.

    Used in request payloads where `allow`/`deny` can be omitted or null.

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    id: Snowflake
    type: OverwriteType
    allow: MissingOrNullable[str] = UNSET
    deny: MissingOrNullable[str] = UNSET


class ThreadMetadata(BaseModel):
    """Thread metadata.

    see https://discord.com/developers/docs/resources/channel#thread-metadata-object"""

    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime.datetime
    locked: bool
    invitable: Missing[bool] = UNSET
    create_timestamp: MissingOrNullable[datetime.datetime] = UNSET


class ThreadMember(BaseModel):
    """Thread member.

    see https://discord.com/developers/docs/resources/channel#thread-member-object"""

    id: Missing[Snowflake] = UNSET
    user_id: Missing[Snowflake] = UNSET
    join_timestamp: datetime.datetime
    flags: int
    member: Missing["GuildMember"] = UNSET


class DefaultReaction(BaseModel):
    """Default reaction.

    see https://discord.com/developers/docs/resources/channel#default-reaction-object"""

    emoji_id: str | None = None
    emoji_name: str | None = None


class ForumTag(BaseModel):
    """An object that represents a tag that is able to be applied
    to a thread in a GUILD_FORUM or GUILD_MEDIA channel.

    see https://discord.com/developers/docs/resources/channel#forum-tag-object"""

    id: Snowflake
    name: str
    moderated: bool
    emoji_id: Snowflake | None = None
    emoji_name: str | None = None


class ForumTagRequest(BaseModel):
    """Forum tag request.

    see https://discord.com/developers/docs/resources/channel#forum-tag-object"""

    id: Missing[Snowflake] = UNSET
    name: str
    moderated: Missing[bool] = UNSET
    emoji_id: MissingOrNullable[Snowflake] = UNSET
    emoji_name: MissingOrNullable[str] = UNSET


class Embed(BaseModel):
    """Embed

    see https://discord.com/developers/docs/resources/channel#embed-object"""

    title: Missing[str] = UNSET
    type: Missing[EmbedTypes] = UNSET
    description: Missing[str] = UNSET
    url: Missing[str] = UNSET
    timestamp: Missing[datetime.datetime] = UNSET
    color: Missing[int] = UNSET
    footer: Missing["EmbedFooter"] = UNSET
    image: Missing["EmbedImage"] = UNSET
    thumbnail: Missing["EmbedThumbnail"] = UNSET
    video: Missing["EmbedVideo"] = UNSET
    provider: Missing["EmbedProvider"] = UNSET
    author: Missing["EmbedAuthor"] = UNSET
    fields: Missing[list["EmbedField"]] = UNSET


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


class ArchivedThreadsResponse(BaseModel):
    """Archived threads response.

    see https://discord.com/developers/docs/resources/channel#list-public-archived-threads-response-body
    """

    threads: list[Channel]
    members: list[ThreadMember]
    has_more: bool


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
    poll: Missing["PollRequest"] = UNSET


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
    poll: MissingOrNullable["PollRequest"] = UNSET


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
    poll: MissingOrNullable["PollRequest"] = UNSET


class ModifyChannelParams(BaseModel):
    """Modify Channel Params

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    # JSON Params (Guild channel)
    # see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    name: Missing[str] = UNSET
    type: Missing[ChannelType] = UNSET
    position: MissingOrNullable[int] = UNSET
    topic: MissingOrNullable[str] = UNSET
    nsfw: MissingOrNullable[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET
    bitrate: MissingOrNullable[int] = UNSET
    user_limit: MissingOrNullable[int] = UNSET
    permission_overwrites: MissingOrNullable[list[PartialOverwrite]] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    rtc_region: MissingOrNullable[str] = UNSET
    video_quality_mode: MissingOrNullable[VideoQualityMode] = UNSET
    default_auto_archive_duration: MissingOrNullable[int] = UNSET
    flags: Missing[ChannelFlags] = UNSET
    available_tags: Missing[list[ForumTagRequest]] = UNSET
    default_reaction_emoji: MissingOrNullable[DefaultReaction] = UNSET
    default_thread_rate_limit_per_user: Missing[int] = UNSET
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    default_forum_layout: Missing[ForumLayoutTypes] = UNSET


class ModifyThreadParams(BaseModel):
    """Modify Thread Params.

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-thread
    """

    name: Missing[str] = UNSET
    archived: Missing[bool] = UNSET
    auto_archive_duration: Missing[int] = UNSET
    locked: Missing[bool] = UNSET
    invitable: Missing[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET
    flags: Missing[ChannelFlags] = UNSET
    applied_tags: Missing[list[Snowflake]] = UNSET


class StartThreadFromMessageParams(BaseModel):
    """Start Thread From Message Params.

    see https://discord.com/developers/docs/resources/channel#start-thread-from-message
    """

    name: str
    auto_archive_duration: Missing[int] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET


class StartThreadWithoutMessageParams(BaseModel):
    """Start Thread Without Message Params.

    see https://discord.com/developers/docs/resources/channel#start-thread-without-message
    """

    name: str
    auto_archive_duration: Missing[int] = UNSET
    type: Missing[ChannelType] = UNSET
    invitable: Missing[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET


class ModifyGuildChannelPositionParams(BaseModel):
    """Modify Guild Channel Position Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions
    """

    id: Snowflake
    position: MissingOrNullable[int] = UNSET
    lock_permissions: MissingOrNullable[bool] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET


class EditCurrentApplicationParams(BaseModel):
    """Edit Current Application Params.

    see https://discord.com/developers/docs/resources/application#edit-current-application
    """

    custom_install_url: Missing[str] = UNSET
    description: Missing[str] = UNSET
    role_connections_verification_url: Missing[str] = UNSET
    install_params: Missing[InstallParams] = UNSET
    integration_types_config: Missing[
        dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration]
    ] = UNSET
    flags: Missing[ApplicationFlag] = UNSET
    icon: MissingOrNullable[str] = UNSET
    cover_image: MissingOrNullable[str] = UNSET
    interactions_endpoint_url: Missing[str] = UNSET
    tags: Missing[list[str]] = UNSET
    event_webhooks_url: Missing[str] = UNSET
    event_webhooks_status: Missing[int] = UNSET
    event_webhooks_types: Missing[list[str]] = UNSET


class ModifyCurrentUserParams(BaseModel):
    """Modify Current User Params.

    see https://discord.com/developers/docs/resources/user#modify-current-user
    """

    username: Missing[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET


class ModifyGuildMemberParams(BaseModel):
    """Modify Guild Member Params.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/guild#modify-guild-member
    """

    nick: MissingOrNullable[str] = UNSET
    roles: MissingOrNullable[list[Snowflake]] = UNSET
    mute: MissingOrNullable[bool] = UNSET
    deaf: MissingOrNullable[bool] = UNSET
    channel_id: MissingOrNullable[Snowflake] = UNSET
    communication_disabled_until: MissingOrNullable[datetime.datetime] = UNSET
    flags: MissingOrNullable[GuildMemberFlags] = UNSET


class ModifyCurrentMemberParams(BaseModel):
    """Modify Current Member Params.

    see https://discord.com/developers/docs/resources/guild#modify-current-member
    """

    nick: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    bio: MissingOrNullable[str] = UNSET


# Emoji
# see https://discord.com/developers/docs/resources/emoji


class Emoji(BaseModel):
    """Emoji Object

    see https://discord.com/developers/docs/resources/emoji#emoji-object"""

    id: Snowflake | None = None
    """emoji id"""
    name: str | None = None
    """emoji name(can be null only in reaction emoji objects)"""
    roles: Missing[list[Snowflake]] = UNSET
    """roles allowed to use this emoji"""
    user: Missing["User"] = UNSET
    """user that created this emoji"""
    require_colons: Missing[bool] = UNSET
    """whether this emoji must be wrapped in colons"""
    managed: Missing[bool] = UNSET
    """whether this emoji is managed"""
    animated: Missing[bool] = UNSET
    """whether this emoji is animated"""
    available: Missing[bool] = UNSET
    """whether this emoji can be used, may be false due to loss of Server Boosts"""


# Guild
# see https://discord.com/developers/docs/resources/guild
class Guild(BaseModel):
    """Guild

    see https://discord.com/developers/docs/resources/guild#guild-object"""

    id: Snowflake
    name: str
    icon: str | None = Field(...)
    icon_hash: MissingOrNullable[str] = UNSET
    splash: str | None = Field(...)
    discovery_splash: str | None = None
    owner: Missing[bool] = UNSET
    owner_id: Snowflake
    permissions: Missing[str] = UNSET
    region: MissingOrNullable[str] = UNSET
    afk_channel_id: Snowflake | None = Field(...)
    afk_timeout: int
    widget_enabled: Missing[bool] = UNSET
    widget_channel_id: MissingOrNullable[Snowflake] = UNSET
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    roles: list["Role"]
    emojis: list[Emoji]
    features: list[GuildFeature]
    mfa_level: MFALevel
    application_id: Snowflake | None = Field(...)
    system_channel_id: Snowflake | None = Field(...)
    system_channel_flags: SystemChannelFlags
    rules_channel_id: Snowflake | None = Field(...)
    max_presences: int | None = Field(...)
    max_members: int | None = Field(...)
    vanity_url_code: str | None = Field(...)
    description: str | None = Field(...)
    banner: str | None = Field(...)
    premium_tier: PremiumTier
    premium_subscription_count: int | None = Field(...)
    preferred_locale: str
    public_updates_channel_id: Snowflake | None = Field(...)
    max_video_channel_users: Missing[int] = UNSET
    max_stage_video_channel_users: Missing[int] = UNSET
    approximate_member_count: Missing[int] = UNSET
    approximate_presence_count: Missing[int] = UNSET
    welcome_screen: Missing["WelcomeScreen"] = UNSET
    nsfw_level: GuildNSFWLevel
    stickers: Missing[list["Sticker"]] = UNSET
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: MissingOrNullable[Snowflake] = UNSET
    incidents_data: MissingOrNullable["GuildIncidentsData"] = UNSET


class GuildIncidentsData(BaseModel):
    """Incidents Data.

    see https://discord.com/developers/docs/resources/guild#incidents-data-object
    """

    invites_disabled_until: datetime.datetime | None = Field(...)
    dms_disabled_until: datetime.datetime | None = Field(...)
    dm_spam_detected_at: MissingOrNullable[datetime.datetime] = UNSET
    raid_detected_at: MissingOrNullable[datetime.datetime] = UNSET


class CurrentUserGuild(BaseModel):
    """partial guild object for Get Current User Guilds API

    see https://discord.com/developers/docs/resources/user#get-current-user-guilds"""

    id: Snowflake
    name: str
    icon: str | None = Field(...)
    owner: Missing[bool] = UNSET
    permissions: Missing[str] = UNSET
    features: list[GuildFeature]
    approximate_member_count: Missing[int] = UNSET
    approximate_presence_count: Missing[int] = UNSET


class UnavailableGuild(BaseModel):
    """Unavailable Guild

    see https://discord.com/developers/docs/resources/guild#unavailable-guild-object"""

    id: Snowflake
    unavailable: Literal[True]


class GuildPreview(BaseModel):
    """Guild Preview

    see https://discord.com/developers/docs/resources/guild#guild-preview-object"""

    id: Snowflake
    name: str
    icon: str | None = None
    splash: str | None = None
    discovery_splash: str | None = None
    emojis: list[Emoji]
    features: list[GuildFeature]
    approximate_member_count: int
    approximate_presence_count: int
    description: str | None = None
    stickers: list["Sticker"]


class GuildWidgetSettings(BaseModel):
    """Guild Widget Settings

    see https://discord.com/developers/docs/resources/guild#guild-widget-settings-object
    """

    enabled: bool
    channel_id: Snowflake | None = None


class GuildWidget(BaseModel):
    """Guild Widget

    see https://discord.com/developers/docs/resources/guild#guild-widget-object"""

    id: Snowflake
    name: str
    instant_invite: str | None = None
    channels: list["GuildWidgetChannel"]
    members: list["GuildWidgetUser"]
    presence_count: int


class GuildVanityURL(BaseModel):
    """Guild Vanity URL.

    see https://discord.com/developers/docs/resources/guild#get-guild-vanity-url
    """

    code: str | None = None
    uses: int


class GuildWidgetChannel(BaseModel):
    """partial channel objects for GuildWidget.channels

    see https://discord.com/developers/docs/resources/guild#guild-widget-object-example-guild-widget
    """

    id: Snowflake
    name: str
    position: Missing[int] = UNSET


class GuildWidgetUser(BaseModel):
    """partial user objects for GuildWidget.members

    The fields id, discriminator and avatar are anonymized to prevent abuse.

    see https://discord.com/developers/docs/resources/guild#guild-widget-object-example-guild-widget
    """

    id: str
    username: str
    discriminator: str
    avatar: str | None = None
    status: str
    avatar_url: str


class GuildMember(BaseModel):
    """Guild Member

    see https://discord.com/developers/docs/resources/guild#guild-member-object"""

    user: Missing["User"] = UNSET
    nick: MissingOrNullable[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    roles: list[Snowflake]
    joined_at: datetime.datetime
    premium_since: MissingOrNullable[datetime.datetime] = UNSET
    deaf: Missing[bool] = UNSET
    mute: Missing[bool] = UNSET
    flags: GuildMemberFlags
    pending: Missing[bool] = UNSET
    permissions: Missing[str] = UNSET
    communication_disabled_until: MissingOrNullable[datetime.datetime] = UNSET
    avatar_decoration_data: MissingOrNullable["AvatarDecorationData"] = UNSET


class Integration(BaseModel):
    """Integration

    see https://discord.com/developers/docs/resources/guild#integration-object"""

    id: Snowflake
    name: str
    type: str
    enabled: bool
    syncing: Missing[bool] = UNSET
    role_id: Missing[Snowflake] = UNSET
    enable_emoticons: Missing[bool] = UNSET
    expire_behavior: Missing[IntegrationExpireBehaviors] = UNSET
    expire_grace_period: Missing[int] = UNSET
    user: Missing["User"] = UNSET
    account: "IntegrationAccount"
    synced_at: Missing[datetime.datetime] = UNSET
    subscriber_count: Missing[int] = UNSET
    revoked: Missing[bool] = UNSET
    application: Missing["IntegrationApplication"] = UNSET
    scopes: Missing[list[str]] = UNSET  # TODO: OAuth2 scopes


class IntegrationAccount(BaseModel):
    """Integration Account

    see https://discord.com/developers/docs/resources/guild#integration-account-object
    """

    id: str
    name: str


class IntegrationApplication(BaseModel):
    """Integration Application

    see https://discord.com/developers/docs/resources/guild#integration-application-object
    """

    id: Snowflake
    name: str
    icon: str | None = None
    description: str
    bot: Missing["User"] = UNSET


class Ban(BaseModel):
    """Ban

    see https://discord.com/developers/docs/resources/guild#ban-object"""

    reason: str | None = None
    user: "User"


class WelcomeScreen(BaseModel):
    """Welcome screen.

    see https://discord.com/developers/docs/resources/guild#welcome-screen-object"""

    description: str | None = None
    welcome_channels: list["WelcomeScreenChannel"]


class WelcomeScreenChannel(BaseModel):
    """Welcome screen channel.

    see https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-channel-structure
    """

    channel_id: Snowflake
    description: str
    emoji_id: Snowflake | None = None
    emoji_name: str | None = None


class GuildOnboarding(BaseModel):
    """Guild onboarding.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object"""

    guild_id: Snowflake
    prompts: list["OnboardingPrompt"]
    default_channel_ids: list[Snowflake]
    enabled: bool
    mode: OnboardingMode


class OnboardingPrompt(BaseModel):
    """Onboarding prompt.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-prompt-structure
    """

    id: Snowflake
    type: OnboardingPromptType
    options: list["OnboardingPromptOption"]
    title: str
    single_select: bool
    required: bool
    in_onboarding: bool


class OnboardingPromptOption(BaseModel):
    """Onboarding prompt option.

    When creating or updating a prompt option, the `emoji_id`, `emoji_name`, and
    `emoji_animated` fields must be used instead of the emoji object.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-prompt-option-structure
    """

    id: Snowflake
    channel_ids: list[Snowflake]
    role_ids: list[Snowflake]
    emoji: Missing[Emoji] = UNSET
    emoji_id: Missing[Snowflake] = UNSET
    emoji_name: Missing[str] = UNSET
    emoji_animated: Missing[bool] = UNSET
    title: str
    description: str | None = None


class MembershipScreening(BaseModel):
    """Membership screening.

    see https://discord.com/developers/docs/resources/guild#membership-screening-object
    """


class CreateGuildParams(BaseModel):
    """Create Guild Params

    see https://discord.com/developers/docs/resources/guild#create-guild"""

    name: str
    region: str | None = None
    icon: str | None = None
    verification_level: VerificationLevel | None = None
    default_message_notifications: DefaultMessageNotificationLevel | None = None
    explicit_content_filter: ExplicitContentFilterLevel | None = None
    roles: list["Role"] | None = None
    channels: list[Channel] | None = None
    afk_channel_id: Snowflake | None = None
    afk_timeout: int | None = None
    system_channel_id: Snowflake | None = None
    system_channel_flags: SystemChannelFlags | None = None


class ModifyGuildParams(BaseModel):
    """Modify Guild Params

    see https://discord.com/developers/docs/resources/guild#modify-guild"""

    name: Missing[str] = UNSET
    region: MissingOrNullable[str] = UNSET
    verification_level: MissingOrNullable[VerificationLevel] = UNSET
    default_message_notifications: MissingOrNullable[
        DefaultMessageNotificationLevel
    ] = UNSET
    explicit_content_filter: MissingOrNullable[ExplicitContentFilterLevel] = UNSET
    afk_channel_id: MissingOrNullable[Snowflake] = UNSET
    afk_timeout: Missing[int] = UNSET
    icon: MissingOrNullable[str] = UNSET
    splash: MissingOrNullable[str] = UNSET
    discovery_splash: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET
    system_channel_id: MissingOrNullable[Snowflake] = UNSET
    system_channel_flags: Missing[SystemChannelFlags] = UNSET
    rules_channel_id: MissingOrNullable[Snowflake] = UNSET
    public_updates_channel_id: MissingOrNullable[Snowflake] = UNSET
    preferred_locale: MissingOrNullable[str] = UNSET
    features: Missing[list[GuildFeature]] = UNSET
    description: MissingOrNullable[str] = UNSET
    premium_progress_bar_enabled: Missing[bool] = UNSET
    safety_alerts_channel_id: MissingOrNullable[Snowflake] = UNSET


class ModifyGuildIncidentActionsParams(BaseModel):
    """Modify Guild Incident Actions Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-incident-actions
    """

    invites_disabled_until: MissingOrNullable[datetime.datetime] = UNSET
    dms_disabled_until: MissingOrNullable[datetime.datetime] = UNSET


class CreateGuildChannelParams(BaseModel):
    """Create Guild Channel Params

    see https://discord.com/developers/docs/resources/guild#create-guild-channel"""

    name: str
    type: ChannelType | None = None
    topic: str | None = None
    bitrate: int | None = None
    user_limit: int | None = None
    rate_limit_per_user: int | None = None
    position: int | None = None
    permission_overwrites: list["Overwrite"] | None = None
    parent_id: Snowflake | None = None
    nsfw: bool | None = None
    rtc_region: str | None = None
    video_quality_mode: VideoQualityMode | None = None
    default_auto_archive_duration: int | None = None
    default_reaction_emoji: DefaultReaction | None = None
    available_tags: list[ForumTagRequest] | None = None
    default_sort_order: SortOrderTypes | None = None
    default_forum_layout: ForumLayoutTypes | None = None
    default_thread_rate_limit_per_user: int | None = None


class ListActiveGuildThreadsResponse(BaseModel):
    """List Active Guild Threads Response

    see https://discord.com/developers/docs/resources/guild#list-active-guild-threads"""

    threads: list[Channel]
    members: list[ThreadMember]


class ModifyGuildWelcomeScreenParams(BaseModel):
    """Modify Guild Welcome Screen Params

    see https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
    """

    enabled: MissingOrNullable[bool] = UNSET
    welcome_channels: MissingOrNullable[list[WelcomeScreenChannel]] = UNSET
    description: MissingOrNullable[str] = UNSET


class ModifyGuildWidgetParams(BaseModel):
    """Modify Guild Widget Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-widget
    """

    enabled: Missing[bool] = UNSET
    channel_id: MissingOrNullable[Snowflake] = UNSET


# Guild Scheduled Event
# see https://discord.com/developers/docs/resources/guild-scheduled-event


class GuildScheduledEvent(BaseModel):
    """Guild Scheduled Event

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object
    """

    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake | None = None
    creator_id: MissingOrNullable[Snowflake] = UNSET
    name: str
    description: MissingOrNullable[str] = UNSET
    scheduled_start_time: datetime.datetime
    scheduled_end_time: datetime.datetime | None = None
    privacy_level: GuildScheduledEventPrivacyLevel
    status: GuildScheduledEventStatus
    entity_type: GuildScheduledEventEntityType
    entity_id: Snowflake | None = None
    entity_metadata: "GuildScheduledEventEntityMetadata | None" = None
    creator: Missing["User"] = UNSET
    user_count: Missing[int] = UNSET
    image: MissingOrNullable[str] = UNSET
    recurrence_rule: "RecurrenceRule | None" = None


class GuildScheduledEventEntityMetadata(BaseModel):
    """Guild Scheduled Event Entity Metadata

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: Missing[str] = UNSET


class GuildScheduledEventUser(BaseModel):
    """Guild Scheduled Event User

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-user-object
    """

    guild_scheduled_event_id: Snowflake
    user: "User"
    member: Missing[GuildMember] = UNSET


class CreateGuildScheduledEventParams(BaseModel):
    """Create Guild Scheduled Event Params

    see https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event-json-params
    """

    channel_id: Snowflake | None = None
    entity_metadata: GuildScheduledEventEntityMetadata | None = None
    name: str
    privacy_level: GuildScheduledEventPrivacyLevel
    scheduled_start_time: datetime.datetime  # ISO8601 timestamp
    scheduled_end_time: datetime.datetime | None = None  # ISO8601 timestamp
    description: str | None = None
    entity_type: GuildScheduledEventEntityType
    image: str | None = None
    recurrence_rule: "RecurrenceRule | None" = None


class ModifyGuildScheduledEventParams(BaseModel):
    """Modify Guild Scheduled Event Params

    see https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event-json-params
    """

    channel_id: MissingOrNullable[Snowflake] = UNSET
    entity_metadata: MissingOrNullable[GuildScheduledEventEntityMetadata] = UNSET
    name: Missing[str] = UNSET
    privacy_level: Missing[GuildScheduledEventPrivacyLevel] = UNSET
    scheduled_start_time: Missing[datetime.datetime] = UNSET  # ISO8601 timestamp
    scheduled_end_time: Missing[datetime.datetime] = UNSET  # ISO8601 timestamp
    description: MissingOrNullable[str] = UNSET
    entity_type: Missing[GuildScheduledEventEntityType] = UNSET
    status: Missing[GuildScheduledEventStatus] = UNSET
    image: Missing[str] = UNSET
    recurrence_rule: MissingOrNullable["RecurrenceRule"] = UNSET


class ModifyGuildEmojiParams(BaseModel):
    """Modify Guild Emoji Params.

    see https://discord.com/developers/docs/resources/emoji#modify-guild-emoji
    """

    name: Missing[str] = UNSET
    roles: MissingOrNullable[list[Snowflake]] = UNSET


class ModifyGuildStickerParams(BaseModel):
    """Modify Guild Sticker Params.

    see https://discord.com/developers/docs/resources/sticker#modify-guild-sticker
    """

    name: Missing[str] = UNSET
    description: MissingOrNullable[str] = UNSET
    tags: Missing[str] = UNSET


class ModifyGuildRoleParams(BaseModel):
    """Modify Guild Role Params.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/guild#modify-guild-role
    """

    name: MissingOrNullable[str] = UNSET
    permissions: MissingOrNullable[str] = UNSET
    color: MissingOrNullable[int] = UNSET
    colors: Missing["RoleColors"] = UNSET
    hoist: MissingOrNullable[bool] = UNSET
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET
    mentionable: MissingOrNullable[bool] = UNSET


class CreateGuildRoleParams(BaseModel):
    """Create Guild Role Params.

    see https://discord.com/developers/docs/resources/guild#create-guild-role
    """

    name: Missing[str] = UNSET
    permissions: Missing[str] = UNSET
    color: Missing[int] = UNSET
    colors: Missing["RoleColors"] = UNSET
    hoist: Missing[bool] = UNSET
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET
    mentionable: Missing[bool] = UNSET


class ModifyGuildRolePositionParams(BaseModel):
    """Modify Guild Role Position Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-role-positions
    """

    id: Snowflake
    position: MissingOrNullable[int] = UNSET


class CreateWebhookParams(BaseModel):
    """Create Webhook Params.

    see https://discord.com/developers/docs/resources/webhook#create-webhook
    """

    name: str
    avatar: MissingOrNullable[str] = UNSET


class ModifyCurrentUserVoiceStateParams(BaseModel):
    """Modify Current User Voice State Params.

    see https://discord.com/developers/docs/resources/voice#modify-current-user-voice-state
    """

    channel_id: Missing[Snowflake] = UNSET
    suppress: Missing[bool] = UNSET
    request_to_speak_timestamp: MissingOrNullable[datetime.datetime] = UNSET


class CreateGuildTemplateParams(BaseModel):
    """Create Guild Template Params.

    see https://discord.com/developers/docs/resources/guild-template#create-guild-template
    """

    name: str
    description: MissingOrNullable[str] = UNSET


class ModifyGuildTemplateParams(BaseModel):
    """Modify Guild Template Params.

    see https://discord.com/developers/docs/resources/guild-template#modify-guild-template
    """

    name: Missing[str] = UNSET
    description: MissingOrNullable[str] = UNSET


# Guild Template
# see https://discord.com/developers/docs/resources/guild-template
class GuildTemplate(BaseModel):
    """Guild Template

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object
    """

    code: str
    name: str
    description: str | None = None
    usage_count: int
    creator_id: Snowflake
    creator: "User"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    source_guild_id: Snowflake
    serialized_source_guild: "GuildTemplateGuild"
    is_dirty: bool | None = None


class GuildTemplateGuild(BaseModel):
    """partial guild object for GuildTemplate

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
    """

    name: str
    description: str | None = None
    region: MissingOrNullable[str] = UNSET
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    preferred_locale: str
    afk_channel_id: Snowflake | None = None
    afk_timeout: int
    system_channel_id: Snowflake | None = None
    system_channel_flags: SystemChannelFlags
    icon_hash: MissingOrNullable[str] = UNSET
    roles: list["GuildTemplateGuildRole"]
    channels: list["GuildTemplateGuildChannel"]


class GuildTemplateGuildRole(BaseModel):
    """partial role object for GuildTemplateGuild

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
    """

    id: Snowflake
    name: str
    permissions: str
    color: int
    hoist: bool
    mentionable: bool
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET


class GuildTemplateGuildChannel(BaseModel):
    """partial role object for GuildTemplateGuild

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
    """

    id: Snowflake
    type: ChannelType
    name: MissingOrNullable[str] = UNSET
    position: Missing[int] = UNSET
    topic: MissingOrNullable[str] = UNSET
    bitrate: Missing[int] = UNSET
    user_limit: Missing[int] = UNSET
    nsfw: Missing[bool] = UNSET
    rate_limit_per_user: Missing[int] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    default_auto_archive_duration: MissingOrNullable[int] = UNSET
    permission_overwrites: Missing[list["Overwrite"]] = UNSET
    available_tags: MissingOrNullable[list["ForumTag"]] = UNSET
    template: Missing[str] = UNSET
    default_reaction_emoji: MissingOrNullable["DefaultReaction"] = UNSET
    default_thread_rate_limit_per_user: MissingOrNullable[int] = UNSET
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    default_forum_layout: MissingOrNullable[ForumLayoutTypes] = UNSET
    icon_emoji: MissingOrNullable[Emoji] = UNSET
    theme_color: MissingOrNullable[int] = UNSET


# Invite
# see https://discord.com/developers/docs/resources/invite
class Invite(BaseModel):
    """Invite

    Warning:
        stage_instance is deprecated by Discord and may be omitted.

    see https://discord.com/developers/docs/resources/invite#invite-object"""

    type: InviteType
    code: str
    guild: Missing["InviteGuild"] = UNSET
    channel: Channel | None = Field(...)  # partial channel object
    inviter: Missing["User"] = UNSET
    target_type: Missing["InviteTargetType"] = UNSET
    target_user: Missing["User"] = UNSET
    target_application: Missing["Application"] = UNSET  # partial application object
    approximate_presence_count: Missing[int] = UNSET
    approximate_member_count: Missing[int] = UNSET
    expires_at: MissingOrNullable[datetime.datetime] = UNSET
    stage_instance: Missing["InviteStageInstance"] = UNSET
    guild_scheduled_event: Missing["GuildScheduledEvent"] = UNSET
    uses: Missing[int] = UNSET
    max_uses: Missing[int] = UNSET
    max_age: Missing[int] = UNSET
    temporary: Missing[bool] = UNSET
    created_at: Missing[datetime.datetime] = UNSET

    def __init__(self, **data) -> None:  # noqa: ANN003
        super().__init__(**data)
        if data.get("stage_instance", UNSET) is not UNSET:
            warnings.warn(
                "Invite.stage_instance is deprecated by Discord",
                DeprecationWarning,
                stacklevel=2,
            )


class InviteGuild(BaseModel):
    """partial guild object for Invite.guild

    see https://discord.com/developers/docs/resources/invite#invite-object-example-invite-object
    """

    id: Snowflake
    name: str
    splash: str | None = None
    banner: str | None = None
    description: str | None = None
    icon: str | None = None
    features: list[GuildFeature]
    verification_level: VerificationLevel
    vanity_url_code: str | None = None
    nsfw_level: GuildNSFWLevel
    premium_subscription_count: int | None = None


class InviteMetadata(BaseModel):
    """Invite Metadata

    see https://discord.com/developers/docs/resources/invite#invite-metadata-object"""

    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: datetime.datetime


class InviteTargetUsersJobStatus(BaseModel):
    """Invite target users job status.

    see https://discord.com/developers/docs/resources/invite#get-target-users-job-status
    """

    status: Literal[0, 1, 2, 3]
    total_users: int
    processed_users: int
    created_at: datetime.datetime
    completed_at: datetime.datetime | None = Field(...)
    error_message: MissingOrNullable[str] = UNSET


class InviteStageInstance(BaseModel):
    """Invite Stage Instance

    This is deprecated.

    see https://discord.com/developers/docs/resources/invite#invite-stage-instance-object
    """

    members: list[GuildMember]  # partial guild member objects
    participant_count: int
    speaker_count: int
    topic: str

    def __init__(self, **data) -> None:  # noqa: ANN003
        super().__init__(**data)
        warnings.warn(
            "InviteStageInstance is deprecated by Discord",
            DeprecationWarning,
            stacklevel=2,
        )


# Stage Instance
# see https://discord.com/developers/docs/resources/stage-instance


class StageInstance(BaseModel):
    """Stage Instance

    see https://discord.com/developers/docs/resources/stage-instance#stage-instance-object
    """

    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: StagePrivacyLevel
    discoverable_disabled: bool
    guild_scheduled_event_id: Snowflake | None = None


# Sticker
# see https://discord.com/developers/docs/resources/sticker
class Sticker(BaseModel):
    """Sticker Object

    see https://discord.com/developers/docs/resources/sticker#sticker-object"""

    id: Snowflake
    pack_id: Missing[Snowflake] = UNSET
    name: str
    description: str | None = Field(...)
    tags: str
    asset: Missing[str] = UNSET
    """Deprecated. previously the sticker asset hash, now an empty string"""
    type: StickerType
    format_type: StickerFormatType
    available: Missing[bool] = UNSET
    guild_id: Missing[Snowflake] = UNSET
    user: Missing["User"] = UNSET
    sort_value: Missing[int] = UNSET


class StickerItem(BaseModel):
    """Sticker item.

    see https://discord.com/developers/docs/resources/sticker#sticker-item-object"""

    id: Snowflake
    name: str
    format_type: StickerFormatType


class StickerPack(BaseModel):
    """Sticker pack.

    see https://discord.com/developers/docs/resources/sticker#sticker-pack-object"""

    id: Snowflake
    stickers: list[Sticker]
    name: str
    sku_id: Snowflake
    cover_sticker_id: Missing[Snowflake] = UNSET
    description: str
    banner_asset_id: Missing[Snowflake] = UNSET


class StickerPacksResponse(BaseModel):
    """List Nitro Sticker Packs Response.

    see https://discord.com/developers/docs/resources/sticker#list-sticker-packs
    """

    sticker_packs: list[StickerPack]


# User
# see https://discord.com/developers/docs/resources/user
class User(BaseModel):
    """User

    see https://discord.com/developers/docs/resources/user#user-object"""

    id: Snowflake
    username: str
    discriminator: str
    global_name: str | None = None
    avatar: str | None = Field(...)
    bot: Missing[bool] = UNSET
    system: Missing[bool] = UNSET
    mfa_enabled: Missing[bool] = UNSET
    banner: MissingOrNullable[str] = UNSET
    accent_color: MissingOrNullable[int] = UNSET
    locale: Missing[str] = UNSET
    verified: Missing[bool] = UNSET
    email: MissingOrNullable[str] = UNSET
    flags: Missing[int] = UNSET
    premium_type: Missing[PremiumType] = UNSET
    public_flags: Missing[UserFlags] = UNSET
    avatar_decoration_data: MissingOrNullable["AvatarDecorationData"] = UNSET


class AvatarDecorationData(BaseModel):
    """Avatar Decoration Data

    see https://discord.com/developers/docs/resources/user#avatar-decoration-data-object
    """

    asset: str
    sku_id: Snowflake


class Connection(BaseModel):
    """Connection

    see https://discord.com/developers/docs/resources/user#connection-object"""

    id: str
    name: str
    type: ConnectionServiceType
    revoked: Missing[bool] = UNSET
    integrations: Missing[list["Integration"]] = UNSET  # partial server integrations
    verified: bool
    friend_sync: bool
    show_activity: bool
    two_way_link: bool
    visibility: VisibilityType


class ApplicationRoleConnection(BaseModel):
    """Application Role Connection

    see https://discord.com/developers/docs/resources/user#application-role-connection-object
    """

    platform_name: str | None = Field(...)
    platform_username: str | None = Field(...)
    metadata: dict  # object


# Voice
# see https://discord.com/developers/docs/resources/voice
class VoiceState(BaseModel):
    """Voice State

    see https://discord.com/developers/docs/resources/voice#voice-state-object"""

    guild_id: Missing[Snowflake] = UNSET
    channel_id: Snowflake | None = Field(...)
    user_id: Snowflake
    member: Missing[GuildMember] = UNSET
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: Missing[bool] = UNSET
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: datetime.datetime | None = Field(...)


class VoiceRegion(BaseModel):
    """Voice Region

    see https://discord.com/developers/docs/resources/voice#voice-region-object"""

    id: str
    name: str
    optimal: bool
    deprecated: bool
    custom: bool


# Webhook
# see https://discord.com/developers/docs/resources/webhook
class SourceGuild(BaseModel):
    """partial guild object for Webhook.source_guild

    see https://discord.com/developers/docs/resources/webhook#webhook-object-example-channel-follower-webhook
    """

    id: Snowflake
    name: str
    icon: str | None = None


class SourceChannel(BaseModel):
    """partial channel object for Webhook.source_channel

    see https://discord.com/developers/docs/resources/webhook#webhook-object-example-channel-follower-webhook"""

    id: Snowflake
    name: str


class Webhook(BaseModel):
    """Used to represent a webhook.

    see https://discord.com/developers/docs/resources/webhook#webhook-object"""

    id: Snowflake
    type: WebhookType
    guild_id: MissingOrNullable[Snowflake] = UNSET
    channel_id: Snowflake | None = Field(...)
    user: Missing[User] = UNSET
    name: str | None = Field(...)
    avatar: str | None = Field(...)
    token: Missing[str] = UNSET
    application_id: Snowflake | None = Field(...)
    source_guild: Missing[SourceGuild] = UNSET
    source_channel: Missing[SourceChannel] = UNSET
    url: Missing[str] = UNSET


class ExecuteWebhookParams(BaseModel):
    """Execute Webhook Parameters

    see https://discord.com/developers/docs/resources/webhook#execute-webhook"""

    content: Missing[str] = UNSET
    username: Missing[str] = UNSET
    avatar_url: Missing[str] = UNSET
    tts: Missing[bool] = UNSET
    embeds: Missing[list[Embed]] = UNSET
    allowed_mentions: Missing[AllowedMention] = UNSET
    components: Missing[list[DirectComponent]] = UNSET
    files: Missing[list[File]] = UNSET
    attachments: Missing[list[AttachmentSend]] = UNSET
    flags: Missing[MessageFlag] = UNSET
    thread_name: Missing[str] = UNSET
    applied_tags: Missing[list[Snowflake]] = UNSET
    poll: Missing["PollRequest"] = UNSET


# gateway
# see https://discord.com/developers/docs/topics/gateway


class Gateway(BaseModel):
    """Get Gateway Response

    see https://discord.com/developers/docs/topics/gateway#get-gateway"""

    url: str


class GatewayBot(BaseModel):
    """Get Gateway Bot Response

    see https://discord.com/developers/docs/topics/gateway#get-gateway-bot"""

    url: str
    shards: int
    session_start_limit: "SessionStartLimit"


class SessionStartLimit(BaseModel):
    """Session start limit

    see https://discord.com/developers/docs/topics/gateway#session-start-limit-object"""

    total: int
    remaining: int
    reset_after: int
    max_concurrency: int


# gateway events
# see https://discord.com/developers/docs/topics/gateway-events
class Identify(BaseModel):
    """Identify Payload data

    see https://discord.com/developers/docs/topics/gateway-events#identify"""

    token: str
    properties: "IdentifyConnectionProperties"
    compress: Missing[bool] = UNSET
    large_threshold: Missing[int] = UNSET
    shard: Missing[list[int]] = UNSET
    presence: Missing["PresenceUpdate"] = UNSET
    intents: int


class IdentifyConnectionProperties(BaseModel):
    """Identify Connection Properties

    see https://discord.com/developers/docs/topics/gateway-events#identify-identify-connection-properties
    """

    os: str
    browser: str
    device: str


class Resume(BaseModel):
    """Resume Payload data

    see https://discord.com/developers/docs/topics/gateway-events#resume"""

    token: str
    session_id: str
    seq: int


class RequestGuildMembers(BaseModel):
    """Request Guild Members Payload data

    see https://discord.com/developers/docs/topics/gateway-events#request-guild-members
    """

    guild_id: Snowflake
    query: Missing[str] = UNSET
    limit: int
    presences: Missing[bool] = UNSET
    user_ids: Missing[Snowflake | list[Snowflake]] = UNSET
    nonce: Missing[str] = UNSET


class UpdateVoiceState(BaseModel):
    """Update Voice State Payload data

    see https://discord.com/developers/docs/topics/gateway-events#update-voice-state"""

    guild_id: Snowflake
    channel_id: Snowflake | None = Field(...)
    self_mute: bool
    self_deaf: bool


class UpdatePresence(BaseModel):
    """Update Presence Payload data

    see https://discord.com/developers/docs/topics/gateway-events#update-presence"""

    since: int | None = Field(...)
    activities: list["Activity"]
    status: UpdatePresenceStatusType
    afk: bool


class Hello(BaseModel):
    """Hello Payload data

    see https://discord.com/developers/docs/topics/gateway-events#hello"""

    heartbeat_interval: int


class ApplicationReady(BaseModel):
    """partial application object for ready event.

    see https://discord.com/developers/docs/events/gateway-events#ready
    """

    id: str
    flags: int


class Ready(BaseModel):
    """Ready Payload data

    see https://discord.com/developers/docs/topics/gateway-events#ready"""

    v: int
    user: User
    guilds: list[UnavailableGuild]
    session_id: str
    resume_gateway_url: str
    shard: Missing[list[int]] = UNSET
    application: ApplicationReady


class AutoModerationRuleCreate(AutoModerationRule):
    """Auto Moderation Rule Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-create
    """


class AutoModerationRuleUpdate(AutoModerationRule):
    """Auto Moderation Rule Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-update
    """


class AutoModerationRuleDelete(AutoModerationRule):
    """Auto Moderation Rule Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-delete
    """


class AutoModerationActionExecution(BaseModel):
    """Auto Moderation Action Execution Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-action-execution
    """

    guild_id: Snowflake
    action: AutoModerationAction
    rule_id: Snowflake
    rule_trigger_type: TriggerType
    user_id: Snowflake
    channel_id: Missing[Snowflake] = UNSET
    message_id: Missing[Snowflake] = UNSET
    alert_system_message_id: Missing[Snowflake] = UNSET
    content: str
    matched_keyword: str | None = Field(...)
    matched_content: str | None = Field(...)


class ChannelCreate(Channel):
    """Channel Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-create"""


class ChannelUpdate(Channel):
    """Channel Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-update"""


class ChannelDelete(Channel):
    """Channel Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-delete"""


class ThreadCreate(Channel):
    """Thread Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-create"""

    newly_created: Missing[bool] = UNSET
    thread_member: Missing[ThreadMember] = UNSET


class ThreadUpdate(Channel):
    """Thread Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-update"""


class ThreadDelete(BaseModel):
    """Thread Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-delete"""

    id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    type: ChannelType


class ThreadListSync(BaseModel):
    """Thread List Sync Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-list-sync
    """

    guild_id: Snowflake
    channel_ids: Missing[list[Snowflake]] = UNSET
    threads: list[Channel]
    members: list[ThreadMember]


class ThreadMemberUpdate(ThreadMember):
    """Thread Member Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-member-update
    """

    guild_id: Snowflake


class ThreadMembersUpdate(BaseModel):
    """Thread Members Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-members-update
    """

    id: Snowflake
    guild_id: Snowflake
    member_count: int
    added_members: Missing[list[ThreadMember]] = UNSET
    removed_member_ids: Missing[list[Snowflake]] = UNSET


class ChannelPinsUpdate(BaseModel):
    """Channel Pins Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-pins-update"""

    guild_id: Missing[Snowflake] = UNSET
    channel_id: Snowflake
    last_pin_timestamp: Missing[datetime.datetime | None] = UNSET


class GuildCreate(BaseModel):
    """Guild Create Event's Guild inner can be either Guild or UnavailableGuild

    see https://discord.com/developers/docs/topics/gateway-events#guild-create"""

    id: Snowflake
    unavailable: Missing[bool] = UNSET
    name: Missing[str] = UNSET
    icon: MissingOrNullable[str] = UNSET
    icon_hash: MissingOrNullable[str] = UNSET
    splash: MissingOrNullable[str] = UNSET
    discovery_splash: MissingOrNullable[str] = UNSET
    owner: Missing[bool] = UNSET
    owner_id: Missing[Snowflake] = UNSET
    permissions: Missing[str] = UNSET
    region: MissingOrNullable[str] = UNSET
    afk_channel_id: MissingOrNullable[Snowflake] = UNSET
    afk_timeout: Missing[int] = UNSET
    widget_enabled: Missing[bool] = UNSET
    widget_channel_id: MissingOrNullable[Snowflake] = UNSET
    verification_level: Missing[VerificationLevel] = UNSET
    default_message_notifications: Missing[DefaultMessageNotificationLevel] = UNSET
    explicit_content_filter: Missing[ExplicitContentFilterLevel] = UNSET
    roles: Missing[list["Role"]] = UNSET
    emojis: Missing[list[Emoji]] = UNSET
    features: Missing[list[GuildFeature]] = UNSET
    mfa_level: Missing[MFALevel] = UNSET
    application_id: MissingOrNullable[Snowflake] = UNSET
    system_channel_id: MissingOrNullable[Snowflake] = UNSET
    system_channel_flags: Missing[SystemChannelFlags] = UNSET
    rules_channel_id: MissingOrNullable[Snowflake] = UNSET
    max_presences: MissingOrNullable[int] = UNSET
    max_members: MissingOrNullable[int] = UNSET
    vanity_url_code: MissingOrNullable[str] = UNSET
    description: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET
    premium_tier: Missing[PremiumTier] = UNSET
    premium_subscription_count: MissingOrNullable[int] = UNSET
    preferred_locale: Missing[str] = UNSET
    public_updates_channel_id: MissingOrNullable[Snowflake] = UNSET
    max_video_channel_users: Missing[int] = UNSET
    max_stage_video_channel_users: Missing[int] = UNSET
    approximate_member_count: Missing[int] = UNSET
    approximate_presence_count: Missing[int] = UNSET
    welcome_screen: Missing[WelcomeScreen] = UNSET
    nsfw_level: Missing[GuildNSFWLevel] = UNSET
    stickers: Missing[list[Sticker]] = UNSET
    premium_progress_bar_enabled: Missing[bool] = UNSET
    joined_at: Missing[str] = UNSET
    large: Missing[bool] = UNSET
    member_count: Missing[int] = UNSET
    voice_states: Missing[list["VoiceState"]] = UNSET
    members: Missing[list["GuildMember"]] = UNSET
    channels: Missing[list["Channel"]] = UNSET
    threads: Missing[list["Channel"]] = UNSET
    presences: Missing[list["PresenceUpdate"]] = (
        UNSET  # partial presence update objects
    )
    stage_instances: Missing[list["StageInstance"]] = UNSET
    guild_scheduled_events: Missing[list["GuildScheduledEvent"]] = UNSET


class GuildCreateCompatRole(BaseModel):
    id: Snowflake
    permissions: str | int


class GuildCreateCompatOverwrite(BaseModel):
    id: Snowflake
    type: OverwriteType | Literal["role", "member"]
    allow: str | int
    deny: str | int


class GuildCreateCompatChannel(BaseModel):
    id: Snowflake
    permission_overwrites: Missing[list[GuildCreateCompatOverwrite]] = UNSET


class GuildCreateCompat(BaseModel):
    """Compatibility shape for mixed-format ``GUILD_CREATE`` payload.

    Official Discord docs define these fields as serialized strings / enum:
    - role ``permissions``: string
    - overwrite ``type``: numeric enum
    - overwrite ``allow``/``deny``: string

    In production, gateway payloads can still contain numeric permissions and
    overwrite types as ``"role"``/``"member"`` strings. This model keeps
    parser compatibility for observed real-world payloads.

    Related issue: https://github.com/nonebot/adapter-discord/issues/48
    """

    id: Snowflake
    roles: list[GuildCreateCompatRole]
    channels: list[GuildCreateCompatChannel]


class GuildUpdate(Guild):
    """Guild Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-update"""


class GuildDelete(UnavailableGuild):
    """Guild Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-delete"""


class GuildAuditLogEntryCreate(AuditLogEntry):
    """Guild Audit Log Entry Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-audit-log-entry-create
    """


class GuildBanAdd(BaseModel):
    """Guild Ban Add Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-ban-add"""

    guild_id: Snowflake
    user: User


class GuildBanRemove(BaseModel):
    """Guild Ban Remove Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-ban-remove"""

    guild_id: Snowflake
    user: User


class GuildEmojisUpdate(BaseModel):
    """Guild Emojis Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-emojis-update"""

    guild_id: Snowflake
    emojis: list[Emoji]


class GuildStickersUpdate(BaseModel):
    """Guild Stickers Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-stickers-update
    """

    guild_id: Snowflake
    stickers: list[Sticker]


class GuildIntegrationsUpdate(BaseModel):
    """Guild Integrations Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-integrations-update
    """

    guild_id: Snowflake


class GuildMemberAdd(GuildMember):
    """Guild Member Add Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-add"""

    guild_id: Snowflake


class GuildMemberRemove(BaseModel):
    """Guild Member Remove Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-remove"""

    guild_id: Snowflake
    user: User


class GuildMemberUpdate(BaseModel):
    """Guild Member Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-update"""

    guild_id: Snowflake
    roles: list[Snowflake]
    user: User
    nick: MissingOrNullable[str] = UNSET
    avatar: str | None = Field(...)
    joined_at: datetime.datetime | None = Field(...)
    premium_since: MissingOrNullable[datetime.datetime] = UNSET
    deaf: Missing[bool] = UNSET
    mute: Missing[bool] = UNSET
    pending: Missing[bool] = UNSET
    communication_disabled_until: MissingOrNullable[datetime.datetime] = UNSET
    flags: Missing[GuildMemberFlags] = UNSET
    avatar_decoration_data: MissingOrNullable[AvatarDecorationData] = UNSET


class GuildMembersChunk(BaseModel):
    """Guild Members Chunk Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-members-chunk"""

    guild_id: Snowflake
    members: list[GuildMember]
    chunk_index: int
    chunk_count: int
    not_found: Missing[list[Snowflake]] = UNSET
    presences: Missing[list["PresenceUpdate"]] = UNSET
    nonce: Missing[str] = UNSET


class GuildRoleCreate(BaseModel):
    """Guild Role Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-create"""

    guild_id: Snowflake
    role: "Role"


class GuildRoleUpdate(BaseModel):
    """Guild Role Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-update"""

    guild_id: Snowflake
    role: "Role"


class GuildRoleDelete(BaseModel):
    """Guild Role Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-delete"""

    guild_id: Snowflake
    role_id: Snowflake


class GuildScheduledEventCreate(GuildScheduledEvent):
    """Guild Scheduled Event Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-create
    """


class GuildScheduledEventUpdate(GuildScheduledEvent):
    """Guild Scheduled Event Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-update
    """


class GuildScheduledEventDelete(GuildScheduledEvent):
    """Guild Scheduled Event Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-delete
    """


class GuildScheduledEventUserAdd(BaseModel):
    """Guild Scheduled Event User Add Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-add-guild-scheduled-event-user-add-event-fields
    """

    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


class GuildScheduledEventUserRemove(BaseModel):
    """Guild Scheduled Event User Remove Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-remove-guild-scheduled-event-user-remove-event-fields
    """

    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


class IntegrationCreate(Integration):
    """Integration Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#integration-create"""

    guild_id: Snowflake


class IntegrationUpdate(Integration):
    """Integration Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#integration-update"""

    guild_id: Snowflake


class IntegrationDelete(BaseModel):
    """Integration Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#integration-delete"""

    id: Snowflake
    guild_id: Snowflake
    application_id: Missing[Snowflake] = UNSET


class InviteCreate(BaseModel):
    """Invite Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#invite-create"""

    channel_id: Snowflake
    code: str
    created_at: datetime.datetime
    guild_id: Missing[Snowflake] = UNSET
    inviter: Missing[User] = UNSET
    max_age: int
    max_uses: int
    target_type: Missing[InviteTargetType] = UNSET
    target_user: Missing[User] = UNSET
    target_application: Missing[Application] = UNSET  # partial application object
    temporary: bool
    uses: int


class InviteDelete(BaseModel):
    """Invite Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#invite-delete"""

    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    code: str


class PresenceUpdateUser(BaseModel):
    """Presence Update User Fields

    see https://discord.com/developers/docs/topics/gateway-events#presence-update"""

    id: Snowflake
    username: Missing[str] = UNSET
    discriminator: Missing[str] = UNSET
    global_name: MissingOrNullable[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    bot: Missing[bool] = UNSET
    system: Missing[bool] = UNSET
    mfa_enabled: Missing[bool] = UNSET
    banner: MissingOrNullable[str] = UNSET
    accent_color: MissingOrNullable[int] = UNSET
    locale: Missing[str] = UNSET
    verified: Missing[bool] = UNSET
    email: MissingOrNullable[str] = UNSET
    flags: Missing[int] = UNSET
    premium_type: Missing[PremiumType] = UNSET
    public_flags: Missing[UserFlags] = UNSET
    avatar_decoration_data: MissingOrNullable["AvatarDecorationData"] = UNSET


class PresenceUpdate(BaseModel):
    """Presence Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#presence-update
    """

    user: PresenceUpdateUser
    guild_id: Snowflake
    status: PresenceStatus
    activities: list["Activity"]
    client_status: "ClientStatus"


class ClientStatus(BaseModel):
    """Client Status

    see https://discord.com/developers/docs/topics/gateway-events#client-status-object
    """

    desktop: Missing[str] = UNSET
    mobile: Missing[str] = UNSET
    web: Missing[str] = UNSET


class Activity(BaseModel):
    """Activity

    see https://discord.com/developers/docs/topics/gateway-events#activity-object"""

    name: str
    type: ActivityType
    url: MissingOrNullable[str] = UNSET
    created_at: int
    timestamps: Missing["ActivityTimestamps"] = UNSET
    application_id: Missing[Snowflake] = UNSET
    details: MissingOrNullable[str] = UNSET
    state: MissingOrNullable[str] = UNSET
    emoji: MissingOrNullable["ActivityEmoji"] = UNSET
    party: Missing["ActivityParty"] = UNSET
    assets: Missing["ActivityAssets"] = UNSET
    secrets: Missing["ActivitySecrets"] = UNSET
    instance: Missing[bool] = UNSET
    flags: Missing[ActivityFlags] = UNSET
    buttons: Missing[list["ActivityButtons"]] = UNSET


class ActivityTimestamps(BaseModel):
    """Activity Timestamps

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-timestamps
    """

    start: Missing[int] = UNSET
    end: Missing[int] = UNSET


class ActivityEmoji(BaseModel):
    """Activity Emoji

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-emoji
    """

    name: str
    id: Missing[Snowflake] = UNSET
    animated: Missing[bool] = UNSET


class ActivityParty(BaseModel):
    """Activity Party

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-party
    """

    id: Missing[str] = UNSET
    size: Missing[tuple[int, int]] = UNSET


class ActivityAssets(BaseModel):
    """Activity Assets

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-assets
    """

    large_image: Missing[ActivityAssetImage] = UNSET
    large_text: Missing[str] = UNSET
    small_image: Missing[ActivityAssetImage] = UNSET
    small_text: Missing[str] = UNSET


class ActivitySecrets(BaseModel):
    """Activity Secrets

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-secrets
    """

    join: Missing[str] = UNSET
    spectate: Missing[str] = UNSET
    match: Missing[str] = UNSET


class ActivityButtons(BaseModel):
    """Activity Buttons

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-buttons
    """

    label: str
    url: str


class UserUpdate(User):
    """User Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#user-update"""


class VoiceStateUpdate(VoiceState):
    """Voice State Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#voice-state-update
    """


class VoiceChannelStatusUpdate(BaseModel):
    """Voice Channel Status Update Event Fields

    This gateway dispatch is observed in production but is not yet fully
    documented on Discord's public Gateway Events page.

    Field shape is based on:
    - https://github.com/discord/discord-api-docs/pull/6398
    - https://github.com/discord/discord-api-docs/pull/6400
    """

    id: Snowflake
    guild_id: Snowflake
    status: str | None = None


class VoiceChannelStartTimeUpdate(BaseModel):
    """Voice Channel Start Time Update Event Fields

    This gateway dispatch is observed in production but is not yet fully
    documented on Discord's public Gateway Events page.

    Field shape is based on observed payloads and community implementations.
    """

    id: Snowflake
    guild_id: Snowflake
    voice_start_time: datetime.datetime | None = None


class VoiceServerUpdate(BaseModel):
    """Voice Server Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#voice-server-update
    """

    token: str
    guild_id: Snowflake
    endpoint: str | None = Field(...)


class WebhooksUpdate(BaseModel):
    """Webhooks Update Event Fields

    Sent when a guild channel's webhook is created, updated, or deleted.

    see https://discord.com/developers/docs/topics/gateway-events#webhooks-update
    """

    guild_id: Snowflake
    channel_id: Snowflake


class StageInstanceCreate(StageInstance):
    """Stage Instance Create Event Fields

    Sent when a Stage instance is created (i.e. the Stage is now "live").
    Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-create
    """


class StageInstanceUpdate(StageInstance):
    """Stage Instance Update Event Fields

    Sent when a Stage instance has been updated. Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-update
    """


class StageInstanceDelete(StageInstance):
    """Stage Instance Delete Event Fields

    Sent when a Stage instance has been deleted (i.e. the Stage has been closed).
    Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-delete
    """


# Permissions
# see https://discord.com/developers/docs/topics/permissions


class RoleColors(BaseModel):
    """Role colors.

    see https://discord.com/developers/docs/topics/permissions#role-object-role-colors-object
    """

    primary_color: int
    secondary_color: int | None = None
    tertiary_color: int | None = None


class Role(BaseModel):
    """Role

    see https://discord.com/developers/docs/topics/permissions#role-object"""

    id: Snowflake
    name: str
    color: int
    colors: Missing[RoleColors] = UNSET
    hoist: bool
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: Missing["RoleTags"] = UNSET
    flags: Missing[RoleFlag] = UNSET


class RoleTags(BaseModel):
    """Role tags.

    see https://discord.com/developers/docs/topics/permissions#role-object-role-tags-structure
    """

    bot_id: Missing[Snowflake] = UNSET
    integration_id: Missing[Snowflake] = UNSET
    premium_subscriber: Missing[None] = UNSET
    subscription_listing_id: Missing[Snowflake] = UNSET
    available_for_purchase: Missing[None] = UNSET
    guild_connections: Missing[None] = UNSET


# Teams
# see https://discord.com/developers/docs/topics/teams
class Team(BaseModel):
    """Team.

    see https://discord.com/developers/docs/topics/teams#data-models-team-object"""

    icon: str | None = Field(...)
    id: str
    members: list["TeamMember"]
    name: str
    owner_user_id: Snowflake


class TeamMember(BaseModel):
    """Team member.

    see https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    membership_state: MembershipState
    team_id: Snowflake
    user: "TeamMemberUser"
    role: TeamMemberRoleType


class TeamMemberUser(BaseModel):
    """partial user object for TeamMember

    see https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    avatar: str | None = None
    discriminator: str
    id: Snowflake
    username: str


class AuthorizationResponse(BaseModel):
    """Get Current Authorization Information Response

    see https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
    """

    application: Application  # partial application object
    scopes: list[str]
    expires: datetime.datetime
    user: Missing[User] = UNSET


class Poll(BaseModel):
    """The poll object has a lot of levels and nested structures.
    It was also designed to support future extensibility,
    so some fields may appear to be more complex than necessary.

    see https://discord.com/developers/docs/resources/poll#poll-object
    """

    question: "PollMedia"
    """The question of the poll. Only `text` is supported."""
    answers: list["PollAnswer"]
    """Each of the answers available in the poll."""
    expiry: datetime.datetime | None = None
    """The time when the poll ends."""
    allow_multiselect: bool
    """Whether a user can select multiple answers"""
    layout_type: int
    """The layout type of the poll"""
    results: Missing["PollResults"] = UNSET
    """The results of the poll"""


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


class PollAnswer(BaseModel):
    """answer_id: Only sent as part of responses from Discord's API/Gateway.

    see https://discord.com/developers/docs/resources/poll#poll-answer-object
    """

    answer_id: int
    poll_media: "PollMedia"


class PollAnswerRequest(BaseModel):
    """Poll answer request object.

    see https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    poll_media: "PollMedia"


class PollMedia(BaseModel):
    """The poll media object is a common object that backs both the question and
    answers. The intention is that it allows us to extensibly add new ways to
    display things in the future. For now, `question` only supports `text`, while
    answers can have an optional `emoji`.

    see https://discord.com/developers/docs/resources/poll#poll-media-object
    """

    text: Missing[str] = UNSET
    emoji: Missing["Emoji"] = UNSET  # partial emoji


class PollResults(BaseModel):
    """Poll Results

    see https://discord.com/developers/docs/resources/poll#poll-results-object
    """

    is_finalized: bool
    answer_counts: list["PollAnswerCount"]


class PollAnswerCount(BaseModel):
    """Poll Answer Count

    see https://discord.com/developers/docs/resources/poll#poll-results-object-poll-answer-count-object-structure
    """

    id: int
    count: int
    me_voted: bool


class Entitlement(BaseModel):
    """see https://discord.com/developers/docs/monetization/entitlements#entitlement-object"""

    id: Snowflake
    """ID of the entitlement"""
    sku_id: Snowflake
    """ID of the SKU"""
    application_id: Snowflake
    """ID of the parent application"""
    user_id: Missing[Snowflake] = UNSET
    """ID of the user that is granted access to the entitlement's sku"""
    type: EntitlementType
    """Type of entitlement"""
    deleted: bool
    """Entitlement was deleted"""
    starts_at: Missing[datetime.datetime] = UNSET
    """Start date at which the entitlement is valid.
    Not present when using test entitlements."""
    ends_at: Missing[datetime.datetime] = UNSET
    """Date at which the entitlement is no longer valid.
    Not present when using test entitlements."""
    guild_id: Missing[Snowflake] = UNSET
    """ID of the guild that is granted access to the entitlement's sku"""
    consumed: Missing[bool] = UNSET
    """For consumable items, whether or not the entitlement has been consumed"""


class RecurrenceRule(BaseModel):
    """Discord's recurrence rule is a subset of the behaviors defined
    in the iCalendar RFC and implemented by python's dateutil rrule

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object
    """

    start: datetime.datetime
    """Starting time of the recurrence interval"""
    end: datetime.datetime | None = None
    """Ending time of the recurrence interval"""
    frequency: GuildScheduledEventRecurrenceRuleFrequency
    """How often the event occurs"""
    interval: int
    """The spacing between the events, defined by frequency. For example,
    frecency of WEEKLY and an interval of 2 would be "every-other week"""
    by_weekday: list[GuildScheduledEventRecurrenceRuleWeekday] | None = None
    """Set of specific days within a week for the event to recur on"""
    by_n_weekday: list["GuildScheduledEventRecurrenceRuleN_WeekdayStructure"] | None = (
        None
    )
    """List of specific days within a specific week (1-5) to recur on"""
    by_month: list[GuildScheduledEventRecurrenceRuleMonth] | None = None
    """Set of specific months to recur on"""
    by_month_day: int | None = None
    """Set of specific dates within a month to recur on"""
    by_year_day: int | None = None
    """Set of days within a year to recur on (1-364)"""
    count: int | None = None
    """The total amount of times that the event is allowed to recur before stopping"""


class GuildScheduledEventRecurrenceRuleN_WeekdayStructure(BaseModel):  # noqa: N801
    """Guild Scheduled Event Recurrence Rule - N_Weekday Structure

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object-guild-scheduled-event-recurrence-rule-nweekday-structure
    """

    n: int
    """The week to reoccur on. 1 - 5"""
    day: GuildScheduledEventRecurrenceRuleWeekday
    """The day within the week to reoccur on"""


class ModifyGuildOnboardingParams(BaseModel):
    """Modify Guild Onboarding Params

    see https://discord.com/developers/docs/resources/guild#modify-guild-onboarding
    """

    prompts: Missing[list[OnboardingPrompt]] = UNSET
    """Prompts shown during onboarding and in customize community"""
    default_channel_ids: Missing[list[Snowflake]] = UNSET
    """Channel IDs that members get opted into automatically"""
    enabled: Missing[bool] = UNSET
    """Whether onboarding is enabled in the guild"""
    mode: Missing[OnboardingMode] = UNSET
    """Current mode of onboarding"""


class ActivityInstance(BaseModel):
    """Activity Instance

    see https://discord.com/developers/docs/resources/application#get-application-activity-instance-activity-instance-object
    """

    application_id: Snowflake
    """Application ID"""
    instance_id: str
    """Activity Instance ID"""
    launch_id: Snowflake
    """Unique identifier for the launch"""
    location: "ActivityLocation"
    """The Location the instance is runnning in"""
    users: list[Snowflake]
    """The IDs of the Users currently connected to the instance"""


class ActivityLocation(BaseModel):
    """The Activity Location is an object that describes
    the location in which an activity instance is running.

    see https://discord.com/developers/docs/resources/application#get-application-activity-instance-activity-location-object
    """

    id: str
    """	The unique identifier for the location"""
    kind: Literal["gc", "pc"]
    """
    Enum describing kind of location

    'gc'	The Location is a Guild Channel\n
    'pc'	The Location is a Private Channel, such as a DM or GDM
    """
    channel_id: Snowflake
    guild_id: MissingOrNullable[Snowflake] = UNSET


class ApplicationEmojis(BaseModel):
    """a list of emoji objects for the given application under the items key.

    see https://discord.com/developers/docs/resources/emoji#list-application-emojis"""

    items: list[Emoji]


class BulkBan(BaseModel):
    """bulk ban response

    see https://discord.com/developers/docs/resources/guild#bulk-guild-ban-bulk-ban-response
    """

    banned_users: list[Snowflake]
    """list of user ids, that were successfully banned"""
    failed_users: list[Snowflake]
    """list of user ids, that were not banned"""


class AnswerVoters(BaseModel):
    """get answer voter response

    see https://discord.com/developers/docs/resources/poll#get-answer-voters-response-body
    """

    users: list[User]
    """Users who voted for this answer"""


class SKU(BaseModel):
    """https://discord.com/developers/docs/resources/sku#sku-object"""

    id: Snowflake
    type: SKUType
    application_id: Snowflake
    name: str
    slug: str
    flags: SKUFlag
    dependent_sku_id: MissingOrNullable[Snowflake] = UNSET
    manifest_labels: MissingOrNullable[list[str]] = UNSET
    access_type: Missing[int] = UNSET
    features: Missing[list[str]] = UNSET
    release_date: MissingOrNullable[datetime.datetime] = UNSET
    premium: Missing[bool] = UNSET
    show_age_gate: Missing[bool] = UNSET


class Subscription(BaseModel):
    """https://discord.com/developers/docs/resources/subscription#subscription-object"""

    id: Snowflake
    user_id: Snowflake
    sku_ids: list[Snowflake]
    entitlement_ids: list[Snowflake]
    renewal_sku_ids: MissingOrNullable[list[Snowflake]] = UNSET
    current_period_start: datetime.datetime
    current_period_end: datetime.datetime
    status: SubscriptionStatus
    canceled_at: datetime.datetime | None = None
    country: Missing[str] = UNSET


class EntitlementCreate(Entitlement):
    """Entitlement Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-create"""


class EntitlementUpdate(Entitlement):
    """Entitlement Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-update"""


class EntitlementDelete(Entitlement):
    """Entitlement Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-delete"""


class SubscriptionCreate(Subscription):
    """Subscription Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#subscription-create"""


class SubscriptionUpdate(Subscription):
    """Subscription Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#subscription-update"""


class SubscriptionDelete(Subscription):
    """Subscription Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#subscription-delete"""


class VoiceChannelEffectSend(BaseModel):
    """Voice Channel Effect Send Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#voice-channel-effect-send-voice-channel-effect-send-event-fields
    """

    channel_id: Snowflake
    guild_id: Snowflake
    user_id: Snowflake
    emoji: MissingOrNullable[Emoji] = UNSET
    animation_type: MissingOrNullable[AnimationType] = UNSET
    animation_id: Missing[int] = UNSET
    sound_id: Missing[Snowflake | int] = UNSET
    sound_volume: Missing[float] = UNSET


class SoundboardSound(BaseModel):
    """Soundboard Sound Object

    see https://discord.com/developers/docs/resources/soundboard#soundboard-sound-object
    """

    name: str
    sound_id: Snowflake
    volume: float
    emoji_id: Snowflake | None = Field(...)
    emoji_name: str | None = Field(...)
    guild_id: Missing[Snowflake] = UNSET
    available: bool
    user: Missing["User"] = UNSET


class SendSoundboardSoundParams(BaseModel):
    """Send Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#send-soundboard-sound
    """

    sound_id: Snowflake
    source_guild_id: Missing[Snowflake] = UNSET


class CreateGuildSoundboardSoundParams(BaseModel):
    """Create Guild Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#create-guild-soundboard-sound
    """

    name: str
    sound: str
    volume: Missing[float] = UNSET
    emoji_id: Missing[Snowflake] = UNSET
    emoji_name: Missing[str] = UNSET


class ModifyGuildSoundboardSoundParams(BaseModel):
    """Modify Guild Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#modify-guild-soundboard-sound
    """

    name: Missing[str] = UNSET
    volume: Missing[float] = UNSET
    emoji_id: MissingOrNullable[Snowflake] = UNSET
    emoji_name: MissingOrNullable[str] = UNSET


class _SoundboardSoundsListResponse(BaseModel):
    items: list[SoundboardSound]


class ListGuildSoundboardSoundsResponse(_SoundboardSoundsListResponse):
    """List Guild Soundboard Sounds Response.

    see https://discord.com/developers/docs/resources/soundboard#list-guild-soundboard-sounds
    """


class ListDefaultSoundboardSoundsResponse(_SoundboardSoundsListResponse):
    """List Default Soundboard Sounds Response.

    see https://discord.com/developers/docs/resources/soundboard#list-default-soundboard-sounds
    """


# Lobby
# see https://discord.com/developers/docs/resources/lobby


class LobbyMember(BaseModel):
    """Lobby Member Object.

    see https://discord.com/developers/docs/resources/lobby#lobby-member-object
    """

    id: Snowflake
    metadata: dict[str, str] | None = Field(...)
    flags: Missing[LobbyMemberFlags] = UNSET


class Lobby(BaseModel):
    """Lobby Object.

    see https://discord.com/developers/docs/resources/lobby#lobby-object
    """

    id: Snowflake
    application_id: Snowflake
    metadata: dict[str, str] | None = Field(...)
    members: list[LobbyMember]
    linked_channel: Missing["Channel"] = UNSET


class _LobbyMemberWriteParamsBase(BaseModel):
    metadata: Missing[dict[str, str]] = UNSET
    flags: Missing[LobbyMemberFlags] = UNSET


class CreateLobbyMemberParams(_LobbyMemberWriteParamsBase):
    """Create Lobby Member Params.

    see https://discord.com/developers/docs/resources/lobby#create-lobby
    """

    id: Snowflake


class CreateLobbyParams(BaseModel):
    """Create Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#create-lobby
    """

    metadata: Missing[dict[str, str]] = UNSET
    members: Missing[list[CreateLobbyMemberParams]] = UNSET
    idle_timeout_seconds: Missing[int] = UNSET


class ModifyLobbyParams(BaseModel):
    """Modify Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#modify-lobby
    """

    metadata: MissingOrNullable[dict[str, str]] = UNSET
    idle_timeout_seconds: Missing[int] = UNSET


class AddLobbyMemberParams(_LobbyMemberWriteParamsBase):
    """Add Lobby Member Params.

    see https://discord.com/developers/docs/resources/lobby#add-lobby-member
    """


class LinkChannelToLobbyParams(BaseModel):
    """Link Channel to Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#link-channel-to-lobby
    """

    channel_id: MissingOrNullable[Snowflake] = UNSET


_model_types_namespace = vars(sys.modules[__name__])

for _, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel:
        if PYDANTIC_V2:
            obj.model_rebuild(_types_namespace=_model_types_namespace)
        else:
            obj.update_forward_refs(
                **{
                    k: v
                    for k, v in _model_types_namespace.items()
                    if isinstance(v, type)
                }
            )

__all__ = [
    "SKU",
    "ActionRow",
    "Activity",
    "ActivityAssets",
    "ActivityButtons",
    "ActivityEmoji",
    "ActivityInstance",
    "ActivityLocation",
    "ActivityParty",
    "ActivitySecrets",
    "ActivityTimestamps",
    "AddLobbyMemberParams",
    "AllowedMention",
    "AnswerVoters",
    "AnyCommandOption",
    "Application",
    "ApplicationCommand",
    "ApplicationCommandBulkOverwriteParams",
    "ApplicationCommandCreate",
    "ApplicationCommandData",
    "ApplicationCommandEditParams",
    "ApplicationCommandInteractionDataOption",
    "ApplicationCommandOption",
    "ApplicationCommandOptionChoice",
    "ApplicationCommandPermissions",
    "ApplicationEmojis",
    "ApplicationIntegrationTypeConfiguration",
    "ApplicationReady",
    "ApplicationRoleConnection",
    "ApplicationRoleConnectionMetadata",
    "ArchivedThreadsResponse",
    "Attachment",
    "AttachmentOption",
    "AttachmentSend",
    "AuditLog",
    "AuditLogChange",
    "AuditLogChangeException",
    "AuditLogEntry",
    "AuthorizationResponse",
    "AutoModerationAction",
    "AutoModerationActionExecution",
    "AutoModerationActionMetadata",
    "AutoModerationRule",
    "AutoModerationRuleCreate",
    "AutoModerationRuleDelete",
    "AutoModerationRuleUpdate",
    "AvatarDecorationData",
    "Ban",
    "BaseModel",
    "BooleanOption",
    "BulkBan",
    "Button",
    "Channel",
    "ChannelCreate",
    "ChannelDelete",
    "ChannelMention",
    "ChannelOption",
    "ChannelPinsUpdate",
    "ChannelUpdate",
    "ClientStatus",
    "CommandOptionBase",
    "Component",
    "ComponentEmoji",
    "Connection",
    "CountDetails",
    "CreateAndModifyAutoModerationRuleParams",
    "CreateGuildChannelParams",
    "CreateGuildParams",
    "CreateGuildScheduledEventParams",
    "CreateGuildSoundboardSoundParams",
    "CreateLobbyMemberParams",
    "CreateLobbyParams",
    "CurrentUserGuild",
    "DefaultReaction",
    "DirectComponent",
    "Embed",
    "EmbedAuthor",
    "EmbedField",
    "EmbedFooter",
    "EmbedImage",
    "EmbedProvider",
    "EmbedThumbnail",
    "EmbedVideo",
    "Emoji",
    "Entitlement",
    "EntitlementCreate",
    "EntitlementDelete",
    "EntitlementUpdate",
    "ExecuteWebhookParams",
    "File",
    "FollowedChannel",
    "ForumTag",
    "ForumTagRequest",
    "Gateway",
    "GatewayBot",
    "Guild",
    "GuildApplicationCommandPermissions",
    "GuildAuditLogEntryCreate",
    "GuildBanAdd",
    "GuildBanRemove",
    "GuildCreate",
    "GuildCreateCompat",
    "GuildCreateCompatChannel",
    "GuildCreateCompatOverwrite",
    "GuildCreateCompatRole",
    "GuildDelete",
    "GuildEmojisUpdate",
    "GuildIncidentsData",
    "GuildIntegrationsUpdate",
    "GuildMember",
    "GuildMemberAdd",
    "GuildMemberRemove",
    "GuildMemberUpdate",
    "GuildMembersChunk",
    "GuildOnboarding",
    "GuildPreview",
    "GuildRoleCreate",
    "GuildRoleDelete",
    "GuildRoleUpdate",
    "GuildScheduledEvent",
    "GuildScheduledEventCreate",
    "GuildScheduledEventDelete",
    "GuildScheduledEventEntityMetadata",
    "GuildScheduledEventRecurrenceRuleN_WeekdayStructure",
    "GuildScheduledEventUpdate",
    "GuildScheduledEventUser",
    "GuildScheduledEventUserAdd",
    "GuildScheduledEventUserRemove",
    "GuildStickersUpdate",
    "GuildTemplate",
    "GuildTemplateGuild",
    "GuildTemplateGuildChannel",
    "GuildTemplateGuildRole",
    "GuildUpdate",
    "GuildWidget",
    "GuildWidgetChannel",
    "GuildWidgetSettings",
    "GuildWidgetUser",
    "Hello",
    "Identify",
    "IdentifyConnectionProperties",
    "InstallParams",
    "IntegerOption",
    "Integration",
    "IntegrationAccount",
    "IntegrationApplication",
    "IntegrationCreate",
    "IntegrationDelete",
    "IntegrationUpdate",
    "InteractionCallbackAutocomplete",
    "InteractionCallbackData",
    "InteractionCallbackMessage",
    "InteractionCallbackModal",
    "InteractionData",
    "InteractionGuild",
    "InteractionResponse",
    "Invite",
    "InviteCreate",
    "InviteDelete",
    "InviteGuild",
    "InviteMetadata",
    "InviteStageInstance",
    "InviteTargetUsersJobStatus",
    "LinkChannelToLobbyParams",
    "ListActiveGuildThreadsResponse",
    "ListDefaultSoundboardSoundsResponse",
    "ListGuildSoundboardSoundsResponse",
    "Lobby",
    "LobbyMember",
    "MembershipScreening",
    "MentionableOption",
    "MessageActivity",
    "MessageComponentData",
    "MessageGet",
    "MessageInteraction",
    "MessageInteractionMetadata",
    "MessageReference",
    "MessageSend",
    "MessageSnapshot",
    "MessageSnapshotMessage",
    "ModalSubmitData",
    "ModifyChannelParams",
    "ModifyGuildIncidentActionsParams",
    "ModifyGuildOnboardingParams",
    "ModifyGuildParams",
    "ModifyGuildScheduledEventParams",
    "ModifyGuildSoundboardSoundParams",
    "ModifyGuildWelcomeScreenParams",
    "ModifyLobbyParams",
    "NumberOption",
    "OnboardingPrompt",
    "OnboardingPromptOption",
    "OptionChoice",
    "OptionalAuditEntryInfo",
    "Overwrite",
    "Poll",
    "PollAnswer",
    "PollAnswerCount",
    "PollAnswerRequest",
    "PollMedia",
    "PollRequest",
    "PollResults",
    "PresenceUpdate",
    "PresenceUpdateUser",
    "Reaction",
    "Ready",
    "RecurrenceRule",
    "RequestGuildMembers",
    "ResolvedData",
    "Resume",
    "Role",
    "RoleColors",
    "RoleOption",
    "RoleSubscriptionData",
    "RoleTags",
    "SelectDefaultValue",
    "SelectMenu",
    "SelectMenuResolved",
    "SelectOption",
    "SendSoundboardSoundParams",
    "SessionStartLimit",
    "Snowflake",
    "SnowflakeType",
    "SoundboardSound",
    "StageInstance",
    "StageInstanceCreate",
    "StageInstanceDelete",
    "StageInstanceUpdate",
    "Sticker",
    "StickerItem",
    "StickerPack",
    "StickerPacksResponse",
    "StringOption",
    "SubCommandGroupOption",
    "SubCommandOption",
    "Subscription",
    "SubscriptionCreate",
    "SubscriptionDelete",
    "SubscriptionUpdate",
    "Team",
    "TeamMember",
    "TeamMemberUser",
    "TextInput",
    "ThreadCreate",
    "ThreadDelete",
    "ThreadListSync",
    "ThreadMember",
    "ThreadMemberUpdate",
    "ThreadMembersUpdate",
    "ThreadMetadata",
    "ThreadUpdate",
    "TriggerMetadata",
    "UnavailableGuild",
    "UpdatePresence",
    "UpdateVoiceState",
    "User",
    "UserOption",
    "UserUpdate",
    "VoiceChannelEffectSend",
    "VoiceChannelStartTimeUpdate",
    "VoiceChannelStatusUpdate",
    "VoiceRegion",
    "VoiceServerUpdate",
    "VoiceState",
    "VoiceStateUpdate",
    "Webhook",
    "WebhooksUpdate",
    "WelcomeScreen",
    "WelcomeScreenChannel",
]
