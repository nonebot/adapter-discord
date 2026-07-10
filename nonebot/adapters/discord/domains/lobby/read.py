"""Canonical lobby.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Channel

from .._model_support import (
    UNSET,
    BaseModel,
    Field,
    LobbyMemberFlags,
    Missing,
    Snowflake,
)


class LobbyMember(BaseModel):
    """Lobby Member Object.

    see https://discord.com/developers/docs/resources/lobby#lobby-member-object
    """

    id: Snowflake
    metadata: dict[str, str] | None = Field(...)
    flags: Missing[LobbyMemberFlags] = UNSET


class Lobby(BaseModel):
    """Lobby Object.

    see https://discord.com/developers/docs/resources/lobby#lobby-object
    """

    id: Snowflake
    application_id: Snowflake
    metadata: dict[str, str] | None = Field(...)
    members: list[LobbyMember]
    linked_channel: Missing[Channel] = UNSET


__all__ = ["Lobby", "LobbyMember"]
