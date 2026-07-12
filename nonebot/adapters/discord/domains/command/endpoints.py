from typing import TYPE_CHECKING
from typing_extensions import Unpack

from .read import (
    ApplicationCommand,
    GuildApplicationCommandPermissions,
)
from .types import ApplicationCommandType
from .write import (
    ApplicationCommandBulkOverwriteParams,
    ApplicationCommandCreate,
    ApplicationCommandEditParams,
    EditApplicationCommandPermissionsParams,
)
from ...api.validation import validate_outbound_value
from ...protocol import UNSET, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BearerAuth,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
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
        payload = ApplicationCommandBulkOverwriteParams(
            **validate_outbound_value(ApplicationCommandBulkOverwriteParams, command)
        )
        payload.setdefault("type", ApplicationCommandType.CHAT_INPUT)
        payload["description"] = _normalize_command_description(
            command_type=payload.get("type", ApplicationCommandType.CHAT_INPUT),
            description=payload.get("description"),
        )
        payloads.append(payload)
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

    async def _api_create_global_application_command(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        **fields: Unpack[ApplicationCommandCreate],
    ) -> ApplicationCommand:
        """Create global application command.

        see https://discord.com/developers/docs/interactions/application-commands#create-global-application-command
        """
        fields = validate_outbound_value(ApplicationCommandCreate, fields)
        name = fields["name"]
        name_localizations = fields.get("name_localizations")
        description = fields.get("description")
        description_localizations = fields.get("description_localizations")
        options = fields.get("options")
        default_member_permissions = fields.get("default_member_permissions")
        dm_permission = fields.get("dm_permission")
        default_permission = fields.get("default_permission")
        integration_types = fields.get("integration_types")
        contexts = fields.get("contexts")
        command_type = fields.get("type")
        nsfw = fields.get("nsfw")

        description = _normalize_command_description(
            command_type=command_type,
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
            "type": command_type,
            "nsfw": nsfw,
            "integration_types": integration_types,
            "contexts": contexts,
        }
        data = {key: value for key, value in data.items() if value is not None}
        payload = validate_outbound_value(
            ApplicationCommandCreate,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"applications/{application_id}/commands",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload),
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

    async def _api_edit_global_application_command(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
        **fields: Unpack[ApplicationCommandEditParams],
    ) -> ApplicationCommand:
        """Edit global application command.

        see https://discord.com/developers/docs/interactions/application-commands#edit-global-application-command
        """
        fields = validate_outbound_value(ApplicationCommandEditParams, fields)
        name = fields.get("name", UNSET)
        name_localizations = fields.get("name_localizations", UNSET)
        description = fields.get("description", UNSET)
        description_localizations = fields.get("description_localizations", UNSET)
        options = fields.get("options", UNSET)
        default_member_permissions = fields.get("default_member_permissions", UNSET)
        dm_permission = fields.get("dm_permission", UNSET)
        default_permission = fields.get("default_permission", UNSET)
        nsfw = fields.get("nsfw", UNSET)
        integration_types = fields.get("integration_types", UNSET)
        contexts = fields.get("contexts", UNSET)

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
        data = validate_outbound_value(
            ApplicationCommandEditParams,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
            body=JsonBody(payload),
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

    async def _api_create_guild_application_command(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        **fields: Unpack[ApplicationCommandCreate],
    ) -> ApplicationCommand:
        """Create guild application command.

        see https://discord.com/developers/docs/interactions/application-commands#create-guild-application-command
        """
        fields = validate_outbound_value(ApplicationCommandCreate, fields)
        name = fields["name"]
        name_localizations = fields.get("name_localizations")
        description = fields.get("description")
        description_localizations = fields.get("description_localizations")
        options = fields.get("options")
        default_member_permissions = fields.get("default_member_permissions")
        default_permission = fields.get("default_permission")
        command_type = fields.get("type")
        nsfw = fields.get("nsfw")

        description = _normalize_command_description(
            command_type=command_type,
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
            "type": command_type,
            "nsfw": nsfw,
        }
        data = {key: value for key, value in data.items() if value is not None}
        payload = validate_outbound_value(
            ApplicationCommandCreate,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="POST",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload),
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

    async def _api_edit_guild_application_command(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        **fields: Unpack[ApplicationCommandEditParams],
    ) -> ApplicationCommand:
        """Edit guild application command.

        see https://discord.com/developers/docs/interactions/application-commands#edit-guild-application-command
        """
        fields = validate_outbound_value(ApplicationCommandEditParams, fields)
        name = fields.get("name", UNSET)
        name_localizations = fields.get("name_localizations", UNSET)
        description = fields.get("description", UNSET)
        description_localizations = fields.get("description_localizations", UNSET)
        options = fields.get("options", UNSET)
        default_member_permissions = fields.get("default_member_permissions", UNSET)
        default_permission = fields.get("default_permission", UNSET)
        nsfw = fields.get("nsfw", UNSET)

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
        data = validate_outbound_value(
            ApplicationCommandEditParams,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            response=JsonResponse(ApplicationCommand),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
            body=JsonBody(payload),
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
        **fields: Unpack[EditApplicationCommandPermissionsParams],
    ) -> GuildApplicationCommandPermissions:
        """Edit application command permissions.

        see https://discord.com/developers/docs/interactions/application-commands#edit-application-command-permissions
        """
        fields = validate_outbound_value(
            EditApplicationCommandPermissionsParams, fields
        )
        permissions = fields["permissions"]

        call = RestCall(
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
            response=JsonResponse(GuildApplicationCommandPermissions),
            auth=BearerAuth(access_token),
            body=JsonBody({"permissions": permissions}),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["CommandEndpointMixin"]
