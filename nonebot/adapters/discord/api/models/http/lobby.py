from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from ..common.snowflake import Snowflake
from ...types import UNSET, LobbyMemberFlags, Missing, MissingOrNullable

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
