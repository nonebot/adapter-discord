from typing import TYPE_CHECKING

from nonebot.compat import type_validate_python

from .read import Lobby, LobbyMember
from .types import LobbyMemberFlags
from .write import (
    AddLobbyMemberParams,
    CreateLobbyMemberParams,
    CreateLobbyParams,
    LinkChannelToLobbyParams,
    ModifyLobbyParams,
)
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    RestCall,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class LobbyEndpointMixin:
    async def _api_create_lobby(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        metadata: Missing[dict[str, str]] = UNSET,
        members: Missing[list[CreateLobbyMemberParams]] = UNSET,
        idle_timeout_seconds: Missing[int] = UNSET,
    ) -> Lobby:
        """Create lobby.

        see https://discord.com/developers/docs/resources/lobby#create-lobby
        """

        data = type_validate_python(
            CreateLobbyParams,
            {
                "metadata": metadata,
                "members": members,
                "idle_timeout_seconds": idle_timeout_seconds,
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / "lobbies",
            response=JsonResponse(Lobby),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_lobby(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
    ) -> Lobby:
        """Get lobby.

        see https://discord.com/developers/docs/resources/lobby#get-lobby
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"lobbies/{lobby_id}",
            response=JsonResponse(Lobby),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_lobby(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
        metadata: MissingOrNullable[dict[str, str]] = UNSET,
        idle_timeout_seconds: Missing[int] = UNSET,
    ) -> Lobby:
        """Modify lobby.

        see https://discord.com/developers/docs/resources/lobby#modify-lobby
        """

        data = type_validate_python(
            ModifyLobbyParams,
            {"metadata": metadata, "idle_timeout_seconds": idle_timeout_seconds},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"lobbies/{lobby_id}",
            response=JsonResponse(Lobby),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_lobby(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
    ) -> None:
        """Delete lobby.

        see https://discord.com/developers/docs/resources/lobby#delete-lobby
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"lobbies/{lobby_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_add_lobby_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
        user_id: SnowflakeType,
        metadata: Missing[dict[str, str]] = UNSET,
        flags: Missing[LobbyMemberFlags] = UNSET,
    ) -> LobbyMember:
        """Add lobby member.

        see https://discord.com/developers/docs/resources/lobby#add-lobby-member
        """

        data = type_validate_python(
            AddLobbyMemberParams, {"metadata": metadata, "flags": flags}
        )
        call = RestCall(
            method="PUT",
            url=self.base_url / f"lobbies/{lobby_id}/members/{user_id}",
            response=JsonResponse(LobbyMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_remove_lobby_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """Remove lobby member.

        see https://discord.com/developers/docs/resources/lobby#remove-lobby-member
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"lobbies/{lobby_id}/members/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_leave_lobby(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
    ) -> None:
        """Leave lobby.

        see https://discord.com/developers/docs/resources/lobby#leave-lobby
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"lobbies/{lobby_id}/members/@me",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_link_channel_to_lobby(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
        channel_id: MissingOrNullable[SnowflakeType] = UNSET,
    ) -> Lobby:
        """Link channel to lobby.

        see https://discord.com/developers/docs/resources/lobby#link-channel-to-lobby
        """

        data = type_validate_python(
            LinkChannelToLobbyParams, {"channel_id": channel_id}
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"lobbies/{lobby_id}/channel-linking",
            response=JsonResponse(Lobby),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["LobbyEndpointMixin"]
