from __future__ import annotations

from pydantic import BaseModel

from ...types import UNSET, Missing, MissingOrNullable


class ModifyGuildStickerParams(BaseModel):
    name: Missing[str] = UNSET
    description: MissingOrNullable[str] = UNSET
    tags: Missing[str] = UNSET


__all__ = ["ModifyGuildStickerParams"]
