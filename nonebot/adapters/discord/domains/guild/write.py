"""Canonical guild.write models."""

from typing import TYPE_CHECKING
from typing_extensions import Required

from .._model_support import OutboundTypedDict

if TYPE_CHECKING:
    from ..models import (
        Channel,
        DefaultReaction,
        ForumTagRequest,
        GuildScheduledEventEntityMetadata,
        OnboardingPrompt,
        Overwrite,
        RecurrenceRule,
        Role,
        RoleColors,
        WelcomeScreenChannel,
    )
    from ...protocol import SnowflakeType

from .._model_support import (
    ChannelType,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    ForumLayoutTypes,
    GuildFeature,
    GuildMemberFlags,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventStatus,
    OnboardingMode,
    Snowflake,
    SortOrderTypes,
    SystemChannelFlags,
    VerificationLevel,
    VideoQualityMode,
    datetime,
)


class ModifyGuildMemberParams(OutboundTypedDict, total=False):
    """Modify Guild Member Params.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/guild#modify-guild-member
    """

    nick: str | None
    roles: list[Snowflake] | None
    mute: bool | None
    deaf: bool | None
    channel_id: Snowflake | None
    communication_disabled_until: datetime.datetime | None
    flags: GuildMemberFlags | None


class ModifyCurrentMemberParams(OutboundTypedDict, total=False):
    """Modify Current Member Params.

    see https://discord.com/developers/docs/resources/guild#modify-current-member
    """

    nick: str | None
    banner: str | None
    avatar: str | None
    bio: str | None


class CreateGuildParams(OutboundTypedDict, total=False):
    """Create Guild Params

    see https://discord.com/developers/docs/resources/guild#create-guild"""

    name: Required[str]
    region: str | None
    icon: str | None
    verification_level: VerificationLevel | None
    default_message_notifications: DefaultMessageNotificationLevel | None
    explicit_content_filter: ExplicitContentFilterLevel | None
    roles: "list[Role] | None"
    channels: "list[Channel] | None"
    afk_channel_id: Snowflake | None
    afk_timeout: int | None
    system_channel_id: Snowflake | None
    system_channel_flags: SystemChannelFlags | None


class ModifyGuildParams(OutboundTypedDict, total=False):
    """Modify Guild Params

    see https://discord.com/developers/docs/resources/guild#modify-guild"""

    name: str
    region: str | None
    verification_level: VerificationLevel | None
    default_message_notifications: DefaultMessageNotificationLevel | None
    explicit_content_filter: ExplicitContentFilterLevel | None
    afk_channel_id: Snowflake | None
    afk_timeout: int
    icon: str | None
    splash: str | None
    discovery_splash: str | None
    banner: str | None
    system_channel_id: Snowflake | None
    system_channel_flags: SystemChannelFlags
    rules_channel_id: Snowflake | None
    public_updates_channel_id: Snowflake | None
    preferred_locale: str | None
    features: list[GuildFeature]
    description: str | None
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: Snowflake | None


class ModifyGuildIncidentActionsParams(OutboundTypedDict, total=False):
    """Modify Guild Incident Actions Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-incident-actions
    """

    invites_disabled_until: datetime.datetime | None
    dms_disabled_until: datetime.datetime | None


class CreateGuildChannelParams(OutboundTypedDict, total=False):
    """Create Guild Channel Params

    see https://discord.com/developers/docs/resources/guild#create-guild-channel"""

    name: Required[str]
    type: ChannelType | None
    topic: str | None
    bitrate: int | None
    user_limit: int | None
    rate_limit_per_user: int | None
    position: int | None
    permission_overwrites: "list[Overwrite] | None"
    parent_id: Snowflake | None
    nsfw: bool | None
    rtc_region: str | None
    video_quality_mode: VideoQualityMode | None
    default_auto_archive_duration: int | None
    default_reaction_emoji: "DefaultReaction | None"
    available_tags: "list[ForumTagRequest] | None"
    default_sort_order: SortOrderTypes | None
    default_forum_layout: ForumLayoutTypes | None
    default_thread_rate_limit_per_user: int | None


class ModifyGuildWelcomeScreenParams(OutboundTypedDict, total=False):
    """Modify Guild Welcome Screen Params

    see https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
    """

    enabled: bool | None
    welcome_channels: "list[WelcomeScreenChannel] | None"
    description: str | None


class ModifyGuildWidgetParams(OutboundTypedDict, total=False):
    """Modify Guild Widget Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-widget
    """

    enabled: bool
    channel_id: Snowflake | None


class CreateGuildScheduledEventParams(OutboundTypedDict, total=False):
    """Create Guild Scheduled Event Params

    see https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event-json-params
    """

    channel_id: Snowflake
    entity_metadata: "GuildScheduledEventEntityMetadata"
    name: Required[str]
    privacy_level: Required[GuildScheduledEventPrivacyLevel]
    scheduled_start_time: Required[datetime.datetime]
    scheduled_end_time: datetime.datetime
    description: str
    entity_type: Required[GuildScheduledEventEntityType]
    image: str
    recurrence_rule: "RecurrenceRule"


class ModifyGuildScheduledEventParams(OutboundTypedDict, total=False):
    """Modify Guild Scheduled Event Params

    see https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event-json-params
    """

    channel_id: Snowflake | None
    entity_metadata: "GuildScheduledEventEntityMetadata | None"
    name: str
    privacy_level: GuildScheduledEventPrivacyLevel
    scheduled_start_time: datetime.datetime
    scheduled_end_time: datetime.datetime
    description: str | None
    entity_type: GuildScheduledEventEntityType
    status: GuildScheduledEventStatus
    image: str
    recurrence_rule: "RecurrenceRule | None"


class ModifyGuildRoleParams(OutboundTypedDict, total=False):
    """Modify Guild Role Params.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/guild#modify-guild-role
    """

    name: str | None
    permissions: str | None
    color: int | None
    colors: "RoleColors"
    hoist: bool | None
    icon: str | None
    unicode_emoji: str | None
    mentionable: bool | None


class CreateGuildRoleParams(OutboundTypedDict, total=False):
    """Create Guild Role Params.

    see https://discord.com/developers/docs/resources/guild#create-guild-role
    """

    name: str
    permissions: str
    color: int
    colors: "RoleColors"
    hoist: bool
    icon: str | None
    unicode_emoji: str | None
    mentionable: bool


class ModifyGuildRolePositionParams(OutboundTypedDict, total=False):
    """Modify Guild Role Position Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-role-positions
    """

    id: Required[Snowflake]
    position: int | None


class CreateGuildTemplateParams(OutboundTypedDict, total=False):
    """Create Guild Template Params.

    see https://discord.com/developers/docs/resources/guild-template#create-guild-template
    """

    name: Required[str]
    description: str | None


class ModifyGuildTemplateParams(OutboundTypedDict, total=False):
    """Modify Guild Template Params.

    see https://discord.com/developers/docs/resources/guild-template#modify-guild-template
    """

    name: str
    description: str | None


class ModifyGuildOnboardingParams(OutboundTypedDict, total=False):
    """Modify Guild Onboarding Params

    see https://discord.com/developers/docs/resources/guild#modify-guild-onboarding
    """

    prompts: "list[OnboardingPrompt]"
    """Prompts shown during onboarding and in customize community"""
    default_channel_ids: list[Snowflake]
    """Channel IDs that members get opted into automatically"""
    enabled: bool
    """Whether onboarding is enabled in the guild"""
    mode: OnboardingMode
    """Current mode of onboarding"""


class AddGuildMemberParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_add_guild_member``."""

    access_token: Required[str]
    nick: str
    roles: "list[SnowflakeType]"
    mute: bool
    deaf: bool


class ModifyCurrentUserNickParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_modify_current_user_nick``."""

    nick: "str | None"


class CreateGuildBanParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_create_guild_ban``."""

    delete_message_days: int
    delete_message_seconds: int


class BulkGuildBanParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_bulk_guild_ban``."""

    user_ids: Required["list[SnowflakeType]"]
    delete_message_seconds: int


class ModifyGuildMFAParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_modify_guild_MFA_level``."""

    level: Required[int]


class BeginGuildPruneParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_begin_guild_prune``."""

    days: int
    compute_prune_count: bool
    include_roles: "list[SnowflakeType]"


__all__ = [
    "AddGuildMemberParams",
    "BeginGuildPruneParams",
    "BulkGuildBanParams",
    "CreateGuildBanParams",
    "CreateGuildChannelParams",
    "CreateGuildParams",
    "CreateGuildRoleParams",
    "CreateGuildScheduledEventParams",
    "CreateGuildTemplateParams",
    "ModifyCurrentMemberParams",
    "ModifyCurrentUserNickParams",
    "ModifyGuildIncidentActionsParams",
    "ModifyGuildMFAParams",
    "ModifyGuildMemberParams",
    "ModifyGuildOnboardingParams",
    "ModifyGuildParams",
    "ModifyGuildRoleParams",
    "ModifyGuildRolePositionParams",
    "ModifyGuildScheduledEventParams",
    "ModifyGuildTemplateParams",
    "ModifyGuildWelcomeScreenParams",
    "ModifyGuildWidgetParams",
]
