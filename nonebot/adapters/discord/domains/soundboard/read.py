"""Canonical soundboard.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import User

from .._model_support import UNSET, BaseModel, Field, Missing, Snowflake


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


__all__ = [
    "ListDefaultSoundboardSoundsResponse",
    "ListGuildSoundboardSoundsResponse",
    "SoundboardSound",
    "_SoundboardSoundsListResponse",
]
