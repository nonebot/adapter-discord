from __future__ import annotations

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ...types import UNSET, Missing, MissingOrNullable


class SendSoundboardSoundParams(BaseModel):
    sound_id: Snowflake
    source_guild_id: Missing[Snowflake] = UNSET


class CreateGuildSoundboardSoundParams(BaseModel):
    name: str
    sound: str
    volume: Missing[float] = UNSET
    emoji_id: Missing[Snowflake] = UNSET
    emoji_name: Missing[str] = UNSET


class ModifyGuildSoundboardSoundParams(BaseModel):
    name: Missing[str] = UNSET
    volume: Missing[float] = UNSET
    emoji_id: MissingOrNullable[Snowflake] = UNSET
    emoji_name: MissingOrNullable[str] = UNSET


__all__ = [
    "CreateGuildSoundboardSoundParams",
    "ModifyGuildSoundboardSoundParams",
    "SendSoundboardSoundParams",
]
