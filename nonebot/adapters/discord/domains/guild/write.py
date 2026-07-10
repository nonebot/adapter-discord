"""Canonical guild.write models."""

from __future__ import annotations

from typing import TYPE_CHECKING

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

from .._model_support import (
    UNSET,
    BaseModel,
    ChannelType,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    ForumLayoutTypes,
    GuildFeature,
    GuildMemberFlags,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventStatus,
    Missing,
    MissingOrNullable,
    OnboardingMode,
    Snowflake,
    SortOrderTypes,
    SystemChannelFlags,
    VerificationLevel,
    VideoQualityMode,
    datetime,
)


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


class CreateGuildParams(BaseModel):
    """Create Guild Params

    see https://discord.com/developers/docs/resources/guild#create-guild"""

    name: str
    region: str | None = None
    icon: str | None = None
    verification_level: VerificationLevel | None = None
    default_message_notifications: DefaultMessageNotificationLevel | None = None
    explicit_content_filter: ExplicitContentFilterLevel | None = None
    roles: list[Role] | None = None
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
    permission_overwrites: list[Overwrite] | None = None
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
    recurrence_rule: RecurrenceRule | None = None


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
    recurrence_rule: MissingOrNullable[RecurrenceRule] = UNSET


class ModifyGuildRoleParams(BaseModel):
    """Modify Guild Role Params.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/guild#modify-guild-role
    """

    name: MissingOrNullable[str] = UNSET
    permissions: MissingOrNullable[str] = UNSET
    color: MissingOrNullable[int] = UNSET
    colors: Missing[RoleColors] = UNSET
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
    colors: Missing[RoleColors] = UNSET
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


__all__ = [
    "CreateGuildChannelParams",
    "CreateGuildParams",
    "CreateGuildRoleParams",
    "CreateGuildScheduledEventParams",
    "CreateGuildTemplateParams",
    "ModifyCurrentMemberParams",
    "ModifyGuildIncidentActionsParams",
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
