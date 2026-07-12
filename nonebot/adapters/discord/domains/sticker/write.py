"""Canonical sticker.write models."""

from typing_extensions import TypedDict


class ModifyGuildStickerParams(TypedDict, total=False):
    """Modify Guild Sticker Params.

    see https://discord.com/developers/docs/resources/sticker#modify-guild-sticker
    """

    name: str
    description: str | None
    tags: str


__all__ = ["ModifyGuildStickerParams"]
