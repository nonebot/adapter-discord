from __future__ import annotations

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ..common.stickers import Sticker, StickerItem
from ...types import UNSET, Missing, MissingOrNullable


class StickerPack(BaseModel):
    id: Snowflake
    stickers: list[Sticker]
    name: str
    sku_id: Snowflake
    cover_sticker_id: Missing[Snowflake] = UNSET
    description: str
    banner_asset_id: Missing[Snowflake] = UNSET


class StickerPacksResponse(BaseModel):
    sticker_packs: list[StickerPack]


class ModifyGuildStickerParams(BaseModel):
    name: Missing[str] = UNSET
    description: MissingOrNullable[str] = UNSET
    tags: Missing[str] = UNSET


__all__ = [
    "ModifyGuildStickerParams",
    "Sticker",
    "StickerItem",
    "StickerPack",
    "StickerPacksResponse",
]
