from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ...types import UNSET, Missing

if TYPE_CHECKING:
    from .user import User


class SoundboardSound(BaseModel):
    name: str
    sound_id: Snowflake
    volume: float
    emoji_id: Snowflake | None = Field(...)
    emoji_name: str | None = Field(...)
    guild_id: Missing[Snowflake] = UNSET
    available: bool
    user: Missing[User] = UNSET


__all__ = ["SoundboardSound"]
