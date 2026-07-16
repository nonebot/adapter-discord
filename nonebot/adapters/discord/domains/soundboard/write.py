"""Canonical soundboard.write models."""

from typing_extensions import Required

from .._model_support import OutboundTypedDict, Snowflake


class SendSoundboardSoundParams(OutboundTypedDict, total=False):
    """Send Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#send-soundboard-sound
    """

    sound_id: Required[Snowflake]
    source_guild_id: Snowflake


class CreateGuildSoundboardSoundParams(OutboundTypedDict, total=False):
    """Create Guild Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#create-guild-soundboard-sound
    """

    name: Required[str]
    sound: Required[str]
    volume: float
    emoji_id: Snowflake
    emoji_name: str


class ModifyGuildSoundboardSoundParams(OutboundTypedDict, total=False):
    """Modify Guild Soundboard Sound Params.

    see https://discord.com/developers/docs/resources/soundboard#modify-guild-soundboard-sound
    """

    name: str
    volume: float
    emoji_id: Snowflake | None
    emoji_name: str | None


__all__ = [
    "CreateGuildSoundboardSoundParams",
    "ModifyGuildSoundboardSoundParams",
    "SendSoundboardSoundParams",
]
