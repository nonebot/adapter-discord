from __future__ import annotations

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ..common.stickers import Sticker
from ...types import UNSET, Missing


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


__all__ = ["StickerPack", "StickerPacksResponse"]
