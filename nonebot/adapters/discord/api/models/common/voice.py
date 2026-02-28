from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ...types import UNSET, Missing

if TYPE_CHECKING:
    from .guild_members import GuildMember


class VoiceState(BaseModel):
    guild_id: Missing[Snowflake] = UNSET
    channel_id: Snowflake | None = Field(...)
    user_id: Snowflake
    member: Missing[GuildMember] = UNSET
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: Missing[bool] = UNSET
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: datetime.datetime | None = Field(...)


class VoiceRegion(BaseModel):
    id: str
    name: str
    optimal: bool
    deprecated: bool
    custom: bool
