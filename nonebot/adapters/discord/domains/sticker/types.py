from __future__ import annotations

from enum import IntEnum


class StickerFormatType(IntEnum):
    """Sticker format type.

    see https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-format-types
    """

    PNG = 1
    APNG = 2
    LOTTIE = 3
    GIF = 4


class StickerType(IntEnum):
    """Sticker type.

    see https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-types
    """

    STANDARD = 1
    """an official sticker in a pack, part of Nitro or in a removed purchasable pack"""
    GUILD = 2
    """a sticker uploaded to a guild for the guild's members"""


__all__ = ["StickerFormatType", "StickerType"]
