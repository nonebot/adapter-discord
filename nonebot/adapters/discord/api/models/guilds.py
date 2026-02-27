from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, Field

from .audit_log import AuditLogEntry
from .emoji import Emoji
from .gateway_event_fields import PresenceUpdate
from .guild_members import GuildMember
from .guild_scheduled_events import GuildScheduledEvent
from .snowflake import Snowflake
from .stage_instance import StageInstance
from .user import AvatarDecorationData, User
from .voice import VoiceState
from ..types import (
    UNSET,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    GuildFeature,
    GuildMemberFlags,
    GuildNSFWLevel,
    MFALevel,
    Missing,
    MissingOrNullable,
    OnboardingMode,
    OnboardingPromptType,
    OverwriteType,
    PremiumTier,
    SystemChannelFlags,
    VerificationLevel,
)

if TYPE_CHECKING:
    from .channels import Channel
    from .guild_welcome import WelcomeScreen
    from .permissions import Role
    from .stickers import Sticker


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
    roles: list[Role]
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
    welcome_screen: Missing[WelcomeScreen] = UNSET
    nsfw_level: GuildNSFWLevel
    stickers: Missing[list[Sticker]] = UNSET
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: MissingOrNullable[Snowflake] = UNSET
    incidents_data: MissingOrNullable[GuildIncidentsData] = UNSET


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
    stickers: list[Sticker]


class GuildWidgetSettings(BaseModel):
    """Guild Widget Settings

    see https://discord.com/developers/docs/resources/guild#guild-widget-settings-object
    """

    enabled: bool
    channel_id: Snowflake | None = None


class ModifyGuildWidgetParams(BaseModel):
    enabled: Missing[bool] = UNSET
    channel_id: MissingOrNullable[Snowflake] = UNSET


class GuildWidget(BaseModel):
    """Guild Widget

    see https://discord.com/developers/docs/resources/guild#guild-widget-object"""

    id: Snowflake
    name: str
    instant_invite: str | None = None
    channels: list[GuildWidgetChannel]
    members: list[GuildWidgetUser]
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


class GuildOnboarding(BaseModel):
    guild_id: Snowflake
    prompts: list[OnboardingPrompt]
    default_channel_ids: list[Snowflake]
    enabled: bool
    mode: OnboardingMode


class OnboardingPrompt(BaseModel):
    id: Snowflake
    type: OnboardingPromptType
    options: list[OnboardingPromptOption]
    title: str
    single_select: bool
    required: bool
    in_onboarding: bool


class OnboardingPromptOption(BaseModel):
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
    pass


class ModifyGuildOnboardingParams(BaseModel):
    prompts: Missing[list[OnboardingPrompt]] = UNSET
    default_channel_ids: Missing[list[Snowflake]] = UNSET
    enabled: Missing[bool] = UNSET
    mode: Missing[OnboardingMode] = UNSET


class Ban(BaseModel):
    reason: str | None = None
    user: User


class BulkBan(BaseModel):
    banned_users: list[Snowflake]
    failed_users: list[Snowflake]


class CreateGuildParams(BaseModel):
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
    invites_disabled_until: MissingOrNullable[datetime.datetime] = UNSET
    dms_disabled_until: MissingOrNullable[datetime.datetime] = UNSET


class GuildCreate(BaseModel):
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
    roles: Missing[list[Role]] = UNSET
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
    voice_states: Missing[list[VoiceState]] = UNSET
    members: Missing[list[GuildMember]] = UNSET
    channels: Missing[list[Channel]] = UNSET
    threads: Missing[list[Channel]] = UNSET
    presences: Missing[list[PresenceUpdate]] = UNSET
    stage_instances: Missing[list[StageInstance]] = UNSET
    guild_scheduled_events: Missing[list[GuildScheduledEvent]] = UNSET


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
    id: Snowflake
    roles: list[GuildCreateCompatRole]
    channels: list[GuildCreateCompatChannel]


class GuildUpdate(Guild):
    pass


class GuildDelete(UnavailableGuild):
    pass


class GuildAuditLogEntryCreate(AuditLogEntry):
    pass


class GuildBanAdd(BaseModel):
    guild_id: Snowflake
    user: User


class GuildBanRemove(BaseModel):
    guild_id: Snowflake
    user: User


class GuildEmojisUpdate(BaseModel):
    guild_id: Snowflake
    emojis: list[Emoji]


class GuildStickersUpdate(BaseModel):
    guild_id: Snowflake
    stickers: list[Sticker]


class GuildIntegrationsUpdate(BaseModel):
    guild_id: Snowflake


class GuildMemberAdd(GuildMember):
    guild_id: Snowflake


class GuildMemberRemove(BaseModel):
    guild_id: Snowflake
    user: User


class GuildMemberUpdate(BaseModel):
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
    guild_id: Snowflake
    members: list[GuildMember]
    chunk_index: int
    chunk_count: int
    not_found: Missing[list[Snowflake]] = UNSET
    presences: Missing[list[PresenceUpdate]] = UNSET
    nonce: Missing[str] = UNSET


class GuildRoleCreate(BaseModel):
    guild_id: Snowflake
    role: Role


class GuildRoleUpdate(BaseModel):
    guild_id: Snowflake
    role: Role


class GuildRoleDelete(BaseModel):
    guild_id: Snowflake
    role_id: Snowflake


class GuildScheduledEventCreate(GuildScheduledEvent):
    pass


class GuildScheduledEventUpdate(GuildScheduledEvent):
    pass


class GuildScheduledEventDelete(GuildScheduledEvent):
    pass


class GuildScheduledEventUserAdd(BaseModel):
    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


class GuildScheduledEventUserRemove(BaseModel):
    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake
