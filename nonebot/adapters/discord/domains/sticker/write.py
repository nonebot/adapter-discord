"""Canonical sticker.write models."""

from .._model_support import UNSET, BaseModel, Missing, MissingOrNullable


class ModifyGuildStickerParams(BaseModel):
    """Modify Guild Sticker Params.

    see https://discord.com/developers/docs/resources/sticker#modify-guild-sticker
    """

    name: Missing[str] = UNSET
    description: MissingOrNullable[str] = UNSET
    tags: Missing[str] = UNSET


__all__ = ["ModifyGuildStickerParams"]
