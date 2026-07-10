"""Canonical soundboard.write models."""

from __future__ import annotations

from .._model_support import UNSET, BaseModel, Missing, MissingOrNullable, Snowflake


class SendSoundboardSoundParams(BaseModel):
    """Send Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#send-soundboard-sound
    """

    sound_id: Snowflake
    source_guild_id: Missing[Snowflake] = UNSET


class CreateGuildSoundboardSoundParams(BaseModel):
    """Create Guild Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#create-guild-soundboard-sound
    """

    name: str
    sound: str
    volume: Missing[float] = UNSET
    emoji_id: Missing[Snowflake] = UNSET
    emoji_name: Missing[str] = UNSET


class ModifyGuildSoundboardSoundParams(BaseModel):
    """Modify Guild Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#modify-guild-soundboard-sound
    """

    name: Missing[str] = UNSET
    volume: Missing[float] = UNSET
    emoji_id: MissingOrNullable[Snowflake] = UNSET
    emoji_name: MissingOrNullable[str] = UNSET


__all__ = [
    "CreateGuildSoundboardSoundParams",
    "ModifyGuildSoundboardSoundParams",
    "SendSoundboardSoundParams",
]
