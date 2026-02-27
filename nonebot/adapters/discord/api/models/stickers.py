from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ..types import UNSET, Missing, StickerFormatType, StickerType

if TYPE_CHECKING:
    from ..model import User


class Sticker(BaseModel):
    """Sticker Object

    see https://discord.com/developers/docs/resources/sticker#sticker-object
    """

    id: Snowflake
    pack_id: Missing[Snowflake] = UNSET
    name: str
    description: str | None = Field(...)
    tags: str
    asset: Missing[str] = UNSET
    """Deprecated. previously the sticker asset hash, now an empty string"""
    type: StickerType
    format_type: StickerFormatType
    available: Missing[bool] = UNSET
    guild_id: Missing[Snowflake] = UNSET
    user: Missing[User] = UNSET
    sort_value: Missing[int] = UNSET


class StickerItem(BaseModel):
    """Sticker item.

    see https://discord.com/developers/docs/resources/sticker#sticker-item-object
    """

    id: Snowflake
    name: str
    format_type: StickerFormatType


class StickerPack(BaseModel):
    """Sticker pack.

    see https://discord.com/developers/docs/resources/sticker#sticker-pack-object
    """

    id: Snowflake
    stickers: list[Sticker]
    name: str
    sku_id: Snowflake
    cover_sticker_id: Missing[Snowflake] = UNSET
    description: str
    banner_asset_id: Missing[Snowflake] = UNSET


class StickerPacksResponse(BaseModel):
    """List Nitro Sticker Packs Response.

    see https://discord.com/developers/docs/resources/sticker#list-sticker-packs
    """

    sticker_packs: list[StickerPack]
