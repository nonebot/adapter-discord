"""Canonical emoji.write models."""

from typing_extensions import Required

from .._model_support import OutboundTypedDict, Snowflake
from ...protocol import SnowflakeType


class ModifyGuildEmojiParams(OutboundTypedDict, total=False):
    """Modify Guild Emoji Params.

    see https://discord.com/developers/docs/resources/emoji#modify-guild-emoji
    """

    name: str
    roles: list[Snowflake] | None


class CreateGuildEmojiParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_create_guild_emoji``."""

    name: Required[str]
    image: Required[str]
    roles: "list[SnowflakeType]"


class CreateApplicationEmojiParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_create_application_emoji``."""

    name: Required[str]
    image: Required[str]


class ModifyApplicationEmojiParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_modify_application_emoji``."""

    name: Required[str]


__all__ = [
    "CreateApplicationEmojiParams",
    "CreateGuildEmojiParams",
    "ModifyApplicationEmojiParams",
    "ModifyGuildEmojiParams",
]
