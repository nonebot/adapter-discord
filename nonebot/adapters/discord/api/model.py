import datetime
import inspect
import sys
from typing import Literal

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
    ActivityInstance,
    ActivityLocation,
    Application,
    ApplicationIntegrationTypeConfiguration,
    ApplicationRoleConnectionMetadata,
    EditCurrentApplicationParams,
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
from .models.channels import (
    ArchivedThreadsResponse,
    Channel,
    DefaultReaction,
    FollowedChannel,
    ForumTag,
    ForumTagRequest,
    ModifyChannelParams,
    ModifyGuildChannelPositionParams,
    ModifyThreadParams,
    Overwrite,
    PartialOverwrite,
    StartThreadFromMessageParams,
    StartThreadWithoutMessageParams,
    ThreadMember,
    ThreadMetadata,
)
from .models.embeds import (
    Embed,
    EmbedAuthor,
    EmbedField,
    EmbedFooter,
    EmbedImage,
    EmbedProvider,
    EmbedThumbnail,
    EmbedVideo,
)
from .models.emoji import ApplicationEmojis, Emoji
from .models.gateway import Gateway, GatewayBot, SessionStartLimit
from .models.gateway_event_fields import (
    StageInstanceCreate,
    StageInstanceDelete,
    StageInstanceUpdate,
    UserUpdate,
    VoiceChannelEffectSend,
    VoiceChannelStartTimeUpdate,
    VoiceChannelStatusUpdate,
    VoiceServerUpdate,
    VoiceStateUpdate,
    WebhooksUpdate,
)
from .models.gateway_payloads import (
    ApplicationReady,
    Hello,
    Identify,
    IdentifyConnectionProperties,
    Ready,
    RequestGuildMembers,
    Resume,
    UpdatePresence,
    UpdateVoiceState,
)
from .models.guild_members import ModifyCurrentMemberParams, ModifyGuildMemberParams
from .models.guild_scheduled_events import (
    CreateGuildScheduledEventParams,
    GuildScheduledEvent,
    GuildScheduledEventEntityMetadata,
    GuildScheduledEventRecurrenceRuleN_WeekdayStructure,
    GuildScheduledEventUser,
    ModifyGuildScheduledEventParams,
    RecurrenceRule,
)
from .models.guild_templates import (
    CreateGuildTemplateParams,
    GuildTemplate,
    GuildTemplateGuild,
    GuildTemplateGuildChannel,
    GuildTemplateGuildRole,
    ModifyGuildTemplateParams,
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
from .models.invites import (
    Invite,
    InviteGuild,
    InviteMetadata,
    InviteStageInstance,
    InviteTargetUsersJobStatus,
)
from .models.lobby import (
    AddLobbyMemberParams,
    CreateLobbyMemberParams,
    CreateLobbyParams,
    LinkChannelToLobbyParams,
    Lobby,
    LobbyMember,
    ModifyLobbyParams,
)
from .models.messages import (
    AllowedMention,
    Attachment,
    AttachmentSend,
    ChannelMention,
    CountDetails,
    File,
    MessageActivity,
    MessageCall,
    MessageEditParams,
    MessageGet,
    MessageReference,
    MessageSend,
    MessageSnapshot,
    MessageSnapshotMessage,
    Reaction,
    RoleSubscriptionData,
    WebhookMessageEditParams,
)
from .models.monetization import (
    SKU,
    Entitlement,
    EntitlementCreate,
    EntitlementDelete,
    EntitlementUpdate,
    Subscription,
    SubscriptionCreate,
    SubscriptionDelete,
    SubscriptionUpdate,
)
from .models.oauth2 import AuthorizationResponse
from .models.permissions import Role, RoleColors, RoleTags
from .models.polls import (
    AnswerVoters,
    Poll,
    PollAnswer,
    PollAnswerCount,
    PollAnswerRequest,
    PollMedia,
    PollRequest,
    PollResults,
)
from .models.snowflake import Snowflake, SnowflakeType
from .models.soundboard import (
    CreateGuildSoundboardSoundParams,
    ListDefaultSoundboardSoundsResponse,
    ListGuildSoundboardSoundsResponse,
    ModifyGuildSoundboardSoundParams,
    SendSoundboardSoundParams,
    SoundboardSound,
)
from .models.stage_instance import StageInstance
from .models.stickers import Sticker, StickerItem, StickerPack, StickerPacksResponse
from .models.teams import Team, TeamMember, TeamMemberUser
from .models.user import (
    ApplicationRoleConnection,
    AvatarDecorationData,
    Connection,
    ModifyCurrentUserParams,
    User,
)
from .models.voice import VoiceRegion, VoiceState
from .models.webhooks import ExecuteWebhookParams, Webhook
from .types import (
    UNSET,
    ActivityAssetImage,
    ActivityFlags,
    ActivityType,
    ChannelType,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    ForumLayoutTypes,
    GuildFeature,
    GuildMemberFlags,
    GuildNSFWLevel,
    IntegrationExpireBehaviors,
    InviteTargetType,
    MFALevel,
    Missing,
    MissingOrNullable,
    OnboardingMode,
    OnboardingPromptType,
    OverwriteType,
    PremiumTier,
    PremiumType,
    PresenceStatus,
    SortOrderTypes,
    SystemChannelFlags,
    TriggerType,
    UserFlags,
    VerificationLevel,
    VideoQualityMode,
)

# Channel
# see https://discord.com/developers/docs/resources/channel


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


# Permissions
# see https://discord.com/developers/docs/topics/permissions


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


class BulkBan(BaseModel):
    """bulk ban response

    see https://discord.com/developers/docs/resources/guild#bulk-guild-ban-bulk-ban-response
    """

    banned_users: list[Snowflake]
    """list of user ids, that were successfully banned"""
    failed_users: list[Snowflake]
    """list of user ids, that were not banned"""


# Lobby
# see https://discord.com/developers/docs/resources/lobby

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
    "CreateGuildTemplateParams",
    "CreateLobbyMemberParams",
    "CreateLobbyParams",
    "CurrentUserGuild",
    "DefaultReaction",
    "DirectComponent",
    "EditCurrentApplicationParams",
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
    "MessageCall",
    "MessageComponentData",
    "MessageEditParams",
    "MessageGet",
    "MessageInteraction",
    "MessageInteractionMetadata",
    "MessageReference",
    "MessageSend",
    "MessageSnapshot",
    "MessageSnapshotMessage",
    "ModalSubmitData",
    "ModifyChannelParams",
    "ModifyCurrentMemberParams",
    "ModifyCurrentUserParams",
    "ModifyGuildChannelPositionParams",
    "ModifyGuildIncidentActionsParams",
    "ModifyGuildMemberParams",
    "ModifyGuildOnboardingParams",
    "ModifyGuildParams",
    "ModifyGuildScheduledEventParams",
    "ModifyGuildSoundboardSoundParams",
    "ModifyGuildTemplateParams",
    "ModifyGuildWelcomeScreenParams",
    "ModifyLobbyParams",
    "ModifyThreadParams",
    "NumberOption",
    "OnboardingPrompt",
    "OnboardingPromptOption",
    "OptionChoice",
    "OptionalAuditEntryInfo",
    "Overwrite",
    "PartialOverwrite",
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
    "StartThreadFromMessageParams",
    "StartThreadWithoutMessageParams",
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
    "WebhookMessageEditParams",
    "WebhooksUpdate",
    "WelcomeScreen",
    "WelcomeScreenChannel",
]
