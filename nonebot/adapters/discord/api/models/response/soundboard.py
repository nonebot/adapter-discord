from __future__ import annotations

from pydantic import BaseModel

from ..common import SoundboardSound


class _SoundboardSoundsListResponse(BaseModel):
    items: list[SoundboardSound]


class ListGuildSoundboardSoundsResponse(_SoundboardSoundsListResponse):
    pass


class ListDefaultSoundboardSoundsResponse(_SoundboardSoundsListResponse):
    pass


__all__ = [
    "ListDefaultSoundboardSoundsResponse",
    "ListGuildSoundboardSoundsResponse",
]
