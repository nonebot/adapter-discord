from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from ..common.snowflake import Snowflake
from ...types import UNSET, Missing, MissingOrNullable

if TYPE_CHECKING:
    from ..common.user import User


class SoundboardSound(BaseModel):
    """Soundboard Sound Object

    see https://discord.com/developers/docs/resources/soundboard#soundboard-sound-object
    """

    name: str
    sound_id: Snowflake
    volume: float
    emoji_id: Snowflake | None = Field(...)
    emoji_name: str | None = Field(...)
    guild_id: Missing[Snowflake] = UNSET
    available: bool
    user: Missing[User] = UNSET


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


class _SoundboardSoundsListResponse(BaseModel):
    items: list[SoundboardSound]


class ListGuildSoundboardSoundsResponse(_SoundboardSoundsListResponse):
    """List Guild Soundboard Sounds Response.

    see https://discord.com/developers/docs/resources/soundboard#list-guild-soundboard-sounds
    """


class ListDefaultSoundboardSoundsResponse(_SoundboardSoundsListResponse):
    """List Default Soundboard Sounds Response.

    see https://discord.com/developers/docs/resources/soundboard#list-default-soundboard-sounds
    """
