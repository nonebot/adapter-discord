"""Canonical lobby.write models."""

from typing_extensions import Required, TypedDict

from .._model_support import LobbyMemberFlags, Snowflake


class _LobbyMemberWriteParamsBase(TypedDict, total=False):
    metadata: dict[str, str]
    flags: LobbyMemberFlags


class CreateLobbyMemberParams(_LobbyMemberWriteParamsBase):
    """Create Lobby Member Params.

    see https://discord.com/developers/docs/resources/lobby#create-lobby
    """

    id: Required[Snowflake]


class CreateLobbyParams(TypedDict, total=False):
    """Create Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#create-lobby
    """

    metadata: dict[str, str]
    members: list[CreateLobbyMemberParams]
    idle_timeout_seconds: int


class ModifyLobbyParams(TypedDict, total=False):
    """Modify Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#modify-lobby
    """

    metadata: dict[str, str] | None
    idle_timeout_seconds: int


class AddLobbyMemberParams(_LobbyMemberWriteParamsBase):
    """Add Lobby Member Params.

    see https://discord.com/developers/docs/resources/lobby#add-lobby-member
    """


class LinkChannelToLobbyParams(TypedDict, total=False):
    """Link Channel to Lobby Params.

    see https://discord.com/developers/docs/resources/lobby#link-channel-to-lobby
    """

    channel_id: Snowflake | None


__all__ = [
    "AddLobbyMemberParams",
    "CreateLobbyMemberParams",
    "CreateLobbyParams",
    "LinkChannelToLobbyParams",
    "ModifyLobbyParams",
    "_LobbyMemberWriteParamsBase",
]
