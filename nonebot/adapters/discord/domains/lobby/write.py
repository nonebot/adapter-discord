"""Canonical lobby.write models."""

from __future__ import annotations

from .._model_support import (
    UNSET,
    BaseModel,
    LobbyMemberFlags,
    Missing,
    MissingOrNullable,
    Snowflake,
)


class _LobbyMemberWriteParamsBase(BaseModel):
    metadata: Missing[dict[str, str]] = UNSET
    flags: Missing[LobbyMemberFlags] = UNSET


class CreateLobbyMemberParams(_LobbyMemberWriteParamsBase):
    """Create Lobby Member Params.

    see https://discord.com/developers/docs/resources/lobby#create-lobby
    """

    id: Snowflake


class CreateLobbyParams(BaseModel):
    """Create Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#create-lobby
    """

    metadata: Missing[dict[str, str]] = UNSET
    members: Missing[list[CreateLobbyMemberParams]] = UNSET
    idle_timeout_seconds: Missing[int] = UNSET


class ModifyLobbyParams(BaseModel):
    """Modify Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#modify-lobby
    """

    metadata: MissingOrNullable[dict[str, str]] = UNSET
    idle_timeout_seconds: Missing[int] = UNSET


class AddLobbyMemberParams(_LobbyMemberWriteParamsBase):
    """Add Lobby Member Params.

    see https://discord.com/developers/docs/resources/lobby#add-lobby-member
    """


class LinkChannelToLobbyParams(BaseModel):
    """Link Channel to Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#link-channel-to-lobby
    """

    channel_id: MissingOrNullable[Snowflake] = UNSET


__all__ = [
    "AddLobbyMemberParams",
    "CreateLobbyMemberParams",
    "CreateLobbyParams",
    "LinkChannelToLobbyParams",
    "ModifyLobbyParams",
    "_LobbyMemberWriteParamsBase",
]
