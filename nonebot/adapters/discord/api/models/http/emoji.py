from __future__ import annotations

from pydantic import BaseModel

from ..common.emoji import ApplicationEmojis, Emoji
from ..common.snowflake import Snowflake
from ...types import UNSET, Missing, MissingOrNullable


class ModifyGuildEmojiParams(BaseModel):
    name: Missing[str] = UNSET
    roles: MissingOrNullable[list[Snowflake]] = UNSET


__all__ = ["ApplicationEmojis", "Emoji", "ModifyGuildEmojiParams"]
