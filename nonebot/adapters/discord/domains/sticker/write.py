"""Canonical sticker.write models."""

from .._model_support import OutboundTypedDict


class ModifyGuildStickerParams(OutboundTypedDict, total=False):
    """Modify Guild Sticker Params.

    see https://discord.com/developers/docs/resources/sticker#modify-guild-sticker
    """

    name: str
    description: str | None
    tags: str


__all__ = ["ModifyGuildStickerParams"]
