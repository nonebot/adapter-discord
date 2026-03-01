from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ...types import UNSET, Missing, StickerFormatType, StickerType

if TYPE_CHECKING:
    from .user import User


class Sticker(BaseModel):
    id: Snowflake
    pack_id: Missing[Snowflake] = UNSET
    name: str
    description: str | None = Field(...)
    tags: str
    asset: Missing[str] = UNSET
    type: StickerType
    format_type: StickerFormatType
    available: Missing[bool] = UNSET
    guild_id: Missing[Snowflake] = UNSET
    user: Missing[User] = UNSET
    sort_value: Missing[int] = UNSET


class StickerItem(BaseModel):
    id: Snowflake
    name: str
    format_type: StickerFormatType
