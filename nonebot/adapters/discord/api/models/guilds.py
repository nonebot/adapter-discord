from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, Field

from .emoji import Emoji
from .snowflake import Snowflake
from ..types import (
    UNSET,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    GuildFeature,
    GuildNSFWLevel,
    MFALevel,
    Missing,
    MissingOrNullable,
    PremiumTier,
    SystemChannelFlags,
    VerificationLevel,
)

if TYPE_CHECKING:
    from .permissions import Role
    from .stickers import Sticker
    from ..model import WelcomeScreen


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
