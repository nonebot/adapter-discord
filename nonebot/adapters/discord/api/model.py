# ruff: noqa: F401

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
    AutoModerationActionExecution,
    AutoModerationActionMetadata,
    AutoModerationRule,
    AutoModerationRuleCreate,
    AutoModerationRuleDelete,
    AutoModerationRuleUpdate,
    CreateAndModifyAutoModerationRuleParams,
    TriggerMetadata,
)
from .models.channels import (
    ArchivedThreadsResponse,
    Channel,
    ChannelCreate,
    ChannelDelete,
    ChannelPinsUpdate,
    ChannelUpdate,
    CreateGuildChannelParams,
    DefaultReaction,
    FollowedChannel,
    ForumTag,
    ForumTagRequest,
    ListActiveGuildThreadsResponse,
    ModifyChannelParams,
    ModifyGuildChannelPositionParams,
    ModifyThreadParams,
    Overwrite,
    PartialOverwrite,
    StartThreadFromMessageParams,
    StartThreadWithoutMessageParams,
    ThreadCreate,
    ThreadDelete,
    ThreadListSync,
    ThreadMember,
    ThreadMembersUpdate,
    ThreadMemberUpdate,
    ThreadMetadata,
    ThreadUpdate,
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
from .models.emoji import (
    ApplicationEmojis,
    Emoji,
    ModifyGuildEmojiParams,
)
from .models.gateway import Gateway, GatewayBot, SessionStartLimit
from .models.gateway_event_fields import (
    Activity,
    ActivityAssets,
    ActivityButtons,
    ActivityEmoji,
    ActivityParty,
    ActivitySecrets,
    ActivityTimestamps,
    ClientStatus,
    PresenceUpdate,
    PresenceUpdateUser,
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
from .models.guild_members import (
    GuildMember,
    ModifyCurrentMemberParams,
    ModifyGuildMemberParams,
)
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
from .models.guild_welcome import (
    ModifyGuildWelcomeScreenParams,
    WelcomeScreen,
    WelcomeScreenChannel,
)
from .models.guilds import (
    Ban,
    BulkBan,
    CreateGuildParams,
    CurrentUserGuild,
    Guild,
    GuildIncidentsData,
    GuildOnboarding,
    GuildPreview,
    GuildVanityURL,
    GuildWidget,
    GuildWidgetChannel,
    GuildWidgetSettings,
    GuildWidgetUser,
    MembershipScreening,
    ModifyGuildIncidentActionsParams,
    ModifyGuildOnboardingParams,
    ModifyGuildParams,
    ModifyGuildWidgetParams,
    OnboardingPrompt,
    OnboardingPromptOption,
    UnavailableGuild,
)
from .models.integrations import (
    Integration,
    IntegrationAccount,
    IntegrationApplication,
    IntegrationCreate,
    IntegrationDelete,
    IntegrationUpdate,
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
    InviteCreate,
    InviteDelete,
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
from .models.permissions import (
    CreateGuildRoleParams,
    ModifyGuildRoleParams,
    ModifyGuildRolePositionParams,
    Role,
    RoleColors,
    RoleTags,
)
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
from .models.stickers import (
    ModifyGuildStickerParams,
    Sticker,
    StickerItem,
    StickerPack,
    StickerPacksResponse,
)
from .models.teams import Team, TeamMember, TeamMemberUser
from .models.user import (
    ApplicationRoleConnection,
    AvatarDecorationData,
    Connection,
    ModifyCurrentUserParams,
    User,
)
from .models.voice import (
    ModifyCurrentUserVoiceStateParams,
    VoiceRegion,
    VoiceState,
)
from .models.webhooks import (
    CreateWebhookParams,
    ExecuteWebhookParams,
    Webhook,
)
from .types import (
    UNSET,
    ActivityAssetImage,
    ActivityFlags,
    ActivityType,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    GuildFeature,
    GuildMemberFlags,
    GuildNSFWLevel,
    InviteTargetType,
    MFALevel,
    Missing,
    MissingOrNullable,
    OverwriteType,
    PremiumTier,
    PremiumType,
    PresenceStatus,
    SystemChannelFlags,
    TriggerType,
    UserFlags,
    VerificationLevel,
)

# Channel
# see https://discord.com/developers/docs/resources/channel


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


# Permissions
# see https://discord.com/developers/docs/topics/permissions


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
    "GuildVanityURL",
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
