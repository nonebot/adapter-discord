from __future__ import annotations

import datetime

from pydantic import BaseModel

from ..common.channels import Channel
from ..common.guilds import (
    Ban,
    BulkBan,
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
    OnboardingPrompt,
    OnboardingPromptOption,
    UnavailableGuild,
)
from ..common.permissions import Role
from ..common.snowflake import Snowflake
from ...types import (
    UNSET,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    GuildFeature,
    Missing,
    MissingOrNullable,
    OnboardingMode,
    SystemChannelFlags,
    VerificationLevel,
)


class ModifyGuildWidgetParams(BaseModel):
    enabled: Missing[bool] = UNSET
    channel_id: MissingOrNullable[Snowflake] = UNSET


class ModifyGuildOnboardingParams(BaseModel):
    prompts: Missing[list[OnboardingPrompt]] = UNSET
    default_channel_ids: Missing[list[Snowflake]] = UNSET
    enabled: Missing[bool] = UNSET
    mode: Missing[OnboardingMode] = UNSET


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


__all__ = [
    "Ban",
    "BulkBan",
    "CreateGuildParams",
    "CurrentUserGuild",
    "Guild",
    "GuildIncidentsData",
    "GuildOnboarding",
    "GuildPreview",
    "GuildVanityURL",
    "GuildWidget",
    "GuildWidgetChannel",
    "GuildWidgetSettings",
    "GuildWidgetUser",
    "MembershipScreening",
    "ModifyGuildIncidentActionsParams",
    "ModifyGuildOnboardingParams",
    "ModifyGuildParams",
    "ModifyGuildWidgetParams",
    "OnboardingPrompt",
    "OnboardingPromptOption",
    "UnavailableGuild",
]
