import base64
from datetime import datetime, timezone
from http import HTTPStatus
import json
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Literal,
    overload,
)
from typing_extensions import Protocol, deprecated
from urllib.parse import quote

from nonebot.compat import type_validate_python
from nonebot.drivers import Request, Response
from nonebot.utils import escape_tag
from yarl import URL

from .model import (
    SKU,
    ActivityInstance,
    AddLobbyMemberParams,
    AllowedMention,
    AnswerVoters,
    Application,
    ApplicationCommand,
    ApplicationCommandBulkOverwriteParams,
    ApplicationCommandCreate,
    ApplicationCommandEditParams,
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
    CreateGuildRoleParams,
    CreateGuildScheduledEventParams,
    CreateGuildSoundboardSoundParams,
    CreateGuildTemplateParams,
    CreateLobbyMemberParams,
    CreateLobbyParams,
    CreateWebhookParams,
    CurrentUserGuild,
    DefaultReaction,
    DirectComponent,
    EditCurrentApplicationParams,
    Embed,
    Emoji,
    Entitlement,
    ExecuteWebhookParams,
    File,
    FollowedChannel,
    ForumTagRequest,
    Gateway,
    GatewayBot,
    Guild,
    GuildApplicationCommandPermissions,
    GuildIncidentsData,
    GuildMember,
    GuildOnboarding,
    GuildPreview,
    GuildScheduledEvent,
    GuildScheduledEventEntityMetadata,
    GuildScheduledEventUser,
    GuildTemplate,
    GuildVanityURL,
    GuildWidget,
    GuildWidgetSettings,
    InstallParams,
    Integration,
    InteractionResponse,
    Invite,
    InviteTargetUsersJobStatus,
    LinkChannelToLobbyParams,
    ListActiveGuildThreadsResponse,
    ListDefaultSoundboardSoundsResponse,
    ListGuildSoundboardSoundsResponse,
    Lobby,
    LobbyMember,
    MessageEditParams,
    MessageGet,
    MessageReference,
    MessageSend,
    ModifyChannelParams,
    ModifyCurrentMemberParams,
    ModifyCurrentUserParams,
    ModifyCurrentUserVoiceStateParams,
    ModifyGuildChannelPositionParams,
    ModifyGuildEmojiParams,
    ModifyGuildIncidentActionsParams,
    ModifyGuildMemberParams,
    ModifyGuildOnboardingParams,
    ModifyGuildParams,
    ModifyGuildRoleParams,
    ModifyGuildRolePositionParams,
    ModifyGuildScheduledEventParams,
    ModifyGuildSoundboardSoundParams,
    ModifyGuildStickerParams,
    ModifyGuildTemplateParams,
    ModifyGuildWelcomeScreenParams,
    ModifyGuildWidgetParams,
    ModifyLobbyParams,
    ModifyThreadParams,
    OnboardingPrompt,
    Overwrite,
    PartialOverwrite,
    PollRequest,
    RecurrenceRule,
    Role,
    RoleColors,
    SendSoundboardSoundParams,
    Snowflake,
    SnowflakeType,
    SoundboardSound,
    StageInstance,
    StartThreadFromMessageParams,
    StartThreadWithoutMessageParams,
    Sticker,
    StickerPack,
    StickerPacksResponse,
    Subscription,
    ThreadMember,
    TriggerMetadata,
    User,
    VoiceRegion,
    VoiceState,
    Webhook,
    WebhookMessageEditParams,
    WelcomeScreen,
    WelcomeScreenChannel,
)
from .types import (
    UNSET,
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
    InteractionContextType,
    InviteTargetType,
    LobbyMemberFlags,
    MessageFlag,
    MessageReferenceType,
    Missing,
    MissingOrNullable,
    OnboardingMode,
    OverwriteType,
    ReactionType,
    SortOrderTypes,
    StagePrivacyLevel,
    SystemChannelFlags,
    TriggerType,
    VerificationLevel,
    VideoQualityMode,
)
from .utils import (
    parse_data,
    parse_forum_thread_message,
    parse_interaction_response,
)
from .validation import (
    AtMostOne,
    ForbidIfEquals,
    Range,
    RequireIfNotEquals,
    validate,
)
from ..config import BotInfo, Config
from ..exception import (
    ActionFailed,
    DiscordAdapterException,
    NetworkError,
    RateLimitException,
    UnauthorizedException,
)
from ..utils import decompress_data, log, model_dump, omit_unset

if TYPE_CHECKING:
    from ..bot import Bot


class AdapterProtocol(Protocol):
    base_url: URL
    discord_config: Config

    @staticmethod
    def get_authorization(bot_info: BotInfo) -> str: ...

    async def request(self, setup: Request) -> Response: ...


async def _request(
    adapter: "AdapterProtocol",
    request: Request,
    *,
    parse_json: bool = True,
) -> Any:  # noqa: ANN401 # TODO)): 重构为泛型函数, 接管type_validate部分
    try:
        request.timeout = adapter.discord_config.discord_api_timeout
        request.proxy = adapter.discord_config.discord_proxy
        data = await adapter.request(request)
        log(
            "TRACE",
            f"API code: {data.status_code} response: {escape_tag(str(data.content))}",
        )
        if data.status_code in (200, 201, 204):
            if not data.content:
                return None
            if not parse_json:
                return data.content
            return json.loads(
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


def _bool_query(*, value: bool | None) -> str | None:
    if value is None:
        return None
    return "true" if value else "false"


def _detect_image_mime_type(*, image: bytes) -> str:
    if image.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if image.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if image.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    msg = "unsupported image format for icon bytes"
    raise ValueError(msg)


def _encode_image_data_uri(*, image: bytes) -> str:
    mime_type = _detect_image_mime_type(image=image)
    encoded = base64.b64encode(image).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def _build_reaction_url(
    *,
    base_url: URL,
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    emoji: str,
    suffix: str = "",
) -> URL:
    encoded_emoji = quote(emoji, safe="")
    suffix_path = f"/{suffix}" if suffix else ""
    return URL(
        (
            f"{base_url}/channels/{channel_id}/messages/"
            f"{message_id}/reactions/{encoded_emoji}{suffix_path}"
        ),
        encoded=True,
    )


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
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for command in commands:
        command_model = type_validate_python(
            ApplicationCommandBulkOverwriteParams, command
        )
        description = _normalize_command_description(
            command_type=command_model.type,
            description=command_model.description,
        )
        command_data = model_dump(
            command_model,
            omit_unset_values=True,
            exclude_none=True,
        )
        command_data["description"] = description
        payloads.append(command_data)
    return payloads


NonSpamTriggerType = Literal[
    TriggerType.KEYWORD,
    TriggerType.KEYWORD_PRESET,
    TriggerType.MENTION_SPAM,
    TriggerType.MEMBER_PROFILE,
]


class HandleMixin:
    # Application Commands

    # see https://discord.com/developers/docs/interactions/application-commands
    async def _api_get_global_application_commands(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        with_localizations: bool | None = None,
    ) -> list[ApplicationCommand]:
        """Get global application commands.

        see https://discord.com/developers/docs/interactions/application-commands#get-global-application-commands
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_localizations": _bool_query(value=with_localizations)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/commands",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[ApplicationCommand], await _request(self, request)
        )

    async def _api_create_global_application_command(  # noqa: PLR0913
        self: AdapterProtocol,
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
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
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
        payload = model_dump(
            type_validate_python(ApplicationCommandCreate, data),
            omit_unset_values=True,
            exclude_none=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"applications/{application_id}/commands",
            json=payload,
        )
        return type_validate_python(ApplicationCommand, await _request(self, request))

    async def _api_get_global_application_command(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> ApplicationCommand:
        """Get global application command.

        see https://discord.com/developers/docs/interactions/application-commands#get-global-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
        )
        return type_validate_python(ApplicationCommand, await _request(self, request))

    async def _api_edit_global_application_command(  # noqa: PLR0913
        self: AdapterProtocol,
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
            "integration_types": integration_types,
            "contexts": contexts,
        }
        data = model_dump(
            type_validate_python(ApplicationCommandEditParams, data),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
            json=data,
        )
        return type_validate_python(ApplicationCommand, await _request(self, request))

    async def _api_delete_global_application_command(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> None:
        """Delete global application command.

        see https://discord.com/developers/docs/interactions/application-commands#delete-global-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"applications/{application_id}/commands/{command_id}",
        )
        await _request(self, request)

    async def _api_bulk_overwrite_global_application_commands(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        commands: list[ApplicationCommandBulkOverwriteParams],
    ) -> list[ApplicationCommand]:
        """Bulk overwrite global application commands.

        see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-global-application-commands
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        payload = _build_command_payloads(commands)
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"applications/{application_id}/commands",
            json=payload,
        )
        return type_validate_python(
            list[ApplicationCommand], await _request(self, request)
        )

    async def _api_get_guild_application_commands(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        with_localizations: bool | None = None,
    ) -> list[ApplicationCommand]:
        """Get guild application commands.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-commands
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_localizations": _bool_query(value=with_localizations)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[ApplicationCommand], await _request(self, request)
        )

    async def _api_create_guild_application_command(  # noqa: PLR0913
        self: AdapterProtocol,
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
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
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
        payload = model_dump(
            type_validate_python(ApplicationCommandCreate, data),
            omit_unset_values=True,
            exclude_none=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            json=payload,
        )
        return type_validate_python(ApplicationCommand, await _request(self, request))

    async def _api_get_guild_application_command(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> ApplicationCommand:
        """Get guild application command.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
        )
        return type_validate_python(ApplicationCommand, await _request(self, request))

    async def _api_edit_guild_application_command(  # noqa: PLR0913
        self: AdapterProtocol,
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
        data = model_dump(
            type_validate_python(ApplicationCommandEditParams, data),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            json=data,
        )
        return type_validate_python(ApplicationCommand, await _request(self, request))

    async def _api_delete_guild_application_command(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> None:
        """Delete guild application command.

        see https://discord.com/developers/docs/interactions/application-commands#delete-guild-application-command
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
        )
        await _request(self, request)

    async def _api_bulk_overwrite_guild_application_commands(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        commands: list[ApplicationCommandBulkOverwriteParams],
    ) -> list[ApplicationCommand]:
        """Bulk overwrite guild application commands.

        see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-guild-application-commands
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        payload = _build_command_payloads(commands)
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands",
            json=payload,
        )
        return type_validate_python(
            list[ApplicationCommand], await _request(self, request)
        )

    async def _api_get_guild_application_command_permissions(
        self: AdapterProtocol,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        access_token: str,
    ) -> list[GuildApplicationCommandPermissions]:
        """Get guild application command permissions.

        see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-command-permissions
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/permissions",
        )
        return type_validate_python(
            list[GuildApplicationCommandPermissions],
            await _request(self, request),
        )

    async def _api_get_application_command_permissions(
        self: AdapterProtocol,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        access_token: str,
    ) -> GuildApplicationCommandPermissions:
        """Get application command permissions.

        see https://discord.com/developers/docs/interactions/application-commands#get-application-command-permissions
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
        )
        return type_validate_python(
            GuildApplicationCommandPermissions, await _request(self, request)
        )

    async def _api_edit_application_command_permissions(
        self: AdapterProtocol,
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
        headers = {"Authorization": f"Bearer {access_token}"}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
            json={
                "permissions": [
                    model_dump(permission, omit_unset_values=True)
                    for permission in permissions
                ]
            },
        )
        return type_validate_python(
            GuildApplicationCommandPermissions, await _request(self, request)
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
        with_response: bool | None = None,
    ) -> InteractionResponse | None:
        """Create an interaction response.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#create-interaction-response
        """
        params = parse_interaction_response(response)
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        query = {"with_response": _bool_query(value=with_response)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url
            / f"interactions/{interaction_id}/{interaction_token}/callback",
            params={key: value for key, value in query.items() if value is not None},
            json=params.get("json"),
            files=params.get("files"),
        )
        resp = await _request(self, request)
        if resp is None:
            return None
        return type_validate_python(InteractionResponse, resp)

    async def _api_get_origin_interaction_response(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = None,
    ) -> MessageGet:
        """Get the original interaction response.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#get-original-interaction-response
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/@original",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_edit_origin_interaction_response(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        content: MissingOrNullable[str] = UNSET,
        embeds: MissingOrNullable[list[Embed]] = UNSET,
        flags: MissingOrNullable[MessageFlag] = UNSET,
        allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
        components: MissingOrNullable[list[Component]] = UNSET,
        files: Missing[list[File]] = UNSET,
        attachments: MissingOrNullable[list[AttachmentSend]] = UNSET,
        poll: MissingOrNullable[PollRequest] = UNSET,
    ) -> MessageGet:
        """Edit the original interaction response.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#edit-original-interaction-response
        """
        params: dict[str, Any] = {"thread_id": thread_id}
        if with_components is not None:
            params["with_components"] = str(with_components).lower()
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "content": content,
            "embeds": embeds,
            "flags": flags,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "poll": poll,
        }
        request_kwargs = parse_data(
            data,
            WebhookMessageEditParams,
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
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_delete_origin_interaction_response(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = None,
    ) -> None:
        """Delete the original interaction response.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#delete-original-interaction-response
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/@original",
            params={key: value for key, value in params.items() if value is not None},
        )
        await _request(self, request)

    async def _api_create_followup_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        content: str | None = None,
        tts: bool | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: AllowedMention | None = None,
        components: list[Component] | None = None,
        files: list[File] | None = None,
        attachments: list[AttachmentSend] | None = None,
        flags: int | None = None,
    ) -> MessageGet:
        """Create a followup message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message
        """
        has_payload = any(
            [
                bool(content),
                bool(embeds),
                bool(components),
                bool(files),
            ]
        )
        if not has_payload:
            msg = "content/embeds/components/files is required"
            raise ValueError(msg)
        data = {
            "content": content,
            "tts": tts,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "flags": flags,
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
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_get_followup_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
    ) -> MessageGet:
        """Get a followup message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#get-followup-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_edit_followup_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        content: MissingOrNullable[str] = UNSET,
        embeds: MissingOrNullable[list[Embed]] = UNSET,
        flags: MissingOrNullable[MessageFlag] = UNSET,
        allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
        components: MissingOrNullable[list[Component]] = UNSET,
        files: Missing[list[File]] = UNSET,
        attachments: MissingOrNullable[list[AttachmentSend]] = UNSET,
        poll: MissingOrNullable[PollRequest] = UNSET,
    ) -> MessageGet:
        """Edit a followup message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#edit-followup-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params: dict[str, Any] = {"thread_id": thread_id}
        if with_components is not None:
            params["with_components"] = str(with_components).lower()
        data = {
            "content": content,
            "embeds": embeds,
            "flags": flags,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "poll": poll,
        }
        request_kwargs = parse_data(
            data,
            WebhookMessageEditParams,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
            params={key: value for key, value in params.items() if value is not None},
            json=request_kwargs.get("json"),
            files=request_kwargs.get("files"),
        )
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_delete_followup_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
    ) -> None:
        """Delete a followup message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#delete-followup-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        await _request(self, request)

    # Application

    # see https://discord.com/developers/docs/resources/application
    async def _api_get_current_application(
        self: AdapterProtocol,
        bot: "Bot",
    ) -> Application:
        """Get current application.

        see https://discord.com/developers/docs/resources/application#get-current-application
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "applications/@me",
        )
        return type_validate_python(Application, await _request(self, request))

    async def _api_edit_current_application(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        custom_install_url: Missing[str] = UNSET,
        description: Missing[str] = UNSET,
        role_connections_verification_url: Missing[str] = UNSET,
        install_params: Missing[InstallParams] = UNSET,
        integration_types_config: Missing[
            dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration]
        ] = UNSET,
        flags: Missing[ApplicationFlag] = UNSET,
        icon: MissingOrNullable[str] = UNSET,
        cover_image: MissingOrNullable[str] = UNSET,
        interactions_endpoint_url: Missing[str] = UNSET,
        tags: Missing[list[str]] = UNSET,
        event_webhooks_url: Missing[str] = UNSET,
        event_webhooks_status: Missing[int] = UNSET,
        event_webhooks_types: Missing[list[str]] = UNSET,
    ) -> Application:
        """Edit current application.

        see https://discord.com/developers/docs/resources/application#edit-current-application
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                EditCurrentApplicationParams,
                {
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
                    "event_webhooks_url": event_webhooks_url,
                    "event_webhooks_status": event_webhooks_status,
                    "event_webhooks_types": event_webhooks_types,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / "applications/@me",
            json=data,
        )
        return type_validate_python(Application, await _request(self, request))

    async def _api_get_application_activity_instance(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        instance_id: str,
    ) -> ActivityInstance:
        """Get application activity instance.

        see https://discord.com/developers/docs/resources/application#get-application-activity-instance
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/activity-instances/{instance_id}",
        )
        return type_validate_python(ActivityInstance, await _request(self, request))

    # Application Role Connection Metadata

    # see https://discord.com/developers/docs/resources/application-role-connection-metadata
    async def _api_get_application_role_connection_metadata_records(
        self: AdapterProtocol, bot: "Bot", *, application_id: SnowflakeType
    ) -> list[ApplicationRoleConnectionMetadata]:
        """Get application role connection metadata records.

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
            await _request(self, request),
        )

    @validate
    async def _api_update_application_role_connection_metadata_records(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        records: Annotated[
            list[ApplicationRoleConnectionMetadata],
            Range(message="metadata records must be 0-5 items", max_length=5),
        ],
    ) -> list[ApplicationRoleConnectionMetadata]:
        """Update application role connection metadata records.

        see https://discord.com/developers/docs/resources/application-role-connection-metadata#update-application-role-connection-metadata-records
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        payload = [
            model_dump(
                type_validate_python(ApplicationRoleConnectionMetadata, record),
                omit_unset_values=True,
            )
            for record in records
        ]
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/role-connections/metadata",
            json=payload,
        )
        return type_validate_python(
            list[ApplicationRoleConnectionMetadata],
            await _request(self, request),
        )

    # Audit Logs

    # see https://discord.com/developers/docs/resources/audit-log
    @overload
    async def _api_get_guild_audit_log(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: SnowflakeType | None = None,
        after: None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog: ...

    @overload
    async def _api_get_guild_audit_log(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog: ...

    @validate(
        cross_rules=(
            AtMostOne(
                fields=("before", "after"),
                message="before and after are mutually exclusive",
            ),
        )
    )
    async def _api_get_guild_audit_log(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog:
        """Get guild audit log.

        see https://discord.com/developers/docs/resources/audit-log#get-guild-audit-log
        """
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
        return type_validate_python(AuditLog, await _request(self, request))

    # Auto Moderation

    # see https://discord.com/developers/docs/resources/auto-moderation
    async def _api_list_auto_moderation_rules_for_guild(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[AutoModerationRule]:
        """List auto moderation rules for guild.

        see https://discord.com/developers/docs/resources/auto-moderation#list-auto-moderation-rules-for-guild
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules",
        )
        return type_validate_python(
            list[AutoModerationRule], await _request(self, request)
        )

    async def _api_get_auto_moderation_rule(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
    ) -> AutoModerationRule:
        """Get auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#get-auto-moderation-rule
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
        )
        return type_validate_python(AutoModerationRule, await _request(self, request))

    @overload
    async def _api_create_auto_moderation_rule(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: Literal[TriggerType.SPAM],
        actions: list[AutoModerationAction],
        trigger_metadata: None = None,
        enabled: bool | None = None,
        exempt_roles: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_roles must be 20 items or fewer", max_length=20),
        ] = None,
        exempt_channels: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_channels must be 50 items or fewer", max_length=50),
        ] = None,
        reason: str | None = None,
    ) -> AutoModerationRule: ...

    @overload
    async def _api_create_auto_moderation_rule(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: NonSpamTriggerType,
        actions: list[AutoModerationAction],
        trigger_metadata: TriggerMetadata,
        enabled: bool | None = None,
        exempt_roles: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_roles must be 20 items or fewer", max_length=20),
        ] = None,
        exempt_channels: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_channels must be 50 items or fewer", max_length=50),
        ] = None,
        reason: str | None = None,
    ) -> AutoModerationRule: ...

    @validate(
        cross_rules=(
            ForbidIfEquals(
                field="trigger_metadata",
                when_field="trigger_type",
                equals=TriggerType.SPAM,
                message="trigger_metadata must be omitted for SPAM rules",
            ),
            RequireIfNotEquals(
                field="trigger_metadata",
                when_field="trigger_type",
                equals=TriggerType.SPAM,
                message="trigger_metadata is required for this trigger_type",
            ),
        )
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
        trigger_metadata: TriggerMetadata | None = None,
        enabled: bool | None = None,
        exempt_roles: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_roles must be 20 items or fewer", max_length=20),
        ] = None,
        exempt_channels: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_channels must be 50 items or fewer", max_length=50),
        ] = None,
        reason: str | None = None,
    ) -> AutoModerationRule:
        """Create auto moderation rule.

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
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules",
            json=data,
        )
        return type_validate_python(AutoModerationRule, await _request(self, request))

    @validate
    async def _api_modify_auto_moderation_rule(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        name: str | None = None,
        event_type: AutoModerationRuleEventType | None = None,
        trigger_metadata: TriggerMetadata | None = None,
        actions: list[AutoModerationAction] | None = None,
        enabled: bool | None = None,
        exempt_roles: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_roles must be 20 items or fewer", max_length=20),
        ] = None,
        exempt_channels: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_channels must be 50 items or fewer", max_length=50),
        ] = None,
        reason: str | None = None,
    ) -> AutoModerationRule:
        """Modify auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "event_type": event_type,
            "trigger_metadata": trigger_metadata,
            "actions": actions,
            "enabled": enabled,
            "exempt_roles": exempt_roles,
            "exempt_channels": exempt_channels,
        }
        data = model_dump(
            type_validate_python(
                CreateAndModifyAutoModerationRuleParams,
                {key: value for key, value in data.items() if value is not None},
            ),
            exclude_none=True,
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
            json=data,
        )
        return type_validate_python(AutoModerationRule, await _request(self, request))

    async def _api_delete_auto_moderation_rule(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete auto moderation rule.

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
        await _request(self, request)

    # Channels

    # see https://discord.com/developers/docs/resources/channel
    async def _api_get_channel(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> Channel:
        """Get a channel by ID.

        see https://discord.com/developers/docs/resources/channel#get-channel
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}",
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_modify_DM(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: str | None = None,
        icon: bytes | None = None,
        reason: str | None = None,
    ) -> Channel:
        """Update a Group DM channel's settings.

        see https://discord.com/developers/docs/resources/channel#modify-channel
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "name": name,
            "icon": _encode_image_data_uri(image=icon) if icon is not None else None,
        }
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_modify_channel(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: Missing[str] = UNSET,
        type: Missing[ChannelType] = UNSET,  # noqa: A002
        position: MissingOrNullable[int] = UNSET,
        topic: MissingOrNullable[str] = UNSET,
        nsfw: MissingOrNullable[bool] = UNSET,
        rate_limit_per_user: MissingOrNullable[int] = UNSET,
        bitrate: MissingOrNullable[int] = UNSET,
        user_limit: MissingOrNullable[int] = UNSET,
        permission_overwrites: MissingOrNullable[list[PartialOverwrite]] = UNSET,
        parent_id: MissingOrNullable[SnowflakeType] = UNSET,
        rtc_region: MissingOrNullable[str] = UNSET,
        video_quality_mode: MissingOrNullable[VideoQualityMode] = UNSET,
        default_auto_archive_duration: MissingOrNullable[int] = UNSET,
        flags: Missing[ChannelFlags] = UNSET,
        available_tags: Missing[list[ForumTagRequest]] = UNSET,
        default_reaction_emoji: MissingOrNullable[DefaultReaction] = UNSET,
        default_thread_rate_limit_per_user: Missing[int] = UNSET,
        default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET,
        default_forum_layout: Missing[ForumLayoutTypes] = UNSET,
        reason: str | None = None,
    ) -> Channel:
        """Update a channel's settings.

        see https://discord.com/developers/docs/resources/channel#modify-channel
        """
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
                data,
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_modify_thread(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: Missing[str] = UNSET,
        archived: Missing[bool] = UNSET,
        auto_archive_duration: Missing[int] = UNSET,
        locked: Missing[bool] = UNSET,
        invitable: Missing[bool] = UNSET,
        rate_limit_per_user: MissingOrNullable[int] = UNSET,
        flags: Missing[ChannelFlags] = UNSET,
        applied_tags: Missing[list[SnowflakeType]] = UNSET,
        reason: str | None = None,
    ) -> Channel:
        """Update a thread's settings.

        see https://discord.com/developers/docs/resources/channel#modify-channel
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                ModifyThreadParams,
                {
                    "name": name,
                    "archived": archived,
                    "auto_archive_duration": auto_archive_duration,
                    "locked": locked,
                    "invitable": invitable,
                    "rate_limit_per_user": rate_limit_per_user,
                    "flags": flags,
                    "applied_tags": applied_tags,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_delete_channel(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
    ) -> Channel:
        """Delete or close a channel.

        see https://discord.com/developers/docs/resources/channel#delete/close-channel
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}",
        )
        return type_validate_python(Channel, await _request(self, request))

    # Messages

    # see https://discord.com/developers/docs/resources/message
    @overload
    async def _api_get_channel_messages(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: SnowflakeType | None = None,
        before: None = None,
        after: None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[MessageGet]: ...

    @overload
    async def _api_get_channel_messages(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: None = None,
        before: SnowflakeType | None = None,
        after: None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[MessageGet]: ...

    @overload
    async def _api_get_channel_messages(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: None = None,
        before: None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[MessageGet]: ...

    @validate(
        cross_rules=(
            AtMostOne(
                fields=("around", "before", "after"),
                message="around, before and after are mutually exclusive",
            ),
        )
    )
    async def _api_get_channel_messages(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: SnowflakeType | None = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[MessageGet]:
        """Get channel messages.

        see https://discord.com/developers/docs/resources/message#get-channel-messages
        """
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
        return type_validate_python(list[MessageGet], await _request(self, request))

    async def _api_get_channel_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """Get a channel message.

        see https://discord.com/developers/docs/resources/message#get-channel-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
        )
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_create_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        content: str | None = None,
        nonce: int | str | None = None,
        enforce_nonce: bool | None = None,
        tts: bool | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: AllowedMention | None = None,
        message_reference: MessageReference | None = None,
        components: list[DirectComponent] | None = None,
        sticker_ids: list[SnowflakeType] | None = None,
        files: list[File] | None = None,
        attachments: list[AttachmentSend] | None = None,
        flags: MessageFlag | None = None,
        poll: PollRequest | None = None,
    ) -> MessageGet:
        """Create a message.

        see https://discord.com/developers/docs/resources/message#create-message
        """
        has_payload = any(
            [
                bool(content),
                bool(embeds),
                bool(sticker_ids),
                bool(components),
                bool(files),
                poll is not None,
            ]
        )
        if not has_payload and (
            message_reference is None
            or message_reference.type != MessageReferenceType.FORWARD
        ):
            msg = "content/embeds/sticker_ids/components/files/poll is required"
            raise ValueError(msg)
        data = {
            "content": content,
            "nonce": nonce,
            "enforce_nonce": enforce_nonce,
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
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_crosspost_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """Crosspost a message.

        see https://discord.com/developers/docs/resources/message#crosspost-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/crosspost",
        )
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_create_reaction(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """Create a reaction.

        see https://discord.com/developers/docs/resources/message#create-reaction
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
                suffix="@me",
            ),
        )
        await _request(self, request)

    async def _api_delete_own_reaction(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """Delete own reaction.

        see https://discord.com/developers/docs/resources/message#delete-own-reaction
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
                suffix="@me",
            ),
        )
        await _request(self, request)

    async def _api_delete_user_reaction(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        user_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """Delete a user reaction.

        see https://discord.com/developers/docs/resources/message#delete-user-reaction
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
                suffix=str(user_id),
            ),
        )
        await _request(self, request)

    @validate
    async def _api_get_reactions(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
        type: ReactionType | None = None,  # noqa: A002
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[User]:
        """Get reactions.

        see https://discord.com/developers/docs/resources/message#get-reactions
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"after": after, "limit": limit, "type": type}
        request = Request(
            headers=headers,
            method="GET",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
            ),
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(list[User], await _request(self, request))

    async def _api_delete_all_reactions(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> None:
        """Delete all reactions.

        see https://discord.com/developers/docs/resources/message#delete-all-reactions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/reactions",
        )
        await _request(self, request)

    async def _api_delete_all_reactions_for_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """Delete all reactions for emoji.

        see https://discord.com/developers/docs/resources/message#delete-all-reactions-for-emoji
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
            ),
        )
        await _request(self, request)

    async def _api_edit_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        content: MissingOrNullable[str] = UNSET,
        embeds: MissingOrNullable[list[Embed]] = UNSET,
        flags: MissingOrNullable[MessageFlag] = UNSET,
        allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
        components: MissingOrNullable[list[Component]] = UNSET,
        files: Missing[list[File]] = UNSET,
        attachments: MissingOrNullable[list[AttachmentSend]] = UNSET,
        sticker_ids: Missing[list[SnowflakeType]] = UNSET,
        poll: MissingOrNullable[PollRequest] = UNSET,
    ) -> MessageGet:
        """Edit a message.

        see https://discord.com/developers/docs/resources/message#edit-message
        """
        data = {
            "content": content,
            "embeds": embeds,
            "flags": flags,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "sticker_ids": sticker_ids,
            "poll": poll,
        }
        params = parse_data(
            data,
            MessageEditParams,
        )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
            json=params.get("json"),
            files=params.get("files"),
        )
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_delete_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete a message.

        see https://discord.com/developers/docs/resources/message#delete-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
        )
        await _request(self, request)

    @validate
    async def _api_bulk_delete_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        messages: Annotated[
            list[SnowflakeType],
            Range(
                message="messages must contain 2-100 items",
                min_length=2,
                max_length=100,
            ),
        ],
        reason: str | None = None,
    ) -> None:
        """Bulk delete messages.

        see https://discord.com/developers/docs/resources/message#bulk-delete-messages
        """
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
        await _request(self, request)

    async def _api_edit_channel_permissions(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        overwrite_id: SnowflakeType,
        allow: str | None = None,
        deny: str | None = None,
        type: OverwriteType,  # noqa: A002
        reason: str | None = None,
    ) -> None:
        """Edit channel permissions.

        see https://discord.com/developers/docs/resources/channel#edit-channel-permissions
        """
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
        await _request(self, request)

    async def _api_get_channel_invites(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[Invite]:
        """Get channel invites.

        see https://discord.com/developers/docs/resources/channel#get-channel-invites
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/invites",
        )
        return type_validate_python(list[Invite], await _request(self, request))

    async def _api_create_channel_invite(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        max_age: int | None = None,
        max_uses: int | None = None,
        temporary: bool | None = None,
        unique: bool | None = None,
        target_type: InviteTargetType | None = None,
        target_user_id: SnowflakeType | None = None,
        target_application_id: SnowflakeType | None = None,
        target_users_file: File | None = None,
        role_ids: list[SnowflakeType] | None = None,
        reason: str | None = None,
    ) -> Invite:
        """Create channel invite.

        see https://discord.com/developers/docs/resources/channel#create-channel-invite
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        if target_type == InviteTargetType.STREAM and target_user_id is None:
            msg = "target_user_id is required when target_type is STREAM"
            raise ValueError(msg)
        if (
            target_type == InviteTargetType.EMBEDDED_APPLICATION
            and target_application_id is None
        ):
            msg = "target_application_id is required when target_type is EMBEDDED_APPLICATION"
            raise ValueError(msg)
        data = {
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary,
            "unique": unique,
            "target_type": target_type,
            "target_user_id": target_user_id,
            "target_application_id": target_application_id,
            "role_ids": role_ids,
        }
        payload = {key: value for key, value in data.items() if value is not None}
        if target_users_file is not None:
            multipart = {
                "target_users_file": (
                    target_users_file.filename,
                    target_users_file.content,
                ),
                "payload_json": (None, json.dumps(payload), "application/json"),
            }
            request = Request(
                headers=headers,
                method="POST",
                url=self.base_url / f"channels/{channel_id}/invites",
                files=multipart,
            )
        else:
            request = Request(
                headers=headers,
                method="POST",
                url=self.base_url / f"channels/{channel_id}/invites",
                json=payload,
            )
        return type_validate_python(Invite, await _request(self, request))

    async def _api_delete_channel_permission(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        overwrite_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete channel permission.

        see https://discord.com/developers/docs/resources/channel#delete-channel-permission
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/permissions/{overwrite_id}",
        )
        await _request(self, request)

    async def _api_follow_announcement_channel(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        webhook_channel_id: SnowflakeType,
        reason: str | None = None,
    ) -> FollowedChannel:
        """Follow announcement channel.

        see https://discord.com/developers/docs/resources/channel#follow-announcement-channel
        """
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
        return type_validate_python(FollowedChannel, await _request(self, request))

    async def _api_trigger_typing_indicator(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """Trigger typing indicator.

        see https://discord.com/developers/docs/resources/channel#trigger-typing-indicator
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/typing",
        )
        await _request(self, request)

    async def _api_get_pinned_messages(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[MessageGet]:
        """Get pinned messages.

        see https://discord.com/developers/docs/resources/message#get-channel-pins
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/messages/pins",
        )
        return type_validate_python(list[MessageGet], await _request(self, request))

    async def _api_pin_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Pin message.

        see https://discord.com/developers/docs/resources/message#pin-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/messages/pins/{message_id}",
        )
        await _request(self, request)

    async def _api_unpin_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Unpin message.

        see https://discord.com/developers/docs/resources/message#unpin-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/messages/pins/{message_id}",
        )
        await _request(self, request)

    async def _api_group_DM_add_recipient(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
        access_token: str,
        nick: str,
    ) -> None:
        """Group DM add recipient.

        see https://discord.com/developers/docs/resources/channel#group-dm-add-recipient
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"access_token": access_token, "nick": nick}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/recipients/{user_id}",
            json=data,
        )
        await _request(self, request)

    async def _api_group_DM_remove_recipient(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """Group DM remove recipient.

        see https://discord.com/developers/docs/resources/channel#group-dm-remove-recipient
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/recipients/{user_id}",
        )
        await _request(self, request)

    async def _api_start_thread_from_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        name: str,
        auto_archive_duration: Missing[int] = UNSET,
        rate_limit_per_user: MissingOrNullable[int] = UNSET,
        reason: str | None = None,
    ) -> Channel:
        """Start thread from message.

        see https://discord.com/developers/docs/resources/channel#start-thread-from-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                StartThreadFromMessageParams,
                {
                    "name": name,
                    "auto_archive_duration": auto_archive_duration,
                    "rate_limit_per_user": rate_limit_per_user,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}/threads",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_start_thread_without_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: str,
        auto_archive_duration: Missing[int] = UNSET,
        type: Missing[ChannelType] = UNSET,  # noqa: A002
        invitable: Missing[bool] = UNSET,
        rate_limit_per_user: MissingOrNullable[int] = UNSET,
        reason: str | None = None,
    ) -> Channel:
        """Start thread without message.

        see https://discord.com/developers/docs/resources/channel#start-thread-without-message
        """
        if type is not UNSET and type not in (
            ChannelType.ANNOUNCEMENT_THREAD,
            ChannelType.PUBLIC_THREAD,
            ChannelType.PRIVATE_THREAD,
        ):
            msg = "type must be ANNOUNCEMENT_THREAD, PUBLIC_THREAD or PRIVATE_THREAD"
            raise ValueError(msg)
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                StartThreadWithoutMessageParams,
                {
                    "name": name,
                    "auto_archive_duration": auto_archive_duration,
                    "type": type,
                    "invitable": invitable,
                    "rate_limit_per_user": rate_limit_per_user,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/threads",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_start_thread_in_forum_channel(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: str,
        auto_archive_duration: Missing[int] = UNSET,
        rate_limit_per_user: MissingOrNullable[int] = UNSET,
        applied_tags: Missing[list[SnowflakeType]] = UNSET,
        content: str | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: AllowedMention | None = None,
        components: list[DirectComponent] | None = None,
        sticker_ids: list[SnowflakeType] | None = None,
        files: list[File] | None = None,
        attachments: list[AttachmentSend] | None = None,
        flags: MessageFlag | None = None,
        reason: str | None = None,
    ) -> Channel:
        """Start thread in forum or media channel.

        see https://discord.com/developers/docs/resources/channel#start-thread-in-forum-or-media-channel
        """
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
        return type_validate_python(Channel, await _request(self, request))

    async def _api_join_thread(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """Join thread.

        see https://discord.com/developers/docs/resources/channel#join-thread
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/thread-members/@me",
        )
        await _request(self, request)

    async def _api_add_thread_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """Add thread member.

        see https://discord.com/developers/docs/resources/channel#add-thread-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
        )
        await _request(self, request)

    async def _api_leave_thread(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """Leave thread.

        see https://discord.com/developers/docs/resources/channel#leave-thread
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/thread-members/@me",
        )
        await _request(self, request)

    async def _api_remove_thread_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """Remove thread member.

        see https://discord.com/developers/docs/resources/channel#remove-thread-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
        )
        await _request(self, request)

    async def _api_get_thread_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
        with_member: bool | None = None,
    ) -> ThreadMember:
        """Get thread member.

        see https://discord.com/developers/docs/resources/channel#get-thread-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_member": _bool_query(value=with_member)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(ThreadMember, await _request(self, request))

    @validate
    async def _api_list_thread_members(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        with_member: bool | None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[ThreadMember]:
        """List thread members.

        see https://discord.com/developers/docs/resources/channel#list-thread-members
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "with_member": _bool_query(value=with_member),
            "after": after,
            "limit": limit,
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/thread-members",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(list[ThreadMember], await _request(self, request))

    async def _api_list_public_archived_threads(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        before: datetime | None = None,
        limit: int | None = None,
    ) -> ArchivedThreadsResponse:
        """List public archived threads.

        see https://discord.com/developers/docs/resources/channel#list-public-archived-threads
        """
        params = {"before": before, "limit": limit}
        if params["before"]:
            before_utc = params["before"]
            if before_utc.tzinfo is None:
                before_utc = before_utc.replace(tzinfo=timezone.utc)
            else:
                before_utc = before_utc.astimezone(timezone.utc)
            params["before"] = before_utc.isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/threads/archived/public",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            ArchivedThreadsResponse, await _request(self, request)
        )

    async def _api_list_private_archived_threads(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        before: datetime | None = None,
        limit: int | None = None,
    ) -> ArchivedThreadsResponse:
        """List private archived threads.

        see https://discord.com/developers/docs/resources/channel#list-private-archived-threads
        """
        params = {"before": before, "limit": limit}
        if params["before"]:
            before_utc = params["before"]
            if before_utc.tzinfo is None:
                before_utc = before_utc.replace(tzinfo=timezone.utc)
            else:
                before_utc = before_utc.astimezone(timezone.utc)
            params["before"] = before_utc.isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/threads/archived/private",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            ArchivedThreadsResponse, await _request(self, request)
        )

    async def _api_list_joined_private_archived_threads(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        before: SnowflakeType | None = None,
        limit: int | None = None,
    ) -> ArchivedThreadsResponse:
        """List joined private archived threads.

        see https://discord.com/developers/docs/resources/channel#list-joined-private-archived-threads
        """
        params = {"before": before, "limit": limit}
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"channels/{channel_id}/users/@me/threads/archived/private",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            ArchivedThreadsResponse, await _request(self, request)
        )

    # Emoji

    # see https://discord.com/developers/docs/resources/emoji
    async def _api_list_guild_emojis(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Emoji]:
        """List guild emojis.

        see https://discord.com/developers/docs/resources/emoji#list-guild-emojis
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/emojis",
        )
        return type_validate_python(list[Emoji], await _request(self, request))

    async def _api_get_guild_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> Emoji:
        """Get guild emoji.

        see https://discord.com/developers/docs/resources/emoji#get-guild-emoji
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
        )
        return type_validate_python(Emoji, await _request(self, request))

    async def _api_create_guild_emoji(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        image: str,
        roles: list[SnowflakeType] | None = None,
        reason: str | None = None,
    ) -> Emoji:
        """Create guild emoji.

        see https://discord.com/developers/docs/resources/emoji#create-guild-emoji
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        if not name:
            msg = "name is required"
            raise ValueError(msg)
        if not image:
            msg = "image is required"
            raise ValueError(msg)
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
        return type_validate_python(Emoji, await _request(self, request))

    async def _api_modify_guild_emoji(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
        name: Missing[str] = UNSET,
        roles: MissingOrNullable[list[SnowflakeType]] = UNSET,
        reason: str | None = None,
    ) -> Emoji:
        """Modify guild emoji.

        see https://discord.com/developers/docs/resources/emoji#modify-guild-emoji
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                ModifyGuildEmojiParams, {"name": name, "roles": roles}
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
            json=data,
        )
        return type_validate_python(Emoji, await _request(self, request))

    async def _api_delete_guild_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete guild emoji.

        see https://discord.com/developers/docs/resources/emoji#delete-guild-emoji
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
        )
        await _request(self, request)

    async def _api_list_application_emojis(
        self: AdapterProtocol, bot: "Bot", *, application_id: SnowflakeType
    ) -> ApplicationEmojis:
        """List application emojis.

        see https://discord.com/developers/docs/resources/emoji#list-application-emojis
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/emojis",
        )
        return type_validate_python(ApplicationEmojis, await _request(self, request))

    async def _api_get_application_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> Emoji:
        """Get application emoji.

        see https://discord.com/developers/docs/resources/emoji#get-application-emoji
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
        )
        return type_validate_python(Emoji, await _request(self, request))

    async def _api_create_application_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        name: str,
        image: str,
    ) -> Emoji:
        """Create application emoji.

        see https://discord.com/developers/docs/resources/emoji#create-application-emoji
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if not name:
            msg = "name is required"
            raise ValueError(msg)
        if not image:
            msg = "image is required"
            raise ValueError(msg)
        data = {"name": name, "image": image}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"applications/{application_id}/emojis",
            json=data,
        )
        return type_validate_python(Emoji, await _request(self, request))

    async def _api_modify_application_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
        name: str,
    ) -> Emoji:
        """Modify application emoji.

        see https://discord.com/developers/docs/resources/emoji#modify-application-emoji
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
            json={"name": name},
        )
        return type_validate_python(Emoji, await _request(self, request))

    async def _api_delete_application_emoji(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> None:
        """Delete application emoji.

        see https://discord.com/developers/docs/resources/emoji#delete-application-emoji
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
        )
        await _request(self, request)

    # Soundboard
    # see https://discord.com/developers/docs/resources/soundboard
    async def _api_send_soundboard_sound(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        sound_id: SnowflakeType,
        source_guild_id: Missing[SnowflakeType] = UNSET,
    ) -> None:
        """Send soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#send-soundboard-sound
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                SendSoundboardSoundParams,
                {
                    "sound_id": sound_id,
                    "source_guild_id": source_guild_id,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/send-soundboard-sound",
            json=data,
        )
        await _request(self, request)

    async def _api_list_default_soundboard_sounds(
        self: AdapterProtocol, bot: "Bot"
    ) -> ListDefaultSoundboardSoundsResponse:
        """List default soundboard sounds.

        see https://discord.com/developers/docs/resources/soundboard#list-default-soundboard-sounds
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "soundboard-default-sounds",
        )
        return type_validate_python(
            ListDefaultSoundboardSoundsResponse, await _request(self, request)
        )

    async def _api_list_guild_soundboard_sounds(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
    ) -> ListGuildSoundboardSoundsResponse:
        """List guild soundboard sounds.

        see https://discord.com/developers/docs/resources/soundboard#list-guild-soundboard-sounds
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds",
        )
        return type_validate_python(
            ListGuildSoundboardSoundsResponse, await _request(self, request)
        )

    async def _api_get_guild_soundboard_sound(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sound_id: SnowflakeType,
    ) -> SoundboardSound:
        """Get guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#get-guild-soundboard-sound
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds/{sound_id}",
        )
        return type_validate_python(SoundboardSound, await _request(self, request))

    async def _api_create_guild_soundboard_sound(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        sound: str,
        volume: Missing[float] = UNSET,
        emoji_id: Missing[SnowflakeType] = UNSET,
        emoji_name: Missing[str] = UNSET,
    ) -> SoundboardSound:
        """Create guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#create-guild-soundboard-sound
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                CreateGuildSoundboardSoundParams,
                {
                    "name": name,
                    "sound": sound,
                    "volume": volume,
                    "emoji_id": emoji_id,
                    "emoji_name": emoji_name,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds",
            json=data,
        )
        return type_validate_python(SoundboardSound, await _request(self, request))

    async def _api_modify_guild_soundboard_sound(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sound_id: SnowflakeType,
        name: Missing[str] = UNSET,
        volume: Missing[float] = UNSET,
        emoji_id: MissingOrNullable[SnowflakeType] = UNSET,
        emoji_name: MissingOrNullable[str] = UNSET,
    ) -> SoundboardSound:
        """Modify guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#modify-guild-soundboard-sound
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                ModifyGuildSoundboardSoundParams,
                {
                    "name": name,
                    "volume": volume,
                    "emoji_id": emoji_id,
                    "emoji_name": emoji_name,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds/{sound_id}",
            json=data,
        )
        return type_validate_python(SoundboardSound, await _request(self, request))

    async def _api_delete_guild_soundboard_sound(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sound_id: SnowflakeType,
    ) -> None:
        """Delete guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#delete-guild-soundboard-sound
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds/{sound_id}",
        )
        await _request(self, request)

    # Lobby
    # see https://discord.com/developers/docs/resources/lobby
    async def _api_create_lobby(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        metadata: Missing[dict[str, str]] = UNSET,
        members: Missing[list[CreateLobbyMemberParams]] = UNSET,
        idle_timeout_seconds: Missing[int] = UNSET,
    ) -> Lobby:
        """Create lobby.

        see https://discord.com/developers/docs/resources/lobby#create-lobby
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                CreateLobbyParams,
                {
                    "metadata": metadata,
                    "members": members,
                    "idle_timeout_seconds": idle_timeout_seconds,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / "lobbies",
            json=data,
        )
        return type_validate_python(Lobby, await _request(self, request))

    async def _api_get_lobby(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
    ) -> Lobby:
        """Get lobby.

        see https://discord.com/developers/docs/resources/lobby#get-lobby
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"lobbies/{lobby_id}",
        )
        return type_validate_python(Lobby, await _request(self, request))

    async def _api_modify_lobby(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
        metadata: MissingOrNullable[dict[str, str]] = UNSET,
        idle_timeout_seconds: Missing[int] = UNSET,
    ) -> Lobby:
        """Modify lobby.

        see https://discord.com/developers/docs/resources/lobby#modify-lobby
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                ModifyLobbyParams,
                {
                    "metadata": metadata,
                    "idle_timeout_seconds": idle_timeout_seconds,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"lobbies/{lobby_id}",
            json=data,
        )
        return type_validate_python(Lobby, await _request(self, request))

    async def _api_delete_lobby(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
    ) -> None:
        """Delete lobby.

        see https://discord.com/developers/docs/resources/lobby#delete-lobby
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"lobbies/{lobby_id}",
        )
        await _request(self, request)

    async def _api_add_lobby_member(
        self: AdapterProtocol,
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
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                AddLobbyMemberParams,
                {
                    "metadata": metadata,
                    "flags": flags,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"lobbies/{lobby_id}/members/{user_id}",
            json=data,
        )
        return type_validate_python(LobbyMember, await _request(self, request))

    async def _api_remove_lobby_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """Remove lobby member.

        see https://discord.com/developers/docs/resources/lobby#remove-lobby-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"lobbies/{lobby_id}/members/{user_id}",
        )
        await _request(self, request)

    async def _api_leave_lobby(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
    ) -> None:
        """Leave lobby.

        see https://discord.com/developers/docs/resources/lobby#leave-lobby
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"lobbies/{lobby_id}/members/@me",
        )
        await _request(self, request)

    async def _api_link_channel_to_lobby(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        lobby_id: SnowflakeType,
        channel_id: MissingOrNullable[SnowflakeType] = UNSET,
    ) -> Lobby:
        """Link channel to lobby.

        see https://discord.com/developers/docs/resources/lobby#link-channel-to-lobby
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                LinkChannelToLobbyParams,
                {
                    "channel_id": channel_id,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"lobbies/{lobby_id}/channel-linking",
            json=data,
        )
        return type_validate_python(Lobby, await _request(self, request))

    # Entitlements

    # see https://discord.com/developers/docs/resources/entitlement
    async def _api_list_entitlements(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        sku_ids: tuple[SnowflakeType] | None = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: int | None = None,
        guild_id: SnowflakeType | None = None,
        exclude_ended: bool | None = None,
        exclude_deleted: bool | None = None,
    ) -> list[Entitlement]:
        """List entitlements.

        see https://discord.com/developers/docs/resources/entitlement#list-entitlements
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "user_id": user_id,
            "sku_ids": ",".join(str(sku_id) for sku_id in sku_ids) if sku_ids else None,
            "before": before,
            "after": after,
            "limit": limit,
            "guild_id": guild_id,
            "exclude_ended": _bool_query(value=exclude_ended),
            "exclude_deleted": _bool_query(value=exclude_deleted),
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/entitlements",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(list[Entitlement], await _request(self, request))

    async def _api_get_entitlement(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        entitlement_id: SnowflakeType,
    ) -> Entitlement:
        """Get entitlement.

        see https://discord.com/developers/docs/resources/entitlement#get-entitlement
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/entitlements/{entitlement_id}",
        )
        return type_validate_python(Entitlement, await _request(self, request))

    async def _api_consume_an_entitlement(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        entitlement_id: SnowflakeType,
    ) -> None:
        """Consume an entitlement.

        see https://discord.com/developers/docs/resources/entitlement#consume-an-entitlement
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url
            / f"applications/{application_id}/entitlements/{entitlement_id}/consume",
        )
        await _request(self, request)

    async def _api_create_test_entitlement(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        sku_id: str,
        owner_id: str,
        owner_type: Literal[1, 2],
    ) -> Entitlement:
        """Create test entitlement.

        see https://discord.com/developers/docs/resources/entitlement#create-test-entitlement
        """
        if owner_type not in (1, 2):
            msg = "owner_type must be 1 or 2"
            raise ValueError(msg)
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
        return type_validate_python(Entitlement, await _request(self, request))

    async def _api_delete_test_entitlement(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        entitlement_id: SnowflakeType,
    ) -> None:
        """Delete test entitlement.

        see https://discord.com/developers/docs/resources/entitlement#delete-test-entitlement
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url
            / f"applications/{application_id}/entitlements/{entitlement_id}",
        )
        await _request(self, request)

    # Guild

    # see https://discord.com/developers/docs/resources/guild
    @deprecated(
        "_api_create_guild (POST /guilds) is deprecated because Discord removed "
        "the endpoint from official bot-facing docs in 2025 "
        "(discord-api-docs #7715/#7720/#7722)."
    )
    async def _api_create_guild(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        name: str,
        region: str | None = None,
        icon: str | None = None,
        verification_level: VerificationLevel | None = None,
        default_message_notifications: DefaultMessageNotificationLevel | None = None,
        explicit_content_filter: ExplicitContentFilterLevel | None = None,
        roles: list[Role] | None = None,
        channels: list[Channel] | None = None,
        afk_channel_id: Snowflake | None = None,
        afk_timeout: int | None = None,
        system_channel_id: Snowflake | None = None,
        system_channel_flags: SystemChannelFlags | None = None,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild"""
        if not name:
            msg = "name is required"
            raise ValueError(msg)
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
            type_validate_python(CreateGuildParams, data), omit_unset_values=True
        )
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers, method="POST", url=self.base_url / "guilds", json=data
        )
        return type_validate_python(Guild, await _request(self, request))

    async def _api_get_guild(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        with_counts: bool | None = None,
    ) -> Guild:
        """Get guild.

        see https://discord.com/developers/docs/resources/guild#get-guild
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_counts": _bool_query(value=with_counts)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(Guild, await _request(self, request))

    async def _api_get_guild_role_member_counts(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
    ) -> dict[Snowflake, int]:
        """Get guild role member counts.

        see https://discord.com/developers/docs/resources/guild#get-guild-role-member-counts
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/roles/member-counts",
        )
        return type_validate_python(dict[Snowflake, int], await _request(self, request))

    async def _api_get_guild_preview(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildPreview:
        """Get guild preview.

        see https://discord.com/developers/docs/resources/guild#get-guild-preview
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/preview",
        )
        return type_validate_python(GuildPreview, await _request(self, request))

    async def _api_modify_guild(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: Missing[str] = UNSET,
        region: MissingOrNullable[str] = UNSET,
        verification_level: MissingOrNullable[VerificationLevel] = UNSET,
        default_message_notifications: MissingOrNullable[
            DefaultMessageNotificationLevel
        ] = UNSET,
        explicit_content_filter: MissingOrNullable[ExplicitContentFilterLevel] = UNSET,
        afk_channel_id: MissingOrNullable[Snowflake] = UNSET,
        afk_timeout: Missing[int] = UNSET,
        icon: MissingOrNullable[str] = UNSET,
        splash: MissingOrNullable[str] = UNSET,
        discovery_splash: MissingOrNullable[str] = UNSET,
        banner: MissingOrNullable[str] = UNSET,
        system_channel_id: MissingOrNullable[Snowflake] = UNSET,
        system_channel_flags: Missing[SystemChannelFlags] = UNSET,
        rules_channel_id: MissingOrNullable[Snowflake] = UNSET,
        public_updates_channel_id: MissingOrNullable[Snowflake] = UNSET,
        preferred_locale: MissingOrNullable[str] = UNSET,
        features: Missing[list[GuildFeature]] = UNSET,
        description: MissingOrNullable[str] = UNSET,
        premium_progress_bar_enabled: Missing[bool] = UNSET,
        safety_alerts_channel_id: MissingOrNullable[Snowflake] = UNSET,
        reason: str | None = None,
    ) -> Guild:
        """Modify guild.

        see https://discord.com/developers/docs/resources/guild#modify-guild
        """
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
            "safety_alerts_channel_id": safety_alerts_channel_id,
        }
        data = model_dump(
            type_validate_python(
                ModifyGuildParams,
                data,
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}",
            json=data,
        )
        return type_validate_python(Guild, await _request(self, request))

    async def _api_modify_guild_incident_actions(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        invites_disabled_until: MissingOrNullable[datetime] = UNSET,
        dms_disabled_until: MissingOrNullable[datetime] = UNSET,
    ) -> GuildIncidentsData:
        """Modify guild incident actions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-incident-actions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                ModifyGuildIncidentActionsParams,
                {
                    "invites_disabled_until": invites_disabled_until,
                    "dms_disabled_until": dms_disabled_until,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/incident-actions",
            json=data,
        )
        return type_validate_python(GuildIncidentsData, await _request(self, request))

    @deprecated(
        "_api_delete_guild (DELETE /guilds/{guild_id}) is deprecated because "
        "Discord removed the endpoint from official bot-facing docs in 2025 "
        "(discord-api-docs #7715/#7720/#7722)."
    )
    async def _api_delete_guild(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/guild"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}",
        )
        await _request(self, request)

    async def _api_get_guild_channels(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Channel]:
        """Get guild channels.

        see https://discord.com/developers/docs/resources/guild#get-guild-channels
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/channels",
        )
        return type_validate_python(list[Channel], await _request(self, request))

    async def _api_create_guild_channel(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        type: ChannelType | None = None,  # noqa: A002
        topic: str | None = None,
        bitrate: int | None = None,
        user_limit: int | None = None,
        rate_limit_per_user: int | None = None,
        position: int | None = None,
        permission_overwrites: list[Overwrite] | None = None,
        parent_id: Snowflake | None = None,
        nsfw: bool | None = None,
        rtc_region: str | None = None,
        video_quality_mode: VideoQualityMode | None = None,
        default_auto_archive_duration: int | None = None,
        default_reaction_emoji: DefaultReaction | None = None,
        available_tags: list[ForumTagRequest] | None = None,
        default_sort_order: SortOrderTypes | None = None,
        reason: str | None = None,
    ) -> Channel:
        """Create guild channel.

        see https://discord.com/developers/docs/resources/guild#create-guild-channel
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        if not name:
            msg = "name is required"
            raise ValueError(msg)
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
            type_validate_python(CreateGuildChannelParams, data), omit_unset_values=True
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/channels",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_modify_guild_channel_positions(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        channels: list[ModifyGuildChannelPositionParams] | None = None,
        id: SnowflakeType | None = None,  # noqa: A002
        position: MissingOrNullable[int] = UNSET,
        lock_permissions: MissingOrNullable[bool] = UNSET,
        parent_id: MissingOrNullable[SnowflakeType] = UNSET,
    ) -> None:
        """Modify guild channel positions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if channels is None:
            if id is None:
                msg = "channels or id must be provided"
                raise ValueError(msg)
            channel = type_validate_python(
                ModifyGuildChannelPositionParams,
                {
                    "id": id,
                    "position": position,
                    "lock_permissions": lock_permissions,
                    "parent_id": parent_id,
                },
            )
            channels = [channel]
        payload = [
            model_dump(
                type_validate_python(ModifyGuildChannelPositionParams, channel),
                omit_unset_values=True,
            )
            for channel in channels
        ]
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/channels",
            json=payload,
        )
        await _request(self, request)

    async def _api_list_active_guild_threads(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> ListActiveGuildThreadsResponse:
        """List active guild threads.

        see https://discord.com/developers/docs/resources/guild#list-active-guild-threads
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/threads/active",
        )
        return type_validate_python(
            ListActiveGuildThreadsResponse, await _request(self, request)
        )

    async def _api_get_guild_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> GuildMember:
        """Get guild member.

        see https://discord.com/developers/docs/resources/guild#get-guild-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
        )
        return type_validate_python(GuildMember, await _request(self, request))

    @validate
    async def _api_list_guild_members(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 1000", ge=1, le=1000),
        ] = None,
        after: SnowflakeType | None = None,
    ) -> list[GuildMember]:
        """List guild members.

        see https://discord.com/developers/docs/resources/guild#list-guild-members
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"limit": limit, "after": after}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(list[GuildMember], await _request(self, request))

    @validate
    async def _api_search_guild_members(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        query: Annotated[str, Range(message="query is required", min_length=1)],
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 1000", ge=1, le=1000),
        ] = None,
    ) -> list[GuildMember]:
        """Search guild members.

        see https://discord.com/developers/docs/resources/guild#search-guild-members
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"query": query, "limit": limit}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members/search",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(list[GuildMember], await _request(self, request))

    async def _api_add_guild_member(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        access_token: str,
        nick: str | None = None,
        roles: list[SnowflakeType] | None = None,
        mute: bool | None = None,
        deaf: bool | None = None,
    ) -> GuildMember | None:
        """Add guild member.

        see https://discord.com/developers/docs/resources/guild#add-guild-member
        """
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
        resp = await _request(self, request)
        if resp:
            return type_validate_python(GuildMember, resp)
        return None

    async def _api_modify_guild_member(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        nick: MissingOrNullable[str] = UNSET,
        roles: MissingOrNullable[list[SnowflakeType]] = UNSET,
        mute: MissingOrNullable[bool] = UNSET,
        deaf: MissingOrNullable[bool] = UNSET,
        channel_id: MissingOrNullable[SnowflakeType] = UNSET,
        communication_disabled_until: MissingOrNullable[datetime] = UNSET,
        flags: MissingOrNullable[GuildMemberFlags] = UNSET,
        reason: str | None = None,
    ) -> GuildMember:
        """Modify guild member.

        see https://discord.com/developers/docs/resources/guild#modify-guild-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                ModifyGuildMemberParams,
                {
                    "nick": nick,
                    "roles": roles,
                    "mute": mute,
                    "deaf": deaf,
                    "channel_id": channel_id,
                    "communication_disabled_until": communication_disabled_until,
                    "flags": flags,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            json=data,
        )
        return type_validate_python(GuildMember, await _request(self, request))

    async def _api_modify_current_member(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        nick: MissingOrNullable[str] = UNSET,
        banner: MissingOrNullable[str] = UNSET,
        avatar: MissingOrNullable[str] = UNSET,
        bio: MissingOrNullable[str] = UNSET,
        reason: str | None = None,
    ) -> GuildMember:
        """Modify current member.

        see https://discord.com/developers/docs/resources/guild#modify-current-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                ModifyCurrentMemberParams,
                {
                    "nick": nick,
                    "banner": banner,
                    "avatar": avatar,
                    "bio": bio,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me",
            json=data,
        )
        return type_validate_python(GuildMember, await _request(self, request))

    async def _api_modify_current_user_nick(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        nick: MissingOrNullable[str] = UNSET,
        reason: str | None = None,
    ) -> GuildMember:
        """Deprecated in favor of Modify Current Member.

        see https://discord.com/developers/docs/resources/guild#modify-current-user-nick
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = omit_unset({"nick": nick})
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me/nick",
            json=data,
        )
        return type_validate_python(GuildMember, await _request(self, request))

    async def _api_add_guild_member_role(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Add guild member role.

        see https://discord.com/developers/docs/resources/guild#add-guild-member-role
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
        )
        await _request(self, request)

    async def _api_remove_guild_member_role(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Remove guild member role.

        see https://discord.com/developers/docs/resources/guild#remove-guild-member-role
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
        )
        await _request(self, request)

    async def _api_remove_guild_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Remove guild member.

        see https://discord.com/developers/docs/resources/guild#remove-guild-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
        )
        await _request(self, request)

    @overload
    async def _api_get_guild_bans(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 1000", ge=1, le=1000),
        ] = None,
        before: SnowflakeType | None = None,
        after: None = None,
    ) -> list[Ban]: ...

    @overload
    async def _api_get_guild_bans(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 1000", ge=1, le=1000),
        ] = None,
        before: None = None,
        after: SnowflakeType | None = None,
    ) -> list[Ban]: ...

    @validate(
        cross_rules=(
            AtMostOne(
                fields=("before", "after"),
                message="before and after are mutually exclusive",
            ),
        )
    )
    async def _api_get_guild_bans(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 1000", ge=1, le=1000),
        ] = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
    ) -> list[Ban]:
        """Get guild bans.

        see https://discord.com/developers/docs/resources/guild#get-guild-bans
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"limit": limit, "before": before, "after": after}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/bans",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(list[Ban], await _request(self, request))

    async def _api_get_guild_ban(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> Ban:
        """Get guild ban.

        see https://discord.com/developers/docs/resources/guild#get-guild-ban
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
        )
        return type_validate_python(Ban, await _request(self, request))

    @overload
    async def _api_create_guild_ban(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        delete_message_days: Annotated[
            int | None,
            Range(message="delete_message_days must be between 0 and 7", ge=0, le=7),
        ] = None,
        delete_message_seconds: None = None,
        reason: str | None = None,
    ) -> None: ...

    @overload
    async def _api_create_guild_ban(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        delete_message_days: None = None,
        delete_message_seconds: Annotated[
            int | None,
            Range(
                message="delete_message_seconds must be between 0 and 604800",
                ge=0,
                le=604800,
            ),
        ] = None,
        reason: str | None = None,
    ) -> None: ...

    @validate(
        cross_rules=(
            AtMostOne(
                fields=("delete_message_days", "delete_message_seconds"),
                message="delete_message_days and delete_message_seconds cannot both be set",
            ),
        )
    )
    async def _api_create_guild_ban(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        delete_message_days: Annotated[
            int | None,
            Range(message="delete_message_days must be between 0 and 7", ge=0, le=7),
        ] = None,
        delete_message_seconds: Annotated[
            int | None,
            Range(
                message="delete_message_seconds must be between 0 and 604800",
                ge=0,
                le=604800,
            ),
        ] = None,
        reason: str | None = None,
    ) -> None:
        """Create guild ban.

        see https://discord.com/developers/docs/resources/guild#create-guild-ban
        """
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
        await _request(self, request)

    async def _api_remove_guild_ban(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Remove guild ban.

        see https://discord.com/developers/docs/resources/guild#remove-guild-ban
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
        )
        await _request(self, request)

    async def _api_bulk_guild_ban(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_ids: list[SnowflakeType],
        delete_message_seconds: int | None = None,
        reason: str | None = None,
    ) -> BulkBan:
        """Bulk guild ban.

        see https://discord.com/developers/docs/resources/guild#bulk-guild-ban
        """
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
        return type_validate_python(BulkBan, await _request(self, request))

    async def _api_get_guild_roles(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Role]:
        """Get guild roles.

        see https://discord.com/developers/docs/resources/guild#get-guild-roles
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/roles",
        )
        return type_validate_python(list[Role], await _request(self, request))

    async def _api_get_guild_role(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
    ) -> Role:
        """Get guild role.

        see https://discord.com/developers/docs/resources/guild#get-guild-role
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
        )
        return type_validate_python(Role, await _request(self, request))

    async def _api_create_guild_role(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: Missing[str] = UNSET,
        permissions: Missing[str] = UNSET,
        color: Missing[int] = UNSET,
        colors: Missing[RoleColors] = UNSET,
        hoist: Missing[bool] = UNSET,
        icon: MissingOrNullable[str] = UNSET,
        unicode_emoji: MissingOrNullable[str] = UNSET,
        mentionable: Missing[bool] = UNSET,
        reason: str | None = None,
    ) -> Role:
        """Create guild role.

        see https://discord.com/developers/docs/resources/guild#create-guild-role
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                CreateGuildRoleParams,
                {
                    "name": name,
                    "permissions": permissions,
                    "color": color,
                    "colors": colors,
                    "hoist": hoist,
                    "icon": icon,
                    "unicode_emoji": unicode_emoji,
                    "mentionable": mentionable,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/roles",
            json=data,
        )
        return type_validate_python(Role, await _request(self, request))

    async def _api_modify_guild_role_positions(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        roles: list[ModifyGuildRolePositionParams] | None = None,
        id: SnowflakeType | None = None,  # noqa: A002
        position: MissingOrNullable[int] = UNSET,
        reason: str | None = None,
    ) -> list[Role]:
        """Modify guild role positions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-role-positions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        if roles is None:
            if id is None:
                msg = "roles or id must be provided"
                raise ValueError(msg)
            role = type_validate_python(
                ModifyGuildRolePositionParams, {"id": id, "position": position}
            )
            roles = [role]
        payload = [
            model_dump(
                type_validate_python(ModifyGuildRolePositionParams, role),
                omit_unset_values=True,
            )
            for role in roles
        ]
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles",
            json=payload,
        )
        return type_validate_python(list[Role], await _request(self, request))

    async def _api_modify_guild_role(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
        name: MissingOrNullable[str] = UNSET,
        permissions: MissingOrNullable[str] = UNSET,
        color: MissingOrNullable[int] = UNSET,
        colors: Missing[RoleColors] = UNSET,
        hoist: MissingOrNullable[bool] = UNSET,
        icon: MissingOrNullable[str] = UNSET,
        unicode_emoji: MissingOrNullable[str] = UNSET,
        mentionable: MissingOrNullable[bool] = UNSET,
        reason: str | None = None,
    ) -> Role:
        """Modify guild role.

        see https://discord.com/developers/docs/resources/guild#modify-guild-role
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                ModifyGuildRoleParams,
                {
                    "name": name,
                    "permissions": permissions,
                    "color": color,
                    "colors": colors,
                    "hoist": hoist,
                    "icon": icon,
                    "unicode_emoji": unicode_emoji,
                    "mentionable": mentionable,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
            json=data,
        )
        return type_validate_python(Role, await _request(self, request))

    @deprecated(
        "_api_modify_guild_MFA_level (PATCH /guilds/{guild_id}/mfa) is "
        "deprecated because Discord removed the endpoint from official "
        "bot-facing docs in 2025 (discord-api-docs #7715/#7720/#7722)."
    )
    async def _api_modify_guild_MFA_level(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        level: int,
        reason: str | None = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild"""
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
        await _request(self, request)

    async def _api_delete_guild_role(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete guild role.

        see https://discord.com/developers/docs/resources/guild#delete-guild-role
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
        )
        await _request(self, request)

    async def _api_get_guild_prune_count(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        days: int | None = None,
        include_roles: list[SnowflakeType] | None = None,
    ) -> dict[Literal["pruned"], int]:
        """Get guild prune count.

        see https://discord.com/developers/docs/resources/guild#get-guild-prune-count
        """
        data = {
            "days": days,
            "include_roles": ",".join(str(role) for role in include_roles)
            if include_roles
            else None,
        }
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/prune",
            params={key: value for key, value in data.items() if value is not None},
        )
        return await _request(self, request)

    async def _api_begin_guild_prune(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        days: int | None = None,
        compute_prune_count: bool | None = None,
        include_roles: list[SnowflakeType] | None = None,
        reason: str | None = None,
    ) -> dict[Literal["pruned"], int]:
        """Begin guild prune.

        see https://discord.com/developers/docs/resources/guild#begin-guild-prune
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "days": days,
            "compute_prune_count": compute_prune_count,
            "include_roles": include_roles,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/prune",
            json={key: value for key, value in data.items() if value is not None},
        )
        return await _request(self, request)

    async def _api_get_guild_voice_regions(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[VoiceRegion]:
        """Get guild voice regions.

        see https://discord.com/developers/docs/resources/guild#get-guild-voice-regions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/regions",
        )
        return type_validate_python(list[VoiceRegion], await _request(self, request))

    async def _api_get_guild_invites(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Invite]:
        """Get guild invites.

        see https://discord.com/developers/docs/resources/guild#get-guild-invites
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/invites",
        )
        return type_validate_python(list[Invite], await _request(self, request))

    async def _api_get_guild_integrations(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Integration]:
        """Get guild integrations.

        see https://discord.com/developers/docs/resources/guild#get-guild-integrations
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/integrations",
        )
        return type_validate_python(list[Integration], await _request(self, request))

    async def _api_delete_guild_integration(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        integration_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete guild integration.

        see https://discord.com/developers/docs/resources/guild#delete-guild-integration
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/integrations/{integration_id}",
        )
        await _request(self, request)

    async def _api_get_guild_widget_settings(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildWidgetSettings:
        """Get guild widget settings.

        see https://discord.com/developers/docs/resources/guild#get-guild-widget-settings
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget",
        )
        return type_validate_python(GuildWidgetSettings, await _request(self, request))

    async def _api_modify_guild_widget(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        enabled: Missing[bool] = UNSET,
        channel_id: MissingOrNullable[SnowflakeType] = UNSET,
        reason: str | None = None,
    ) -> GuildWidgetSettings:
        """Modify guild widget.

        see https://discord.com/developers/docs/resources/guild#modify-guild-widget
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                ModifyGuildWidgetParams,
                {"enabled": enabled, "channel_id": channel_id},
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/widget",
            json=data,
        )
        return type_validate_python(GuildWidgetSettings, await _request(self, request))

    async def _api_get_guild_widget(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildWidget:
        """Get guild widget.

        see https://discord.com/developers/docs/resources/guild#get-guild-widget
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget.json",
        )
        return type_validate_python(GuildWidget, await _request(self, request))

    async def _api_get_guild_vanity_url(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildVanityURL:
        """Get guild vanity URL.

        see https://discord.com/developers/docs/resources/guild#get-guild-vanity-url
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/vanity-url",
        )
        return type_validate_python(GuildVanityURL, await _request(self, request))

    async def _api_get_guild_widget_image(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        style: Literal["shield", "banner1", "banner2", "banner3", "banner4"]
        | None = None,
    ) -> bytes:
        """Get guild widget image.

        see https://discord.com/developers/docs/resources/guild#get-guild-widget-image
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"style": style}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget.png",
            params={key: value for key, value in params.items() if value is not None},
        )
        return await _request(self, request, parse_json=False)

    async def _api_get_guild_welcome_screen(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> WelcomeScreen:
        """Get guild welcome screen.

        see https://discord.com/developers/docs/resources/guild#get-guild-welcome-screen
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/welcome-screen",
        )
        return type_validate_python(WelcomeScreen, await _request(self, request))

    async def _api_modify_guild_welcome_screen(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        enabled: MissingOrNullable[bool] = UNSET,
        welcome_channels: MissingOrNullable[list[WelcomeScreenChannel]] = UNSET,
        description: MissingOrNullable[str] = UNSET,
        reason: str | None = None,
    ) -> WelcomeScreen:
        """Modify guild welcome screen.

        see https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
        """
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
                data,
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/welcome-screen",
            json=data,
        )
        return type_validate_python(WelcomeScreen, await _request(self, request))

    async def _api_get_guild_onboarding(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildOnboarding:
        """Get guild onboarding.

        see https://discord.com/developers/docs/resources/guild#get-guild-onboarding
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/onboarding",
        )
        return type_validate_python(GuildOnboarding, await _request(self, request))

    async def _api_modify_guild_onboarding(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        prompts: Missing[list[OnboardingPrompt]] = UNSET,
        default_channel_ids: Missing[list[Snowflake]] = UNSET,
        enabled: Missing[bool] = UNSET,
        mode: Missing[OnboardingMode] = UNSET,
        reason: str | None = None,
    ) -> GuildOnboarding:
        """Modify guild onboarding.

        see https://discord.com/developers/docs/resources/guild#modify-guild-onboarding
        """
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
            type_validate_python(ModifyGuildOnboardingParams, data),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/onboarding",
            json=data,
        )
        return type_validate_python(GuildOnboarding, await _request(self, request))

    # Voice

    # see https://discord.com/developers/docs/resources/voice
    async def _api_list_voice_regions(
        self: AdapterProtocol, bot: "Bot"
    ) -> list[VoiceRegion]:
        """List voice regions.

        see https://discord.com/developers/docs/resources/voice#list-voice-regions
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "voice/regions",
        )
        return type_validate_python(list[VoiceRegion], await _request(self, request))

    async def _api_get_current_user_voice_state(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> VoiceState:
        """Get current user voice state.

        see https://discord.com/developers/docs/resources/voice#get-current-user-voice-state
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/voice-states/@me",
        )
        return type_validate_python(VoiceState, await _request(self, request))

    async def _api_get_user_voice_state(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> VoiceState:
        """Get user voice state.

        see https://discord.com/developers/docs/resources/voice#get-user-voice-state
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
        )
        return type_validate_python(VoiceState, await _request(self, request))

    async def _api_modify_current_user_voice_state(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        channel_id: Missing[SnowflakeType] = UNSET,
        suppress: Missing[bool] = UNSET,
        request_to_speak_timestamp: MissingOrNullable[datetime] = UNSET,
    ) -> None:
        """Modify current user voice state.

        see https://discord.com/developers/docs/resources/voice#modify-current-user-voice-state
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                ModifyCurrentUserVoiceStateParams,
                {
                    "channel_id": channel_id,
                    "suppress": suppress,
                    "request_to_speak_timestamp": request_to_speak_timestamp,
                },
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/voice-states/@me",
            json=data,
        )
        await _request(self, request)

    async def _api_modify_user_voice_state(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        channel_id: SnowflakeType | None = None,
        suppress: bool | None = None,
    ) -> None:
        """Modify user voice state.

        see https://discord.com/developers/docs/resources/voice#modify-user-voice-state
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"channel_id": channel_id, "suppress": suppress}
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
            json={key: value for key, value in data.items() if value is not None},
        )
        await _request(self, request)

    # Guild Scheduled Event

    # see https://discord.com/developers/docs/resources/guild-scheduled-event
    async def _api_list_scheduled_events_for_guild(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        with_user_count: bool | None = None,
    ) -> list[GuildScheduledEvent]:
        """List scheduled events for guild.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#list-scheduled-events-for-guild
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_user_count": _bool_query(value=with_user_count)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[GuildScheduledEvent], await _request(self, request)
        )

    async def _api_create_guild_schedule_event(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        channel_id: Snowflake | None = None,
        entity_metadata: GuildScheduledEventEntityMetadata | None = None,
        name: str,
        privacy_level: GuildScheduledEventPrivacyLevel,
        scheduled_start_time: datetime,
        scheduled_end_time: datetime | None = None,
        description: str | None = None,
        entity_type: GuildScheduledEventEntityType,
        image: str | None = None,
        recurrence_rule: RecurrenceRule | None = None,
        reason: str | None = None,
    ) -> GuildScheduledEvent:
        """Create guild scheduled event.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event
        """
        if entity_type == GuildScheduledEventEntityType.EXTERNAL:
            if channel_id is not None:
                msg = "channel_id must be None for EXTERNAL events"
                raise ValueError(msg)
            if (
                entity_metadata is None
                or entity_metadata.location is UNSET
                or entity_metadata.location == ""
            ):
                msg = "entity_metadata.location is required for EXTERNAL events"
                raise ValueError(msg)
            if scheduled_end_time is None:
                msg = "scheduled_end_time is required for EXTERNAL events"
                raise ValueError(msg)
        elif channel_id is None:
            msg = "channel_id is required for non-EXTERNAL events"
            raise ValueError(msg)
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
            "recurrence_rule": recurrence_rule,
        }
        data = model_dump(
            type_validate_python(CreateGuildScheduledEventParams, data),
            exclude_none=True,
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events",
            json=data,
        )
        return type_validate_python(GuildScheduledEvent, await _request(self, request))

    async def _api_get_guild_scheduled_event(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        with_user_count: bool | None = None,
    ) -> GuildScheduledEvent:
        """Get guild scheduled event.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"with_user_count": _bool_query(value=with_user_count)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(GuildScheduledEvent, await _request(self, request))

    async def _api_modify_guild_scheduled_event(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        channel_id: MissingOrNullable[Snowflake] = UNSET,
        entity_metadata: MissingOrNullable[GuildScheduledEventEntityMetadata] = UNSET,
        name: Missing[str] = UNSET,
        privacy_level: Missing[GuildScheduledEventPrivacyLevel] = UNSET,
        scheduled_start_time: Missing[datetime] = UNSET,
        scheduled_end_time: Missing[datetime] = UNSET,
        description: MissingOrNullable[str] = UNSET,
        entity_type: Missing[GuildScheduledEventEntityType] = UNSET,
        status: Missing[GuildScheduledEventStatus] = UNSET,
        image: Missing[str] = UNSET,
        recurrence_rule: MissingOrNullable[RecurrenceRule] = UNSET,
        reason: str | None = None,
    ) -> GuildScheduledEvent:
        """Modify guild scheduled event.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event
        """
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
            "recurrence_rule": recurrence_rule,
        }
        data = model_dump(
            type_validate_python(
                ModifyGuildScheduledEventParams,
                data,
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            json=data,
        )
        return type_validate_python(GuildScheduledEvent, await _request(self, request))

    async def _api_delete_guild_scheduled_event(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
    ) -> None:
        """Delete guild scheduled event.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#delete-guild-scheduled-event
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
        )
        await _request(self, request)

    @validate
    async def _api_get_guild_scheduled_event_users(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
        with_member: bool | None = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
    ) -> list[GuildScheduledEventUser]:
        """Get guild scheduled event users.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event-users
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "limit": limit,
            "with_member": _bool_query(value=with_member),
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
            list[GuildScheduledEventUser], await _request(self, request)
        )

    # Guild Template

    # see https://discord.com/developers/docs/resources/guild-template
    async def _api_get_guild_template(
        self: AdapterProtocol, bot: "Bot", *, template_code: str
    ) -> GuildTemplate:
        """Get guild template.

        see https://discord.com/developers/docs/resources/guild-template#get-guild-template
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/templates/{template_code}",
        )
        return type_validate_python(GuildTemplate, await _request(self, request))

    @deprecated(
        "_api_create_guild_from_guild_template "
        "(POST /guilds/templates/{template_code}) is deprecated because Discord "
        "removed the endpoint from official bot-facing docs in 2025 "
        "(discord-api-docs #7715/#7720/#7722)."
    )
    async def _api_create_guild_from_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        template_code: str,
        name: str,
        icon: str | None = None,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild-template"""
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"name": name, "icon": icon}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/templates/{template_code}",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(Guild, await _request(self, request))

    async def _api_get_guild_templates(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[GuildTemplate]:
        """Get guild templates.

        see https://discord.com/developers/docs/resources/guild-template#get-guild-templates
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/templates",
        )
        return type_validate_python(list[GuildTemplate], await _request(self, request))

    async def _api_create_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        description: MissingOrNullable[str] = UNSET,
    ) -> GuildTemplate:
        """Create guild template.

        see https://discord.com/developers/docs/resources/guild-template#create-guild-template
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                CreateGuildTemplateParams,
                {"name": name, "description": description},
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/templates",
            json=data,
        )
        return type_validate_python(GuildTemplate, await _request(self, request))

    async def _api_sync_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
    ) -> GuildTemplate:
        """Sync guild template.

        see https://discord.com/developers/docs/resources/guild-template#sync-guild-template
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
        )
        return type_validate_python(GuildTemplate, await _request(self, request))

    async def _api_modify_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
        name: Missing[str] = UNSET,
        description: MissingOrNullable[str] = UNSET,
    ) -> GuildTemplate:
        """Modify guild template.

        see https://discord.com/developers/docs/resources/guild-template#modify-guild-template
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                ModifyGuildTemplateParams,
                {"name": name, "description": description},
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
            json=data,
        )
        return type_validate_python(GuildTemplate, await _request(self, request))

    async def _api_delete_guild_template(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
    ) -> GuildTemplate:
        """Delete guild template.

        see https://discord.com/developers/docs/resources/guild-template#delete-guild-template
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
        )
        return type_validate_python(GuildTemplate, await _request(self, request))

    # Invite

    # see https://discord.com/developers/docs/resources/invite
    async def _api_get_invite(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        invite_code: str,
        with_counts: bool | None = None,
        with_expiration: bool | None = None,
        guild_scheduled_event_id: SnowflakeType | None = None,
    ) -> Invite:
        """Get invite.

        see https://discord.com/developers/docs/resources/invite#get-invite
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "with_counts": _bool_query(value=with_counts),
            "with_expiration": _bool_query(value=with_expiration),
            "guild_scheduled_event_id": guild_scheduled_event_id,
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"invites/{invite_code}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(Invite, await _request(self, request))

    async def _api_delete_invite(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        invite_code: str,
        reason: str | None = None,
    ) -> Invite:
        """Delete invite.

        see https://discord.com/developers/docs/resources/invite#delete-invite
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"invites/{invite_code}",
        )
        return type_validate_python(Invite, await _request(self, request))

    async def _api_get_invite_target_users(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        invite_code: str,
    ) -> bytes:
        """Get invite target users.

        see https://discord.com/developers/docs/resources/invite#get-target-users
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"invites/{invite_code}/target-users",
        )
        return await _request(self, request, parse_json=False)

    async def _api_update_invite_target_users(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        invite_code: str,
        target_users_file: File,
    ) -> None:
        """Update invite target users.

        see https://discord.com/developers/docs/resources/invite#update-target-users
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url / f"invites/{invite_code}/target-users",
            files={
                "target_users_file": (
                    target_users_file.filename,
                    target_users_file.content,
                )
            },
        )
        await _request(self, request, parse_json=False)

    async def _api_get_invite_target_users_job_status(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        invite_code: str,
    ) -> InviteTargetUsersJobStatus:
        """Get invite target users job status.

        see https://discord.com/developers/docs/resources/invite#get-target-users-job-status
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"invites/{invite_code}/target-users/job-status",
        )
        return type_validate_python(
            InviteTargetUsersJobStatus, await _request(self, request)
        )

    # Poll

    # see https://discord.com/developers/docs/resources/poll
    @validate
    async def _api_get_answer_voters(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        answer_id: int,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AnswerVoters:
        """Get answer voters.

        see https://discord.com/developers/docs/resources/poll#get-answer-voters
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"after": after, "limit": limit}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"channels/{channel_id}/polls/{message_id}/answers/{answer_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(AnswerVoters, await _request(self, request))

    async def _api_end_poll(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """End poll.

        see https://discord.com/developers/docs/resources/poll#end-poll
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/polls/{message_id}/expire",
        )
        return type_validate_python(MessageGet, await _request(self, request))

    # SKU

    # see https://discord.com/developers/docs/resources/sku
    async def _api_list_SKUs(  # noqa: N802
        self: AdapterProtocol, bot: "Bot", *, application_id: SnowflakeType
    ) -> list[SKU]:
        """List SKUs.

        see https://discord.com/developers/docs/resources/sku#list-skus
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"applications/{application_id}/skus",
        )
        return type_validate_python(list[SKU], await _request(self, request))

    # Stage Instance

    # see https://discord.com/developers/docs/resources/stage-instance
    async def _api_create_stage_instance(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        topic: str,
        privacy_level: StagePrivacyLevel | None = None,
        send_start_notification: bool | None = None,
        guild_scheduled_event_id: SnowflakeType | None = None,
        reason: str | None = None,
    ) -> StageInstance:
        """Create stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#create-stage-instance
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = {
            "channel_id": channel_id,
            "topic": topic,
            "privacy_level": privacy_level,
            "send_start_notification": send_start_notification,
            "guild_scheduled_event_id": guild_scheduled_event_id,
        }
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / "stage-instances",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(StageInstance, await _request(self, request))

    async def _api_get_stage_instance(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> StageInstance:
        """Get stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#get-stage-instance
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"stage-instances/{channel_id}",
        )
        return type_validate_python(StageInstance, await _request(self, request))

    async def _api_modify_stage_instance(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        topic: str | None = None,
        privacy_level: StagePrivacyLevel | None = None,
        reason: str | None = None,
    ) -> StageInstance:
        """Modify stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#modify-stage-instance
        """
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
        return type_validate_python(StageInstance, await _request(self, request))

    async def _api_delete_stage_instance(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#delete-stage-instance
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"stage-instances/{channel_id}",
        )
        await _request(self, request)

    # Sticker

    # see https://discord.com/developers/docs/resources/sticker
    async def _api_get_sticker(
        self: AdapterProtocol, bot: "Bot", *, sticker_id: SnowflakeType
    ) -> Sticker:
        """Get sticker.

        see https://discord.com/developers/docs/resources/sticker#get-sticker
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"stickers/{sticker_id}",
        )
        return type_validate_python(Sticker, await _request(self, request))

    async def _api_list_nitro_sticker_packs(
        self: AdapterProtocol, bot: "Bot"
    ) -> StickerPacksResponse:
        """List sticker packs.

        see https://discord.com/developers/docs/resources/sticker#list-sticker-packs
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "sticker-packs",
        )
        return type_validate_python(StickerPacksResponse, await _request(self, request))

    async def _api_get_sticker_packs(
        self: AdapterProtocol, bot: "Bot", *, pack_id: SnowflakeType
    ) -> StickerPack:
        """Get sticker pack.

        see https://discord.com/developers/docs/resources/sticker#get-sticker-pack
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"sticker-packs/{pack_id}",
        )
        return type_validate_python(StickerPack, await _request(self, request))

    async def _api_list_guild_stickers(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Sticker]:
        """List guild stickers.

        see https://discord.com/developers/docs/resources/sticker#list-guild-stickers
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/stickers",
        )
        return type_validate_python(list[Sticker], await _request(self, request))

    async def _api_get_guild_sticker(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
    ) -> Sticker:
        """Get guild sticker.

        see https://discord.com/developers/docs/resources/sticker#get-guild-sticker
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
        )
        return type_validate_python(Sticker, await _request(self, request))

    async def _api_create_guild_sticker(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        description: str,
        tags: str,
        file: File,
        reason: str | None = None,
    ) -> Sticker:
        """Create guild sticker.

        see https://discord.com/developers/docs/resources/sticker#create-guild-sticker
        """
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
            headers=headers,
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/stickers",
            files=form,
        )
        return type_validate_python(Sticker, await _request(self, request))

    async def _api_modify_guild_sticker(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
        name: Missing[str] = UNSET,
        description: MissingOrNullable[str] = UNSET,
        tags: Missing[str] = UNSET,
        reason: str | None = None,
    ) -> Sticker:
        """Modify guild sticker.

        see https://discord.com/developers/docs/resources/sticker#modify-guild-sticker
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(
                ModifyGuildStickerParams,
                {"name": name, "description": description, "tags": tags},
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
            json=data,
        )
        return type_validate_python(Sticker, await _request(self, request))

    async def _api_delete_guild_sticker(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete guild sticker.

        see https://discord.com/developers/docs/resources/sticker#delete-guild-sticker
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
        )
        await _request(self, request)

    # Subscription

    # see https://discord.com/developers/docs/resources/subscription
    @validate
    async def _api_list_SKU_subscriptions(  # noqa: N802, PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        sku_id: SnowflakeType,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
        user_id: SnowflakeType | None = None,
    ) -> list[Subscription]:
        """List SKU subscriptions.

        see https://discord.com/developers/docs/resources/subscription#list-sku-subscriptions
        """
        if user_id is None:
            msg = "user_id is required for bot token queries"
            raise ValueError(msg)
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
        return type_validate_python(list[Subscription], await _request(self, request))

    async def _api_get_SKU_subscription(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        sku_id: SnowflakeType,
        subscription_id: SnowflakeType,
    ) -> Subscription:
        """Get SKU subscription.

        see https://discord.com/developers/docs/resources/subscription#get-sku-subscription
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"skus/{sku_id}/subscriptions/{subscription_id}",
        )
        return type_validate_python(Subscription, await _request(self, request))

    # Users

    # see https://discord.com/developers/docs/resources/user
    async def _api_get_current_user(self: AdapterProtocol, bot: "Bot") -> User:
        """Get current user.

        see https://discord.com/developers/docs/resources/user#get-current-user
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "users/@me",
        )
        return type_validate_python(User, await _request(self, request))

    async def _api_get_user(
        self: AdapterProtocol, bot: "Bot", *, user_id: SnowflakeType
    ) -> User:
        """Get user.

        see https://discord.com/developers/docs/resources/user#get-user
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"users/{user_id}",
        )
        return type_validate_python(User, await _request(self, request))

    async def _api_modify_current_user(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        username: Missing[str] = UNSET,
        avatar: MissingOrNullable[str] = UNSET,
        banner: MissingOrNullable[str] = UNSET,
    ) -> User:
        """Modify current user.

        see https://discord.com/developers/docs/resources/user#modify-current-user
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = model_dump(
            type_validate_python(
                ModifyCurrentUserParams,
                {"username": username, "avatar": avatar, "banner": banner},
            ),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / "users/@me",
            json=data,
        )
        return type_validate_python(User, await _request(self, request))

    async def _api_get_current_user_guilds(
        self: AdapterProtocol,
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
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {
            "before": before,
            "after": after,
            "limit": limit,
            "with_counts": _bool_query(value=with_counts),
        }
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "users/@me/guilds",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(
            list[CurrentUserGuild], await _request(self, request)
        )

    async def _api_get_current_user_guild_member(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
    ) -> GuildMember:
        """Get current user guild member.

        see https://discord.com/developers/docs/resources/user#get-current-user-guild-member
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"users/@me/guilds/{guild_id}/member",
        )
        return type_validate_python(GuildMember, await _request(self, request))

    async def _api_leave_guild(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> None:
        """Leave guild.

        see https://discord.com/developers/docs/resources/user#leave-guild
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"users/@me/guilds/{guild_id}",
        )
        await _request(self, request)

    async def _api_create_DM(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        recipient_id: SnowflakeType,
    ) -> Channel:
        """Create DM.

        see https://discord.com/developers/docs/resources/user#create-dm
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / "users/@me/channels",
            json={"recipient_id": recipient_id},
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_create_group_DM(  # noqa: N802
        self: AdapterProtocol,
        bot: "Bot",
        *,
        access_tokens: list[str],
        nicks: dict[SnowflakeType, str],
    ) -> Channel:
        """Create group DM.

        see https://discord.com/developers/docs/resources/user#create-group-dm
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {"access_tokens": access_tokens, "nicks": nicks}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / "users/@me/channels",
            json=data,
        )
        return type_validate_python(Channel, await _request(self, request))

    async def _api_get_user_connections(
        self: AdapterProtocol,
        *,
        access_token: str,
    ) -> list[Connection]:
        """Get current user connections.

        see https://discord.com/developers/docs/resources/user#get-current-user-connections
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "users/@me/connections",
        )
        return type_validate_python(list[Connection], await _request(self, request))

    async def _api_get_user_application_role_connection(
        self: AdapterProtocol,
        *,
        application_id: SnowflakeType,
        access_token: str,
    ) -> ApplicationRoleConnection:
        """Get current user application role connection.

        see https://discord.com/developers/docs/resources/user#get-current-user-application-role-connection
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url
            / f"users/@me/applications/{application_id}/role-connection",
        )
        return type_validate_python(
            ApplicationRoleConnection, await _request(self, request)
        )

    async def _api_update_user_application_role_connection(
        self: AdapterProtocol,
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
        headers = {"Authorization": f"Bearer {access_token}"}
        request = Request(
            headers=headers,
            method="PUT",
            url=self.base_url
            / f"users/@me/applications/{application_id}/role-connection",
            json={key: value for key, value in data.items() if value is not None},
        )
        return type_validate_python(
            ApplicationRoleConnection, await _request(self, request)
        )

    # Webhook

    # see https://discord.com/developers/docs/resources/webhook
    async def _api_create_webhook(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        name: str,
        avatar: MissingOrNullable[str] = UNSET,
        reason: str | None = None,
    ) -> Webhook:
        """Create webhook.

        see https://discord.com/developers/docs/resources/webhook#create-webhook
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = model_dump(
            type_validate_python(CreateWebhookParams, {"name": name, "avatar": avatar}),
            omit_unset_values=True,
        )
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"channels/{channel_id}/webhooks",
            json=data,
        )
        return type_validate_python(Webhook, await _request(self, request))

    async def _api_get_channel_webhooks(
        self: AdapterProtocol, bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[Webhook]:
        """Get channel webhooks.

        see https://discord.com/developers/docs/resources/webhook#get-channel-webhooks
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"channels/{channel_id}/webhooks",
        )
        return type_validate_python(list[Webhook], await _request(self, request))

    async def _api_get_guild_webhooks(
        self: AdapterProtocol, bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Webhook]:
        """Get guild webhooks.

        see https://discord.com/developers/docs/resources/webhook#get-guild-webhooks
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/webhooks",
        )
        return type_validate_python(list[Webhook], await _request(self, request))

    async def _api_get_webhook(
        self: AdapterProtocol, bot: "Bot", *, webhook_id: SnowflakeType
    ) -> Webhook:
        """Get webhook.

        see https://discord.com/developers/docs/resources/webhook#get-webhook
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}",
        )
        return type_validate_python(Webhook, await _request(self, request))

    async def _api_get_webhook_with_token(
        self: AdapterProtocol,
        *,
        webhook_id: SnowflakeType,
        token: str,
    ) -> Webhook:
        """Get webhook with token.

        see https://discord.com/developers/docs/resources/webhook#get-webhook-with-token
        """
        request = Request(
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
        )
        return type_validate_python(Webhook, await _request(self, request))

    async def _api_modify_webhook(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        name: Missing[str] = UNSET,
        avatar: MissingOrNullable[str] = UNSET,
        channel_id: Missing[SnowflakeType] = UNSET,
        reason: str | None = None,
    ) -> Webhook:
        """Modify webhook.

        see https://discord.com/developers/docs/resources/webhook#modify-webhook
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        data = omit_unset({"name": name, "avatar": avatar, "channel_id": channel_id})
        request = Request(
            headers=headers,
            method="PATCH",
            url=self.base_url / f"webhooks/{webhook_id}",
            json=data,
        )
        return type_validate_python(Webhook, await _request(self, request))

    async def _api_modify_webhook_with_token(
        self: AdapterProtocol,
        *,
        webhook_id: SnowflakeType,
        token: str,
        name: Missing[str] = UNSET,
        avatar: MissingOrNullable[str] = UNSET,
    ) -> Webhook:
        """Modify webhook with token.

        see https://discord.com/developers/docs/resources/webhook#modify-webhook-with-token
        """
        data = omit_unset({"name": name, "avatar": avatar})
        request = Request(
            method="PATCH",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
            json=data,
        )
        return type_validate_python(Webhook, await _request(self, request))

    async def _api_delete_webhook(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete webhook.

        see https://discord.com/developers/docs/resources/webhook#delete-webhook
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}",
        )
        await _request(self, request)

    async def _api_delete_webhook_with_token(
        self: AdapterProtocol,
        *,
        webhook_id: SnowflakeType,
        token: str,
    ) -> None:
        """Delete webhook with token.

        see https://discord.com/developers/docs/resources/webhook#delete-webhook-with-token
        """
        request = Request(
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
        )
        await _request(self, request)

    @overload
    async def _api_execute_webhook(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: Literal[True],
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        content: str | None = None,
        username: str | None = None,
        avatar_url: str | None = None,
        tts: bool | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: AllowedMention | None = None,
        components: list[Component] | None = None,
        files: list[File] | None = None,
        attachments: list[AttachmentSend] | None = None,
        flags: int | None = None,
        thread_name: str | None = None,
        applied_tags: list[SnowflakeType] | None = None,
        poll: PollRequest | None = None,
    ) -> MessageGet: ...

    @overload
    async def _api_execute_webhook(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: Literal[False] | None = None,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        content: str | None = None,
        username: str | None = None,
        avatar_url: str | None = None,
        tts: bool | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: AllowedMention | None = None,
        components: list[Component] | None = None,
        files: list[File] | None = None,
        attachments: list[AttachmentSend] | None = None,
        flags: int | None = None,
        thread_name: str | None = None,
        applied_tags: list[SnowflakeType] | None = None,
        poll: PollRequest | None = None,
    ) -> None: ...

    async def _api_execute_webhook(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: bool | None = None,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        content: str | None = None,
        username: str | None = None,
        avatar_url: str | None = None,
        tts: bool | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: AllowedMention | None = None,
        components: list[Component] | None = None,
        files: list[File] | None = None,
        attachments: list[AttachmentSend] | None = None,
        flags: int | None = None,
        thread_name: str | None = None,
        applied_tags: list[SnowflakeType] | None = None,
        poll: PollRequest | None = None,
    ) -> MessageGet | None:
        """Execute webhook.

        see https://discord.com/developers/docs/resources/webhook#execute-webhook
        """
        has_payload = any(
            [
                bool(content),
                bool(embeds),
                bool(components),
                bool(files),
                poll is not None,
            ]
        )
        if not has_payload:
            msg = "content/embeds/components/files/poll is required"
            raise ValueError(msg)
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
        resp = await _request(self, request)
        if resp is None:
            return None
        return type_validate_python(MessageGet, resp)

    async def _api_execute_slack_compatible_webhook(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        payload: dict[str, Any],
        thread_id: SnowflakeType | None = None,
        wait: bool | None = None,
    ) -> MessageGet | None:
        """Execute Slack-compatible webhook.

        see https://discord.com/developers/docs/resources/webhook#execute-slack-compatible-webhook
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id, "wait": _bool_query(value=wait)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/slack",
            params={key: value for key, value in params.items() if value is not None},
            json=payload,
        )
        resp = await _request(self, request)
        if resp is None:
            return None
        return type_validate_python(MessageGet, resp)

    async def _api_execute_github_compatible_webhook(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        payload: dict[str, Any],
        thread_id: SnowflakeType | None = None,
        wait: bool | None = None,
    ) -> MessageGet | None:
        """Execute GitHub-compatible webhook.

        see https://discord.com/developers/docs/resources/webhook#execute-github-compatible-webhook
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id, "wait": _bool_query(value=wait)}
        request = Request(
            headers=headers,
            method="POST",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/github",
            params={key: value for key, value in params.items() if value is not None},
            json=payload,
        )
        resp = await _request(self, request)
        if resp is None:
            return None
        return type_validate_python(MessageGet, resp)

    async def _api_get_webhook_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
    ) -> MessageGet:
        """Get webhook message.

        see https://discord.com/developers/docs/resources/webhook#get-webhook-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/messages/{message_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_edit_webhook_message(  # noqa: PLR0913
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        webhook_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        content: MissingOrNullable[str] = UNSET,
        embeds: MissingOrNullable[list[Embed]] = UNSET,
        flags: MissingOrNullable[MessageFlag] = UNSET,
        allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
        components: MissingOrNullable[list[Component]] = UNSET,
        files: Missing[list[File]] = UNSET,
        attachments: MissingOrNullable[list[AttachmentSend]] = UNSET,
        poll: MissingOrNullable[PollRequest] = UNSET,
    ) -> MessageGet:
        """Edit webhook message.

        see https://discord.com/developers/docs/resources/webhook#edit-webhook-message
        """
        params: dict[str, Any] = {"thread_id": thread_id}
        if with_components is not None:
            params["with_components"] = str(with_components).lower()
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        data = {
            "content": content,
            "embeds": embeds,
            "flags": flags,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "poll": poll,
        }
        request_kwargs = parse_data(
            data,
            WebhookMessageEditParams,
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
        return type_validate_python(MessageGet, await _request(self, request))

    async def _api_delete_webhook_message(
        self: AdapterProtocol,
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
    ) -> None:
        """Delete webhook message.

        see https://discord.com/developers/docs/resources/webhook#delete-webhook-message
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        params = {"thread_id": thread_id}
        request = Request(
            headers=headers,
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/messages/{message_id}",
            params={key: value for key, value in params.items() if value is not None},
        )
        await _request(self, request)

    # Gateway

    # see https://discord.com/developers/docs/events/gateway
    async def _api_get_gateway(self: AdapterProtocol) -> Gateway:
        """Get gateway.

        see https://discord.com/developers/docs/events/gateway#get-gateway
        """
        request = Request(
            method="GET",
            url=self.base_url / "gateway",
        )
        return type_validate_python(Gateway, await _request(self, request))

    async def _api_get_gateway_bot(self: AdapterProtocol, bot: "Bot") -> GatewayBot:
        """Get gateway bot.

        see https://discord.com/developers/docs/events/gateway#get-gateway-bot
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "gateway/bot",
        )
        return type_validate_python(GatewayBot, await _request(self, request))

    # OAuth2

    # see https://discord.com/developers/docs/topics/oauth2
    async def _api_get_current_bot_application_information(
        self: AdapterProtocol, bot: "Bot"
    ) -> Application:
        """Get current bot application information.

        see https://discord.com/developers/docs/topics/oauth2#get-current-bot-application-information
        """
        headers = {"Authorization": self.get_authorization(bot.bot_info)}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "oauth2/applications/@me",
        )
        return type_validate_python(Application, await _request(self, request))

    async def _api_get_current_authorization_information(
        self: AdapterProtocol,
        *,
        access_token: str,
    ) -> AuthorizationResponse:
        """Get current authorization information.

        see https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        request = Request(
            headers=headers,
            method="GET",
            url=self.base_url / "oauth2/@me",
        )
        return type_validate_python(
            AuthorizationResponse, await _request(self, request)
        )


__all__ = ["HandleMixin"]
