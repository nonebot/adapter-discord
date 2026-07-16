from typing import TYPE_CHECKING

from nonebot.compat import type_validate_python

from .read import Connection, User
from .write import ModifyCurrentUserParams
from ..application.read import ApplicationRoleConnection
from ..channel.read import Channel
from ..guild.read import CurrentUserGuild, GuildMember
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BearerAuth,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    JsonValueBody,
    RestCall,
    _bool_query,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class UserEndpointMixin:
    async def _api_get_current_user(self: "AdapterProtocol", bot: "Bot") -> User:
        """Get current user.

        see https://discord.com/developers/docs/resources/user#get-current-user
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "users/@me",
            response=JsonResponse(User),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_user(
        self: "AdapterProtocol", bot: "Bot", *, user_id: SnowflakeType
    ) -> User:
        """Get user.

        see https://discord.com/developers/docs/resources/user#get-user
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"users/{user_id}",
            response=JsonResponse(User),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_current_user(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        username: Missing[str] = UNSET,
        avatar: MissingOrNullable[str] = UNSET,
        banner: MissingOrNullable[str] = UNSET,
    ) -> User:
        """Modify current user.

        see https://discord.com/developers/docs/resources/user#modify-current-user
        """

        data = type_validate_python(
            ModifyCurrentUserParams,
            {"username": username, "avatar": avatar, "banner": banner},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / "users/@me",
            response=JsonResponse(User),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_current_user_guilds(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: int | None = None,
        with_counts: bool | None = None,
    ) -> list[CurrentUserGuild]:
        """Get current user guilds.

        see https://discord.com/developers/docs/resources/user#get-current-user-guilds
        """

        params = {
            "before": before,
            "after": after,
            "limit": limit,
            "with_counts": _bool_query(value=with_counts),
        }
        call = RestCall(
            method="GET",
            url=self.base_url / "users/@me/guilds",
            response=JsonResponse(list[CurrentUserGuild]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_current_user_guild_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
    ) -> GuildMember:
        """Get current user guild member.

        see https://discord.com/developers/docs/resources/user#get-current-user-guild-member
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"users/@me/guilds/{guild_id}/member",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_leave_guild(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> None:
        """Leave guild.

        see https://discord.com/developers/docs/resources/user#leave-guild
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"users/@me/guilds/{guild_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_create_DM(  # noqa: N802
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        recipient_id: SnowflakeType,
    ) -> Channel:
        """Create DM.

        see https://discord.com/developers/docs/resources/user#create-dm
        """

        call = RestCall(
            method="POST",
            url=self.base_url / "users/@me/channels",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody({"recipient_id": recipient_id}),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_group_DM(  # noqa: N802
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        access_tokens: list[str],
        nicks: dict[SnowflakeType, str],
    ) -> Channel:
        """Create group DM.

        see https://discord.com/developers/docs/resources/user#create-group-dm
        """

        data = {"access_tokens": access_tokens, "nicks": nicks}
        call = RestCall(
            method="POST",
            url=self.base_url / "users/@me/channels",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(data),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_user_connections(
        self: "AdapterProtocol",
        *,
        access_token: str,
    ) -> list[Connection]:
        """Get current user connections.

        see https://discord.com/developers/docs/resources/user#get-current-user-connections
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "users/@me/connections",
            response=JsonResponse(list[Connection]),
            auth=BearerAuth(access_token),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_user_application_role_connection(
        self: "AdapterProtocol",
        *,
        application_id: SnowflakeType,
        access_token: str,
    ) -> ApplicationRoleConnection:
        """Get current user application role connection.

        see https://discord.com/developers/docs/resources/user#get-current-user-application-role-connection
        """

        call = RestCall(
            method="GET",
            url=self.base_url
            / f"users/@me/applications/{application_id}/role-connection",
            response=JsonResponse(ApplicationRoleConnection),
            auth=BearerAuth(access_token),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_update_user_application_role_connection(
        self: "AdapterProtocol",
        *,
        application_id: SnowflakeType,
        access_token: str,
        platform_name: str | None = None,
        platform_username: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> ApplicationRoleConnection:
        """Update current user application role connection.

        see https://discord.com/developers/docs/resources/user#update-current-user-application-role-connection
        """
        data = {
            "platform_name": platform_name,
            "platform_username": platform_username,
            "metadata": metadata,
        }

        call = RestCall(
            method="PUT",
            url=self.base_url
            / f"users/@me/applications/{application_id}/role-connection",
            response=JsonResponse(ApplicationRoleConnection),
            auth=BearerAuth(access_token),
            body=JsonValueBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["UserEndpointMixin"]
