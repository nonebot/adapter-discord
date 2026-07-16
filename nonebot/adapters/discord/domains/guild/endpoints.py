from typing import TYPE_CHECKING, Annotated, Any, Literal, overload
from typing_extensions import Unpack, deprecated

from .read import (
    Ban,
    Guild,
    GuildIncidentsData,
    GuildMember,
    GuildOnboarding,
    GuildPreview,
    GuildScheduledEvent,
    GuildScheduledEventUser,
    GuildTemplate,
    GuildVanityURL,
    GuildWidget,
    GuildWidgetSettings,
    Integration,
    ListActiveGuildThreadsResponse,
    Role,
    WelcomeScreen,
)
from .types import (
    GuildScheduledEventEntityType,
)
from .write import (
    AddGuildMemberParams,
    BeginGuildPruneParams,
    BulkGuildBanParams,
    CreateGuildBanParams,
    CreateGuildChannelParams,
    CreateGuildParams,
    CreateGuildRoleParams,
    CreateGuildScheduledEventParams,
    CreateGuildTemplateParams,
    ModifyCurrentMemberParams,
    ModifyCurrentUserNickParams,
    ModifyGuildIncidentActionsParams,
    ModifyGuildMemberParams,
    ModifyGuildMFAParams,
    ModifyGuildOnboardingParams,
    ModifyGuildParams,
    ModifyGuildRoleParams,
    ModifyGuildRolePositionParams,
    ModifyGuildScheduledEventParams,
    ModifyGuildTemplateParams,
    ModifyGuildWelcomeScreenParams,
    ModifyGuildWidgetParams,
)
from ..channel.read import Channel
from ..channel.write import (
    ModifyGuildChannelPositionParams,
)
from ..invite.read import Invite
from ..moderation.read import BulkBan
from ..voice.read import VoiceRegion
from ...api.validation import (
    AtMostOne,
    Range,
    validate,
    validate_outbound_value,
)
from ...protocol import UNSET, Snowflake, SnowflakeType, UnsetType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    BytesResponse,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    RestCall,
    _bool_query,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class GuildEndpointMixin:
    @deprecated(
        "_api_create_guild (POST /guilds) is deprecated because Discord removed "
        "the endpoint from official bot-facing docs in 2025 "
        "(discord-api-docs #7715/#7720/#7722)."
    )
    async def _api_create_guild(
        self: "AdapterProtocol",
        bot: "Bot",
        **fields: Unpack[CreateGuildParams],
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild"""
        fields = validate_outbound_value(CreateGuildParams, fields)
        if not fields["name"]:
            msg = "name is required"
            raise ValueError(msg)

        call = RestCall(
            method="POST",
            url=self.base_url / "guilds",
            response=JsonResponse(Guild),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        with_counts: bool | None = None,
    ) -> Guild:
        """Get guild.

        see https://discord.com/developers/docs/resources/guild#get-guild
        """

        params = {"with_counts": _bool_query(value=with_counts)}
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}",
            response=JsonResponse(Guild),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_role_member_counts(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
    ) -> dict[Snowflake, int]:
        """Get guild role member counts.

        see https://discord.com/developers/docs/resources/guild#get-guild-role-member-counts
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/roles/member-counts",
            response=JsonResponse(dict[Snowflake, int]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_preview(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildPreview:
        """Get guild preview.

        see https://discord.com/developers/docs/resources/guild#get-guild-preview
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/preview",
            response=JsonResponse(GuildPreview),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildParams],
    ) -> Guild:
        """Modify guild.

        see https://discord.com/developers/docs/resources/guild#modify-guild
        """
        fields = validate_outbound_value(ModifyGuildParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}",
            response=JsonResponse(Guild),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_incident_actions(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        **fields: Unpack[ModifyGuildIncidentActionsParams],
    ) -> GuildIncidentsData:
        """Modify guild incident actions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-incident-actions
        """
        fields = validate_outbound_value(ModifyGuildIncidentActionsParams, fields)
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/incident-actions",
            response=JsonResponse(GuildIncidentsData),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
        )
        return await REST_EXCHANGE.execute(self, call)

    @deprecated(
        "_api_delete_guild (DELETE /guilds/{guild_id}) is deprecated because "
        "Discord removed the endpoint from official bot-facing docs in 2025 "
        "(discord-api-docs #7715/#7720/#7722)."
    )
    async def _api_delete_guild(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/guild"""

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_channels(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Channel]:
        """Get guild channels.

        see https://discord.com/developers/docs/resources/guild#get-guild-channels
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/channels",
            response=JsonResponse(list[Channel]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_guild_channel(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[CreateGuildChannelParams],
    ) -> Channel:
        """Create guild channel.

        see https://discord.com/developers/docs/resources/guild#create-guild-channel
        """
        fields = validate_outbound_value(CreateGuildChannelParams, fields)
        if not fields["name"]:
            msg = "name is required"
            raise ValueError(msg)
        payload: dict[str, object] = dict(fields)
        for key in (
            "type",
            "topic",
            "bitrate",
            "user_limit",
            "rate_limit_per_user",
            "position",
            "permission_overwrites",
            "parent_id",
            "nsfw",
            "rtc_region",
            "video_quality_mode",
            "default_auto_archive_duration",
            "default_reaction_emoji",
            "available_tags",
            "default_sort_order",
            "default_forum_layout",
            "default_thread_rate_limit_per_user",
        ):
            payload.setdefault(key, None)
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/channels",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_channel_positions(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        channels: list[ModifyGuildChannelPositionParams] | None = None,
        id: SnowflakeType | None = None,  # noqa: A002
        position: int | None | UnsetType = UNSET,
        lock_permissions: bool | UnsetType = UNSET,
        parent_id: SnowflakeType | None | UnsetType = UNSET,
    ) -> None:
        """Modify guild channel positions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions
        """

        if channels is None:
            if id is None:
                msg = "channels or id must be provided"
                raise ValueError(msg)
            channel = ModifyGuildChannelPositionParams(id=Snowflake(id))
            if position is not UNSET:
                channel["position"] = position
            if lock_permissions is not UNSET:
                channel["lock_permissions"] = lock_permissions
            if parent_id is not UNSET:
                channel["parent_id"] = (
                    None if parent_id is None else Snowflake(parent_id)
                )
            channels = [channel]
        payload = [
            validate_outbound_value(ModifyGuildChannelPositionParams, channel)
            for channel in channels
        ]
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/channels",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_list_active_guild_threads(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> ListActiveGuildThreadsResponse:
        """List active guild threads.

        see https://discord.com/developers/docs/resources/guild#list-active-guild-threads
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/threads/active",
            response=JsonResponse(ListActiveGuildThreadsResponse),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> GuildMember:
        """Get guild member.

        see https://discord.com/developers/docs/resources/guild#get-guild-member
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_list_guild_members(
        self: "AdapterProtocol",
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

        params = {"limit": limit, "after": after}
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members",
            response=JsonResponse(list[GuildMember]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_search_guild_members(
        self: "AdapterProtocol",
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

        params = {"query": query, "limit": limit}
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/members/search",
            response=JsonResponse(list[GuildMember]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_add_guild_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        **fields: Unpack[AddGuildMemberParams],
    ) -> GuildMember | None:
        """Add guild member.

        see https://discord.com/developers/docs/resources/guild#add-guild-member
        """
        fields = validate_outbound_value(AddGuildMemberParams, fields)
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            response=JsonResponse(GuildMember, allow_empty=True),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
        )
        resp = await REST_EXCHANGE.execute(self, call)
        if resp:
            return resp
        return None

    async def _api_modify_guild_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildMemberParams],
    ) -> GuildMember:
        """Modify guild member.

        see https://discord.com/developers/docs/resources/guild#modify-guild-member
        """
        fields = validate_outbound_value(ModifyGuildMemberParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_current_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyCurrentMemberParams],
    ) -> GuildMember:
        """Modify current member.

        see https://discord.com/developers/docs/resources/guild#modify-current-member
        """
        fields = validate_outbound_value(ModifyCurrentMemberParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_current_user_nick(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyCurrentUserNickParams],
    ) -> GuildMember:
        """Deprecated in favor of Modify Current Member.

        see https://discord.com/developers/docs/resources/guild#modify-current-user-nick
        """
        fields = validate_outbound_value(ModifyCurrentUserNickParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me/nick",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_add_guild_member_role(
        self: "AdapterProtocol",
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

        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_remove_guild_member_role(
        self: "AdapterProtocol",
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

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_remove_guild_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Remove guild member.

        see https://discord.com/developers/docs/resources/guild#remove-guild-member
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    @overload
    async def _api_get_guild_bans(
        self: "AdapterProtocol",
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
        self: "AdapterProtocol",
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
        self: "AdapterProtocol",
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

        params = {"limit": limit, "before": before, "after": after}
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/bans",
            response=JsonResponse(list[Ban]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_ban(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> Ban:
        """Get guild ban.

        see https://discord.com/developers/docs/resources/guild#get-guild-ban
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
            response=JsonResponse(Ban),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    @overload
    async def _api_create_guild_ban(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        delete_message_days: Annotated[
            int,
            Range(message="delete_message_days must be between 0 and 7", ge=0, le=7),
        ] = ...,
        reason: str | None = None,
    ) -> None: ...

    @overload
    async def _api_create_guild_ban(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        delete_message_seconds: Annotated[
            int,
            Range(
                message="delete_message_seconds must be between 0 and 604800",
                ge=0,
                le=604800,
            ),
        ] = ...,
        reason: str | None = None,
    ) -> None: ...

    async def _api_create_guild_ban(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[CreateGuildBanParams],
    ) -> None:
        """Create guild ban.

        see https://discord.com/developers/docs/resources/guild#create-guild-ban
        """
        fields = validate_outbound_value(CreateGuildBanParams, fields)
        delete_message_days = fields.get("delete_message_days")
        delete_message_seconds = fields.get("delete_message_seconds")
        if "delete_message_days" in fields and "delete_message_seconds" in fields:
            msg = "delete_message_days and delete_message_seconds cannot both be set"
            raise ValueError(msg)
        if delete_message_days is not None and not 0 <= delete_message_days <= 7:  # noqa: PLR2004
            msg = "delete_message_days must be between 0 and 7"
            raise ValueError(msg)
        if (
            delete_message_seconds is not None
            and not 0 <= delete_message_seconds <= 604800  # noqa: PLR2004
        ):
            msg = "delete_message_seconds must be between 0 and 604800"
            raise ValueError(msg)

        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_remove_guild_ban(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Remove guild ban.

        see https://discord.com/developers/docs/resources/guild#remove-guild-ban
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_bulk_guild_ban(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[BulkGuildBanParams],
    ) -> BulkBan:
        """Bulk guild ban.

        see https://discord.com/developers/docs/resources/guild#bulk-guild-ban
        """
        fields = validate_outbound_value(BulkGuildBanParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/bulk-ban",
            response=JsonResponse(BulkBan),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_roles(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Role]:
        """Get guild roles.

        see https://discord.com/developers/docs/resources/guild#get-guild-roles
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/roles",
            response=JsonResponse(list[Role]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_role(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
    ) -> Role:
        """Get guild role.

        see https://discord.com/developers/docs/resources/guild#get-guild-role
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
            response=JsonResponse(Role),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_guild_role(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[CreateGuildRoleParams],
    ) -> Role:
        """Create guild role.

        see https://discord.com/developers/docs/resources/guild#create-guild-role
        """
        fields = validate_outbound_value(CreateGuildRoleParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/roles",
            response=JsonResponse(Role),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_role_positions(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        roles: list[ModifyGuildRolePositionParams] | None = None,
        id: SnowflakeType | None = None,  # noqa: A002
        position: int | None | UnsetType = UNSET,
        reason: str | None = None,
    ) -> list[Role]:
        """Modify guild role positions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-role-positions
        """

        if roles is None:
            if id is None:
                msg = "roles or id must be provided"
                raise ValueError(msg)
            role = ModifyGuildRolePositionParams(id=Snowflake(id))
            if position is not UNSET:
                role["position"] = position
            roles = [role]
        payload = [
            validate_outbound_value(ModifyGuildRolePositionParams, role)
            for role in roles
        ]
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles",
            response=JsonResponse(list[Role]),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_role(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildRoleParams],
    ) -> Role:
        """Modify guild role.

        see https://discord.com/developers/docs/resources/guild#modify-guild-role
        """
        fields = validate_outbound_value(ModifyGuildRoleParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
            response=JsonResponse(Role),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    @deprecated(
        "_api_modify_guild_MFA_level (PATCH /guilds/{guild_id}/mfa) is "
        "deprecated because Discord removed the endpoint from official "
        "bot-facing docs in 2025 (discord-api-docs #7715/#7720/#7722)."
    )
    async def _api_modify_guild_MFA_level(  # noqa: N802
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildMFAParams],
    ) -> None:
        """https://discord.com/developers/docs/resources/guild"""
        fields = validate_outbound_value(ModifyGuildMFAParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/mfa",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_delete_guild_role(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete guild role.

        see https://discord.com/developers/docs/resources/guild#delete-guild-role
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_prune_count(
        self: "AdapterProtocol",
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

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/prune",
            response=JsonResponse(Any),
            auth=BotAuth(bot.bot_info),
            query=data,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_begin_guild_prune(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[BeginGuildPruneParams],
    ) -> dict[Literal["pruned"], int]:
        """Begin guild prune.

        see https://discord.com/developers/docs/resources/guild#begin-guild-prune
        """
        fields = validate_outbound_value(BeginGuildPruneParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/prune",
            response=JsonResponse(Any),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_voice_regions(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[VoiceRegion]:
        """Get guild voice regions.

        see https://discord.com/developers/docs/resources/guild#get-guild-voice-regions
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/regions",
            response=JsonResponse(list[VoiceRegion]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_invites(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Invite]:
        """Get guild invites.

        see https://discord.com/developers/docs/resources/guild#get-guild-invites
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/invites",
            response=JsonResponse(list[Invite]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_integrations(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Integration]:
        """Get guild integrations.

        see https://discord.com/developers/docs/resources/guild#get-guild-integrations
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/integrations",
            response=JsonResponse(list[Integration]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_guild_integration(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        integration_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete guild integration.

        see https://discord.com/developers/docs/resources/guild#delete-guild-integration
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/integrations/{integration_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_widget_settings(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildWidgetSettings:
        """Get guild widget settings.

        see https://discord.com/developers/docs/resources/guild#get-guild-widget-settings
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget",
            response=JsonResponse(GuildWidgetSettings),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_widget(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildWidgetParams],
    ) -> GuildWidgetSettings:
        """Modify guild widget.

        see https://discord.com/developers/docs/resources/guild#modify-guild-widget
        """
        fields = validate_outbound_value(ModifyGuildWidgetParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/widget",
            response=JsonResponse(GuildWidgetSettings),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_widget(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildWidget:
        """Get guild widget.

        see https://discord.com/developers/docs/resources/guild#get-guild-widget
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget.json",
            response=JsonResponse(GuildWidget),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_vanity_url(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildVanityURL:
        """Get guild vanity URL.

        see https://discord.com/developers/docs/resources/guild#get-guild-vanity-url
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/vanity-url",
            response=JsonResponse(GuildVanityURL),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_widget_image(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        style: Literal["shield", "banner1", "banner2", "banner3", "banner4"]
        | None = None,
    ) -> bytes:
        """Get guild widget image.

        see https://discord.com/developers/docs/resources/guild#get-guild-widget-image
        """

        params = {"style": style}
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/widget.png",
            response=BytesResponse(),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_welcome_screen(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> WelcomeScreen:
        """Get guild welcome screen.

        see https://discord.com/developers/docs/resources/guild#get-guild-welcome-screen
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/welcome-screen",
            response=JsonResponse(WelcomeScreen),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_welcome_screen(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildWelcomeScreenParams],
    ) -> WelcomeScreen:
        """Modify guild welcome screen.

        see https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
        """
        fields = validate_outbound_value(ModifyGuildWelcomeScreenParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/welcome-screen",
            response=JsonResponse(WelcomeScreen),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_onboarding(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> GuildOnboarding:
        """Get guild onboarding.

        see https://discord.com/developers/docs/resources/guild#get-guild-onboarding
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/onboarding",
            response=JsonResponse(GuildOnboarding),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_onboarding(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildOnboardingParams],
    ) -> GuildOnboarding:
        """Modify guild onboarding.

        see https://discord.com/developers/docs/resources/guild#modify-guild-onboarding
        """
        fields = validate_outbound_value(ModifyGuildOnboardingParams, fields)
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/onboarding",
            response=JsonResponse(GuildOnboarding),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_scheduled_events_for_guild(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        with_user_count: bool | None = None,
    ) -> list[GuildScheduledEvent]:
        """List scheduled events for guild.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#list-scheduled-events-for-guild
        """

        params = {"with_user_count": _bool_query(value=with_user_count)}
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events",
            response=JsonResponse(list[GuildScheduledEvent]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_guild_schedule_event(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[CreateGuildScheduledEventParams],
    ) -> GuildScheduledEvent:
        """Create guild scheduled event.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event
        """
        fields = validate_outbound_value(CreateGuildScheduledEventParams, fields)
        channel_id = fields.get("channel_id")
        entity_metadata = fields.get("entity_metadata")
        scheduled_end_time = fields.get("scheduled_end_time")
        entity_type = fields["entity_type"]
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

        payload = {key: value for key, value in fields.items() if value is not None}
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events",
            response=JsonResponse(GuildScheduledEvent),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_scheduled_event(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        with_user_count: bool | None = None,
    ) -> GuildScheduledEvent:
        """Get guild scheduled event.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event
        """

        params = {"with_user_count": _bool_query(value=with_user_count)}
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            response=JsonResponse(GuildScheduledEvent),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_scheduled_event(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildScheduledEventParams],
    ) -> GuildScheduledEvent:
        """Modify guild scheduled event.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event
        """
        fields = validate_outbound_value(ModifyGuildScheduledEventParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            response=JsonResponse(GuildScheduledEvent),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_guild_scheduled_event(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
    ) -> None:
        """Delete guild scheduled event.

        see https://discord.com/developers/docs/resources/guild-scheduled-event#delete-guild-scheduled-event
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_get_guild_scheduled_event_users(  # noqa: PLR0913
        self: "AdapterProtocol",
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

        params = {
            "limit": limit,
            "with_member": _bool_query(value=with_member),
            "before": before,
            "after": after,
        }
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}/users",
            response=JsonResponse(list[GuildScheduledEventUser]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_template(
        self: "AdapterProtocol", bot: "Bot", *, template_code: str
    ) -> GuildTemplate:
        """Get guild template.

        see https://discord.com/developers/docs/resources/guild-template#get-guild-template
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/templates/{template_code}",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    @deprecated(
        "_api_create_guild_from_guild_template "
        "(POST /guilds/templates/{template_code}) is deprecated because Discord "
        "removed the endpoint from official bot-facing docs in 2025 "
        "(discord-api-docs #7715/#7720/#7722)."
    )
    async def _api_create_guild_from_guild_template(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        template_code: str,
        name: str,
        icon: str | None = None,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild-template"""

        data = {"name": name, "icon": icon}
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/templates/{template_code}",
            response=JsonResponse(Guild),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_templates(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[GuildTemplate]:
        """Get guild templates.

        see https://discord.com/developers/docs/resources/guild-template#get-guild-templates
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/templates",
            response=JsonResponse(list[GuildTemplate]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_guild_template(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        **fields: Unpack[CreateGuildTemplateParams],
    ) -> GuildTemplate:
        """Create guild template.

        see https://discord.com/developers/docs/resources/guild-template#create-guild-template
        """
        fields = validate_outbound_value(CreateGuildTemplateParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/templates",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_sync_guild_template(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
    ) -> GuildTemplate:
        """Sync guild template.

        see https://discord.com/developers/docs/resources/guild-template#sync-guild-template
        """

        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_template(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
        **fields: Unpack[ModifyGuildTemplateParams],
    ) -> GuildTemplate:
        """Modify guild template.

        see https://discord.com/developers/docs/resources/guild-template#modify-guild-template
        """
        fields = validate_outbound_value(ModifyGuildTemplateParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_guild_template(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        template_code: str,
    ) -> GuildTemplate:
        """Delete guild template.

        see https://discord.com/developers/docs/resources/guild-template#delete-guild-template
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["GuildEndpointMixin"]
