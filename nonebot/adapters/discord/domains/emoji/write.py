"""Canonical emoji.write models."""

from typing_extensions import Required, TypedDict

from .._model_support import Snowflake
from ...protocol import SnowflakeType


class ModifyGuildEmojiParams(TypedDict, total=False):
    """Modify Guild Emoji Params.

    see https://discord.com/developers/docs/resources/emoji#modify-guild-emoji
    """

    name: str
    roles: list[Snowflake] | None


class CreateGuildEmojiParams(TypedDict, total=False):
    """Parameters for ``_api_create_guild_emoji``."""

    name: Required[str]
    image: Required[str]
    roles: "list[SnowflakeType]"


class CreateApplicationEmojiParams(TypedDict, total=False):
    """Parameters for ``_api_create_application_emoji``."""

    name: Required[str]
    image: Required[str]


class ModifyApplicationEmojiParams(TypedDict, total=False):
    """Parameters for ``_api_modify_application_emoji``."""

    name: Required[str]


__all__ = [
    "CreateApplicationEmojiParams",
    "CreateGuildEmojiParams",
    "ModifyApplicationEmojiParams",
    "ModifyGuildEmojiParams",
]
