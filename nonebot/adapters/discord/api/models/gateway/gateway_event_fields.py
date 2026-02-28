from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from ..common.snowflake import Snowflake
from ..common.user import User
from ..common.emoji import Emoji
from ..common.stage_instance import StageInstance
from ..common.voice import VoiceState
from ...types import (
    UNSET,
    ActivityAssetImage,
    ActivityFlags,
    ActivityType,
    AnimationType,
    Missing,
    MissingOrNullable,
    PremiumType,
    PresenceStatus,
    UserFlags,
)

if TYPE_CHECKING:
    from ..common.user import AvatarDecorationData


class UserUpdate(User):
    pass


class VoiceStateUpdate(VoiceState):
    pass


class VoiceChannelStatusUpdate(BaseModel):
    id: Snowflake
    guild_id: Snowflake
    status: str | None = None


class VoiceChannelStartTimeUpdate(BaseModel):
    id: Snowflake
    guild_id: Snowflake
    voice_start_time: datetime.datetime | None = None


class VoiceServerUpdate(BaseModel):
    token: str
    guild_id: Snowflake
    endpoint: str | None = Field(...)


class WebhooksUpdate(BaseModel):
    guild_id: Snowflake
    channel_id: Snowflake


class StageInstanceCreate(StageInstance):
    pass


class StageInstanceUpdate(StageInstance):
    pass


class StageInstanceDelete(StageInstance):
    pass


class VoiceChannelEffectSend(BaseModel):
    channel_id: Snowflake
    guild_id: Snowflake
    user_id: Snowflake
    emoji: MissingOrNullable[Emoji] = UNSET
    animation_type: MissingOrNullable[AnimationType] = UNSET
    animation_id: Missing[int] = UNSET
    sound_id: Missing[Snowflake | int] = UNSET
    sound_volume: Missing[float] = UNSET


class PresenceUpdateUser(BaseModel):
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
    avatar_decoration_data: MissingOrNullable[AvatarDecorationData] = UNSET


class PresenceUpdate(BaseModel):
    user: PresenceUpdateUser
    guild_id: Snowflake
    status: PresenceStatus
    activities: list[Activity]
    client_status: ClientStatus


class ClientStatus(BaseModel):
    desktop: Missing[str] = UNSET
    mobile: Missing[str] = UNSET
    web: Missing[str] = UNSET


class Activity(BaseModel):
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


class ActivityTimestamps(BaseModel):
    start: Missing[int] = UNSET
    end: Missing[int] = UNSET


class ActivityEmoji(BaseModel):
    name: str
    id: Missing[Snowflake] = UNSET
    animated: Missing[bool] = UNSET


class ActivityParty(BaseModel):
    id: Missing[str] = UNSET
    size: Missing[tuple[int, int]] = UNSET


class ActivityAssets(BaseModel):
    large_image: Missing[ActivityAssetImage] = UNSET
    large_text: Missing[str] = UNSET
    small_image: Missing[ActivityAssetImage] = UNSET
    small_text: Missing[str] = UNSET


class ActivitySecrets(BaseModel):
    join: Missing[str] = UNSET
    spectate: Missing[str] = UNSET
    match: Missing[str] = UNSET


class ActivityButtons(BaseModel):
    label: str
    url: str
