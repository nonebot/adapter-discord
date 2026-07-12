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
from ...utils import omit_unset

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
        name = fields["name"]
        if not name:
            msg = "name is required"
            raise ValueError(msg)
        data = dict(fields)

        call = RestCall(
            method="POST",
            url=self.base_url / "guilds",
            response=JsonResponse(Guild),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields.get("name", UNSET)
        region = fields.get("region", UNSET)
        verification_level = fields.get("verification_level", UNSET)
        default_message_notifications = fields.get(
            "default_message_notifications", UNSET
        )
        explicit_content_filter = fields.get("explicit_content_filter", UNSET)
        afk_channel_id = fields.get("afk_channel_id", UNSET)
        afk_timeout = fields.get("afk_timeout", UNSET)
        icon = fields.get("icon", UNSET)
        splash = fields.get("splash", UNSET)
        discovery_splash = fields.get("discovery_splash", UNSET)
        banner = fields.get("banner", UNSET)
        system_channel_id = fields.get("system_channel_id", UNSET)
        system_channel_flags = fields.get("system_channel_flags", UNSET)
        rules_channel_id = fields.get("rules_channel_id", UNSET)
        public_updates_channel_id = fields.get("public_updates_channel_id", UNSET)
        preferred_locale = fields.get("preferred_locale", UNSET)
        features = fields.get("features", UNSET)
        description = fields.get("description", UNSET)
        premium_progress_bar_enabled = fields.get("premium_progress_bar_enabled", UNSET)
        safety_alerts_channel_id = fields.get("safety_alerts_channel_id", UNSET)

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
        data = validate_outbound_value(
            ModifyGuildParams,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}",
            response=JsonResponse(Guild),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        invites_disabled_until = fields.get("invites_disabled_until", UNSET)
        dms_disabled_until = fields.get("dms_disabled_until", UNSET)

        data = validate_outbound_value(
            ModifyGuildIncidentActionsParams,
            {
                key: value
                for key, value in {
                    "invites_disabled_until": invites_disabled_until,
                    "dms_disabled_until": dms_disabled_until,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/incident-actions",
            response=JsonResponse(GuildIncidentsData),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields["name"]
        channel_type = fields.get("type")
        topic = fields.get("topic")
        bitrate = fields.get("bitrate")
        user_limit = fields.get("user_limit")
        rate_limit_per_user = fields.get("rate_limit_per_user")
        position = fields.get("position")
        permission_overwrites = fields.get("permission_overwrites")
        parent_id = fields.get("parent_id")
        nsfw = fields.get("nsfw")
        rtc_region = fields.get("rtc_region")
        video_quality_mode = fields.get("video_quality_mode")
        default_auto_archive_duration = fields.get("default_auto_archive_duration")
        default_reaction_emoji = fields.get("default_reaction_emoji")
        available_tags = fields.get("available_tags")
        default_sort_order = fields.get("default_sort_order")

        default_forum_layout = fields.get("default_forum_layout")
        default_thread_rate_limit_per_user = fields.get(
            "default_thread_rate_limit_per_user"
        )
        if not name:
            msg = "name is required"
            raise ValueError(msg)
        data = {
            "name": name,
            "type": channel_type,
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
            "default_forum_layout": default_forum_layout,
            "default_thread_rate_limit_per_user": default_thread_rate_limit_per_user,
        }
        data = validate_outbound_value(
            CreateGuildChannelParams,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/channels",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
            validate_outbound_value(
                ModifyGuildChannelPositionParams,
                {key: value for key, value in channel.items() if value is not UNSET},
            )
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
        access_token = fields["access_token"]
        nick = fields.get("nick")
        roles = fields.get("roles")
        mute = fields.get("mute")
        deaf = fields.get("deaf")

        data = {
            "access_token": access_token,
            "nick": nick,
            "roles": roles,
            "mute": mute,
            "deaf": deaf,
        }
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            response=JsonResponse(GuildMember, allow_empty=True),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
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
        nick = fields.get("nick", UNSET)
        roles = fields.get("roles", UNSET)
        mute = fields.get("mute", UNSET)
        deaf = fields.get("deaf", UNSET)
        channel_id = fields.get("channel_id", UNSET)
        communication_disabled_until = fields.get("communication_disabled_until", UNSET)
        flags = fields.get("flags", UNSET)

        data = validate_outbound_value(
            ModifyGuildMemberParams,
            {
                key: value
                for key, value in {
                    "nick": nick,
                    "roles": roles,
                    "mute": mute,
                    "deaf": deaf,
                    "channel_id": channel_id,
                    "communication_disabled_until": communication_disabled_until,
                    "flags": flags,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        nick = fields.get("nick", UNSET)
        banner = fields.get("banner", UNSET)
        avatar = fields.get("avatar", UNSET)
        bio = fields.get("bio", UNSET)

        data = validate_outbound_value(
            ModifyCurrentMemberParams,
            {
                key: value
                for key, value in {
                    "nick": nick,
                    "banner": banner,
                    "avatar": avatar,
                    "bio": bio,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        nick = fields.get("nick", UNSET)

        data = omit_unset({"nick": nick})
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me/nick",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
            int | None,
            Range(message="delete_message_days must be between 0 and 7", ge=0, le=7),
        ] = None,
        delete_message_seconds: None = None,
        reason: str | None = None,
    ) -> None: ...

    @overload
    async def _api_create_guild_ban(
        self: "AdapterProtocol",
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

        data = {
            "delete_message_days": delete_message_days,
            "delete_message_seconds": delete_message_seconds,
        }
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
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
        user_ids = fields["user_ids"]
        delete_message_seconds = fields.get("delete_message_seconds")

        data = {
            "user_ids": user_ids,
            "delete_message_seconds": delete_message_seconds,
        }
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/bulk-ban",
            response=JsonResponse(BulkBan),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
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
        name = fields.get("name", UNSET)
        permissions = fields.get("permissions", UNSET)
        color = fields.get("color", UNSET)
        colors = fields.get("colors", UNSET)
        hoist = fields.get("hoist", UNSET)
        icon = fields.get("icon", UNSET)
        unicode_emoji = fields.get("unicode_emoji", UNSET)
        mentionable = fields.get("mentionable", UNSET)

        data = validate_outbound_value(
            CreateGuildRoleParams,
            {
                key: value
                for key, value in {
                    "name": name,
                    "permissions": permissions,
                    "color": color,
                    "colors": colors,
                    "hoist": hoist,
                    "icon": icon,
                    "unicode_emoji": unicode_emoji,
                    "mentionable": mentionable,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/roles",
            response=JsonResponse(Role),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
            validate_outbound_value(
                ModifyGuildRolePositionParams,
                {key: value for key, value in role.items() if value is not UNSET},
            )
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
        name = fields.get("name", UNSET)
        permissions = fields.get("permissions", UNSET)
        color = fields.get("color", UNSET)
        colors = fields.get("colors", UNSET)
        hoist = fields.get("hoist", UNSET)
        icon = fields.get("icon", UNSET)
        unicode_emoji = fields.get("unicode_emoji", UNSET)
        mentionable = fields.get("mentionable", UNSET)

        data = validate_outbound_value(
            ModifyGuildRoleParams,
            {
                key: value
                for key, value in {
                    "name": name,
                    "permissions": permissions,
                    "color": color,
                    "colors": colors,
                    "hoist": hoist,
                    "icon": icon,
                    "unicode_emoji": unicode_emoji,
                    "mentionable": mentionable,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
            response=JsonResponse(Role),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        level = fields["level"]

        data = {"level": level}
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/mfa",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        days = fields.get("days")
        compute_prune_count = fields.get("compute_prune_count")
        include_roles = fields.get("include_roles")

        data = {
            "days": days,
            "compute_prune_count": compute_prune_count,
            "include_roles": include_roles,
        }
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/prune",
            response=JsonResponse(Any),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
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
        enabled = fields.get("enabled", UNSET)
        channel_id = fields.get("channel_id", UNSET)

        data = validate_outbound_value(
            ModifyGuildWidgetParams,
            {
                key: value
                for key, value in {"enabled": enabled, "channel_id": channel_id}.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/widget",
            response=JsonResponse(GuildWidgetSettings),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        enabled = fields.get("enabled", UNSET)
        welcome_channels = fields.get("welcome_channels", UNSET)
        description = fields.get("description", UNSET)

        data = {
            "enabled": enabled,
            "welcome_channels": welcome_channels,
            "description": description,
        }
        data = validate_outbound_value(
            ModifyGuildWelcomeScreenParams,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/welcome-screen",
            response=JsonResponse(WelcomeScreen),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        prompts = fields.get("prompts", UNSET)
        default_channel_ids = fields.get("default_channel_ids", UNSET)
        enabled = fields.get("enabled", UNSET)
        mode = fields.get("mode", UNSET)

        data = {
            "prompts": prompts,
            "default_channel_ids": default_channel_ids,
            "enabled": enabled,
            "mode": mode,
        }
        data = validate_outbound_value(
            ModifyGuildOnboardingParams,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/onboarding",
            response=JsonResponse(GuildOnboarding),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields["name"]
        privacy_level = fields["privacy_level"]
        scheduled_start_time = fields["scheduled_start_time"]
        scheduled_end_time = fields.get("scheduled_end_time")
        description = fields.get("description")
        entity_type = fields["entity_type"]
        image = fields.get("image")
        recurrence_rule = fields.get("recurrence_rule")
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
        data = validate_outbound_value(
            CreateGuildScheduledEventParams,
            {
                key: value
                for key, value in data.items()
                if value is not UNSET and value is not None
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events",
            response=JsonResponse(GuildScheduledEvent),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        channel_id = fields.get("channel_id", UNSET)
        entity_metadata = fields.get("entity_metadata", UNSET)
        name = fields.get("name", UNSET)
        privacy_level = fields.get("privacy_level", UNSET)
        scheduled_start_time = fields.get("scheduled_start_time", UNSET)
        scheduled_end_time = fields.get("scheduled_end_time", UNSET)
        description = fields.get("description", UNSET)
        entity_type = fields.get("entity_type", UNSET)
        status = fields.get("status", UNSET)
        image = fields.get("image", UNSET)
        recurrence_rule = fields.get("recurrence_rule", UNSET)

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
        data = validate_outbound_value(
            ModifyGuildScheduledEventParams,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            response=JsonResponse(GuildScheduledEvent),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields["name"]
        description = fields.get("description", UNSET)

        data = validate_outbound_value(
            CreateGuildTemplateParams,
            {
                key: value
                for key, value in {"name": name, "description": description}.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/templates",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields.get("name", UNSET)
        description = fields.get("description", UNSET)

        data = validate_outbound_value(
            ModifyGuildTemplateParams,
            {
                key: value
                for key, value in {"name": name, "description": description}.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
