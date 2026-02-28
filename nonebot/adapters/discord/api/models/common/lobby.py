from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ...types import UNSET, LobbyMemberFlags, Missing

if TYPE_CHECKING:
    from .channels import Channel


class LobbyMember(BaseModel):
    id: Snowflake
    metadata: dict[str, str] | None = Field(...)
    flags: Missing[LobbyMemberFlags] = UNSET


class Lobby(BaseModel):
    id: Snowflake
    application_id: Snowflake
    metadata: dict[str, str] | None = Field(...)
    members: list[LobbyMember]
    linked_channel: Missing[Channel] = UNSET


__all__ = ["Lobby", "LobbyMember"]
