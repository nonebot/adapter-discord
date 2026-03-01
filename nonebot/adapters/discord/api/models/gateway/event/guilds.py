from __future__ import annotations

import datetime
from typing import Literal

from pydantic import BaseModel, Field

from ..gateway_event_fields import PresenceUpdate
from ...common.audit_log import AuditLogEntry
from ...common.channels import Channel
from ...common.emoji import Emoji
from ...common.guild_members import GuildMember
from ...common.guild_scheduled_events import GuildScheduledEvent
from ...common.guild_welcome import WelcomeScreen
from ...common.guilds import Guild, UnavailableGuild
from ...common.permissions import Role
from ...common.snowflake import Snowflake
from ...common.stage_instance import StageInstance
from ...common.stickers import Sticker
from ...common.user import AvatarDecorationData, User
from ...common.voice import VoiceState
from ....types import (
    UNSET,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    GuildFeature,
    GuildMemberFlags,
    GuildNSFWLevel,
    MFALevel,
    Missing,
    MissingOrNullable,
    OverwriteType,
    PremiumTier,
    SystemChannelFlags,
    VerificationLevel,
)


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


__all__ = [
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
    "GuildIntegrationsUpdate",
    "GuildMemberAdd",
    "GuildMemberRemove",
    "GuildMemberUpdate",
    "GuildMembersChunk",
    "GuildRoleCreate",
    "GuildRoleDelete",
    "GuildRoleUpdate",
    "GuildScheduledEventCreate",
    "GuildScheduledEventDelete",
    "GuildScheduledEventUpdate",
    "GuildScheduledEventUserAdd",
    "GuildScheduledEventUserRemove",
    "GuildStickersUpdate",
    "GuildUpdate",
]
