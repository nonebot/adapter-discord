from typing import TYPE_CHECKING
from typing_extensions import Unpack

from .read import Lobby, LobbyMember
from .write import (
    AddLobbyMemberParams,
    CreateLobbyParams,
    LinkChannelToLobbyParams,
    ModifyLobbyParams,
)
from ...api.validation import validate_outbound_value
from ...protocol import SnowflakeType
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
        **fields: Unpack[CreateLobbyParams],
    ) -> Lobby:
        """Create lobby.

        see https://discord.com/developers/docs/resources/lobby#create-lobby
        """
        fields = validate_outbound_value(CreateLobbyParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / "lobbies",
            response=JsonResponse(Lobby),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
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
        **fields: Unpack[ModifyLobbyParams],
    ) -> Lobby:
        """Modify lobby.

        see https://discord.com/developers/docs/resources/lobby#modify-lobby
        """
        fields = validate_outbound_value(ModifyLobbyParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"lobbies/{lobby_id}",
            response=JsonResponse(Lobby),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
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
        **fields: Unpack[AddLobbyMemberParams],
    ) -> LobbyMember:
        """Add lobby member.

        see https://discord.com/developers/docs/resources/lobby#add-lobby-member
        """

        fields = validate_outbound_value(AddLobbyMemberParams, fields)
        call = RestCall(
            method="PUT",
            url=self.base_url / f"lobbies/{lobby_id}/members/{user_id}",
            response=JsonResponse(LobbyMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
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
        **fields: Unpack[LinkChannelToLobbyParams],
    ) -> Lobby:
        """Link channel to lobby.

        see https://discord.com/developers/docs/resources/lobby#link-channel-to-lobby
        """
        fields = validate_outbound_value(LinkChannelToLobbyParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"lobbies/{lobby_id}/channel-linking",
            response=JsonResponse(Lobby),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["LobbyEndpointMixin"]
