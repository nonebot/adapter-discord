"""Canonical emoji.write models."""

from .._model_support import UNSET, BaseModel, Missing, MissingOrNullable, Snowflake


class ModifyGuildEmojiParams(BaseModel):
    """Modify Guild Emoji Params.

    see https://discord.com/developers/docs/resources/emoji#modify-guild-emoji
    """

    name: Missing[str] = UNSET
    roles: MissingOrNullable[list[Snowflake]] = UNSET


__all__ = ["ModifyGuildEmojiParams"]
