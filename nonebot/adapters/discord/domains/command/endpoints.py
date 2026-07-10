from typing import TYPE_CHECKING

from nonebot.compat import type_validate_python

from .read import (
    ApplicationCommand,
    ApplicationCommandOption,
    ApplicationCommandPermissions,
    GuildApplicationCommandPermissions,
)
from .types import ApplicationCommandType
from .write import (
    ApplicationCommandBulkOverwriteParams,
    ApplicationCommandCreate,
    ApplicationCommandEditParams,
)
from ..application.types import ApplicationIntegrationType
from ..interaction.types import InteractionContextType
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


def _normalize_command_description(
    *,
    command_type: ApplicationCommandType | None,
    description: str | None,
) -> str:
    resolved_type = command_type or ApplicationCommandType.CHAT_INPUT
    if resolved_type in (ApplicationCommandType.USER, ApplicationCommandType.MESSAGE):
        if description not in (None, ""):
            msg = "description must be empty for USER or MESSAGE commands"
            raise ValueError(msg)
        return ""
    if description is None or description == "":
        msg = "description is required for CHAT_INPUT commands"
        raise ValueError(msg)
    return description


def _build_command_payloads(
    commands: list[ApplicationCommandBulkOverwriteParams],
) -> list[ApplicationCommandBulkOverwriteParams]:
    payloads: list[ApplicationCommandBulkOverwriteParams] = []
    for command in commands:
        command_model = type_validate_python(
            ApplicationCommandBulkOverwriteParams, command
        )
        description = _normalize_command_description(
            command_type=command_model.type,
            description=command_model.description,
        )
        payloads.append(command_model.copy(update={"description": description}))
    return payloads


class CommandEndpointMixin:
    async def _api_get_global_application_commands(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        with_localizations: bool | None = None,
    ) -> list[ApplicationCommand]:
        """Get global application commands.

        see https://discord.com/developers/docs/interactions/application-commands#get-global-application-commands
        """

        params = {"with_localizations": _bool_query(value=with_localizations)}
        call = RestCall(
            method="GET",
            url=self.base_url / f"applications/{application_id}/commands",
            response=JsonResponse(list[ApplicationCommand]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_global_application_command(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        name: str,
        name_localizations: dict[str, str] | None = None,
        description: str | None = None,
        description_localizations: dict[str, str] | None = None,
        options: list[ApplicationCommandOption] | None = None,
        default_member_permissions: str | None = None,
        dm_permission: bool | None = None,
        default_permission: bool | None = None,
        type: ApplicationCommandType | None = None,  # noqa: A002
        nsfw: bool | None = None,
        integration_types: list[ApplicationIntegrationType] | None = None,
        contexts: list[InteractionContextType] | None = None,
    ) -> ApplicationCommand:
        """Create global application command.

        see https://discord.com/developers/docs/interactions/application-commands#create-global-application-command
        """

        description = _normalize_command_description(
            command_type=type,
            description=description,
        )
        data = {
            "name": name,
            "name_localizations": name_localizations,
            "description": description,
            "description_localizations": description_localizations,
            "options": options,
            "default_member_permissions": default_member_permissions,
            "dm_permission": dm_permission,
            "default_permission": default_permission,
            "type": type,
            "nsfw": nsfw,
            "integration_types": integration_types,
            "contexts": contexts,
        }
        data = {key: value for key, value in data.items() if value is not None}
        payload = type_validate_python(ApplicationCommandCreate, data)
        call = RestCall(
            method="POST",
            url=self.base_url / f"applications/{application_id}/commands",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload, omit_unset_values=True, exclude_none=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_global_application_command(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> ApplicationCommand:
        """Get global application command.

        see https://discord.com/developers/docs/interactions/application-commands#get-global-application-command
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_edit_global_application_command(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
        name: Missing[str] = UNSET,
        name_localizations: MissingOrNullable[dict[str, str]] = UNSET,
        description: Missing[str] = UNSET,
        description_localizations: MissingOrNullable[dict[str, str]] = UNSET,
        options: Missing[list[ApplicationCommandOption]] = UNSET,
        default_member_permissions: MissingOrNullable[str] = UNSET,
        dm_permission: Missing[bool] = UNSET,
        default_permission: MissingOrNullable[bool] = UNSET,
        nsfw: Missing[bool] = UNSET,
        integration_types: Missing[list[ApplicationIntegrationType]] = UNSET,
        contexts: MissingOrNullable[list[InteractionContextType]] = UNSET,
    ) -> ApplicationCommand:
        """Edit global application command.

        see https://discord.com/developers/docs/interactions/application-commands#edit-global-application-command
        """

        data = {
            "name": name,
            "name_localizations": name_localizations,
            "description": description,
            "description_localizations": description_localizations,
            "options": options,
            "default_member_permissions": default_member_permissions,
            "dm_permission": dm_permission,
            "default_permission": default_permission,
            "nsfw": nsfw,
            "integration_types": integration_types,
            "contexts": contexts,
        }
        data = type_validate_python(ApplicationCommandEditParams, data)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_global_application_command(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> None:
        """Delete global application command.

        see https://discord.com/developers/docs/interactions/application-commands#delete-global-application-command
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_bulk_overwrite_global_application_commands(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        commands: list[ApplicationCommandBulkOverwriteParams],
    ) -> list[ApplicationCommand]:
        """Bulk overwrite global application commands.

        see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-global-application-commands
        """

        payload = _build_command_payloads(commands)
        call = RestCall(
            method="PUT",
            url=self.base_url / f"applications/{application_id}/commands",
            response=JsonResponse(list[ApplicationCommand]),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(payload),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_application_commands(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        with_localizations: bool | None = None,
    ) -> list[ApplicationCommand]:
        """Get guild application commands.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-commands
        """

        params = {"with_localizations": _bool_query(value=with_localizations)}
        call = RestCall(
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            response=JsonResponse(list[ApplicationCommand]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_guild_application_command(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        name: str,
        name_localizations: dict[str, str] | None = None,
        description: str | None = None,
        description_localizations: dict[str, str] | None = None,
        options: list[ApplicationCommandOption] | None = None,
        default_member_permissions: str | None = None,
        default_permission: bool | None = None,
        type: ApplicationCommandType | None = None,  # noqa: A002
        nsfw: bool | None = None,
    ) -> ApplicationCommand:
        """Create guild application command.

        see https://discord.com/developers/docs/interactions/application-commands#create-guild-application-command
        """

        description = _normalize_command_description(
            command_type=type,
            description=description,
        )
        data = {
            "name": name,
            "name_localizations": name_localizations,
            "description": description,
            "description_localizations": description_localizations,
            "options": options,
            "default_member_permissions": default_member_permissions,
            "default_permission": default_permission,
            "type": type,
            "nsfw": nsfw,
        }
        data = {key: value for key, value in data.items() if value is not None}
        payload = type_validate_python(ApplicationCommandCreate, data)
        call = RestCall(
            method="POST",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload, omit_unset_values=True, exclude_none=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_application_command(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> ApplicationCommand:
        """Get guild application command.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-command
        """

        call = RestCall(
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_edit_guild_application_command(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        name: Missing[str] = UNSET,
        name_localizations: MissingOrNullable[dict[str, str]] = UNSET,
        description: Missing[str] = UNSET,
        description_localizations: MissingOrNullable[dict[str, str]] = UNSET,
        options: Missing[list[ApplicationCommandOption]] = UNSET,
        default_member_permissions: MissingOrNullable[str] = UNSET,
        default_permission: MissingOrNullable[bool] = UNSET,
        nsfw: Missing[bool] = UNSET,
    ) -> ApplicationCommand:
        """Edit guild application command.

        see https://discord.com/developers/docs/interactions/application-commands#edit-guild-application-command
        """

        data = {
            "name": name,
            "name_localizations": name_localizations,
            "description": description,
            "description_localizations": description_localizations,
            "options": options,
            "default_member_permissions": default_member_permissions,
            "default_permission": default_permission,
            "nsfw": nsfw,
        }
        data = type_validate_python(ApplicationCommandEditParams, data)
        call = RestCall(
            method="PATCH",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_guild_application_command(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> None:
        """Delete guild application command.

        see https://discord.com/developers/docs/interactions/application-commands#delete-guild-application-command
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_bulk_overwrite_guild_application_commands(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        commands: list[ApplicationCommandBulkOverwriteParams],
    ) -> list[ApplicationCommand]:
        """Bulk overwrite guild application commands.

        see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-guild-application-commands
        """

        payload = _build_command_payloads(commands)
        call = RestCall(
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            response=JsonResponse(list[ApplicationCommand]),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(payload),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_application_command_permissions(
        self: "AdapterProtocol",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        access_token: str,
    ) -> list[GuildApplicationCommandPermissions]:
        """Get guild application command permissions.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-command-permissions
        """

        call = RestCall(
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/permissions",
            response=JsonResponse(list[GuildApplicationCommandPermissions]),
            auth=BearerAuth(access_token),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_application_command_permissions(
        self: "AdapterProtocol",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        access_token: str,
    ) -> GuildApplicationCommandPermissions:
        """Get application command permissions.

        see https://discord.com/developers/docs/interactions/application-commands#get-application-command-permissions
        """

        call = RestCall(
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
            response=JsonResponse(GuildApplicationCommandPermissions),
            auth=BearerAuth(access_token),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_edit_application_command_permissions(
        self: "AdapterProtocol",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        access_token: str,
        permissions: list[ApplicationCommandPermissions],
    ) -> GuildApplicationCommandPermissions:
        """Edit application command permissions.

        see https://discord.com/developers/docs/interactions/application-commands#edit-application-command-permissions
        """

        call = RestCall(
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
            response=JsonResponse(GuildApplicationCommandPermissions),
            auth=BearerAuth(access_token),
            body=JsonValueBody({"permissions": permissions}),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["CommandEndpointMixin"]
