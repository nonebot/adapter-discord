from __future__ import annotations

import datetime

from pydantic import BaseModel, Field

from .emoji import Emoji
from .snowflake import Snowflake
from .stage_instance import StageInstance
from .user import User
from .voice import VoiceState
from ..types import UNSET, AnimationType, Missing, MissingOrNullable


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
