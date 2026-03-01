from __future__ import annotations

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ...types import UNSET, LobbyMemberFlags, Missing, MissingOrNullable


class _LobbyMemberWriteParamsBase(BaseModel):
    metadata: Missing[dict[str, str]] = UNSET
    flags: Missing[LobbyMemberFlags] = UNSET


class CreateLobbyMemberParams(_LobbyMemberWriteParamsBase):
    id: Snowflake


class CreateLobbyParams(BaseModel):
    metadata: Missing[dict[str, str]] = UNSET
    members: Missing[list[CreateLobbyMemberParams]] = UNSET
    idle_timeout_seconds: Missing[int] = UNSET


class ModifyLobbyParams(BaseModel):
    metadata: MissingOrNullable[dict[str, str]] = UNSET
    idle_timeout_seconds: Missing[int] = UNSET


class AddLobbyMemberParams(_LobbyMemberWriteParamsBase):
    pass


class LinkChannelToLobbyParams(BaseModel):
    channel_id: MissingOrNullable[Snowflake] = UNSET


__all__ = [
    "AddLobbyMemberParams",
    "CreateLobbyMemberParams",
    "CreateLobbyParams",
    "LinkChannelToLobbyParams",
    "ModifyLobbyParams",
]
