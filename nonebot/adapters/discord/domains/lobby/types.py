from __future__ import annotations

from enum import IntFlag


class LobbyMemberFlags(IntFlag):
    """Lobby Member Flags

    see https://discord.com/developers/docs/resources/lobby#lobby-member-object-lobby-member-flags
    """

    CAN_LINK_LOBBY = 1 << 0


__all__ = ["LobbyMemberFlags"]
