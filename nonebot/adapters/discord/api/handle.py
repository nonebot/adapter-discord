from datetime import datetime
from http import HTTPStatus
import json
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Optional,
    Union,
)
from typing_extensions import Protocol
from urllib.parse import quote

from nonebot.compat import type_validate_python
from nonebot.drivers import Request, Response
from nonebot.utils import escape_tag
from yarl import URL

from .model import (
    SKU,
    ActivityInstance,
    AllowedMention,
    AnswerVoters,
    Application,
    ApplicationCommand,
    ApplicationCommandCreate,
    ApplicationCommandOption,
    ApplicationCommandPermissions,
    ApplicationEmojis,
    ApplicationIntegrationTypeConfiguration,
    ApplicationRoleConnection,
    ApplicationRoleConnectionMetadata,
    ArchivedThreadsResponse,
    AttachmentSend,
    AuditLog,
    AuthorizationResponse,
    AutoModerationAction,
    AutoModerationRule,
    Ban,
    BulkBan,
    Channel,
    Component,
    Connection,
    CreateAndModifyAutoModerationRuleParams,
    CreateGuildChannelParams,
    CreateGuildParams,
    CreateGuildScheduledEventParams,
    CurrentUserGuild,
    DefaultReaction,
    DirectComponent,
    Embed,
    Emoji,
    Entitlement,
    ExecuteWebhookParams,
    File,
    FollowedChannel,
    ForumTag,
    Gateway,
    GatewayBot,
    Guild,
    GuildApplicationCommandPermissions,
    GuildMember,
    GuildOnboarding,
    GuildPreview,
    GuildScheduledEvent,
    GuildScheduledEventEntityMetadata,
    GuildScheduledEventUser,
    GuildTemplate,
    GuildWidget,
    GuildWidgetSettings,
    InstallParams,
    Integration,
    InteractionResponse,
    Invite,
    ListActiveGuildThreadsResponse,
    MessageGet,
    MessageReference,
    MessageSend,
    ModifyChannelParams,
    ModifyGuildOnboardingParams,
    ModifyGuildParams,
    ModifyGuildScheduledEventParams,
    ModifyGuildWelcomeScreenParams,
    OnboardingPrompt,
    Overwrite,
    PollRequest,
    Role,
    Snowflake,
    SnowflakeType,
    StageInstance,
    Sticker,
    StickerPack,
    Subscription,
    ThreadMember,
    TriggerMetadata,
    User,
    VoiceRegion,
    VoiceState,
    Webhook,
    WelcomeScreen,
    WelcomeScreenChannel,
)
from .types import (
    ApplicationCommandType,
    ApplicationFlag,
    ApplicationIntegrationType,
    AuditLogEventType,
    AutoModerationRuleEventType,
    ChannelFlags,
    ChannelType,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    ForumLayoutTypes,
    GuildFeature,
    GuildMemberFlags,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventStatus,
    MessageFlag,
    OnboardingMode,
    OverwriteType,
    SortOrderTypes,
    StagePrivacyLevel,
    SystemChannelFlags,
    TriggerType,
    VerificationLevel,
    VideoQualityMode,
)
from .utils import parse_data, parse_forum_thread_message, parse_interaction_response
from ..config import BotInfo, Config
from ..exception import (
    ActionFailed,
    DiscordAdapterException,
    NetworkError,
    RateLimitException,
    UnauthorizedException,
)
from ..utils import decompress_data, log, model_dump

if TYPE_CHECKING:
    from ..bot import Bot


class AdapterProtocol(Protocol):
    base_url: URL
    discord_config: Config

    @staticmethod
    def get_authorization(bot_info: BotInfo) -> str: ...

    async def request(self, setup: Request) -> Response: ...


async def _request(adapter: "AdapterProtocol", bot: "Bot", request: Request) -> Any:  # noqa: ANN401, ARG001 # TODO)): 验证bot参数是否需要, 重构为泛型函数, 接管type_validate部分
    try:
        request.timeout = adapter.discord_config.discord_api_timeout
        request.proxy = adapter.discord_config.discord_proxy
        data = await adapter.request(request)
        log(
            "TRACE",
            f"API code: {data.status_code} response: {escape_tag(str(data.content))}",
        )
        if data.status_code in (200, 201, 204):
            return data.content and json.loads(
                decompress_data(
                    data.content, compress=adapter.discord_config.discord_compress
                )
            )
        if data.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
            raise UnauthorizedException(data)  # noqa: TRY301
        if data.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitException(data)  # noqa: TRY301
        raise ActionFailed(data)  # noqa: TRY301
    except DiscordAdapterException:
        raise
    except Exception as e:
        msg = "API request failed"
        raise NetworkError(msg) from e


class HandleMixin:
    # Application Commands

    # see https://discord.com/developers/docs/interactions/application-commands
    async def _api_get_global_application_commands(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        with_localizations: Optional[bool] = None,
    ) -> list[ApplicationCommand]:
        """Fetch global commands for your application.
        Returns an array of application command objects.

        see https://discord.com/developers/docs/interactions/application-commands#get-global-application-commands
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_localizations": with_localizations}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/commands",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[ApplicationCommand], await _request(self, bot, request)
        )

    async def _api_create_global_application_command(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        name: str,
        name_localizations: Optional[dict[str, str]] = None,
        description: Optional[str] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[ApplicationCommandOption]] = None,
        default_member_permissions: Optional[str] = None,
        dm_permission: Optional[bool] = None,
        default_permission: Optional[bool] = None,
        type: Optional[ApplicationCommandType] = None,  # noqa: A002
        nsfw: Optional[bool] = None,
    ) -> ApplicationCommand:
        """Create a new global command.
        Returns 201 if a command with the same name does not already exist,
        or a 200 if it does (in which case the previous command will be overwritten).
        Both responses include an application command object.

        see https://discord.com/developers/docs/interactions/application-commands#create-global-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
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
        }
        payload = model_dump(
            type_validate_python(ApplicationCommandCreate, data),
            exclude_unset=True,
            exclude_none=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"applications/{application_id}/commands",
            json=payload,
        )
        return type_validate_python(
            ApplicationCommand, await _request(self, bot, request)
        )

    async def _api_get_global_application_command(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> ApplicationCommand:
        """Fetch a global command for your application.
        Returns an application command object.

        see https://discord.com/developers/docs/interactions/application-commands#get-global-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
        )
        return type_validate_python(
            ApplicationCommand, await _request(self, bot, request)
        )

    async def _api_edit_global_application_command(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
        name: Optional[str] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description: Optional[str] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[ApplicationCommandOption]] = None,
        default_member_permissions: Optional[str] = None,
        dm_permission: Optional[bool] = None,
        default_permission: Optional[bool] = None,
        nsfw: Optional[bool] = None,
    ) -> ApplicationCommand:
        """Edit a global command. Returns 200 and an application command object.
        All fields are optional, but any fields provided will entirely overwrite
        the existing values of those fields.

        see https://discord.com/developers/docs/interactions/application-commands#edit-global-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
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
        }
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(
            ApplicationCommand, await _request(self, bot, request)
        )

    async def _api_delete_global_application_command(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> None:
        """Deletes a global command. Returns 204 No Content on success.

        see https://discord.com/developers/docs/interactions/application-commands#delete-global-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
        )
        await _request(self, bot, request)

    async def _api_bulk_overwrite_global_application_commands(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        commands: list[ApplicationCommandCreate],
    ) -> list[ApplicationCommand]:
        """Takes a list of application commands,
        overwriting the existing global command list for this application.
        Returns 200 and a list of application command objects.
        Commands that do not already exist will count toward
        daily application command create limits.

        see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-global-application-commands
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"applications/{application_id}/commands",
            json=[model_dump(command, exclude_unset=True) for command in commands],
        )
        return type_validate_python(
            list[ApplicationCommand], await _request(self, bot, request)
        )

    async def _api_get_guild_application_commands(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        with_localizations: Optional[bool] = None,
    ) -> list[ApplicationCommand]:
        """Fetch all of the guild commands for your application for a specific guild.
        Returns an array of application command objects.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-commands
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_localizations": with_localizations}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[ApplicationCommand], await _request(self, bot, request)
        )

    async def _api_create_guild_application_command(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        name: str,
        name_localizations: Optional[dict[str, str]] = None,
        description: Optional[str] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[ApplicationCommandOption]] = None,
        default_member_permissions: Optional[str] = None,
        default_permission: Optional[bool] = None,
        type: Optional[ApplicationCommandType] = None,  # noqa: A002
        nsfw: Optional[bool] = None,
    ) -> ApplicationCommand:
        """Create a new guild command.
        New guild commands will be available in the guild immediately.
        Returns 201 if a command with the same name does not already exist,
        or a 200 if it does (in which case the previous command will be overwritten).
        Both responses include an application command object.

        see https://discord.com/developers/docs/interactions/application-commands#create-guild-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
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
        payload = model_dump(
            type_validate_python(ApplicationCommandCreate, data),
            exclude_unset=True,
            exclude_none=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            json=payload,
        )
        return type_validate_python(
            ApplicationCommand, await _request(self, bot, request)
        )

    async def _api_get_guild_application_command(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> ApplicationCommand:
        """Fetch a guild command for your application.
        Returns an application command object.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
        )
        return type_validate_python(
            ApplicationCommand, await _request(self, bot, request)
        )

    async def _api_edit_guild_application_command(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        name: Optional[str] = None,
        name_localizations: Optional[dict[str, str]] = None,
        description: Optional[str] = None,
        description_localizations: Optional[dict[str, str]] = None,
        options: Optional[list[ApplicationCommandOption]] = None,
        default_member_permissions: Optional[str] = None,
        default_permission: Optional[bool] = None,
        nsfw: Optional[bool] = None,
    ) -> ApplicationCommand:
        """Edit a guild command.
        Updates for guild commands will be available immediately.
        Returns 200 and an application command object.
        All fields are optional,
        but any fields provided will entirely overwrite the existing values of those fields.

        see https://discord.com/developers/docs/interactions/application-commands#edit-guild-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
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
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(
            ApplicationCommand, await _request(self, bot, request)
        )

    async def _api_delete_guild_application_command(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> None:
        """Delete a guild command. Returns 204 No Content on success.

        see https://discord.com/developers/docs/interactions/application-commands#delete-guild-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
        )
        await _request(self, bot, request)

    async def _api_bulk_overwrite_guild_application_commands(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        commands: list[ApplicationCommandCreate],
    ) -> list[ApplicationCommand]:
        """Takes a list of application commands,
        overwriting the existing command list for this application for the targeted guild.
        Returns 200 and a list of application command objects.

        see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-guild-application-commands
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            json=[model_dump(command, exclude_unset=True) for command in commands],
        )
        return type_validate_python(
            list[ApplicationCommand], await _request(self, bot, request)
        )

    async def _api_get_guild_application_command_permissions(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
    ) -> list[GuildApplicationCommandPermissions]:
        """
        Fetches permissions for all commands for your application in a guild.
        Returns an array of guild application command permissions objects.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-command-permissions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/permissions",
        )
        return type_validate_python(
            list[GuildApplicationCommandPermissions],
            await _request(self, bot, request),
        )

    async def _api_get_application_command_permissions(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> GuildApplicationCommandPermissions:
        """
        Fetches permissions for a specific command for your application in a guild.
        Returns a guild application command permissions object.

        see https://discord.com/developers/docs/interactions/application-commands#get-application-command-permissions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
        )
        return type_validate_python(
            GuildApplicationCommandPermissions, await _request(self, bot, request)
        )

    async def _api_edit_application_command_permissions(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        permissions: list[ApplicationCommandPermissions],
    ) -> GuildApplicationCommandPermissions:
        """
        Edits command permissions for a specific command for your application in a guild
        and returns a guild application command permissions object.
        Fires an Application Command Permissions Update Gateway event.

        You can add up to 100 permission overwrites for a command.

        see https://discord.com/developers/docs/interactions/application-commands#edit-application-command-permissions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
            json={
                "permissions": [
                    model_dump(permission, exclude_unset=True)
                    for permission in permissions
                ]
            },
        )
        return type_validate_python(
            GuildApplicationCommandPermissions, await _request(self, bot, request)
        )

    # Receiving and Responding

    # see https://discord.com/developers/docs/interactions/receiving-and-responding
    async def _api_create_interaction_response(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        interaction_id: SnowflakeType,
        interaction_token: str,
        response: InteractionResponse,
    ) -> None:
        """https://discord.com/developers/docs/interactions/receiving-and-responding#create-interaction-response"""
        params = parse_interaction_response(response)
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url
            / f"interactions/{interaction_id}/{interaction_token}/callback",
            json=params.get("json"),
            files=params.get("files"),
        )
        await _request(self, bot, request)

    async def _api_get_origin_interaction_response(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: Optional[SnowflakeType] = None,
    ) -> MessageGet:
        """https://discord.com/developers/docs/interactions/receiving-and-responding#get-original-interaction-response"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/@original",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_edit_origin_interaction_response(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: Optional[SnowflakeType] = None,
        content: Optional[str] = None,
        embeds: Optional[list[Embed]] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        components: Optional[list[Component]] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[AttachmentSend]] = None,
    ) -> MessageGet:
        """https://discord.com/developers/docs/interactions/receiving-and-responding#edit-original-interaction-response"""
        params = {"thread_id": thread_id}
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "content": content,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
        }
        request_kwargs = parse_data(
            {key: value for key, value in data.items() if value is not None},
            ExecuteWebhookParams,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/@original",
            params={key: value for key, value in params.items() if value is not None},
            json=request_kwargs.get("json"),
            files=request_kwargs.get("files"),
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_delete_origin_interaction_response(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
    ) -> None:
        """https://discord.com/developers/docs/interactions/receiving-and-responding#delete-original-interaction-response"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/@original",
        )
        await _request(self, bot, request)

    async def _api_create_followup_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        content: Optional[str] = None,
        tts: Optional[bool] = None,
        embeds: Optional[list[Embed]] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        components: Optional[list[Component]] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[AttachmentSend]] = None,
        flags: Optional[int] = None,
        thread_name: Optional[str] = None,
    ) -> MessageGet:
        """https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message"""
        data = {
            "content": content,
            "tts": tts,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "flags": flags,
            "thread_name": thread_name,
        }
        request_kwargs = parse_data(
            {key: value for key, value in data.items() if value is not None},
            ExecuteWebhookParams,
        )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"webhooks/{application_id}/{interaction_token}",
            json=request_kwargs.get("json"),
            files=request_kwargs.get("files"),
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_get_followup_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """Returns a followup message for an Interaction. Functions the same as Get Webhook Message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#get-followup-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_edit_followup_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
        content: Optional[str] = None,
        embeds: Optional[list[Embed]] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        components: Optional[list[Component]] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[AttachmentSend]] = None,
    ) -> MessageGet:
        """Edits a followup message for an Interaction. Functions the same as Edit Webhook Message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#edit-followup-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "content": content,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
        }
        request_kwargs = parse_data(
            {key: value for key, value in data.items() if value is not None},
            ExecuteWebhookParams,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
            json=request_kwargs.get("json"),
            files=request_kwargs.get("files"),
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_delete_followup_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
    ) -> None:
        """Deletes a followup message for an Interaction.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#delete-followup-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
        )
        await _request(self, bot, request)

    # Application

    # see https://discord.com/developers/docs/resources/application
    async def _api_get_current_application(
        self: AdapterProtocol,
        bot: "Bot",
    ) -> Application:
        """Returns the application object associated with the requesting bot user.

        see https://discord.com/developers/docs/resources/application#get-current-application
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "applications/@me",
        )
        return type_validate_python(Application, await _request(self, bot, request))

    async def _api_edit_current_application(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        custom_install_url: Optional[str] = None,
        description: Optional[str] = None,
        role_connections_verification_url: Optional[str] = None,
        install_params: Optional[InstallParams] = None,
        integration_types_config: Optional[
            dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration]
        ] = None,
        flags: Optional[ApplicationFlag] = None,
        icon: Optional[str] = None,
        cover_image: Optional[str] = None,
        interactions_endpoint_url: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> Application:
        """Edit properties of the app associated with the requesting bot user.

        see https://discord.com/developers/docs/resources/application#edit-current-application
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "custom_install_url": custom_install_url,
            "description": description,
            "role_connections_verification_url": role_connections_verification_url,
            "install_params": install_params,
            "integration_types_config": integration_types_config,
            "flags": flags,
            "icon": icon,
            "cover_image": cover_image,
            "interactions_endpoint_url": interactions_endpoint_url,
            "tags": tags,
        }
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / "applications/@me",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Application, await _request(self, bot, request))

    async def _api_get_application_activity_instance(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        instance_id: str,
    ) -> ActivityInstance:
        """Returns a serialized activity instance, if it exists.
        Useful for preventing unwanted activity sessions.

        see https://discord.com/developers/docs/resources/application#get-application-activity-instance
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/activity-instances/{instance_id}",
        )
        return type_validate_python(
            ActivityInstance, await _request(self, bot, request)
        )

    # Application Role Connection Metadata

    # see https://discord.com/developers/docs/resources/application-role-connection-metadata
    async def _api_get_application_role_connection_metadata_records(
        self: AdapterProtocol, bot: "Bot", *, application_id: SnowflakeType
    ) -> list[ApplicationRoleConnectionMetadata]:
        """get application role connection metadata records

        see https://discord.com/developers/docs/resources/application-role-connection-metadata#get-application-role-connection-metadata-records
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/role-connections/metadata",
        )
        return type_validate_python(
            list[ApplicationRoleConnectionMetadata],
            await _request(self, bot, request),
        )

    async def _api_update_application_role_connection_metadata_records(
        self: AdapterProtocol, bot: "Bot", *, application_id: SnowflakeType
    ) -> list[ApplicationRoleConnectionMetadata]:
        """update application role connection metadata records

        see https://discord.com/developers/docs/resources/application-role-connection-metadata#update-application-role-connection-metadata-records
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/role-connections/metadata",
        )
        return type_validate_python(
            list[ApplicationRoleConnectionMetadata],
            await _request(self, bot, request),
        )

    # Audit Logs

    # see https://discord.com/developers/docs/resources/audit-log
    async def _api_get_guild_audit_log(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: Optional[SnowflakeType] = None,
        action_type: Optional[AuditLogEventType] = None,
        before: Optional[SnowflakeType] = None,
        after: Optional[SnowflakeType] = None,
        limit: Optional[int] = None,
    ) -> AuditLog:
        """Returns an audit log object for the guild.
        Requires the VIEW_AUDIT_LOG permission.

        The returned list of audit log entries is ordered based on whether you use
        before or after. When using before, the list is ordered by the audit log entry
        ID descending (newer entries first). If after is used, the list is reversed and
        appears in ascending order (older entries first). Omitting both before and after
        defaults to before the current timestamp and will show the most recent entries
        in descending order by ID, the opposite can be achieved using after=0 (showing
        oldest entries).

        see https://discord.com/developers/docs/resources/audit-log#get-guild-audit-log"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "user_id": user_id,
            "action_type": action_type,
            "before": before,
            "after": after,
            "limit": limit,
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/audit-logs",
            params={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(AuditLog, await _request(self, bot, request))

    # Auto Moderation

    # see https://discord.com/developers/docs/resources/auto-moderation
    async def _api_list_auto_moderation_rules_for_guild(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[AutoModerationRule]:
        """list auto moderation rules for guild

        see https://discord.com/developers/docs/resources/auto-moderation#list-auto-moderation-rules-for-guild
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules",
        )
        return type_validate_python(
            list[AutoModerationRule], await _request(self, bot, request)
        )

    async def _api_get_auto_moderation_rule(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
    ) -> AutoModerationRule:
        """get auto moderation rule

        see https://discord.com/developers/docs/resources/auto-moderation#get-auto-moderation-rule
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
        )
        return type_validate_python(
            AutoModerationRule, await _request(self, bot, request)
        )

    async def _api_create_auto_moderation_rule(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: TriggerType,
        actions: list[AutoModerationAction],
        trigger_metadata: Optional[TriggerMetadata] = None,
        enabled: Optional[bool] = None,
        exempt_roles: Optional[list[SnowflakeType]] = None,
        exempt_channels: Optional[list[SnowflakeType]] = None,
        reason: Optional[str] = None,
    ) -> AutoModerationRule:
        """create auto moderation rule

        see https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "event_type": event_type,
            "trigger_type": trigger_type,
            "actions": actions,
            "trigger_metadata": trigger_metadata,
            "enabled": enabled,
            "exempt_roles": exempt_roles,
            "exempt_channels": exempt_channels,
        }
        data = model_dump(
            type_validate_python(CreateAndModifyAutoModerationRuleParams, data),
            exclude_none=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules",
            json=data,
        )
        return type_validate_python(
            AutoModerationRule, await _request(self, bot, request)
        )

    async def _api_modify_auto_moderation_rule(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: TriggerType,
        trigger_metadata: Optional[TriggerMetadata] = None,
        actions: list[AutoModerationAction] = ...,
        enabled: Optional[bool] = None,
        exempt_roles: list[SnowflakeType] = ...,
        exempt_channels: list[SnowflakeType] = ...,
        reason: Optional[str] = None,
    ) -> AutoModerationRule:
        """modify auto moderation rule

        see https://discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "event_type": event_type,
            "trigger_type": trigger_type,
            "trigger_metadata": trigger_metadata,
            "actions": actions,
            "enabled": enabled,
            "exempt_roles": exempt_roles,
            "exempt_channels": exempt_channels,
        }
        data = model_dump(
            type_validate_python(
                CreateAndModifyAutoModerationRuleParams,
                {
                    key: value
                    for key, value in data.items()
                    if value is not None and value is not ...
                },
            ),
            exclude_none=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
            json=data,
        )
        return type_validate_python(
            AutoModerationRule, await _request(self, bot, request)
        )

    async def _api_delete_auto_moderation_rule(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """delete auto moderation rule

        see https://discord.com/developers/docs/resources/auto-moderation#delete-auto-moderation-rule
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
        )
        await _request(self, bot, request)

    # Channels

    # https://discord.com/developers/docs/resources/channel
    async def _api_get_channel(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> Channel:
        """get channel

        see https://discord.com/developers/docs/resources/channel#get-channel"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}",
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_modify_DM(  # noqa: N802 # TODO)): 疑似与_modify_channel重复, 确认后弃用
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: Optional[str] = None,
        icon: Optional[bytes] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """modify channel

        see https://discord.com/developers/docs/resources/channel#modify-channel"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"name": name, "icon": icon}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_modify_channel(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: Optional[str] = None,
        type: Optional[ChannelType] = None,  # noqa: A002
        position: Optional[int] = None,
        topic: Optional[str] = None,
        nsfw: Optional[bool] = None,
        rate_limit_per_user: Optional[int] = None,
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        permission_overwrites: Optional[list[Overwrite]] = None,
        parent_id: Optional[SnowflakeType] = None,
        rtc_region: Optional[str] = None,
        video_quality_mode: Optional[VideoQualityMode] = None,
        default_auto_archive_duration: Optional[int] = None,
        flags: Optional[ChannelFlags] = None,
        available_tags: Optional[list[ForumTag]] = None,
        default_reaction_emoji: Optional[DefaultReaction] = None,
        default_thread_rate_limit_per_user: Optional[int] = None,
        default_sort_order: Optional[SortOrderTypes] = None,
        default_forum_layout: Optional[ForumLayoutTypes] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#modify-channel"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "type": type,
            "position": position,
            "topic": topic,
            "nsfw": nsfw,
            "rate_limit_per_user": rate_limit_per_user,
            "bitrate": bitrate,
            "user_limit": user_limit,
            "permission_overwrites": permission_overwrites,
            "parent_id": parent_id,
            "rtc_region": rtc_region,
            "video_quality_mode": video_quality_mode,
            "default_auto_archive_duration": default_auto_archive_duration,
            "flags": flags,
            "available_tags": available_tags,
            "default_reaction_emoji": default_reaction_emoji,
            "default_thread_rate_limit_per_user": default_thread_rate_limit_per_user,
            "default_sort_order": default_sort_order,
            "default_forum_layout": default_forum_layout,
        }
        data = model_dump(
            type_validate_python(
                ModifyChannelParams,
                {key: value for key, value in data.items() if value is not None},
            ),
            exclude_unset=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_modify_thread(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: Optional[str] = None,
        archived: Optional[bool] = None,
        auto_archive_duration: Optional[int] = None,
        locked: Optional[bool] = None,
        invitable: Optional[bool] = None,
        rate_limit_per_user: Optional[int] = None,
        flags: Optional[ChannelFlags] = None,
        applied_tags: Optional[list[SnowflakeType]] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#modify-channel"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "archived": archived,
            "auto_archive_duration": auto_archive_duration,
            "locked": locked,
            "invitable": invitable,
            "rate_limit_per_user": rate_limit_per_user,
            "flags": flags,
            "applied_tags": applied_tags,
        }
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_delete_channel(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#deleteclose-channel"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}",
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    # Messages

    # see https://discord.com/developers/docs/resources/message
    async def _api_get_channel_messages(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: Optional[SnowflakeType] = None,
        before: Optional[SnowflakeType] = None,
        after: Optional[SnowflakeType] = None,
        limit: Optional[int] = None,
    ) -> list[MessageGet]:
        """https://discord.com/developers/docs/resources/message#get-channel-messages"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "around": around,
            "before": before,
            "after": after,
            "limit": limit,
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/messages",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[MessageGet], await _request(self, bot, request)
        )

    async def _api_get_channel_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/message#get-channel-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_create_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        content: Optional[str] = None,
        nonce: Optional[Union[int, str]] = None,
        tts: Optional[bool] = None,
        embeds: Optional[list[Embed]] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        message_reference: Optional[MessageReference] = None,
        components: Optional[list[DirectComponent]] = None,
        sticker_ids: Optional[list[SnowflakeType]] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[AttachmentSend]] = None,
        flags: Optional[MessageFlag] = None,
        poll: Optional[PollRequest] = None,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/message#create-message"""
        data = {
            "content": content,
            "nonce": nonce,
            "tts": tts,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "message_reference": message_reference,
            "components": components,
            "sticker_ids": sticker_ids,
            "files": files,
            "attachments": attachments,
            "flags": flags,
            "poll": poll,
        }
        params = parse_data(
            {key: value for key, value in data.items() if value is not None},
            MessageSend,
        )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/messages",
            json=params.get("json"),
            files=params.get("files"),
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_crosspost_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/message#crosspost-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/crosspost",
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_create_reaction(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: Optional[SnowflakeType] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/message#create-reaction"""
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}/@me",
        )
        await _request(self, bot, request)

    async def _api_delete_own_reaction(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: Optional[SnowflakeType] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/message#delete-own-reaction"""
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}/@me",
        )
        await _request(self, bot, request)

    async def _api_delete_user_reaction(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        user_id: SnowflakeType,
        emoji: str,
        emoji_id: Optional[SnowflakeType] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/message#delete-user-reaction"""
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}/{user_id}",
        )
        await _request(self, bot, request)

    async def _api_get_reactions(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: Optional[SnowflakeType] = None,
        after: Optional[SnowflakeType] = None,
        limit: Optional[int] = None,
    ) -> list[User]:
        """https://discord.com/developers/docs/resources/message#get-reactions"""
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"after": after, "limit": limit}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(list[User], await _request(self, bot, request))

    async def _api_delete_all_reactions(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> None:
        """https://discord.com/developers/docs/resources/message#delete-all-reactions"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/reactions",
        )
        await _request(self, bot, request)

    async def _api_delete_all_reactions_for_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: Optional[SnowflakeType] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/message#delete-all-reactions-for-emoji"""
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}",
        )
        await _request(self, bot, request)

    async def _api_edit_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        content: Optional[str] = None,
        embeds: Optional[list[Embed]] = None,
        flags: Optional[MessageFlag] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        components: Optional[list[DirectComponent]] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[AttachmentSend]] = None,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/message#edit-message"""
        data = {
            "content": content,
            "embeds": embeds,
            "flags": flags,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
        }
        params = parse_data(
            {key: value for key, value in data.items() if value is not None},
            MessageSend,
        )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
            json=params.get("json"),
            files=params.get("files"),
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_delete_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/message#delete-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
        )
        await _request(self, bot, request)

    async def _api_bulk_delete_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        messages: list[SnowflakeType],
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/message#bulk-delete-messages"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"messages": messages}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/messages/bulk-delete",
            json=data,
        )
        await _request(self, bot, request)

    async def _api_edit_channel_permissions(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        overwrite_id: SnowflakeType,
        allow: Optional[str] = None,
        deny: Optional[str] = None,
        type: Optional[OverwriteType] = None,  # noqa: A002
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#edit-channel-permissions"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "allow": allow,
            "deny": deny,
            "type": type,
        }
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/permissions/{overwrite_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        await _request(self, bot, request)

    async def _api_get_channel_invites(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[Invite]:
        """https://discord.com/developers/docs/resources/channel#get-channel-invites"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/invites",
        )
        return type_validate_python(list[Invite], await _request(self, bot, request))

    async def _api_create_channel_invite(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        max_age: Optional[int] = None,
        max_uses: Optional[int] = None,
        temporary: Optional[bool] = None,
        unique: Optional[bool] = None,
        target_type: Optional[int] = None,
        target_user_id: Optional[SnowflakeType] = None,
        target_application_id: Optional[SnowflakeType] = None,
        reason: Optional[str] = None,
    ) -> Invite:
        """https://discord.com/developers/docs/resources/channel#create-channel-invite"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary,
            "unique": unique,
            "target_type": target_type,
            "target_user_id": target_user_id,
            "target_application_id": target_application_id,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/invites",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Invite, await _request(self, bot, request))

    async def _api_delete_channel_permission(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        overwrite_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#delete-channel-permission"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/permissions/{overwrite_id}",
        )
        await _request(self, bot, request)

    async def _api_follow_announcement_channel(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        webhook_channel_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> FollowedChannel:
        """https://discord.com/developers/docs/resources/channel#follow-announcement-channel"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"webhook_channel_id": webhook_channel_id}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/followers",
            json=data,
        )
        return type_validate_python(FollowedChannel, await _request(self, bot, request))

    async def _api_trigger_typing_indicator(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#trigger-typing-indicator"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/typing",
        )
        await _request(self, bot, request)

    async def _api_get_pinned_messages(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[MessageGet]:
        """https://discord.com/developers/docs/resources/channel#get-pinned-messages"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/pins",
        )
        return type_validate_python(
            list[MessageGet], await _request(self, bot, request)
        )

    async def _api_pin_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#pin-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/pins/{message_id}",
        )
        await _request(self, bot, request)

    async def _api_unpin_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#unpin-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/pins/{message_id}",
        )
        await _request(self, bot, request)

    async def _api_group_DM_add_recipient(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
        access_token: str,
        nick: str = "",
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#group-dm-add-recipient"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"access_token": access_token, "nick": nick}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/recipients/{user_id}",
            json=data,
        )
        await _request(self, bot, request)

    async def _api_group_DM_remove_recipient(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#group-dm-remove-recipient"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/recipients/{user_id}",
        )
        await _request(self, bot, request)

    async def _api_start_thread_from_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        name: str,
        auto_archive_duration: Optional[int] = None,
        rate_limit_per_user: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#start-thread-from-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "auto_archive_duration": auto_archive_duration,
            "rate_limit_per_user": rate_limit_per_user,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}/threads",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_start_thread_without_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: str,
        auto_archive_duration: Optional[int] = None,
        type: Optional[ChannelType] = None,  # noqa: A002
        invitable: Optional[bool] = None,
        rate_limit_per_user: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#start-thread-without-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "auto_archive_duration": auto_archive_duration,
            "type": type,
            "invitable": invitable,
            "rate_limit_per_user": rate_limit_per_user,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/threads",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_start_thread_in_forum_channel(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: str,
        auto_archive_duration: Optional[int] = None,
        rate_limit_per_user: Optional[int] = None,
        applied_tags: Optional[list[SnowflakeType]] = None,
        content: Optional[str] = None,
        embeds: Optional[list[Embed]] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        components: Optional[list[DirectComponent]] = None,
        sticker_ids: Optional[list[SnowflakeType]] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[AttachmentSend]] = None,
        flags: Optional[MessageFlag] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#start-thread-in-forum-or-media-channel"""
        data = {
            "name": name,
            "auto_archive_duration": auto_archive_duration,
            "rate_limit_per_user": rate_limit_per_user,
            "applied_tags": applied_tags,
            "content": content,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "sticker_ids": sticker_ids,
            "files": files,
            "attachments": attachments,
            "flags": flags,
        }
        params = parse_forum_thread_message(data)
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/threads",
            json=params.get("json"),
            files=params.get("files"),
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_join_thread(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#join-thread"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/thread-members/@me",
        )
        await _request(self, bot, request)

    async def _api_add_thread_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#add-thread-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
        )
        await _request(self, bot, request)

    async def _api_leave_thread(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#leave-thread"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/thread-members/@me",
        )
        await _request(self, bot, request)

    async def _api_remove_thread_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#remove-thread-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
        )
        await _request(self, bot, request)

    async def _api_get_thread_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
        with_member: Optional[bool] = None,
    ) -> ThreadMember:
        """https://discord.com/developers/docs/resources/channel#get-thread-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_member": with_member}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(ThreadMember, await _request(self, bot, request))

    async def _api_list_thread_members(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        with_member: Optional[bool] = None,
        after: Optional[SnowflakeType] = None,
        limit: Optional[int] = None,
    ) -> list[ThreadMember]:
        """https://discord.com/developers/docs/resources/channel#list-thread-members"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_member": with_member, "after": after, "limit": limit}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/thread-members",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[ThreadMember], await _request(self, bot, request)
        )

    async def _api_list_public_archived_threads(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        before: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> ArchivedThreadsResponse:
        """https://discord.com/developers/docs/resources/channel#list-public-archived-threads"""
        params = {"before": before, "limit": limit}
        if params["before"]:
            params["before"] = params["before"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/threads/archived/public",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            ArchivedThreadsResponse, await _request(self, bot, request)
        )

    async def _api_list_private_archived_threads(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        before: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> ArchivedThreadsResponse:
        """https://discord.com/developers/docs/resources/channel#list-private-archived-threads"""
        params = {"before": before, "limit": limit}
        if params["before"]:
            params["before"] = params["before"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/threads/archived/private",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            ArchivedThreadsResponse, await _request(self, bot, request)
        )

    async def _api_list_joined_private_archived_threads(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        before: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> ArchivedThreadsResponse:
        """https://discord.com/developers/docs/resources/channel#list-joined-private-archived-threads"""
        params = {"before": before, "limit": limit}
        if params["before"]:
            params["before"] = params["before"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"channels/{channel_id}/users/@me/threads/archived/private",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            ArchivedThreadsResponse, await _request(self, bot, request)
        )

    # Emoji

    # see https://discord.com/developers/docs/resources/emoji
    async def _api_list_guild_emojis(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Emoji]:
        """https://discord.com/developers/docs/resources/emoji#list-guild-emojis"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/emojis",
        )
        return type_validate_python(list[Emoji], await _request(self, bot, request))

    async def _api_get_guild_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#get-guild-emoji"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
        )
        return type_validate_python(Emoji, await _request(self, bot, request))

    async def _api_create_guild_emoji(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str = "",
        image: str = "",
        roles: Optional[list[SnowflakeType]] = None,
        reason: Optional[str] = None,
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#create-guild-emoji"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "image": image,
            "roles": roles,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/emojis",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Emoji, await _request(self, bot, request))

    async def _api_modify_guild_emoji(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
        name: str = ...,
        roles: Optional[list[SnowflakeType]] = None,
        reason: Optional[str] = None,
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#modify-guild-emoji"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"name": name, "roles": roles}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
            json={
                key: value
                for key, value in data.items()
                if value is not None and value is not ...
            },
        )
        return type_validate_python(Emoji, await _request(self, bot, request))

    async def _api_delete_guild_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/emoji#delete-guild-emoji"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
        )
        await _request(self, bot, request)

    async def _api_list_application_emojis(
        self: AdapterProtocol, bot: "Bot", *, application_id: SnowflakeType
    ) -> ApplicationEmojis:
        """https://discord.com/developers/docs/resources/emoji#list-application-emojis"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/emojis",
        )
        return type_validate_python(
            ApplicationEmojis, await _request(self, bot, request)
        )

    async def _api_get_application_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#get-application-emoji"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
        )
        return type_validate_python(Emoji, await _request(self, bot, request))

    async def _api_create_application_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        name: str = "",
        image: str = "",
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#create-application-emoji"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"name": name, "image": image}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"applications/{application_id}/emojis",
            json=data,
        )
        return type_validate_python(Emoji, await _request(self, bot, request))

    async def _api_modify_application_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
        name: str,
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#modify-application-emoji"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
            json={"name": name},
        )
        return type_validate_python(Emoji, await _request(self, bot, request))

    async def _api_delete_application_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> None:
        """https://discord.com/developers/docs/resources/emoji#delete-application-emoji"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
        )
        await _request(self, bot, request)

    # Entitlements

    # see https://discord.com/developers/docs/resources/entitlement
    async def _api_list_entitlements(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        user_id: Optional[SnowflakeType] = None,
        sku_ids: Optional[tuple[SnowflakeType]] = None,
        before: Optional[SnowflakeType] = None,
        after: Optional[SnowflakeType] = None,
        limit: Optional[int] = None,
        guild_id: Optional[SnowflakeType] = None,
        exclude_ended: Optional[bool] = None,
    ) -> list[Entitlement]:
        """https://discord.com/developers/docs/resources/entitlement#list-entitlements"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "user_id": user_id,
            "sku_ids": ",".join(str(sku_id) for sku_id in sku_ids) if sku_ids else None,
            "before": before,
            "after": after,
            "limit": limit,
            "guild_id": guild_id,
            "exclude_ended": exclude_ended,
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/entitlements",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[Entitlement], await _request(self, bot, request)
        )

    async def _api_consume_an_entitlement(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        entitlement_id: SnowflakeType,
    ) -> None:
        """https://discord.com/developers/docs/resources/entitlement#consume-an-entitlement"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url
            / f"applications/{application_id}/entitlements/{entitlement_id}/consume",
        )
        await _request(self, bot, request)

    async def _api_create_test_entitlement(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        sku_id: str = "",
        owner_id: str = "",
        owner_type: int = 0,
    ) -> Entitlement:
        """https://discord.com/developers/docs/resources/entitlement#create-test-entitlement"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "sku_id": sku_id,
            "owner_id": owner_id,
            "owner_type": owner_type,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"applications/{application_id}/entitlements",
            json=data,
        )
        return type_validate_python(Entitlement, await _request(self, bot, request))

    async def _api_delete_test_entitlement(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        entitlement_id: SnowflakeType,
    ) -> None:
        """https://discord.com/developers/docs/resources/entitlement#delete-test-entitlement"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"applications/{application_id}/entitlements/{entitlement_id}",
        )
        await _request(self, bot, request)

    # Guild

    # see https://discord.com/developers/docs/resources/guild
    async def _api_create_guild(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        name: str = "",
        region: Optional[str] = None,
        icon: Optional[str] = None,
        verification_level: Optional[VerificationLevel] = None,
        default_message_notifications: Optional[DefaultMessageNotificationLevel] = None,
        explicit_content_filter: Optional[ExplicitContentFilterLevel] = None,
        roles: Optional[list[Role]] = None,
        channels: Optional[list[Channel]] = None,
        afk_channel_id: Optional[Snowflake] = None,
        afk_timeout: Optional[int] = None,
        system_channel_id: Optional[Snowflake] = None,
        system_channel_flags: Optional[SystemChannelFlags] = None,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild#create-guild"""
        data = {
            "name": name,
            "region": region,
            "icon": icon,
            "verification_level": verification_level,
            "default_message_notifications": default_message_notifications,
            "explicit_content_filter": explicit_content_filter,
            "roles": roles,
            "channels": channels,
            "afk_channel_id": afk_channel_id,
            "afk_timeout": afk_timeout,
            "system_channel_id": system_channel_id,
            "system_channel_flags": system_channel_flags,
        }
        data = model_dump(
            type_validate_python(CreateGuildParams, data), exclude_unset=True
        )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers, method="POST", url=self.base_url / "guilds", json=data
        )
        return type_validate_python(Guild, await _request(self, bot, request))

    async def _api_get_guild(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        with_counts: Optional[bool] = None,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild#get-guild"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_counts": with_counts}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(Guild, await _request(self, bot, request))

    async def _api_get_guild_preview(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildPreview:
        """https://discord.com/developers/docs/resources/guild#get-guild-preview"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/preview",
        )
        return type_validate_python(GuildPreview, await _request(self, bot, request))

    async def _api_modify_guild(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        region: Optional[str] = None,
        verification_level: Optional[VerificationLevel] = None,
        default_message_notifications: Optional[DefaultMessageNotificationLevel] = None,
        explicit_content_filter: Optional[ExplicitContentFilterLevel] = None,
        afk_channel_id: Optional[Snowflake] = None,
        afk_timeout: Optional[int] = None,
        icon: Optional[str] = None,
        owner_id: Optional[Snowflake] = None,
        splash: Optional[str] = None,
        discovery_splash: Optional[str] = None,
        banner: Optional[str] = None,
        system_channel_id: Optional[Snowflake] = None,
        system_channel_flags: Optional[SystemChannelFlags] = None,
        rules_channel_id: Optional[Snowflake] = None,
        public_updates_channel_id: Optional[Snowflake] = None,
        preferred_locale: Optional[str] = None,
        features: Optional[list[GuildFeature]] = None,
        description: Optional[str] = None,
        premium_progress_bar_enabled: Optional[bool] = None,
        reason: Optional[str] = None,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild#modify-guild"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "region": region,
            "verification_level": verification_level,
            "default_message_notifications": default_message_notifications,
            "explicit_content_filter": explicit_content_filter,
            "afk_channel_id": afk_channel_id,
            "afk_timeout": afk_timeout,
            "icon": icon,
            "owner_id": owner_id,
            "splash": splash,
            "discovery_splash": discovery_splash,
            "banner": banner,
            "system_channel_id": system_channel_id,
            "system_channel_flags": system_channel_flags,
            "rules_channel_id": rules_channel_id,
            "public_updates_channel_id": public_updates_channel_id,
            "preferred_locale": preferred_locale,
            "features": features,
            "description": description,
            "premium_progress_bar_enabled": premium_progress_bar_enabled,
        }
        data = model_dump(
            type_validate_python(
                ModifyGuildParams,
                {key: value for key, value in data.items() if value is not None},
            ),
            exclude_unset=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}",
            json=data,
        )
        return type_validate_python(Guild, await _request(self, bot, request))

    async def _api_delete_guild(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#delete-guild"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}",
        )
        await _request(self, bot, request)

    async def _api_get_guild_channels(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Channel]:
        """https://discord.com/developers/docs/resources/guild#get-guild-channels"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/channels",
        )
        return type_validate_python(list[Channel], await _request(self, bot, request))

    async def _api_create_guild_channel(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str = "",
        type: Optional[ChannelType] = None,  # noqa: A002
        topic: Optional[str] = None,
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        rate_limit_per_user: Optional[int] = None,
        position: Optional[int] = None,
        permission_overwrites: Optional[list[Overwrite]] = None,
        parent_id: Optional[Snowflake] = None,
        nsfw: Optional[bool] = None,
        rtc_region: Optional[str] = None,
        video_quality_mode: Optional[VideoQualityMode] = None,
        default_auto_archive_duration: Optional[int] = None,
        default_reaction_emoji: Optional[DefaultReaction] = None,
        available_tags: Optional[list[ForumTag]] = None,
        default_sort_order: Optional[SortOrderTypes] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/guild#create-guild-channel"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "type": type,
            "topic": topic,
            "bitrate": bitrate,
            "user_limit": user_limit,
            "rate_limit_per_user": rate_limit_per_user,
            "position": position,
            "permission_overwrites": permission_overwrites,
            "parent_id": parent_id,
            "nsfw": nsfw,
            "rtc_region": rtc_region,
            "video_quality_mode": video_quality_mode,
            "default_auto_archive_duration": default_auto_archive_duration,
            "default_reaction_emoji": default_reaction_emoji,
            "available_tags": available_tags,
            "default_sort_order": default_sort_order,
        }
        data = model_dump(
            type_validate_python(CreateGuildChannelParams, data), exclude_unset=True
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/channels",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_modify_guild_channel_positions(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        id: SnowflakeType = ...,  # noqa: A002
        position: Optional[int] = None,
        lock_permissions: Optional[bool] = None,
        parent_id: Optional[SnowflakeType] = None,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "id": id,
            "position": position,
            "lock_permissions": lock_permissions,
            "parent_id": parent_id,
        }
        payload = [
            {
                key: value
                for key, value in data.items()
                if value is not None and value is not ...
            }
        ]
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/channels",
            json=payload,
        )
        return type_validate_python(Guild, await _request(self, bot, request))

    async def _api_list_active_guild_threads(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> ListActiveGuildThreadsResponse:
        """https://discord.com/developers/docs/resources/guild#list-active-guild-threads"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/threads/active",
        )
        return type_validate_python(
            ListActiveGuildThreadsResponse, await _request(self, bot, request)
        )

    async def _api_get_guild_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#get-guild-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
        )
        return type_validate_python(GuildMember, await _request(self, bot, request))

    async def _api_list_guild_members(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        limit: Optional[int] = None,
        after: Optional[SnowflakeType] = None,
    ) -> list[GuildMember]:
        """https://discord.com/developers/docs/resources/guild#list-guild-members"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"limit": limit, "after": after}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[GuildMember], await _request(self, bot, request)
        )

    async def _api_search_guild_members(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        query: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[GuildMember]:
        """https://discord.com/developers/docs/resources/guild#search-guild-members"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"query": query, "limit": limit}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members/search",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[GuildMember], await _request(self, bot, request)
        )

    async def _api_add_guild_member(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        access_token: str,
        nick: Optional[str] = None,
        roles: Optional[list[SnowflakeType]] = None,
        mute: Optional[bool] = None,
        deaf: Optional[bool] = None,
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#add-guild-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "access_token": access_token,
            "nick": nick,
            "roles": roles,
            "mute": mute,
            "deaf": deaf,
        }
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(GuildMember, await _request(self, bot, request))

    async def _api_modify_guild_member(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        nick: Optional[str] = None,
        roles: Optional[list[SnowflakeType]] = None,
        mute: Optional[bool] = None,
        deaf: Optional[bool] = None,
        channel_id: Optional[SnowflakeType] = None,
        communication_disabled_until: Optional[datetime] = None,
        flags: Optional[GuildMemberFlags] = None,
        reason: Optional[str] = None,
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#modify-guild-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "nick": nick,
            "roles": roles,
            "mute": mute,
            "deaf": deaf,
            "channel_id": channel_id,
            "communication_disabled_until": communication_disabled_until,
            "flags": flags,
        }
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(GuildMember, await _request(self, bot, request))

    async def _api_modify_current_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        nick: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#modify-current-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"nick": nick}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(GuildMember, await _request(self, bot, request))

    async def _api_modify_current_user_nick(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        nick: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> GuildMember:
        """Deprecated in favor of Modify Current Member.

        https://discord.com/developers/docs/resources/guild#modify-current-user-nick"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"nick": nick}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me/nick",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(GuildMember, await _request(self, bot, request))

    async def _api_add_guild_member_role(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#add-guild-member-role"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
        )
        await _request(self, bot, request)

    async def _api_remove_guild_member_role(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#remove-guild-member-role"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
        )
        await _request(self, bot, request)

    async def _api_remove_guild_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#remove-guild-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
        )
        await _request(self, bot, request)

    async def _api_get_guild_bans(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        limit: Optional[int] = None,
        before: Optional[SnowflakeType] = None,
        after: Optional[SnowflakeType] = None,
    ) -> list[Ban]:
        """https://discord.com/developers/docs/resources/guild#get-guild-bans"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"limit": limit, "before": before, "after": after}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/bans",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(list[Ban], await _request(self, bot, request))

    async def _api_get_guild_ban(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> Ban:
        """https://discord.com/developers/docs/resources/guild#get-guild-ban"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
        )
        return type_validate_python(Ban, await _request(self, bot, request))

    async def _api_create_guild_ban(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        delete_message_days: Optional[int] = None,
        delete_message_seconds: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#create-guild-ban"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "delete_message_days": delete_message_days,
            "delete_message_seconds": delete_message_seconds,
        }
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        await _request(self, bot, request)

    async def _api_remove_guild_ban(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#remove-guild-ban"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
        )
        await _request(self, bot, request)

    async def _api_bulk_guild_ban(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_ids: list[SnowflakeType],
        delete_message_seconds: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> BulkBan:
        """https://discord.com/developers/docs/resources/guild#bulk-guild-ban"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "user_ids": user_ids,
            "delete_message_seconds": delete_message_seconds,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/bulk-ban",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(BulkBan, await _request(self, bot, request))

    async def _api_get_guild_roles(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Role]:
        """https://discord.com/developers/docs/resources/guild#get-guild-roles"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/roles",
        )
        return type_validate_python(list[Role], await _request(self, bot, request))

    async def _api_get_guild_role(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
    ) -> Role:
        """https://discord.com/developers/docs/resources/guild#get-guild-role"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
        )
        return type_validate_python(Role, await _request(self, bot, request))

    async def _api_create_guild_role(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: Optional[str] = None,
        permissions: Optional[str] = None,
        color: Optional[int] = None,
        hoist: Optional[bool] = None,
        icon: Optional[str] = None,
        unicode_emoji: Optional[str] = None,
        mentionable: Optional[bool] = None,
        reason: Optional[str] = None,
    ) -> Role:
        """https://discord.com/developers/docs/resources/guild#create-guild-role"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "permissions": permissions,
            "color": color,
            "hoist": hoist,
            "icon": icon,
            "unicode_emoji": unicode_emoji,
            "mentionable": mentionable,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/roles",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Role, await _request(self, bot, request))

    async def _api_modify_guild_role_positions(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        id: SnowflakeType,  # noqa: A002
        position: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> list[Role]:
        """https://discord.com/developers/docs/resources/guild#modify-guild-role-positions"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"id": id, "position": position}
        payload = {key: value for key, value in data.items() if value is not None}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles",
            json=[payload],
        )
        return type_validate_python(list[Role], await _request(self, bot, request))

    async def _api_modify_guild_role(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
        name: Optional[str] = None,
        permissions: Optional[str] = None,
        color: Optional[int] = None,
        hoist: Optional[bool] = None,
        icon: Optional[str] = None,
        unicode_emoji: Optional[str] = None,
        mentionable: Optional[bool] = None,
        reason: Optional[str] = None,
    ) -> Role:
        """https://discord.com/developers/docs/resources/guild#modify-guild-role"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "permissions": permissions,
            "color": color,
            "hoist": hoist,
            "icon": icon,
            "unicode_emoji": unicode_emoji,
            "mentionable": mentionable,
        }
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Role, await _request(self, bot, request))

    async def _api_modify_guild_MFA_level(  # noqa: N802 # TODO)): 验证接口是否还存在
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        level: int,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#modify-guild-mfa-level"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"level": level}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/mfa",
            json=data,
        )
        await _request(self, bot, request)

    async def _api_delete_guild_role(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#delete-guild-role"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
        )
        await _request(self, bot, request)

    async def _api_get_guild_prune_count(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        days: int,
        include_roles: list[SnowflakeType],
    ) -> dict[Literal["pruned"], int]:
        """https://discord.com/developers/docs/resources/guild#get-guild-prune-count"""
        data = {"days": days, "include_roles": include_roles}
        data["include_roles"] = ",".join(str(role) for role in include_roles)
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/prune",
            params=data,
        )
        return await _request(self, bot, request)

    async def _api_begin_guild_prune(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        days: Optional[int] = None,
        compute_prune_count: Optional[bool] = None,
        include_roles: Optional[list[SnowflakeType]] = None,
        reason: Optional[str] = None,
    ) -> dict[Literal["pruned"], int]:
        """https://discord.com/developers/docs/resources/guild#begin-guild-prune"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "days": days,
            "compute_prune_count": compute_prune_count,
            "include_roles": include_roles,
        }
        if include_roles:
            data["include_roles"] = ",".join(str(role) for role in include_roles)
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/prune",
            json={key: value for key, value in data.items() if value is not None},
        )
        return await _request(self, bot, request)

    async def _api_get_guild_voice_regions(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[VoiceRegion]:
        """https://discord.com/developers/docs/resources/guild#get-guild-voice-regions"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/regions",
        )
        return type_validate_python(
            list[VoiceRegion], await _request(self, bot, request)
        )

    async def _api_get_guild_invites(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Invite]:
        """https://discord.com/developers/docs/resources/guild#get-guild-invites"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/invites",
        )
        return type_validate_python(list[Invite], await _request(self, bot, request))

    async def _api_get_guild_integrations(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Integration]:
        """https://discord.com/developers/docs/resources/guild#get-guild-integrations"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/integrations",
        )
        return type_validate_python(
            list[Integration], await _request(self, bot, request)
        )

    async def _api_delete_guild_integration(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        integration_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#delete-guild-integration"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/integrations/{integration_id}",
        )
        await _request(self, bot, request)

    async def _api_get_guild_widget_settings(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildWidgetSettings:
        """https://discord.com/developers/docs/resources/guild#get-guild-widget-settings"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget",
        )
        return type_validate_python(
            GuildWidgetSettings, await _request(self, bot, request)
        )

    async def _api_modify_guild_widget(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        enabled: Optional[bool] = None,
        channel_id: Optional[SnowflakeType] = None,
        reason: Optional[str] = None,
    ) -> GuildWidget:
        """https://discord.com/developers/docs/resources/guild#modify-guild-widget"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"enabled": enabled, "channel_id": channel_id}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/widget",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(GuildWidget, await _request(self, bot, request))

    async def _api_get_guild_widget(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildWidget:
        """https://discord.com/developers/docs/resources/guild#get-guild-widget"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget.json",
        )
        return type_validate_python(GuildWidget, await _request(self, bot, request))

    async def _api_get_guild_vanity_url(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> Invite:
        """https://discord.com/developers/docs/resources/guild#get-guild-vanity-url"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/vanity-url",
        )
        return type_validate_python(Invite, await _request(self, bot, request))

    async def _api_get_guild_widget_image(  # TODO)): 校验接口返回值并更新类型
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        style: Optional[
            Literal["shield", "banner1", "banner2", "banner3", "banner4"]
        ] = None,
    ) -> str:
        """https://discord.com/developers/docs/resources/guild#get-guild-widget-image"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"style": style}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget.png",
            params={key: value for key, value in params.items() if value is not None},
        )
        return await _request(self, bot, request)

    async def _api_get_guild_welcome_screen(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> WelcomeScreen:
        """https://discord.com/developers/docs/resources/guild#get-guild-welcome-screen"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/welcome-screen",
        )
        return type_validate_python(WelcomeScreen, await _request(self, bot, request))

    async def _api_modify_guild_welcome_screen(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        enabled: Optional[bool] = None,
        welcome_channels: Optional[list[WelcomeScreenChannel]] = None,
        description: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> WelcomeScreen:
        """https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "enabled": enabled,
            "welcome_channels": welcome_channels,
            "description": description,
        }
        data = model_dump(
            type_validate_python(
                ModifyGuildWelcomeScreenParams,
                {key: value for key, value in data.items() if value is not None},
            ),
            exclude_unset=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/welcome-screen",
            json=data,
        )
        return type_validate_python(WelcomeScreen, await _request(self, bot, request))

    async def _api_get_guild_onboarding(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildOnboarding:
        """https://discord.com/developers/docs/resources/guild#get-guild-onboarding"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/onboarding",
        )
        return type_validate_python(GuildOnboarding, await _request(self, bot, request))

    async def _api_modify_guild_onboarding(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        prompts: list[OnboardingPrompt],
        default_channel_ids: list[Snowflake],
        enabled: bool,
        mode: OnboardingMode,
        reason: Optional[str] = None,
    ) -> GuildOnboarding:
        """https://discord.com/developers/docs/resources/guild#modify-guild-onboarding"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "prompts": prompts,
            "default_channel_ids": default_channel_ids,
            "enabled": enabled,
            "mode": mode,
        }
        data = model_dump(
            type_validate_python(ModifyGuildOnboardingParams, data), exclude_unset=True
        )
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/onboarding",
            json=data,
        )
        return type_validate_python(GuildOnboarding, await _request(self, bot, request))

    # Voice

    # https://discord.com/developers/docs/resources/voice
    async def _api_list_voice_regions(
        self: AdapterProtocol, bot: "Bot"
    ) -> list[VoiceRegion]:
        """https://discord.com/developers/docs/resources/voice#list-voice-regions"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "voice/regions",
        )
        return type_validate_python(
            list[VoiceRegion], await _request(self, bot, request)
        )

    async def _api_get_current_user_voice_state(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> VoiceState:
        """https://discord.com/developers/docs/resources/voice#get-current-user-voice-state"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/voice-states/@me",
        )
        return type_validate_python(VoiceState, await _request(self, bot, request))

    async def _api_get_user_voice_state(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> VoiceState:
        """https://discord.com/developers/docs/resources/voice#get-user-voice-state"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
        )
        return type_validate_python(VoiceState, await _request(self, bot, request))

    async def _api_modify_current_user_voice_state(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        channel_id: Optional[SnowflakeType] = None,
        suppress: Optional[bool] = None,
        request_to_speak_timestamp: Optional[datetime] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/voice#modify-current-user-voice-state"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "channel_id": channel_id,
            "suppress": suppress,
            "request_to_speak_timestamp": request_to_speak_timestamp,
        }
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/voice-states/@me",
            json={key: value for key, value in data.items() if value is not None},
        )
        await _request(self, bot, request)

    async def _api_modify_user_voice_state(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        channel_id: SnowflakeType,
        suppress: Optional[bool] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/voice#modify-user-voice-state"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"channel_id": channel_id, "suppress": suppress}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        await _request(self, bot, request)

    # Guild Scheduled Event

    # see https://discord.com/developers/docs/resources/guild-scheduled-event
    async def _api_list_scheduled_events_for_guild(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        with_user_count: Optional[bool] = None,
    ) -> list[GuildScheduledEvent]:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#list-scheduled-events-for-guild"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_user_count": with_user_count}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[GuildScheduledEvent], await _request(self, bot, request)
        )

    async def _api_create_guild_schedule_event(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        channel_id: Optional[Snowflake] = None,
        entity_metadata: Optional[GuildScheduledEventEntityMetadata] = None,
        name: str,
        privacy_level: GuildScheduledEventPrivacyLevel,
        scheduled_start_time: datetime,
        scheduled_end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        entity_type: GuildScheduledEventEntityType,
        image: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> GuildScheduledEvent:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "channel_id": channel_id,
            "entity_metadata": entity_metadata,
            "name": name,
            "privacy_level": privacy_level,
            "scheduled_start_time": scheduled_start_time,
            "scheduled_end_time": scheduled_end_time,
            "description": description,
            "entity_type": entity_type,
            "image": image,
        }
        data = model_dump(
            type_validate_python(CreateGuildScheduledEventParams, data),
            exclude_none=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events",
            json=data,
        )
        return type_validate_python(
            GuildScheduledEvent, await _request(self, bot, request)
        )

    async def _api_get_guild_scheduled_event(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        with_user_count: Optional[bool] = None,
    ) -> GuildScheduledEvent:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_user_count": with_user_count}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            GuildScheduledEvent, await _request(self, bot, request)
        )

    async def _api_modify_guild_scheduled_event(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        channel_id: Optional[Snowflake] = None,
        entity_metadata: Optional[GuildScheduledEventEntityMetadata] = None,
        name: Optional[str] = None,
        privacy_level: Optional[GuildScheduledEventPrivacyLevel] = None,
        scheduled_start_time: Optional[datetime] = None,
        scheduled_end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        entity_type: Optional[GuildScheduledEventEntityType] = None,
        status: Optional[GuildScheduledEventStatus] = None,
        image: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> GuildScheduledEvent:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "channel_id": channel_id,
            "entity_metadata": entity_metadata,
            "name": name,
            "privacy_level": privacy_level,
            "scheduled_start_time": scheduled_start_time,
            "scheduled_end_time": scheduled_end_time,
            "description": description,
            "entity_type": entity_type,
            "status": status,
            "image": image,
        }
        data = model_dump(
            type_validate_python(
                ModifyGuildScheduledEventParams,
                {key: value for key, value in data.items() if value is not None},
            ),
            exclude_unset=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            json=data,
        )
        return type_validate_python(
            GuildScheduledEvent, await _request(self, bot, request)
        )

    async def _api_delete_guild_scheduled_event(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#delete-guild-scheduled-event"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
        )
        await _request(self, bot, request)

    async def _api_get_guild_scheduled_event_users(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        limit: Optional[int] = None,
        with_member: Optional[bool] = None,
        before: Optional[SnowflakeType] = None,
        after: Optional[SnowflakeType] = None,
    ) -> list[GuildScheduledEventUser]:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event-users"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "limit": limit,
            "with_member": with_member,
            "before": before,
            "after": after,
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}/users",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[GuildScheduledEventUser], await _request(self, bot, request)
        )

    # Guild Template

    # see https://discord.com/developers/docs/resources/guild-template
    async def _api_get_guild_template(
        self: AdapterProtocol, bot: "Bot", *, template_code: str
    ) -> GuildTemplate:
        """https://discord.com/developers/docs/resources/guild-template#get-guild-template"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/templates/{template_code}",
        )
        return type_validate_python(GuildTemplate, await _request(self, bot, request))

    async def _api_create_guild_from_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        template_code: str,
        name: str,
        icon: Optional[str] = None,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild-template#create-guild-from-guild-template"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"name": name, "icon": icon}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/templates/{template_code}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Guild, await _request(self, bot, request))

    async def _api_get_guild_templates(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[GuildTemplate]:
        """https://discord.com/developers/docs/resources/guild-template#get-guild-templates"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/templates",
        )
        return type_validate_python(
            list[GuildTemplate], await _request(self, bot, request)
        )

    async def _api_create_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        description: Optional[str] = None,
    ) -> GuildTemplate:
        """https://discord.com/developers/docs/resources/guild-template#create-guild-template"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"name": name, "description": description}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/templates",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(GuildTemplate, await _request(self, bot, request))

    async def _api_sync_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
    ) -> GuildTemplate:
        """https://discord.com/developers/docs/resources/guild-template#sync-guild-template"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
        )
        return type_validate_python(GuildTemplate, await _request(self, bot, request))

    async def _api_modify_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> GuildTemplate:
        """https://discord.com/developers/docs/resources/guild-template#modify-guild-template"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"name": name, "description": description}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(GuildTemplate, await _request(self, bot, request))

    async def _api_delete_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild-template#delete-guild-template"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
        )
        await _request(self, bot, request)

    # Invite

    # see https://discord.com/developers/docs/resources/invite
    async def _api_get_invite(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        invite_code: str,
        with_counts: Optional[bool] = None,
        with_expiration: Optional[bool] = None,
        guild_scheduled_event_id: Optional[SnowflakeType] = None,
    ) -> Invite:
        """https://discord.com/developers/docs/resources/invite#get-invite"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "with_counts": with_counts,
            "with_expiration": with_expiration,
            "guild_scheduled_event_id": guild_scheduled_event_id,
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"invites/{invite_code}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(Invite, await _request(self, bot, request))

    async def _api_delete_invite(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        invite_code: str,
        reason: Optional[str] = None,
    ) -> Invite:
        """https://discord.com/developers/docs/resources/invite#delete-invite"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"invites/{invite_code}",
        )
        return type_validate_python(Invite, await _request(self, bot, request))

    # Poll

    # see https://discord.com/developers/docs/resources/poll
    async def _api_get_answer_voters(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        answer_id: int,
        after: Optional[SnowflakeType] = None,
        limit: Optional[int] = None,
    ) -> AnswerVoters:
        """https://discord.com/developers/docs/resources/poll#get-answer-voters"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"after": after, "limit": limit}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"channels/{channel_id}/polls/{message_id}/answers/{answer_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(AnswerVoters, await _request(self, bot, request))

    async def _api_end_poll(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/poll#end-poll"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/polls/{message_id}/expire",
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    # SKU

    # see https://discord.com/developers/docs/resources/sku
    async def _api_list_SKUs(  # noqa: N802
        self: AdapterProtocol, bot: "Bot", *, application_id: SnowflakeType
    ) -> list[SKU]:
        """https://discord.com/developers/docs/resources/sku#list-skus"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/skus",
        )
        return type_validate_python(list[SKU], await _request(self, bot, request))

    # Stage Instance

    # see https://discord.com/developers/docs/resources/stage-instance
    async def _api_create_stage_instance(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        topic: str,
        privacy_level: Optional[StagePrivacyLevel] = None,
        send_start_notification: Optional[bool] = None,
        reason: Optional[str] = None,
    ) -> StageInstance:
        """https://discord.com/developers/docs/resources/stage-instance#create-stage-instance"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "channel_id": channel_id,
            "topic": topic,
            "privacy_level": privacy_level,
            "send_start_notification": send_start_notification,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / "stage-instances",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(StageInstance, await _request(self, bot, request))

    async def _api_get_stage_instance(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> Optional[StageInstance]:
        """https://discord.com/developers/docs/resources/stage-instance#get-stage-instance"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"stage-instances/{channel_id}",
        )
        return type_validate_python(
            Optional[StageInstance],
            await _request(self, bot, request),
        )

    async def _api_modify_stage_instance(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        topic: Optional[str] = None,
        privacy_level: Optional[StagePrivacyLevel] = None,
        reason: Optional[str] = None,
    ) -> StageInstance:
        """https://discord.com/developers/docs/resources/stage-instance#modify-stage-instance"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"topic": topic, "privacy_level": privacy_level}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"stage-instances/{channel_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(StageInstance, await _request(self, bot, request))

    async def _api_delete_stage_instance(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/stage-instance#delete-stage-instance"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"stage-instances/{channel_id}",
        )
        await _request(self, bot, request)

    # Sticker

    # see https://discord.com/developers/docs/resources/sticker
    async def _api_get_sticker(
        self: AdapterProtocol, bot: "Bot", *, sticker_id: SnowflakeType
    ) -> Sticker:
        """https://discord.com/developers/docs/resources/sticker#get-sticker"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"stickers/{sticker_id}",
        )
        return type_validate_python(Sticker, await _request(self, bot, request))

    async def _api_list_nitro_sticker_packs(
        self: AdapterProtocol, bot: "Bot"
    ) -> list[StickerPack]:
        """https://discord.com/developers/docs/resources/sticker#list-sticker-packs"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "sticker-packs",
        )
        return type_validate_python(
            list[StickerPack], await _request(self, bot, request)
        )

    async def _api_get_sticker_packs(
        self: AdapterProtocol, bot: "Bot", *, pack_id: SnowflakeType
    ) -> StickerPack:
        """https://discord.com/developers/docs/resources/sticker#get-sticker-pack"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"sticker-packs/{pack_id}",
        )
        return type_validate_python(StickerPack, await _request(self, bot, request))

    async def _api_list_guild_stickers(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Sticker]:
        """https://discord.com/developers/docs/resources/sticker#list-guild-stickers"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/stickers",
        )
        return type_validate_python(list[Sticker], await _request(self, bot, request))

    async def _api_get_guild_sticker(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
    ) -> Sticker:
        """https://discord.com/developers/docs/resources/sticker#get-guild-sticker"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
        )
        return type_validate_python(Sticker, await _request(self, bot, request))

    async def _api_create_guild_sticker(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        description: str,
        tags: str,
        file: File,
        reason: Optional[str] = None,
    ) -> Sticker:
        """https://discord.com/developers/docs/resources/sticker#create-guild-sticker"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        form = {
            "name": (None, name),
            "description": (None, description),
            "tags": (None, tags),
            "file": (file.filename, file.content),
        }
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/stickers",
            json={"name": name, "description": description, "tags": tags},
            files=form,
        )
        return type_validate_python(Sticker, await _request(self, bot, request))

    async def _api_modify_guild_sticker(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> Sticker:
        """https://discord.com/developers/docs/resources/sticker#modify-guild-sticker"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"name": name, "description": description, "tags": tags}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Sticker, await _request(self, bot, request))

    async def _api_delete_guild_sticker(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/sticker#delete-guild-sticker"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
        )
        await _request(self, bot, request)

    # Subscription

    # see https://discord.com/developers/docs/resources/subscription
    async def _api_list_SKU_subscriptions(  # noqa: N802, PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        sku_id: SnowflakeType,
        before: Optional[SnowflakeType] = None,
        after: Optional[SnowflakeType] = None,
        limit: Optional[int] = None,
        user_id: Optional[SnowflakeType] = None,
    ) -> list[Subscription]:
        """https://discord.com/developers/docs/resources/subscription#list-sku-subscriptions

        Note: user_id is required except for OAuth queries.
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "before": before,
            "after": after,
            "limit": limit,
            "user_id": user_id,
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"skus/{sku_id}/subscriptions",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[Subscription], await _request(self, bot, request)
        )

    async def _api_get_SKU_subscription(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        sku_id: SnowflakeType,
        subscription_id: SnowflakeType,
    ) -> Subscription:
        """https://discord.com/developers/docs/resources/subscription#get-sku-subscription"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"skus/{sku_id}/subscriptions/{subscription_id}",
        )
        return type_validate_python(Subscription, await _request(self, bot, request))

    # Users

    # see https://discord.com/developers/docs/resources/user
    async def _api_get_current_user(self: AdapterProtocol, bot: "Bot") -> User:
        """https://discord.com/developers/docs/resources/user#get-current-user"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "users/@me",
        )
        return type_validate_python(User, await _request(self, bot, request))

    async def _api_get_user(
        self: AdapterProtocol, bot: "Bot", *, user_id: SnowflakeType
    ) -> User:
        """https://discord.com/developers/docs/resources/user#get-user"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"users/{user_id}",
        )
        return type_validate_python(User, await _request(self, bot, request))

    async def _api_modify_current_user(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        username: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> User:
        """https://discord.com/developers/docs/resources/user#modify-current-user"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"username": username, "avatar": avatar}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / "users/@me",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(User, await _request(self, bot, request))

    async def _api_get_current_user_guilds(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        before: Optional[SnowflakeType] = None,
        after: Optional[SnowflakeType] = None,
        limit: Optional[int] = None,
    ) -> list[CurrentUserGuild]:
        """https://discord.com/developers/docs/resources/user#get-current-user-guilds"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"before": before, "after": after, "limit": limit}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "users/@me/guilds",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[CurrentUserGuild], await _request(self, bot, request)
        )

    async def _api_get_current_user_guild_member(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/user#get-current-user-guild-member"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"users/@me/guilds/{guild_id}/member",
        )
        return type_validate_python(GuildMember, await _request(self, bot, request))

    async def _api_leave_guild(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/user#leave-guild"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"users/@me/guilds/{guild_id}",
        )
        await _request(self, bot, request)

    async def _api_create_DM(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        recipient_id: SnowflakeType,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/user#create-dm"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / "users/@me/channels",
            json={"recipient_id": recipient_id},
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_create_group_DM(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        access_tokens: list[str],
        nicks: dict[SnowflakeType, str],
    ) -> Channel:
        """https://discord.com/developers/docs/resources/user#create-group-dm"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"access_tokens": access_tokens, "nicks": nicks}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / "users/@me/channels",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, bot, request))

    async def _api_get_user_connections(
        self: AdapterProtocol,
        bot: "Bot",
    ) -> list[Connection]:
        """https://discord.com/developers/docs/resources/user#get-current-user-connections"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "users/@me/connections",
        )
        return type_validate_python(
            list[Connection], await _request(self, bot, request)
        )

    async def _api_get_user_application_role_connection(
        self: AdapterProtocol, bot: "Bot", *, application_id: SnowflakeType
    ) -> ApplicationRoleConnection:
        """https://discord.com/developers/docs/resources/user#get-current-user-application-role-connection"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"users/@me/applications/{application_id}/role-connection",
        )
        return type_validate_python(
            ApplicationRoleConnection, await _request(self, bot, request)
        )

    async def _api_update_user_application_role_connection(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        platform_name: Optional[str] = None,
        platform_username: Optional[str] = None,
        metadata: Optional[ApplicationRoleConnectionMetadata] = None,
    ) -> ApplicationRoleConnection:
        """https://discord.com/developers/docs/resources/user#update-current-user-application-role-connection"""
        data = {
            "platform_name": platform_name,
            "platform_username": platform_username,
            "metadata": metadata,
        }
        if data["metadata"] is not None:
            data["metadata"] = model_dump(data["metadata"], exclude_unset=True)
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url
            / f"users/@me/applications/{application_id}/role-connection",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(
            ApplicationRoleConnection, await _request(self, bot, request)
        )

    # Webhook

    # see https://discord.com/developers/docs/resources/webhook
    async def _api_create_webhook(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: str,
        avatar: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#create-webhook"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"name": name, "avatar": avatar}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/webhooks",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Webhook, await _request(self, bot, request))

    async def _api_get_channel_webhooks(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[Webhook]:
        """https://discord.com/developers/docs/resources/webhook#get-channel-webhooks"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/webhooks",
        )
        return type_validate_python(list[Webhook], await _request(self, bot, request))

    async def _api_get_guild_webhooks(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Webhook]:
        """https://discord.com/developers/docs/resources/webhook#get-guild-webhooks"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/webhooks",
        )
        return type_validate_python(list[Webhook], await _request(self, bot, request))

    async def _api_get_webhook(
        self: AdapterProtocol, bot: "Bot", *, webhook_id: SnowflakeType
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#get-webhook"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}",
        )
        return type_validate_python(Webhook, await _request(self, bot, request))

    async def _api_get_webhook_with_token(
        self: AdapterProtocol, bot: "Bot", *, webhook_id: SnowflakeType, token: str
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#get-webhook-with-token"""
        request = Request(
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
        )
        return type_validate_python(Webhook, await _request(self, bot, request))

    async def _api_modify_webhook(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        name: Optional[str] = None,
        avatar: Optional[str] = None,
        channel_id: Optional[SnowflakeType] = None,
        reason: Optional[str] = None,
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#modify-webhook"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {"name": name, "avatar": avatar, "channel_id": channel_id}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"webhooks/{webhook_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Webhook, await _request(self, bot, request))

    async def _api_modify_webhook_with_token(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        name: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#modify-webhook-with-token"""
        data = {"name": name, "avatar": avatar}
        request = Request(
            method="PATCH",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Webhook, await _request(self, bot, request))

    async def _api_delete_webhook(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        reason: Optional[str] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#delete-webhook"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}",
        )
        await _request(self, bot, request)

    async def _api_delete_webhook_with_token(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#delete-webhook-with-token"""
        request = Request(
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
        )
        await _request(self, bot, request)

    async def _api_execute_webhook(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: Optional[bool] = None,
        thread_id: Optional[SnowflakeType] = None,
        with_components: Optional[bool] = None,
        content: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        tts: Optional[bool] = None,
        embeds: Optional[list[Embed]] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        components: Optional[list[Component]] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[AttachmentSend]] = None,
        flags: Optional[int] = None,
        thread_name: Optional[str] = None,
        applied_tags: Optional[list[SnowflakeType]] = None,
        poll: Optional[PollRequest] = None,
    ) -> Optional[MessageGet]:
        """https://discord.com/developers/docs/resources/webhook#execute-webhook"""
        params = {}
        if wait is not None:
            params["wait"] = str(wait).lower()
        if thread_id is not None:
            params["thread_id"] = thread_id
        if with_components is not None:
            params["with_components"] = str(with_components).lower()
        payload = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url,
            "tts": tts,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "flags": flags,
            "thread_name": thread_name,
            "applied_tags": applied_tags,
            "poll": poll,
        }
        request_kwargs = parse_data(
            {key: value for key, value in payload.items() if value is not None},
            ExecuteWebhookParams,
        )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
            params=params,
            json=request_kwargs.get("json"),
            files=request_kwargs.get("files"),
        )
        resp = await _request(self, bot, request)
        if resp:
            return type_validate_python(MessageGet, resp)
        return resp

    async def _api_execute_slack_compatible_webhook(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        thread_id: Optional[SnowflakeType] = None,
        wait: Optional[bool] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#execute-slackcompatible-webhook"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id, "wait": wait}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/slack",
            params={key: value for key, value in params.items() if value is not None},
        )
        await _request(self, bot, request)

    async def _api_execute_github_compatible_webhook(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        thread_id: Optional[SnowflakeType] = None,
        wait: Optional[bool] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#execute-githubcompatible-webhook"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id, "wait": wait}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/github",
            params={key: value for key, value in params.items() if value is not None},
        )
        await _request(self, bot, request)

    async def _api_get_webhook_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        message_id: SnowflakeType,
        thread_id: Optional[SnowflakeType] = None,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/webhook#get-webhook-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/messages/{message_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_edit_webhook_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        webhook_token: str,
        message_id: SnowflakeType,
        thread_id: Optional[SnowflakeType] = None,
        content: Optional[str] = None,
        embeds: Optional[list[Embed]] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        components: Optional[list[Component]] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[AttachmentSend]] = None,
        poll: Optional[PollRequest] = None,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/webhook#edit-webhook-message"""
        params = {"thread_id": thread_id}
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "content": content,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "poll": poll,
        }
        request_kwargs = parse_data(
            {key: value for key, value in data.items() if value is not None},
            ExecuteWebhookParams,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url
            / f"webhooks/{webhook_id}/{webhook_token}/messages/{message_id}",
            params={key: value for key, value in params.items() if value is not None},
            json=request_kwargs.get("json"),
            files=request_kwargs.get("files"),
        )
        return type_validate_python(MessageGet, await _request(self, bot, request))

    async def _api_delete_webhook_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        message_id: SnowflakeType,
        thread_id: Optional[SnowflakeType] = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#delete-webhook-message"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/messages/{message_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        await _request(self, bot, request)

    # Gateway

    # see https://discord.com/developers/docs/topics/gateway
    async def _api_get_gateway(self: AdapterProtocol, bot: "Bot") -> Gateway:
        """https://discord.com/developers/docs/topics/gateway#get-gateway"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "gateway",
        )
        return type_validate_python(Gateway, await _request(self, bot, request))

    async def _api_get_gateway_bot(self: AdapterProtocol, bot: "Bot") -> GatewayBot:
        """https://discord.com/developers/docs/topics/gateway#get-gateway-bot"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "gateway/bot",
        )
        return type_validate_python(GatewayBot, await _request(self, bot, request))

    # OAuth2

    # see https://discord.com/developers/docs/topics/oauth2
    async def _api_get_current_bot_application_information(
        self: AdapterProtocol, bot: "Bot"
    ) -> Application:
        """https://discord.com/developers/docs/topics/oauth2#get-current-bot-application-information"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "oauth2/applications/@me",
        )
        return type_validate_python(Application, await _request(self, bot, request))

    async def _api_get_current_authorization_information(
        self: AdapterProtocol, bot: "Bot"
    ) -> AuthorizationResponse:
        """https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "oauth2/@me",
        )
        return type_validate_python(
            AuthorizationResponse, await _request(self, bot, request)
        )


__all__ = ["HandleMixin"]
