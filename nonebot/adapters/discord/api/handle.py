from collections.abc import Awaitable
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
)
from urllib.parse import quote

from nonebot.compat import type_validate_python
from nonebot.drivers import Request

from .model import (
    SKU,
    ActivityInstance,
    AnswerVoters,
    Application,
    ApplicationCommand,
    ApplicationCommandCreate,
    ApplicationCommandPermissions,
    ApplicationEmojis,
    ApplicationRoleConnection,
    ApplicationRoleConnectionMetadata,
    ArchivedThreadsResponse,
    AuditLog,
    AuthorizationResponse,
    AutoModerationRule,
    Ban,
    BulkBan,
    Channel,
    Connection,
    CreateAndModifyAutoModerationRuleParams,
    CreateGuildChannelParams,
    CreateGuildParams,
    CreateGuildScheduledEventParams,
    CurrentUserGuild,
    Emoji,
    Entitlement,
    ExecuteWebhookParams,
    File,
    FollowedChannel,
    Gateway,
    GatewayBot,
    Guild,
    GuildApplicationCommandPermissions,
    GuildMember,
    GuildOnboarding,
    GuildPreview,
    GuildScheduledEvent,
    GuildScheduledEventUser,
    GuildTemplate,
    GuildWidget,
    GuildWidgetSettings,
    Integration,
    InteractionResponse,
    Invite,
    ListActiveGuildThreadsResponse,
    MessageGet,
    MessageSend,
    ModifyChannelParams,
    ModifyGuildOnboardingParams,
    ModifyGuildParams,
    ModifyGuildScheduledEventParams,
    ModifyGuildWelcomeScreenParams,
    Role,
    SnowflakeType,
    StageInstance,
    Sticker,
    StickerPack,
    Subscription,
    ThreadMember,
    User,
    VoiceRegion,
    VoiceState,
    Webhook,
    WelcomeScreen,
)
from .request import _request
from .utils import parse_data, parse_forum_thread_message, parse_interaction_response
from ..utils import model_dump

if TYPE_CHECKING:
    from ..adapter import Adapter
    from ..bot import Bot

# ruff: noqa: ANN003 # TODO)): 将所有params/kwargs类型补全

# Application Commands
# see https://discord.com/developers/docs/interactions/application-commands


async def _get_global_application_commands(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType, **params
) -> list[ApplicationCommand]:
    """Fetch global commands for your application.
    Returns an array of application command objects.

    see https://discord.com/developers/docs/interactions/application-commands#get-global-application-commands
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"applications/{application_id}/commands",
        params=params,
    )
    return type_validate_python(
        list[ApplicationCommand], await _request(adapter, bot, request)
    )


async def _create_global_application_command(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType, **data
) -> ApplicationCommand:
    """Create a new global command.
    Returns 201 if a command with the same name does not already exist,
    or a 200 if it does (in which case the previous command will be overwritten).
    Both responses include an application command object.

    see https://discord.com/developers/docs/interactions/application-commands#create-global-application-command
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"applications/{application_id}/commands",
        json=data,
    )
    return type_validate_python(
        ApplicationCommand, await _request(adapter, bot, request)
    )


async def _get_global_application_command(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    command_id: SnowflakeType,
) -> ApplicationCommand:
    """Fetch a global command for your application.
    Returns an application command object.

    see https://discord.com/developers/docs/interactions/application-commands#get-global-application-command
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"applications/{application_id}/commands/{command_id}",
    )
    return type_validate_python(
        ApplicationCommand, await _request(adapter, bot, request)
    )


async def _edit_global_application_command(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    command_id: SnowflakeType,
    **data,
) -> ApplicationCommand:
    """Edit a global command. Returns 200 and an application command object.
    All fields are optional, but any fields provided will entirely overwrite
    the existing values of those fields.

    see https://discord.com/developers/docs/interactions/application-commands#edit-global-application-command
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"applications/{application_id}/commands/{command_id}",
        json=data,
    )
    return type_validate_python(
        ApplicationCommand, await _request(adapter, bot, request)
    )


async def _delete_global_application_command(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    command_id: SnowflakeType,
) -> None:
    """Deletes a global command. Returns 204 No Content on success.

    see https://discord.com/developers/docs/interactions/application-commands#delete-global-application-command
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"applications/{application_id}/commands/{command_id}",
    )
    await _request(adapter, bot, request)


async def _bulk_overwrite_global_application_commands(
    adapter: "Adapter",
    bot: "Bot",
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
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"applications/{application_id}/commands",
        json=[model_dump(command, exclude_unset=True) for command in commands],
    )
    return type_validate_python(
        list[ApplicationCommand], await _request(adapter, bot, request)
    )


async def _get_guild_application_commands(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    guild_id: SnowflakeType,
    **params,
) -> list[ApplicationCommand]:
    """Fetch all of the guild commands for your application for a specific guild.
    Returns an array of application command objects.

    see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-commands
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands",
        params=params,
    )
    return type_validate_python(
        list[ApplicationCommand], await _request(adapter, bot, request)
    )


async def _create_guild_application_command(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    guild_id: SnowflakeType,
    **data,
) -> ApplicationCommand:
    """Create a new guild command.
    New guild commands will be available in the guild immediately.
    Returns 201 if a command with the same name does not already exist,
    or a 200 if it does (in which case the previous command will be overwritten).
    Both responses include an application command object.

    see https://discord.com/developers/docs/interactions/application-commands#create-guild-application-command
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands",
        json=data,
    )
    return type_validate_python(
        ApplicationCommand, await _request(adapter, bot, request)
    )


async def _get_guild_application_command(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    guild_id: SnowflakeType,
    command_id: SnowflakeType,
) -> ApplicationCommand:
    """Fetch a guild command for your application.
    Returns an application command object.

    see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-command
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
    )
    return type_validate_python(
        ApplicationCommand, await _request(adapter, bot, request)
    )


async def _edit_guild_application_command(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    guild_id: SnowflakeType,
    command_id: SnowflakeType,
    **data,
) -> ApplicationCommand:
    """Edit a guild command.
    Updates for guild commands will be available immediately.
    Returns 200 and an application command object.
    All fields are optional,
    but any fields provided will entirely overwrite the existing values of those fields.

    see https://discord.com/developers/docs/interactions/application-commands#edit-guild-application-command
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
        json=data,
    )
    return type_validate_python(
        ApplicationCommand, await _request(adapter, bot, request)
    )


async def _delete_guild_application_command(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    guild_id: SnowflakeType,
    command_id: SnowflakeType,
) -> None:
    """Delete a guild command. Returns 204 No Content on success.

    see https://discord.com/developers/docs/interactions/application-commands#delete-guild-application-command
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
    )
    await _request(adapter, bot, request)


async def _bulk_overwrite_guild_application_commands(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    guild_id: SnowflakeType,
    commands: list[ApplicationCommandCreate],
) -> list[ApplicationCommand]:
    """Takes a list of application commands,
    overwriting the existing command list for this application for the targeted guild.
    Returns 200 and a list of application command objects.

    see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-guild-application-commands
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands",
        json=[model_dump(command, exclude_unset=True) for command in commands],
    )
    return type_validate_python(
        list[ApplicationCommand], await _request(adapter, bot, request)
    )


async def _get_guild_application_command_permissions(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    guild_id: SnowflakeType,
) -> list[GuildApplicationCommandPermissions]:
    """
    Fetches permissions for all commands for your application in a guild.
    Returns an array of guild application command permissions objects.

    see https://discord.com/developers/docs/interactions/application-commands#get-guild-application-command-permissions
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands/permissions",
    )
    return type_validate_python(
        list[GuildApplicationCommandPermissions], await _request(adapter, bot, request)
    )


async def _get_application_command_permissions(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    guild_id: SnowflakeType,
    command_id: SnowflakeType,
) -> GuildApplicationCommandPermissions:
    """
    Fetches permissions for a specific command for your application in a guild.
    Returns a guild application command permissions object.

    see https://discord.com/developers/docs/interactions/application-commands#get-application-command-permissions
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
    )
    return type_validate_python(
        GuildApplicationCommandPermissions, await _request(adapter, bot, request)
    )


async def _edit_application_command_permissions(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
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
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url
        / f"applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
        json={
            "permissions": [
                model_dump(permission, exclude_unset=True) for permission in permissions
            ]
        },
    )
    return type_validate_python(
        GuildApplicationCommandPermissions, await _request(adapter, bot, request)
    )


# Receiving and Responding
# see https://discord.com/developers/docs/interactions/receiving-and-responding


async def _create_interaction_response(
    adapter: "Adapter",
    bot: "Bot",
    interaction_id: SnowflakeType,
    interaction_token: str,
    response: InteractionResponse,
) -> None:
    """https://discord.com/developers/docs/interactions/receiving-and-responding#create-interaction-response"""
    params = parse_interaction_response(response)
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url
        / f"interactions/{interaction_id}/{interaction_token}/callback",
        **params,
    )
    await _request(adapter, bot, request)


async def _get_origin_interaction_response(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    interaction_token: str,
) -> MessageGet:
    """https://discord.com/developers/docs/interactions/receiving-and-responding#get-original-interaction-response"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"webhooks/{application_id}/{interaction_token}/messages/@original",
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _edit_origin_interaction_response(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    interaction_token: str,
    **data,
) -> MessageGet:
    """https://discord.com/developers/docs/interactions/receiving-and-responding#edit-original-interaction-response"""
    params = {}
    if data.get("thread_id"):
        params["thread_id"] = data.pop("thread_id")
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url
        / f"webhooks/{application_id}/{interaction_token}/messages/@original",
        params=params,
        json=data,
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _delete_origin_interaction_response(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    interaction_token: str,
    **data,
) -> None:
    """https://discord.com/developers/docs/interactions/receiving-and-responding#delete-original-interaction-response"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url
        / f"webhooks/{application_id}/{interaction_token}/messages/@original",
        json=data,
    )
    await _request(adapter, bot, request)


async def _create_followup_message(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    interaction_token: str,
    **data,
) -> MessageGet:
    """https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message"""
    data = parse_data(data, ExecuteWebhookParams)
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"webhooks/{application_id}/{interaction_token}",
        **data,
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _get_followup_message(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    interaction_token: str,
    message_id: SnowflakeType,
    **params,
) -> MessageGet:
    """Returns a followup message for an Interaction. Functions the same as Get Webhook Message.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#get-followup-message
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
        params=params,
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _edit_followup_message(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    interaction_token: str,
    message_id: SnowflakeType,
    **data,
) -> MessageGet:
    """Edits a followup message for an Interaction. Functions the same as Edit Webhook Message.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#edit-followup-message
    """
    params = {}
    if data.get("thread_id"):
        params["thread_id"] = data.pop("thread_id")
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    data = parse_data(data, ExecuteWebhookParams)
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url
        / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
        params=params,
        **data,
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _delete_followup_message(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    interaction_token: str,
    message_id: SnowflakeType,
) -> None:
    """Deletes a followup message for an Interaction.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#delete-followup-message
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url
        / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
    )
    await _request(adapter, bot, request)


# Application
# see https://discord.com/developers/docs/resources/application


async def _get_current_application(
    adapter: "Adapter",
    bot: "Bot",
) -> Application:
    """Returns the application object associated with the requesting bot user.

    see https://discord.com/developers/docs/resources/application#get-current-application
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "applications/@me",
    )
    return type_validate_python(Application, await _request(adapter, bot, request))


async def _edit_current_application(
    adapter: "Adapter",
    bot: "Bot",
    **data,
) -> Application:
    """Edit properties of the app associated with the requesting bot user.

    see https://discord.com/developers/docs/resources/application#edit-current-application
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / "applications/@me",
        json=data,
    )
    return type_validate_python(Application, await _request(adapter, bot, request))


async def _get_application_activity_instance(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    instance_id: str,
) -> ActivityInstance:
    """Returns a serialized activity instance, if it exists.
    Useful for preventing unwanted activity sessions.

    see https://discord.com/developers/docs/resources/application#get-application-activity-instance
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"applications/{application_id}/activity-instances/{instance_id}",
    )
    return type_validate_python(ActivityInstance, await _request(adapter, bot, request))


# Application Role Connection Metadata
# see https://discord.com/developers/docs/resources/application-role-connection-metadata


async def _get_application_role_connection_metadata_records(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType
) -> list[ApplicationRoleConnectionMetadata]:
    """get application role connection metadata records

    see https://discord.com/developers/docs/resources/application-role-connection-metadata#get-application-role-connection-metadata-records
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"applications/{application_id}/role-connections/metadata",
    )
    return type_validate_python(
        list[ApplicationRoleConnectionMetadata], await _request(adapter, bot, request)
    )


async def _update_application_role_connection_metadata_records(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType
) -> list[ApplicationRoleConnectionMetadata]:
    """update application role connection metadata records

    see https://discord.com/developers/docs/resources/application-role-connection-metadata#update-application-role-connection-metadata-records
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url
        / f"applications/{application_id}/role-connections/metadata",
    )
    return type_validate_python(
        list[ApplicationRoleConnectionMetadata], await _request(adapter, bot, request)
    )


# Audit Logs
# see https://discord.com/developers/docs/resources/audit-log


async def _get_guild_audit_log(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
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
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/audit-logs",
        params=data,
    )
    return type_validate_python(AuditLog, await _request(adapter, bot, request))


# Auto Moderation
# see https://discord.com/developers/docs/resources/auto-moderation


async def _list_auto_moderation_rules_for_guild(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[AutoModerationRule]:
    """list auto moderation rules for guild

    see https://discord.com/developers/docs/resources/auto-moderation#list-auto-moderation-rules-for-guild
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/auto-moderation/rules",
    )
    return type_validate_python(
        list[AutoModerationRule], await _request(adapter, bot, request)
    )


async def _get_auto_moderation_rule(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, rule_id: SnowflakeType
) -> AutoModerationRule:
    """get auto moderation rule

    see https://discord.com/developers/docs/resources/auto-moderation#get-auto-moderation-rule
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
    )
    return type_validate_python(
        AutoModerationRule, await _request(adapter, bot, request)
    )


async def _create_auto_moderation_rule(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> AutoModerationRule:
    """create auto moderation rule

    see https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(
        type_validate_python(CreateAndModifyAutoModerationRuleParams, data),
        exclude_none=True,
    )
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/{guild_id}/auto-moderation/rules",
        json=data,
    )
    return type_validate_python(
        AutoModerationRule, await _request(adapter, bot, request)
    )


async def _modify_auto_moderation_rule(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    rule_id: SnowflakeType,
    **data,
) -> AutoModerationRule:
    """modify auto moderation rule

    see https://discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(
        type_validate_python(CreateAndModifyAutoModerationRuleParams, data),
        exclude_none=True,
    )
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
        json=data,
    )
    return type_validate_python(
        AutoModerationRule, await _request(adapter, bot, request)
    )


async def _delete_auto_moderation_rule(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    rule_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """delete auto moderation rule

    see https://discord.com/developers/docs/resources/auto-moderation#delete-auto-moderation-rule
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
    )
    await _request(adapter, bot, request)


# Channels
# https://discord.com/developers/docs/resources/channel


async def _get_channel(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType
) -> Channel:
    """get channel

    see https://discord.com/developers/docs/resources/channel#get-channel"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}",
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _modify_DM(  # noqa: N802 # TODO)): 疑似与_modify_channel重复, 确认后弃用
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> Channel:
    """modify channel

    see https://discord.com/developers/docs/resources/channel#modify-channel"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"channels/{channel_id}",
        json=data,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _modify_channel(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> Channel:
    """https://discord.com/developers/docs/resources/channel#modify-channel"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(
        type_validate_python(ModifyChannelParams, data), exclude_unset=True
    )
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"channels/{channel_id}",
        json=data,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _modify_thread(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> Channel:
    """https://discord.com/developers/docs/resources/channel#modify-channel"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"channels/{channel_id}",
        json=data,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _delete_channel(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    reason: Optional[str] = None,
) -> Channel:
    """https://discord.com/developers/docs/resources/channel#deleteclose-channel"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"channels/{channel_id}",
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


# Messages
# see https://discord.com/developers/docs/resources/message


async def _get_channel_messages(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> list[MessageGet]:
    """https://discord.com/developers/docs/resources/message#get-channel-messages"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/messages",
        params=data,
    )
    return type_validate_python(list[MessageGet], await _request(adapter, bot, request))


async def _get_channel_message(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, message_id: SnowflakeType
) -> MessageGet:
    """https://discord.com/developers/docs/resources/message#get-channel-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/messages/{message_id}",
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _create_message(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> MessageGet:
    """https://discord.com/developers/docs/resources/message#create-message"""
    params = parse_data(data, MessageSend)
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/messages",
        **params,
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _crosspost_message(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, message_id: SnowflakeType
) -> MessageGet:
    """https://discord.com/developers/docs/resources/message#crosspost-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/messages/{message_id}/crosspost",
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _create_reaction(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    emoji: str,
    emoji_id: Optional[SnowflakeType] = None,
) -> None:
    """https://discord.com/developers/docs/resources/message#create-reaction"""
    if emoji_id is not None:
        emoji = f"{emoji}:{emoji_id}"
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url
        / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}/@me",
    )
    await _request(adapter, bot, request)


async def _delete_own_reaction(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    emoji: str,
    emoji_id: Optional[SnowflakeType] = None,
) -> None:
    """https://discord.com/developers/docs/resources/message#delete-own-reaction"""
    if emoji_id is not None:
        emoji = f"{emoji}:{emoji_id}"
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url
        / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}/@me",
    )
    await _request(adapter, bot, request)


async def _delete_user_reaction(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    user_id: SnowflakeType,
    emoji: str,
    emoji_id: Optional[SnowflakeType] = None,
) -> None:
    """https://discord.com/developers/docs/resources/message#delete-user-reaction"""
    if emoji_id is not None:
        emoji = f"{emoji}:{emoji_id}"
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url
        / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}/{user_id}",
    )
    await _request(adapter, bot, request)


async def _get_reactions(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    emoji: str,
    emoji_id: Optional[SnowflakeType] = None,
    **params,
) -> list[User]:
    """https://discord.com/developers/docs/resources/message#get-reactions"""
    if emoji_id is not None:
        emoji = f"{emoji}:{emoji_id}"
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}",
        params=params,
    )
    return type_validate_python(list[User], await _request(adapter, bot, request))


async def _delete_all_reactions(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
) -> None:
    """https://discord.com/developers/docs/resources/message#delete-all-reactions"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"channels/{channel_id}/messages/{message_id}/reactions",
    )
    await _request(adapter, bot, request)


async def _delete_all_reactions_for_emoji(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    emoji: str,
    emoji_id: Optional[SnowflakeType] = None,
) -> None:
    """https://discord.com/developers/docs/resources/message#delete-all-reactions-for-emoji"""
    if emoji_id is not None:
        emoji = f"{emoji}:{emoji_id}"
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url
        / f"channels/{channel_id}/messages/{message_id}/reactions/{quote(emoji)}",
    )
    await _request(adapter, bot, request)


async def _edit_message(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    **data,
) -> MessageGet:
    """https://discord.com/developers/docs/resources/message#edit-message"""
    params = parse_data(data, MessageSend)
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"channels/{channel_id}/messages/{message_id}",
        **params,
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _delete_message(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/message#delete-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"channels/{channel_id}/messages/{message_id}",
    )
    await _request(adapter, bot, request)


async def _bulk_delete_message(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> None:
    """https://discord.com/developers/docs/resources/message#bulk-delete-messages"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/messages/bulk-delete",
        json=data,
    )
    await _request(adapter, bot, request)


async def _edit_channel_permissions(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    overwrite_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/channel#edit-channel-permissions"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"channels/{channel_id}/permissions/{overwrite_id}",
    )
    await _request(adapter, bot, request)


async def _get_channel_invites(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType
) -> list[Invite]:
    """https://discord.com/developers/docs/resources/channel#get-channel-invites"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/invites",
    )
    return type_validate_python(list[Invite], await _request(adapter, bot, request))


async def _create_channel_invite(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> Invite:
    """https://discord.com/developers/docs/resources/channel#create-channel-invite"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/invites",
        json=data,
    )
    return type_validate_python(Invite, await _request(adapter, bot, request))


async def _delete_channel_permission(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    overwrite_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/channel#delete-channel-permission"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"channels/{channel_id}/permissions/{overwrite_id}",
    )
    await _request(adapter, bot, request)


async def _follow_announcement_channel(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> FollowedChannel:
    """https://discord.com/developers/docs/resources/channel#follow-announcement-channel"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/followers",
        json=data,
    )
    return type_validate_python(FollowedChannel, await _request(adapter, bot, request))


async def _trigger_typing_indicator(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType
) -> None:
    """https://discord.com/developers/docs/resources/channel#trigger-typing-indicator"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/typing",
    )
    await _request(adapter, bot, request)


async def _get_pinned_messages(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType
) -> list[MessageGet]:
    """https://discord.com/developers/docs/resources/channel#get-pinned-messages"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/pins",
    )
    return type_validate_python(list[MessageGet], await _request(adapter, bot, request))


async def _pin_message(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/channel#pin-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"channels/{channel_id}/pins/{message_id}",
    )
    await _request(adapter, bot, request)


async def _unpin_message(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/channel#unpin-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"channels/{channel_id}/pins/{message_id}",
    )
    await _request(adapter, bot, request)


async def _group_DM_add_recipient(  # noqa: N802
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    user_id: SnowflakeType,
    **data,
) -> None:
    """https://discord.com/developers/docs/resources/channel#group-dm-add-recipient"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"channels/{channel_id}/recipients/{user_id}",
        json=data,
    )
    await _request(adapter, bot, request)


async def _group_DM_remove_recipient(  # noqa: N802
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, user_id: SnowflakeType
) -> None:
    """https://discord.com/developers/docs/resources/channel#group-dm-remove-recipient"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"channels/{channel_id}/recipients/{user_id}",
    )
    await _request(adapter, bot, request)


async def _start_thread_from_message(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    **data,
) -> Channel:
    """https://discord.com/developers/docs/resources/channel#start-thread-from-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/messages/{message_id}/threads",
        json=data,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _start_thread_without_message(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> Channel:
    """https://discord.com/developers/docs/resources/channel#start-thread-without-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/threads",
        json=data,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _start_thread_in_forum_channel(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> Channel:
    """https://discord.com/developers/docs/resources/channel#start-thread-in-forum-or-media-channel"""
    params = parse_forum_thread_message(data)
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/threads",
        **params,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _join_thread(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType
) -> None:
    """https://discord.com/developers/docs/resources/channel#join-thread"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"channels/{channel_id}/thread-members/@me",
    )
    await _request(adapter, bot, request)


async def _add_thread_member(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, user_id: SnowflakeType
) -> None:
    """https://discord.com/developers/docs/resources/channel#add-thread-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"channels/{channel_id}/thread-members/{user_id}",
    )
    await _request(adapter, bot, request)


async def _leave_thread(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType
) -> None:
    """https://discord.com/developers/docs/resources/channel#leave-thread"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"channels/{channel_id}/thread-members/@me",
    )
    await _request(adapter, bot, request)


async def _remove_thread_member(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, user_id: SnowflakeType
) -> None:
    """https://discord.com/developers/docs/resources/channel#remove-thread-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"channels/{channel_id}/thread-members/{user_id}",
    )
    await _request(adapter, bot, request)


async def _get_thread_member(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    user_id: SnowflakeType,
    **params,
) -> ThreadMember:
    """https://discord.com/developers/docs/resources/channel#get-thread-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/thread-members/{user_id}",
        params=params,
    )
    return type_validate_python(ThreadMember, await _request(adapter, bot, request))


async def _list_thread_members(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **params
) -> list[ThreadMember]:
    """https://discord.com/developers/docs/resources/channel#list-thread-members"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/thread-members",
        params=params,
    )
    return type_validate_python(
        list[ThreadMember], await _request(adapter, bot, request)
    )


async def _list_public_archived_threads(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **params
) -> ArchivedThreadsResponse:
    """https://discord.com/developers/docs/resources/channel#list-public-archived-threads"""
    if before := params.get("before"):
        params["before"] = before.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/threads/archived/public",
        params=params,
    )
    return type_validate_python(
        ArchivedThreadsResponse, await _request(adapter, bot, request)
    )


async def _list_private_archived_threads(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **params
) -> ArchivedThreadsResponse:
    """https://discord.com/developers/docs/resources/channel#list-private-archived-threads"""
    if before := params.get("before"):
        params["before"] = before.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/threads/archived/private",
        params=params,
    )
    return type_validate_python(
        ArchivedThreadsResponse, await _request(adapter, bot, request)
    )


async def _list_joined_private_archived_threads(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **params
) -> ArchivedThreadsResponse:
    """https://discord.com/developers/docs/resources/channel#list-joined-private-archived-threads"""
    if before := params.get("before"):
        params["before"] = before.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"channels/{channel_id}/users/@me/threads/archived/private",
        params=params,
    )
    return type_validate_python(
        ArchivedThreadsResponse, await _request(adapter, bot, request)
    )


# Emoji
# see https://discord.com/developers/docs/resources/emoji


async def _list_guild_emojis(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[Emoji]:
    """https://discord.com/developers/docs/resources/emoji#list-guild-emojis"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/emojis",
    )
    return type_validate_python(list[Emoji], await _request(adapter, bot, request))


async def _get_guild_emoji(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, emoji_id: SnowflakeType
) -> Emoji:
    """https://discord.com/developers/docs/resources/emoji#get-guild-emoji"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
    )
    return type_validate_python(Emoji, await _request(adapter, bot, request))


async def _create_guild_emoji(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> Emoji:
    """https://discord.com/developers/docs/resources/emoji#create-guild-emoji"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/{guild_id}/emojis",
        json=data,
    )
    return type_validate_python(Emoji, await _request(adapter, bot, request))


async def _modify_guild_emoji(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    emoji_id: SnowflakeType,
    **data,
) -> Emoji:
    """https://discord.com/developers/docs/resources/emoji#modify-guild-emoji"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
        json=data,
    )
    return type_validate_python(Emoji, await _request(adapter, bot, request))


async def _delete_guild_emoji(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    emoji_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/emoji#delete-guild-emoji"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
    )
    await _request(adapter, bot, request)


async def _list_application_emojis(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType
) -> ApplicationEmojis:
    """https://discord.com/developers/docs/resources/emoji#list-application-emojis"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"applications/{application_id}/emojis",
    )
    return type_validate_python(
        ApplicationEmojis, await _request(adapter, bot, request)
    )


async def _get_application_emoji(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    emoji_id: SnowflakeType,
) -> Emoji:
    """https://discord.com/developers/docs/resources/emoji#get-application-emoji"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"applications/{application_id}/emojis/{emoji_id}",
    )
    return type_validate_python(Emoji, await _request(adapter, bot, request))


async def _create_application_emoji(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType, **data
) -> Emoji:
    """https://discord.com/developers/docs/resources/emoji#create-application-emoji"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"applications/{application_id}/emojis",
        json=data,
    )
    return type_validate_python(Emoji, await _request(adapter, bot, request))


async def _modify_application_emoji(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    emoji_id: SnowflakeType,
    **data,
) -> Emoji:
    """https://discord.com/developers/docs/resources/emoji#modify-application-emoji"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"applications/{application_id}/emojis/{emoji_id}",
        json=data,
    )
    return type_validate_python(Emoji, await _request(adapter, bot, request))


async def _delete_application_emoji(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    emoji_id: SnowflakeType,
) -> None:
    """https://discord.com/developers/docs/resources/emoji#delete-application-emoji"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"applications/{application_id}/emojis/{emoji_id}",
    )
    await _request(adapter, bot, request)


# Entitlements
# see https://discord.com/developers/docs/resources/entitlement


async def _list_entitlements(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType, **params
) -> list[Entitlement]:
    """https://discord.com/developers/docs/resources/entitlement#list-entitlements"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"applications/{application_id}/entitlements",
        params=params,
    )
    return type_validate_python(
        list[Entitlement], await _request(adapter, bot, request)
    )


async def _consume_an_entitlement(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    entitlement_id: SnowflakeType,
) -> None:
    """https://discord.com/developers/docs/resources/entitlement#consume-an-entitlement"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url
        / f"applications/{application_id}/entitlements/{entitlement_id}/consume",
    )
    await _request(adapter, bot, request)


async def _create_test_entitlement(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    **data,
) -> Entitlement:
    """https://discord.com/developers/docs/resources/entitlement#create-test-entitlement"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"applications/{application_id}/entitlements",
        json=data,
    )
    return type_validate_python(Entitlement, await _request(adapter, bot, request))


async def _delete_test_entitlement(
    adapter: "Adapter",
    bot: "Bot",
    application_id: SnowflakeType,
    entitlement_id: SnowflakeType,
) -> None:
    """https://discord.com/developers/docs/resources/entitlement#delete-test-entitlement"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url
        / f"applications/{application_id}/entitlements/{entitlement_id}",
    )
    await _request(adapter, bot, request)


# Guild
# see https://discord.com/developers/docs/resources/guild


async def _create_guild(adapter: "Adapter", bot: "Bot", **data) -> Guild:
    """https://discord.com/developers/docs/resources/guild#create-guild"""
    data = model_dump(type_validate_python(CreateGuildParams, data), exclude_unset=True)
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers, method="POST", url=adapter.base_url / "guilds", json=data
    )
    return type_validate_python(Guild, await _request(adapter, bot, request))


async def _get_guild(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **params
) -> Guild:
    """https://discord.com/developers/docs/resources/guild#get-guild"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}",
        params=params,
    )
    return type_validate_python(Guild, await _request(adapter, bot, request))


async def _get_guild_preview(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> GuildPreview:
    """https://discord.com/developers/docs/resources/guild#get-guild-preview"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/preview",
    )
    return type_validate_python(GuildPreview, await _request(adapter, bot, request))


async def _modify_guild(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> Guild:
    """https://discord.com/developers/docs/resources/guild#modify-guild"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(type_validate_python(ModifyGuildParams, data), exclude_unset=True)
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}",
        json=data,
    )
    return type_validate_python(Guild, await _request(adapter, bot, request))


async def _delete_guild(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> None:
    """https://discord.com/developers/docs/resources/guild#delete-guild"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}",
    )
    await _request(adapter, bot, request)


async def _get_guild_channels(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[Channel]:
    """https://discord.com/developers/docs/resources/guild#get-guild-channels"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/channels",
    )
    return type_validate_python(list[Channel], await _request(adapter, bot, request))


async def _create_guild_channel(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> Channel:
    """https://discord.com/developers/docs/resources/guild#create-guild-channel"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(
        type_validate_python(CreateGuildChannelParams, data), exclude_unset=True
    )
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/{guild_id}/channels",
        json=data,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _modify_guild_channel_positions(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> Guild:
    """https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/channels",
        json=data,
    )
    return type_validate_python(Guild, await _request(adapter, bot, request))


async def _list_active_guild_threads(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> ListActiveGuildThreadsResponse:
    """https://discord.com/developers/docs/resources/guild#list-active-guild-threads"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/threads/active",
    )
    return type_validate_python(
        ListActiveGuildThreadsResponse, await _request(adapter, bot, request)
    )


async def _get_guild_member(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, user_id: SnowflakeType
) -> GuildMember:
    """https://discord.com/developers/docs/resources/guild#get-guild-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/members/{user_id}",
    )
    return type_validate_python(GuildMember, await _request(adapter, bot, request))


async def _list_guild_members(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **params
) -> list[GuildMember]:
    """https://discord.com/developers/docs/resources/guild#list-guild-members"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/members",
        params=params,
    )
    return type_validate_python(
        list[GuildMember], await _request(adapter, bot, request)
    )


async def _search_guild_members(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **params
) -> list[GuildMember]:
    """https://discord.com/developers/docs/resources/guild#search-guild-members"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/members/search",
        params=params,
    )
    return type_validate_python(
        list[GuildMember], await _request(adapter, bot, request)
    )


async def _add_guild_member(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    user_id: SnowflakeType,
    **data,
) -> GuildMember:
    """https://discord.com/developers/docs/resources/guild#add-guild-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"guilds/{guild_id}/members/{user_id}",
        json=data,
    )
    return type_validate_python(GuildMember, await _request(adapter, bot, request))


async def _modify_guild_member(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    user_id: SnowflakeType,
    **data,
) -> GuildMember:
    """https://discord.com/developers/docs/resources/guild#modify-guild-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/members/{user_id}",
        json=data,
    )
    return type_validate_python(GuildMember, await _request(adapter, bot, request))


async def _modify_current_member(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> GuildMember:
    """https://discord.com/developers/docs/resources/guild#modify-current-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/members/@me",
        json=data,
    )
    return type_validate_python(GuildMember, await _request(adapter, bot, request))


async def _modify_current_user_nick(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> GuildMember:
    """Deprecated in favor of Modify Current Member.

    https://discord.com/developers/docs/resources/guild#modify-current-user-nick"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/members/@me/nick",
        json=data,
    )
    return type_validate_python(GuildMember, await _request(adapter, bot, request))


async def _add_guild_member_role(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    user_id: SnowflakeType,
    role_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/guild#add-guild-member-role"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
    )
    await _request(adapter, bot, request)


async def _remove_guild_member_role(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    user_id: SnowflakeType,
    role_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/guild#remove-guild-member-role"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
    )
    await _request(adapter, bot, request)


async def _remove_guild_member(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    user_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/guild#remove-guild-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/members/{user_id}",
    )
    await _request(adapter, bot, request)


async def _get_guild_bans(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **params
) -> list[Ban]:
    """https://discord.com/developers/docs/resources/guild#get-guild-bans"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/bans",
        params=params,
    )
    return type_validate_python(list[Ban], await _request(adapter, bot, request))


async def _get_guild_ban(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, user_id: SnowflakeType
) -> Ban:
    """https://discord.com/developers/docs/resources/guild#get-guild-ban"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/bans/{user_id}",
    )
    return type_validate_python(Ban, await _request(adapter, bot, request))


async def _create_guild_ban(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    user_id: SnowflakeType,
    **data,
) -> None:
    """https://discord.com/developers/docs/resources/guild#create-guild-ban"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"guilds/{guild_id}/bans/{user_id}",
        json=data,
    )
    await _request(adapter, bot, request)


async def _remove_guild_ban(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    user_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/guild#remove-guild-ban"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/bans/{user_id}",
    )
    await _request(adapter, bot, request)


async def _bulk_guild_ban(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    **data,
) -> BulkBan:
    """https://discord.com/developers/docs/resources/guild#bulk-guild-ban"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/{guild_id}/bulk-ban",
        json=data,
    )
    return type_validate_python(BulkBan, await _request(adapter, bot, request))


async def _get_guild_roles(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[Role]:
    """https://discord.com/developers/docs/resources/guild#get-guild-roles"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/roles",
    )
    return type_validate_python(list[Role], await _request(adapter, bot, request))


async def _get_guild_role(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, role_id: SnowflakeType
) -> Role:
    """https://discord.com/developers/docs/resources/guild#get-guild-role"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/roles/{role_id}",
    )
    return type_validate_python(Role, await _request(adapter, bot, request))


async def _create_guild_role(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> Role:
    """https://discord.com/developers/docs/resources/guild#create-guild-role"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/{guild_id}/roles",
        json=data,
    )
    return type_validate_python(Role, await _request(adapter, bot, request))


async def _modify_guild_role_positions(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> list[Role]:
    """https://discord.com/developers/docs/resources/guild#modify-guild-role-positions"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/roles",
        json=data,
    )
    return type_validate_python(list[Role], await _request(adapter, bot, request))


async def _modify_guild_role(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    role_id: SnowflakeType,
    **data,
) -> Role:
    """https://discord.com/developers/docs/resources/guild#modify-guild-role"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/roles/{role_id}",
        json=data,
    )
    return type_validate_python(Role, await _request(adapter, bot, request))


async def _modify_guild_MFA_level(  # noqa: N802 # TODO)): 验证接口是否还存在
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> None:
    """https://discord.com/developers/docs/resources/guild#modify-guild-mfa-level"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/mfa",
        json=data,
    )
    await _request(adapter, bot, request)


async def _delete_guild_role(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    role_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/guild#delete-guild-role"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/roles/{role_id}",
    )
    await _request(adapter, bot, request)


async def _get_guild_prune_count(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> dict[Literal["pruned"], int]:
    """https://discord.com/developers/docs/resources/guild#get-guild-prune-count"""
    if "include_roles" in data:
        data["include_roles"] = ",".join(str(role) for role in data["include_roles"])
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/prune",
        params=data,
    )
    return await _request(adapter, bot, request)


async def _begin_guild_prune(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> dict[Literal["pruned"], int]:
    """https://discord.com/developers/docs/resources/guild#begin-guild-prune"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/{guild_id}/prune",
        json=data,
    )
    return await _request(adapter, bot, request)


async def _get_guild_voice_regions(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[VoiceRegion]:
    """https://discord.com/developers/docs/resources/guild#get-guild-voice-regions"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/regions",
    )
    return type_validate_python(
        list[VoiceRegion], await _request(adapter, bot, request)
    )


async def _get_guild_invites(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[Invite]:
    """https://discord.com/developers/docs/resources/guild#get-guild-invites"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/invites",
    )
    return type_validate_python(list[Invite], await _request(adapter, bot, request))


async def _get_guild_integrations(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[Integration]:
    """https://discord.com/developers/docs/resources/guild#get-guild-integrations"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/integrations",
    )
    return type_validate_python(
        list[Integration], await _request(adapter, bot, request)
    )


async def _delete_guild_integration(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    integration_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/guild#delete-guild-integration"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/integrations/{integration_id}",
    )
    await _request(adapter, bot, request)


async def _get_guild_widget_settings(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> GuildWidgetSettings:
    """https://discord.com/developers/docs/resources/guild#get-guild-widget-settings"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/widget",
    )
    return type_validate_python(
        GuildWidgetSettings, await _request(adapter, bot, request)
    )


async def _modify_guild_widget(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> GuildWidget:
    """https://discord.com/developers/docs/resources/guild#modify-guild-widget"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/widget",
        json=data,
    )
    return type_validate_python(GuildWidget, await _request(adapter, bot, request))


async def _get_guild_widget(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> GuildWidget:
    """https://discord.com/developers/docs/resources/guild#get-guild-widget"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/widget.json",
    )
    return type_validate_python(GuildWidget, await _request(adapter, bot, request))


async def _get_guild_vanity_url(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> Invite:
    """https://discord.com/developers/docs/resources/guild#get-guild-vanity-url"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/vanity-url",
    )
    return type_validate_python(Invite, await _request(adapter, bot, request))


async def _get_guild_widget_image(  # noqa: ANN202 # TODO)): 校验接口返回值并更新类型
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **params
):
    """https://discord.com/developers/docs/resources/guild#get-guild-widget-image"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/widget.png",
        params=params,
    )
    return await _request(adapter, bot, request)


async def _get_guild_welcome_screen(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> WelcomeScreen:
    """https://discord.com/developers/docs/resources/guild#get-guild-welcome-screen"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/welcome-screen",
    )
    return type_validate_python(WelcomeScreen, await _request(adapter, bot, request))


async def _modify_guild_welcome_screen(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> WelcomeScreen:
    """https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(
        type_validate_python(ModifyGuildWelcomeScreenParams, data), exclude_unset=True
    )
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/welcome-screen",
        json=data,
    )
    return type_validate_python(WelcomeScreen, await _request(adapter, bot, request))


async def _get_guild_onboarding(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> GuildOnboarding:
    """https://discord.com/developers/docs/resources/guild#get-guild-onboarding"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/onboarding",
    )
    return type_validate_python(GuildOnboarding, await _request(adapter, bot, request))


async def _modify_guild_onboarding(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> GuildOnboarding:
    """https://discord.com/developers/docs/resources/guild#modify-guild-onboarding"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(
        type_validate_python(ModifyGuildOnboardingParams, data), exclude_unset=True
    )
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"guilds/{guild_id}/onboarding",
        json=data,
    )
    return type_validate_python(GuildOnboarding, await _request(adapter, bot, request))


# Voice
# https://discord.com/developers/docs/resources/voice


async def _list_voice_regions(adapter: "Adapter", bot: "Bot") -> list[VoiceRegion]:
    """https://discord.com/developers/docs/resources/voice#list-voice-regions"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "voice/regions",
    )
    return type_validate_python(
        list[VoiceRegion], await _request(adapter, bot, request)
    )


async def _get_current_user_voice_state(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> VoiceState:
    """https://discord.com/developers/docs/resources/voice#get-current-user-voice-state"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/voice-states/@me",
    )
    return type_validate_python(VoiceState, await _request(adapter, bot, request))


async def _get_user_voice_state(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, user_id: SnowflakeType
) -> VoiceState:
    """https://discord.com/developers/docs/resources/voice#get-user-voice-state"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
    )
    return type_validate_python(VoiceState, await _request(adapter, bot, request))


async def _modify_current_user_voice_state(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> None:
    """https://discord.com/developers/docs/resources/voice#modify-current-user-voice-state"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/voice-states/@me",
        json=data,
    )
    await _request(adapter, bot, request)


async def _modify_user_voice_state(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    user_id: SnowflakeType,
    **data,
) -> None:
    """https://discord.com/developers/docs/resources/voice#modify-user-voice-state"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
        json=data,
    )
    await _request(adapter, bot, request)


# Guild Scheduled Event
# see https://discord.com/developers/docs/resources/guild-scheduled-event


async def _list_scheduled_events_for_guild(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **params
) -> list[GuildScheduledEvent]:
    """https://discord.com/developers/docs/resources/guild-scheduled-event#list-scheduled-events-for-guild"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/scheduled-events",
        params=params,
    )
    return type_validate_python(
        list[GuildScheduledEvent], await _request(adapter, bot, request)
    )


async def _create_guild_schedule_event(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> GuildScheduledEvent:
    """https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(
        type_validate_python(CreateGuildScheduledEventParams, data), exclude_none=True
    )
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/{guild_id}/scheduled-events",
        json=data,
    )
    return type_validate_python(
        GuildScheduledEvent, await _request(adapter, bot, request)
    )


async def _get_guild_scheduled_event(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    event_id: SnowflakeType,
    **params,
) -> GuildScheduledEvent:
    """https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
        params=params,
    )
    return type_validate_python(
        GuildScheduledEvent, await _request(adapter, bot, request)
    )


async def _modify_guild_scheduled_event(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    event_id: SnowflakeType,
    **data,
) -> GuildScheduledEvent:
    """https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    data = model_dump(
        type_validate_python(ModifyGuildScheduledEventParams, data), exclude_unset=True
    )
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
        json=data,
    )
    return type_validate_python(
        GuildScheduledEvent, await _request(adapter, bot, request)
    )


async def _delete_guild_scheduled_event(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, event_id: SnowflakeType
) -> None:
    """https://discord.com/developers/docs/resources/guild-scheduled-event#delete-guild-scheduled-event"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
    )
    await _request(adapter, bot, request)


async def _get_guild_scheduled_event_users(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    event_id: SnowflakeType,
    **params,
) -> list[GuildScheduledEventUser]:
    """https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event-users"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}/users",
        params=params,
    )
    return type_validate_python(
        list[GuildScheduledEventUser], await _request(adapter, bot, request)
    )


# Guild Template
# see https://discord.com/developers/docs/resources/guild-template


async def _get_guild_template(
    adapter: "Adapter", bot: "Bot", template_code: str
) -> GuildTemplate:
    """https://discord.com/developers/docs/resources/guild-template#get-guild-template"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/templates/{template_code}",
    )
    return type_validate_python(GuildTemplate, await _request(adapter, bot, request))


async def _create_guild_from_guild_template(
    adapter: "Adapter", bot: "Bot", template_code: str, **data
) -> Guild:
    """https://discord.com/developers/docs/resources/guild-template#create-guild-from-guild-template"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/templates/{template_code}",
        json=data,
    )
    return type_validate_python(Guild, await _request(adapter, bot, request))


async def _get_guild_templates(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[GuildTemplate]:
    """https://discord.com/developers/docs/resources/guild-template#get-guild-templates"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/templates",
    )
    return type_validate_python(
        list[GuildTemplate], await _request(adapter, bot, request)
    )


async def _create_guild_template(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, **data
) -> GuildTemplate:
    """https://discord.com/developers/docs/resources/guild-template#create-guild-template"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"guilds/{guild_id}/templates",
        json=data,
    )
    return type_validate_python(GuildTemplate, await _request(adapter, bot, request))


async def _sync_guild_template(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, template_code: str
) -> GuildTemplate:
    """https://discord.com/developers/docs/resources/guild-template#sync-guild-template"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PUT",
        url=adapter.base_url / f"guilds/{guild_id}/templates/{template_code}",
    )
    return type_validate_python(GuildTemplate, await _request(adapter, bot, request))


async def _modify_guild_template(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, template_code: str, **data
) -> GuildTemplate:
    """https://discord.com/developers/docs/resources/guild-template#modify-guild-template"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/templates/{template_code}",
        json=data,
    )
    return type_validate_python(GuildTemplate, await _request(adapter, bot, request))


async def _delete_guild_template(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, template_code: str
) -> None:
    """https://discord.com/developers/docs/resources/guild-template#delete-guild-template"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/templates/{template_code}",
    )
    await _request(adapter, bot, request)


# Invite
# see https://discord.com/developers/docs/resources/invite


async def _get_invite(
    adapter: "Adapter", bot: "Bot", invite_code: str, **params
) -> Invite:
    """https://discord.com/developers/docs/resources/invite#get-invite"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"invites/{invite_code}",
        params=params,
    )
    return type_validate_python(Invite, await _request(adapter, bot, request))


async def _delete_invite(
    adapter: "Adapter", bot: "Bot", invite_code: str, reason: Optional[str] = None
) -> Invite:
    """https://discord.com/developers/docs/resources/invite#delete-invite"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"invites/{invite_code}",
    )
    return type_validate_python(Invite, await _request(adapter, bot, request))


# Poll
# see https://discord.com/developers/docs/resources/poll


async def _get_answer_voters(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    answer_id: int,
    **params,
) -> AnswerVoters:
    """https://discord.com/developers/docs/resources/poll#get-answer-voters"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"channels/{channel_id}/polls/{message_id}/answers/{answer_id}",
        params=params,
    )
    return type_validate_python(AnswerVoters, await _request(adapter, bot, request))


async def _end_poll(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
) -> MessageGet:
    """https://discord.com/developers/docs/resources/poll#end-poll"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/polls/{message_id}/expire",
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


# SKU
# see https://discord.com/developers/docs/resources/sku


async def _list_SKUs(  # noqa: N802
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType
) -> list[SKU]:
    """https://discord.com/developers/docs/resources/sku#list-skus"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"applications/{application_id}/skus",
    )
    return type_validate_python(list[SKU], await _request(adapter, bot, request))


# Stage Instance
# see https://discord.com/developers/docs/resources/stage-instance


async def _create_stage_instance(
    adapter: "Adapter", bot: "Bot", **data
) -> StageInstance:
    """https://discord.com/developers/docs/resources/stage-instance#create-stage-instance"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / "stage-instances",
        json=data,
    )
    return type_validate_python(StageInstance, await _request(adapter, bot, request))


async def _get_stage_instance(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType
) -> Optional[StageInstance]:
    """https://discord.com/developers/docs/resources/stage-instance#get-stage-instance"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"stage-instances/{channel_id}",
    )
    return type_validate_python(
        Optional[StageInstance],
        await _request(adapter, bot, request),
    )


async def _modify_stage_instance(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> StageInstance:
    """https://discord.com/developers/docs/resources/stage-instance#modify-stage-instance"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"stage-instances/{channel_id}",
        json=data,
    )
    return type_validate_python(StageInstance, await _request(adapter, bot, request))


async def _delete_stage_instance(
    adapter: "Adapter",
    bot: "Bot",
    channel_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/stage-instance#delete-stage-instance"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"stage-instances/{channel_id}",
    )
    await _request(adapter, bot, request)


# Sticker
# see https://discord.com/developers/docs/resources/sticker


async def _get_sticker(
    adapter: "Adapter", bot: "Bot", sticker_id: SnowflakeType
) -> Sticker:
    """https://discord.com/developers/docs/resources/sticker#get-sticker"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"stickers/{sticker_id}",
    )
    return type_validate_python(Sticker, await _request(adapter, bot, request))


async def _list_nitro_sticker_packs(
    adapter: "Adapter", bot: "Bot"
) -> list[StickerPack]:
    """https://discord.com/developers/docs/resources/sticker#list-sticker-packs"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "sticker-packs",
    )
    return type_validate_python(
        list[StickerPack], await _request(adapter, bot, request)
    )


async def _get_sticker_packs(
    adapter: "Adapter", bot: "Bot", pack_id: SnowflakeType
) -> StickerPack:
    """https://discord.com/developers/docs/resources/sticker#get-sticker-pack"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"sticker-packs/{pack_id}",
    )
    return type_validate_python(StickerPack, await _request(adapter, bot, request))


async def _list_guild_stickers(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[Sticker]:
    """https://discord.com/developers/docs/resources/sticker#list-guild-stickers"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/stickers",
    )
    return type_validate_python(list[Sticker], await _request(adapter, bot, request))


async def _get_guild_sticker(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType, sticker_id: SnowflakeType
) -> Sticker:
    """https://discord.com/developers/docs/resources/sticker#get-guild-sticker"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
    )
    return type_validate_python(Sticker, await _request(adapter, bot, request))


async def _create_guild_sticker(  # noqa: PLR0913
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    name: str,
    description: str,
    tags: str,
    file: File,
    reason: Optional[str] = None,
) -> Sticker:
    """https://discord.com/developers/docs/resources/sticker#create-guild-sticker"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
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
        url=adapter.base_url / f"guilds/{guild_id}/stickers",
        json={"name": name, "description": description, "tags": tags},
        files=form,
    )
    return type_validate_python(Sticker, await _request(adapter, bot, request))


async def _modify_guild_sticker(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    sticker_id: SnowflakeType,
    **data,
) -> Sticker:
    """https://discord.com/developers/docs/resources/sticker#modify-guild-sticker"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
        json=data,
    )
    return type_validate_python(Sticker, await _request(adapter, bot, request))


async def _delete_guild_sticker(
    adapter: "Adapter",
    bot: "Bot",
    guild_id: SnowflakeType,
    sticker_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/sticker#delete-guild-sticker"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
    )
    await _request(adapter, bot, request)


# Subscription
# see https://discord.com/developers/docs/resources/subscription


async def _list_SKU_subscriptions(  # noqa: N802, PLR0913
    adapter: "Adapter",
    bot: "Bot",
    sku_id: SnowflakeType,
    before: Optional[SnowflakeType] = None,
    after: Optional[SnowflakeType] = None,
    limit: Optional[int] = None,
    user_id: Optional[SnowflakeType] = None,
) -> list[Subscription]:
    """https://discord.com/developers/docs/resources/subscription#list-sku-subscriptions

    Note: user_id is required except for OAuth queries.
    """
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    params = {
        "before": before,
        "after": after,
        "limit": limit,
        "user_id": user_id,
    }
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"skus/{sku_id}/subscriptions",
        params={key: value for key, value in params.items() if value is not None},
    )
    return type_validate_python(
        list[Subscription], await _request(adapter, bot, request)
    )


async def _get_SKU_subscription(  # noqa: N802
    adapter: "Adapter",
    bot: "Bot",
    sku_id: SnowflakeType,
    subscription_id: SnowflakeType,
) -> Subscription:
    """https://discord.com/developers/docs/resources/subscription#get-sku-subscription"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"skus/{sku_id}/subscriptions/{subscription_id}",
    )
    return type_validate_python(Subscription, await _request(adapter, bot, request))


# Users
# see https://discord.com/developers/docs/resources/user


async def _get_current_user(adapter: "Adapter", bot: "Bot") -> User:
    """https://discord.com/developers/docs/resources/user#get-current-user"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "users/@me",
    )
    return type_validate_python(User, await _request(adapter, bot, request))


async def _get_user(adapter: "Adapter", bot: "Bot", user_id: SnowflakeType) -> User:
    """https://discord.com/developers/docs/resources/user#get-user"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"users/{user_id}",
    )
    return type_validate_python(User, await _request(adapter, bot, request))


async def _modify_current_user(adapter: "Adapter", bot: "Bot", **data) -> User:
    """https://discord.com/developers/docs/resources/user#modify-current-user"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / "users/@me",
        json=data,
    )
    return type_validate_python(User, await _request(adapter, bot, request))


async def _get_current_user_guilds(
    adapter: "Adapter", bot: "Bot", **params
) -> list[CurrentUserGuild]:
    """https://discord.com/developers/docs/resources/user#get-current-user-guilds"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "users/@me/guilds",
        params=params,
    )
    return type_validate_python(
        list[CurrentUserGuild], await _request(adapter, bot, request)
    )


async def _get_current_user_guild_member(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> GuildMember:
    """https://discord.com/developers/docs/resources/user#get-current-user-guild-member"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"users/@me/guilds/{guild_id}/member",
    )
    return type_validate_python(GuildMember, await _request(adapter, bot, request))


async def _leave_guild(adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType) -> None:
    """https://discord.com/developers/docs/resources/user#leave-guild"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"users/@me/guilds/{guild_id}",
    )
    await _request(adapter, bot, request)


async def _create_DM(adapter: "Adapter", bot: "Bot", **data) -> Channel:  # noqa: N802
    """https://discord.com/developers/docs/resources/user#create-dm"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / "users/@me/channels",
        json=data,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _create_group_DM(adapter: "Adapter", bot: "Bot", **data) -> Channel:  # noqa: N802
    """https://discord.com/developers/docs/resources/user#create-group-dm"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / "users/@me/channels",
        json=data,
    )
    return type_validate_python(Channel, await _request(adapter, bot, request))


async def _get_user_connections(
    adapter: "Adapter",
    bot: "Bot",
) -> list[Connection]:
    """https://discord.com/developers/docs/resources/user#get-current-user-connections"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "users/@me/connections",
    )
    return type_validate_python(list[Connection], await _request(adapter, bot, request))


async def _get_user_application_role_connection(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType
) -> ApplicationRoleConnection:
    """https://discord.com/developers/docs/resources/user#get-current-user-application-role-connection"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url
        / f"users/@me/applications/{application_id}/role-connection",
    )
    return type_validate_python(
        ApplicationRoleConnection, await _request(adapter, bot, request)
    )


async def _update_user_application_role_connection(
    adapter: "Adapter", bot: "Bot", application_id: SnowflakeType, **data
) -> ApplicationRoleConnection:
    """https://discord.com/developers/docs/resources/user#update-current-user-application-role-connection"""
    if "metadata" in data and isinstance(
        data["metadata"], ApplicationRoleConnectionMetadata
    ):
        data["metadata"] = model_dump(data["metadata"], exclude_unset=True)
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url
        / f"users/@me/applications/{application_id}/role-connection",
        json=data,
    )
    return type_validate_python(
        ApplicationRoleConnection, await _request(adapter, bot, request)
    )


# Webhook
# see https://discord.com/developers/docs/resources/webhook


async def _create_webhook(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType, **data
) -> Webhook:
    """https://discord.com/developers/docs/resources/webhook#create-webhook"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"channels/{channel_id}/webhooks",
        json=data,
    )
    return type_validate_python(Webhook, await _request(adapter, bot, request))


async def _get_channel_webhooks(
    adapter: "Adapter", bot: "Bot", channel_id: SnowflakeType
) -> list[Webhook]:
    """https://discord.com/developers/docs/resources/webhook#get-channel-webhooks"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"channels/{channel_id}/webhooks",
    )
    return type_validate_python(list[Webhook], await _request(adapter, bot, request))


async def _get_guild_webhooks(
    adapter: "Adapter", bot: "Bot", guild_id: SnowflakeType
) -> list[Webhook]:
    """https://discord.com/developers/docs/resources/webhook#get-guild-webhooks"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"guilds/{guild_id}/webhooks",
    )
    return type_validate_python(list[Webhook], await _request(adapter, bot, request))


async def _get_webhook(
    adapter: "Adapter", bot: "Bot", webhook_id: SnowflakeType
) -> Webhook:
    """https://discord.com/developers/docs/resources/webhook#get-webhook"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"webhooks/{webhook_id}",
    )
    return type_validate_python(Webhook, await _request(adapter, bot, request))


async def _get_webhook_with_token(
    adapter: "Adapter", bot: "Bot", webhook_id: SnowflakeType, token: str
) -> Webhook:
    """https://discord.com/developers/docs/resources/webhook#get-webhook-with-token"""
    request = Request(
        method="GET",
        url=adapter.base_url / f"webhooks/{webhook_id}/{token}",
    )
    return type_validate_python(Webhook, await _request(adapter, bot, request))


async def _modify_webhook(
    adapter: "Adapter", bot: "Bot", webhook_id: SnowflakeType, **data
) -> Webhook:
    """https://discord.com/developers/docs/resources/webhook#modify-webhook"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if data.get("reason"):
        headers["X-Audit-Log-Reason"] = data.pop("reason")
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / f"webhooks/{webhook_id}",
        json=data,
    )
    return type_validate_python(Webhook, await _request(adapter, bot, request))


async def _modify_webhook_with_token(
    adapter: "Adapter", bot: "Bot", webhook_id: SnowflakeType, token: str, **data
) -> Webhook:
    """https://discord.com/developers/docs/resources/webhook#modify-webhook-with-token"""
    request = Request(
        method="PATCH",
        url=adapter.base_url / f"webhooks/{webhook_id}/{token}",
        json=data,
    )
    return type_validate_python(Webhook, await _request(adapter, bot, request))


async def _delete_webhook(
    adapter: "Adapter",
    bot: "Bot",
    webhook_id: SnowflakeType,
    reason: Optional[str] = None,
) -> None:
    """https://discord.com/developers/docs/resources/webhook#delete-webhook"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    if reason:
        headers["X-Audit-Log-Reason"] = reason
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"webhooks/{webhook_id}",
    )
    await _request(adapter, bot, request)


async def _delete_webhook_with_token(
    adapter: "Adapter", bot: "Bot", webhook_id: SnowflakeType, token: str
) -> None:
    """https://discord.com/developers/docs/resources/webhook#delete-webhook-with-token"""
    request = Request(
        method="DELETE",
        url=adapter.base_url / f"webhooks/{webhook_id}/{token}",
    )
    await _request(adapter, bot, request)


async def _execute_webhook(
    adapter: "Adapter", bot: "Bot", webhook_id: SnowflakeType, token: str, **data
) -> Optional[MessageGet]:
    """https://discord.com/developers/docs/resources/webhook#execute-webhook"""
    params = {}
    if data.get("wait"):
        params["wait"] = str(data.pop("wait"))
    if data.get("thread_id"):
        params["thread_id"] = data.pop("thread_id")
    data = parse_data(data, ExecuteWebhookParams)
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"webhooks/{webhook_id}/{token}",
        params=params,
        **data,
    )
    resp = await _request(adapter, bot, request)
    if resp:
        return type_validate_python(MessageGet, resp)
    return resp


async def _execute_slack_compatible_webhook(
    adapter: "Adapter", bot: "Bot", webhook_id: SnowflakeType, token: str, **params
) -> None:
    """https://discord.com/developers/docs/resources/webhook#execute-slackcompatible-webhook"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"webhooks/{webhook_id}/{token}/slack",
        params=params,
    )
    await _request(adapter, bot, request)


async def _execute_github_compatible_webhook(
    adapter: "Adapter", bot: "Bot", webhook_id: SnowflakeType, token: str, **params
) -> None:
    """https://discord.com/developers/docs/resources/webhook#execute-githubcompatible-webhook"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="POST",
        url=adapter.base_url / f"webhooks/{webhook_id}/{token}/github",
        params=params,
    )
    await _request(adapter, bot, request)


async def _get_webhook_message(
    adapter: "Adapter",
    bot: "Bot",
    webhook_id: SnowflakeType,
    token: str,
    message_id: SnowflakeType,
    **params,
) -> MessageGet:
    """https://discord.com/developers/docs/resources/webhook#get-webhook-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / f"webhooks/{webhook_id}/{token}/messages/{message_id}",
        params=params,
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _edit_webhook_message(adapter: "Adapter", bot: "Bot", **data) -> MessageGet:
    """https://discord.com/developers/docs/resources/webhook#edit-webhook-message"""
    params = {}
    if data.get("thread_id"):
        params["thread_id"] = data.pop("thread_id")
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    data = parse_data(data, ExecuteWebhookParams)
    request = Request(
        headers=headers,
        method="PATCH",
        url=adapter.base_url / "webhooks/@me/messages",
        params=params,
        **data,
    )
    return type_validate_python(MessageGet, await _request(adapter, bot, request))


async def _delete_webhook_message(
    adapter: "Adapter",
    bot: "Bot",
    webhook_id: SnowflakeType,
    token: str,
    message_id: SnowflakeType,
    **params,
) -> None:
    """https://discord.com/developers/docs/resources/webhook#delete-webhook-message"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="DELETE",
        url=adapter.base_url / f"webhooks/{webhook_id}/{token}/messages/{message_id}",
        params=params,
    )
    await _request(adapter, bot, request)


# Gateway
# see https://discord.com/developers/docs/topics/gateway


async def _get_gateway(adapter: "Adapter", bot: "Bot") -> Gateway:
    """https://discord.com/developers/docs/topics/gateway#get-gateway"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "gateway",
    )
    return type_validate_python(Gateway, await _request(adapter, bot, request))


async def _get_gateway_bot(adapter: "Adapter", bot: "Bot") -> GatewayBot:
    """https://discord.com/developers/docs/topics/gateway#get-gateway-bot"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "gateway/bot",
    )
    return type_validate_python(GatewayBot, await _request(adapter, bot, request))


# OAuth2
# see https://discord.com/developers/docs/topics/oauth2


async def _get_current_bot_application_information(
    adapter: "Adapter", bot: "Bot"
) -> Application:
    """https://discord.com/developers/docs/topics/oauth2#get-current-bot-application-information"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "oauth2/applications/@me",
    )
    return type_validate_python(Application, await _request(adapter, bot, request))


async def _get_current_authorization_information(
    adapter: "Adapter", bot: "Bot"
) -> AuthorizationResponse:
    """https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information"""
    headers = {"Authorization": adapter.get_authorization(bot.bot_info)}
    request = Request(
        headers=headers,
        method="GET",
        url=adapter.base_url / "oauth2/@me",
    )
    return type_validate_python(
        AuthorizationResponse, await _request(adapter, bot, request)
    )


API_HANDLERS: dict[str, Callable[..., Awaitable[Any]]] = {
    "get_global_application_commands": _get_global_application_commands,
    "create_global_application_command": _create_global_application_command,
    "get_global_application_command": _get_global_application_command,
    "edit_global_application_command": _edit_global_application_command,
    "delete_global_application_command": _delete_global_application_command,
    "bulk_overwrite_global_application_commands": (
        _bulk_overwrite_global_application_commands
    ),
    "get_guild_application_commands": _get_guild_application_commands,
    "create_guild_application_command": _create_guild_application_command,
    "get_guild_application_command": _get_guild_application_command,
    "edit_guild_application_command": _edit_guild_application_command,
    "delete_guild_application_command": _delete_guild_application_command,
    "bulk_overwrite_guild_application_commands": (
        _bulk_overwrite_guild_application_commands
    ),
    "get_guild_application_command_permissions": (
        _get_guild_application_command_permissions
    ),
    "get_application_command_permissions": _get_application_command_permissions,
    "edit_application_command_permissions": _edit_application_command_permissions,
    "create_interaction_response": _create_interaction_response,
    "get_origin_interaction_response": _get_origin_interaction_response,
    "edit_origin_interaction_response": _edit_origin_interaction_response,
    "delete_origin_interaction_response": _delete_origin_interaction_response,
    "create_followup_message": _create_followup_message,
    "get_followup_message": _get_followup_message,
    "edit_followup_message": _edit_followup_message,
    "delete_followup_message": _delete_followup_message,
    "get_current_application": _get_current_application,
    "edit_current_application": _edit_current_application,
    "get_application_activity_instance": _get_application_activity_instance,
    "get_application_role_connection_metadata_records": (
        _get_application_role_connection_metadata_records
    ),
    "update_application_role_connection_metadata_records": (
        _update_application_role_connection_metadata_records
    ),
    "get_guild_audit_log": _get_guild_audit_log,
    "list_auto_moderation_rules_for_guild": _list_auto_moderation_rules_for_guild,
    "get_auto_moderation_rule": _get_auto_moderation_rule,
    "create_auto_moderation_rule": _create_auto_moderation_rule,
    "modify_auto_moderation_rule": _modify_auto_moderation_rule,
    "delete_auto_moderation_rule": _delete_auto_moderation_rule,
    "get_channel": _get_channel,
    "modify_DM": _modify_DM,
    "modify_channel": _modify_channel,
    "modify_thread": _modify_thread,
    "delete_channel": _delete_channel,
    "get_channel_messages": _get_channel_messages,
    "get_channel_message": _get_channel_message,
    "create_message": _create_message,
    "crosspost_message": _crosspost_message,
    "create_reaction": _create_reaction,
    "delete_own_reaction": _delete_own_reaction,
    "delete_user_reaction": _delete_user_reaction,
    "get_reactions": _get_reactions,
    "delete_all_reactions": _delete_all_reactions,
    "delete_all_reactions_for_emoji": _delete_all_reactions_for_emoji,
    "edit_message": _edit_message,
    "delete_message": _delete_message,
    "bulk_delete_message": _bulk_delete_message,
    "edit_channel_permissions": _edit_channel_permissions,
    "get_channel_invites": _get_channel_invites,
    "create_channel_invite": _create_channel_invite,
    "delete_channel_permission": _delete_channel_permission,
    "follow_announcement_channel": _follow_announcement_channel,
    "trigger_typing_indicator": _trigger_typing_indicator,
    "get_pinned_messages": _get_pinned_messages,
    "pin_message": _pin_message,
    "unpin_message": _unpin_message,
    "group_DM_add_recipient": _group_DM_add_recipient,
    "group_DM_remove_recipient": _group_DM_remove_recipient,
    "start_thread_from_message": _start_thread_from_message,
    "start_thread_without_message": _start_thread_without_message,
    "start_thread_in_forum_channel": _start_thread_in_forum_channel,
    "join_thread": _join_thread,
    "add_thread_member": _add_thread_member,
    "leave_thread": _leave_thread,
    "remove_thread_member": _remove_thread_member,
    "get_thread_member": _get_thread_member,
    "list_thread_members": _list_thread_members,
    "list_public_archived_threads": _list_public_archived_threads,
    "list_private_archived_threads": _list_private_archived_threads,
    "list_joined_private_archived_threads": _list_joined_private_archived_threads,
    "list_guild_emojis": _list_guild_emojis,
    "get_guild_emoji": _get_guild_emoji,
    "create_guild_emoji": _create_guild_emoji,
    "modify_guild_emoji": _modify_guild_emoji,
    "delete_guild_emoji": _delete_guild_emoji,
    "list_application_emojis": _list_application_emojis,
    "get_application_emoji": _get_application_emoji,
    "create_application_emoji": _create_application_emoji,
    "modify_application_emoji": _modify_application_emoji,
    "delete_application_emoji": _delete_application_emoji,
    "list_entitlements": _list_entitlements,
    "consume_an_entitlement": _consume_an_entitlement,
    "create_test_entitlement": _create_test_entitlement,
    "delete_test_entitlement": _delete_test_entitlement,
    "create_guild": _create_guild,
    "get_guild": _get_guild,
    "get_guild_preview": _get_guild_preview,
    "modify_guild": _modify_guild,
    "delete_guild": _delete_guild,
    "get_guild_channels": _get_guild_channels,
    "create_guild_channel": _create_guild_channel,
    "modify_guild_channel_positions": _modify_guild_channel_positions,
    "list_active_guild_threads": _list_active_guild_threads,
    "get_guild_member": _get_guild_member,
    "list_guild_members": _list_guild_members,
    "search_guild_members": _search_guild_members,
    "add_guild_member": _add_guild_member,
    "modify_guild_member": _modify_guild_member,
    "modify_current_member": _modify_current_member,
    "modify_current_user_nick": _modify_current_user_nick,
    "add_guild_member_role": _add_guild_member_role,
    "remove_guild_member_role": _remove_guild_member_role,
    "remove_guild_member": _remove_guild_member,
    "get_guild_bans": _get_guild_bans,
    "get_guild_ban": _get_guild_ban,
    "create_guild_ban": _create_guild_ban,
    "remove_guild_ban": _remove_guild_ban,
    "bulk_guild_ban": _bulk_guild_ban,
    "get_guild_roles": _get_guild_roles,
    "get_guild_role": _get_guild_role,
    "create_guild_role": _create_guild_role,
    "modify_guild_role_positions": _modify_guild_role_positions,
    "modify_guild_role": _modify_guild_role,
    "modify_guild_MFA_level": _modify_guild_MFA_level,
    "delete_guild_role": _delete_guild_role,
    "get_guild_prune_count": _get_guild_prune_count,
    "begin_guild_prune": _begin_guild_prune,
    "get_guild_voice_regions": _get_guild_voice_regions,
    "get_guild_invites": _get_guild_invites,
    "get_guild_integrations": _get_guild_integrations,
    "delete_guild_integration": _delete_guild_integration,
    "get_guild_widget_settings": _get_guild_widget_settings,
    "modify_guild_widget": _modify_guild_widget,
    "get_guild_widget": _get_guild_widget,
    "get_guild_vanity_url": _get_guild_vanity_url,
    "get_guild_widget_image": _get_guild_widget_image,
    "get_guild_welcome_screen": _get_guild_welcome_screen,
    "modify_guild_welcome_screen": _modify_guild_welcome_screen,
    "get_guild_onboarding": _get_guild_onboarding,
    "modify_guild_onboarding": _modify_guild_onboarding,
    "list_voice_regions": _list_voice_regions,
    "get_current_user_voice_state": _get_current_user_voice_state,
    "get_user_voice_state": _get_user_voice_state,
    "modify_current_user_voice_state": _modify_current_user_voice_state,
    "modify_user_voice_state": _modify_user_voice_state,
    "list_scheduled_events_for_guild": _list_scheduled_events_for_guild,
    "create_guild_schedule_event": _create_guild_schedule_event,
    "get_guild_scheduled_event": _get_guild_scheduled_event,
    "modify_guild_scheduled_event": _modify_guild_scheduled_event,
    "delete_guild_scheduled_event": _delete_guild_scheduled_event,
    "get_guild_scheduled_event_users": _get_guild_scheduled_event_users,
    "get_guild_template": _get_guild_template,
    "create_guild_from_guild_template": _create_guild_from_guild_template,
    "get_guild_templates": _get_guild_templates,
    "create_guild_template": _create_guild_template,
    "sync_guild_template": _sync_guild_template,
    "modify_guild_template": _modify_guild_template,
    "delete_guild_template": _delete_guild_template,
    "get_invite": _get_invite,
    "delete_invite": _delete_invite,
    "get_answer_voters": _get_answer_voters,
    "end_poll": _end_poll,
    "list_SKUs": _list_SKUs,
    "create_stage_instance": _create_stage_instance,
    "get_stage_instance": _get_stage_instance,
    "modify_stage_instance": _modify_stage_instance,
    "delete_stage_instance": _delete_stage_instance,
    "get_sticker": _get_sticker,
    "list_nitro_sticker_packs": _list_nitro_sticker_packs,
    "get_sticker_packs": _get_sticker_packs,
    "list_guild_stickers": _list_guild_stickers,
    "get_guild_sticker": _get_guild_sticker,
    "create_guild_sticker": _create_guild_sticker,
    "modify_guild_sticker": _modify_guild_sticker,
    "delete_guild_sticker": _delete_guild_sticker,
    "list_SKU_subscriptions": _list_SKU_subscriptions,
    "get_SKU_subscription": _get_SKU_subscription,
    "get_current_user": _get_current_user,
    "get_user": _get_user,
    "modify_current_user": _modify_current_user,
    "get_current_user_guilds": _get_current_user_guilds,
    "get_current_user_guild_member": _get_current_user_guild_member,
    "leave_guild": _leave_guild,
    "create_DM": _create_DM,
    "create_group_DM": _create_group_DM,
    "get_user_connections": _get_user_connections,
    "get_user_application_role_connection": _get_user_application_role_connection,
    "update_user_application_role_connection": _update_user_application_role_connection,
    "create_webhook": _create_webhook,
    "get_channel_webhooks": _get_channel_webhooks,
    "get_guild_webhooks": _get_guild_webhooks,
    "get_webhook": _get_webhook,
    "get_webhook_with_token": _get_webhook_with_token,
    "modify_webhook": _modify_webhook,
    "modify_webhook_with_token": _modify_webhook_with_token,
    "delete_webhook": _delete_webhook,
    "delete_webhook_with_token": _delete_webhook_with_token,
    "execute_webhook": _execute_webhook,
    "execute_slack_compatible_webhook": _execute_slack_compatible_webhook,
    "execute_github_compatible_webhook": _execute_github_compatible_webhook,
    "get_webhook_message": _get_webhook_message,
    "edit_webhook_message": _edit_webhook_message,
    "delete_webhook_message": _delete_webhook_message,
    "get_gateway": _get_gateway,
    "get_gateway_bot": _get_gateway_bot,
    "get_current_bot_application_information": _get_current_bot_application_information,
    "get_current_authorization_information": _get_current_authorization_information,
}
