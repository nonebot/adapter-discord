from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Any, Literal, overload
from typing_extensions import deprecated

from nonebot.compat import type_validate_python

from .read import (
    Ban,
    Guild,
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
    Integration,
    ListActiveGuildThreadsResponse,
    OnboardingPrompt,
    RecurrenceRule,
    Role,
    RoleColors,
    WelcomeScreen,
    WelcomeScreenChannel,
)
from .types import (
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    GuildFeature,
    GuildMemberFlags,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventStatus,
    OnboardingMode,
    SystemChannelFlags,
    VerificationLevel,
)
from .write import (
    CreateGuildChannelParams,
    CreateGuildParams,
    CreateGuildRoleParams,
    CreateGuildScheduledEventParams,
    CreateGuildTemplateParams,
    ModifyCurrentMemberParams,
    ModifyGuildIncidentActionsParams,
    ModifyGuildMemberParams,
    ModifyGuildOnboardingParams,
    ModifyGuildParams,
    ModifyGuildRoleParams,
    ModifyGuildRolePositionParams,
    ModifyGuildScheduledEventParams,
    ModifyGuildTemplateParams,
    ModifyGuildWelcomeScreenParams,
    ModifyGuildWidgetParams,
)
from ..channel.read import Channel, DefaultReaction, ForumTagRequest, Overwrite
from ..channel.types import ChannelType, SortOrderTypes, VideoQualityMode
from ..channel.write import ModifyGuildChannelPositionParams
from ..invite.read import Invite
from ..moderation.read import BulkBan
from ..voice.read import VoiceRegion
from ...api.validation import AtMostOne, Range, validate
from ...protocol import UNSET, Missing, MissingOrNullable, Snowflake, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    BytesResponse,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    JsonValueBody,
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
    async def _api_create_guild(  # noqa: PLR0913
        self: "AdapterProtocol",
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
        data = type_validate_python(CreateGuildParams, data)

        call = RestCall(
            method="POST",
            url=self.base_url / "guilds",
            response=JsonResponse(Guild),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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

    async def _api_modify_guild(  # noqa: PLR0913
        self: "AdapterProtocol",
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
        data = type_validate_python(ModifyGuildParams, data)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}",
            response=JsonResponse(Guild),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_incident_actions(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        invites_disabled_until: MissingOrNullable[datetime] = UNSET,
        dms_disabled_until: MissingOrNullable[datetime] = UNSET,
    ) -> GuildIncidentsData:
        """Modify guild incident actions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-incident-actions
        """

        data = type_validate_python(
            ModifyGuildIncidentActionsParams,
            {
                "invites_disabled_until": invites_disabled_until,
                "dms_disabled_until": dms_disabled_until,
            },
        )
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/incident-actions",
            response=JsonResponse(GuildIncidentsData),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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

    async def _api_create_guild_channel(  # noqa: PLR0913
        self: "AdapterProtocol",
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
        data = type_validate_python(CreateGuildChannelParams, data)
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/channels",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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
        position: MissingOrNullable[int] = UNSET,
        lock_permissions: MissingOrNullable[bool] = UNSET,
        parent_id: MissingOrNullable[SnowflakeType] = UNSET,
    ) -> None:
        """Modify guild channel positions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions
        """

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
            type_validate_python(ModifyGuildChannelPositionParams, channel)
            for channel in channels
        ]
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/channels",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(payload),
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

    async def _api_add_guild_member(  # noqa: PLR0913
        self: "AdapterProtocol",
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
            body=JsonValueBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
        )
        resp = await REST_EXCHANGE.execute(self, call)
        if resp:
            return resp
        return None

    async def _api_modify_guild_member(  # noqa: PLR0913
        self: "AdapterProtocol",
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

        data = type_validate_python(
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
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/{user_id}",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_current_member(  # noqa: PLR0913
        self: "AdapterProtocol",
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

        data = type_validate_python(
            ModifyCurrentMemberParams,
            {"nick": nick, "banner": banner, "avatar": avatar, "bio": bio},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_current_user_nick(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        nick: MissingOrNullable[str] = UNSET,
        reason: str | None = None,
    ) -> GuildMember:
        """Deprecated in favor of Modify Current Member.

        see https://discord.com/developers/docs/resources/guild#modify-current-user-nick
        """

        data = omit_unset({"nick": nick})
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/members/@me/nick",
            response=JsonResponse(GuildMember),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(data),
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
    async def _api_create_guild_ban(  # noqa: PLR0913
        self: "AdapterProtocol",
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

        data = {
            "delete_message_days": delete_message_days,
            "delete_message_seconds": delete_message_seconds,
        }
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/bans/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(
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
        user_ids: list[SnowflakeType],
        delete_message_seconds: int | None = None,
        reason: str | None = None,
    ) -> BulkBan:
        """Bulk guild ban.

        see https://discord.com/developers/docs/resources/guild#bulk-guild-ban
        """

        data = {
            "user_ids": user_ids,
            "delete_message_seconds": delete_message_seconds,
        }
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/bulk-ban",
            response=JsonResponse(BulkBan),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(
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

    async def _api_create_guild_role(  # noqa: PLR0913
        self: "AdapterProtocol",
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

        data = type_validate_python(
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
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/roles",
            response=JsonResponse(Role),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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
        position: MissingOrNullable[int] = UNSET,
        reason: str | None = None,
    ) -> list[Role]:
        """Modify guild role positions.

        see https://discord.com/developers/docs/resources/guild#modify-guild-role-positions
        """

        if roles is None:
            if id is None:
                msg = "roles or id must be provided"
                raise ValueError(msg)
            role = type_validate_python(
                ModifyGuildRolePositionParams, {"id": id, "position": position}
            )
            roles = [role]
        payload = [
            type_validate_python(ModifyGuildRolePositionParams, role) for role in roles
        ]
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles",
            response=JsonResponse(list[Role]),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(payload),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_role(  # noqa: PLR0913
        self: "AdapterProtocol",
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

        data = type_validate_python(
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
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/roles/{role_id}",
            response=JsonResponse(Role),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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
        level: int,
        reason: str | None = None,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild"""

        data = {"level": level}
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/mfa",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(data),
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

    async def _api_begin_guild_prune(  # noqa: PLR0913
        self: "AdapterProtocol",
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
            body=JsonValueBody(
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
        enabled: Missing[bool] = UNSET,
        channel_id: MissingOrNullable[SnowflakeType] = UNSET,
        reason: str | None = None,
    ) -> GuildWidgetSettings:
        """Modify guild widget.

        see https://discord.com/developers/docs/resources/guild#modify-guild-widget
        """

        data = type_validate_python(
            ModifyGuildWidgetParams, {"enabled": enabled, "channel_id": channel_id}
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/widget",
            response=JsonResponse(GuildWidgetSettings),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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

    async def _api_modify_guild_welcome_screen(  # noqa: PLR0913
        self: "AdapterProtocol",
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

        data = {
            "enabled": enabled,
            "welcome_channels": welcome_channels,
            "description": description,
        }
        data = type_validate_python(ModifyGuildWelcomeScreenParams, data)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/welcome-screen",
            response=JsonResponse(WelcomeScreen),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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

    async def _api_modify_guild_onboarding(  # noqa: PLR0913
        self: "AdapterProtocol",
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

        data = {
            "prompts": prompts,
            "default_channel_ids": default_channel_ids,
            "enabled": enabled,
            "mode": mode,
        }
        data = type_validate_python(ModifyGuildOnboardingParams, data)
        call = RestCall(
            method="PUT",
            url=self.base_url / f"guilds/{guild_id}/onboarding",
            response=JsonResponse(GuildOnboarding),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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

    async def _api_create_guild_schedule_event(  # noqa: PLR0913
        self: "AdapterProtocol",
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
        data = type_validate_python(CreateGuildScheduledEventParams, data)
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events",
            response=JsonResponse(GuildScheduledEvent),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, exclude_none=True, omit_unset_values=True),
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

    async def _api_modify_guild_scheduled_event(  # noqa: PLR0913
        self: "AdapterProtocol",
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
        data = type_validate_python(ModifyGuildScheduledEventParams, data)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/scheduled-events/{event_id}",
            response=JsonResponse(GuildScheduledEvent),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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
            body=JsonValueBody(
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
        name: str,
        description: MissingOrNullable[str] = UNSET,
    ) -> GuildTemplate:
        """Create guild template.

        see https://discord.com/developers/docs/resources/guild-template#create-guild-template
        """

        data = type_validate_python(
            CreateGuildTemplateParams, {"name": name, "description": description}
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/templates",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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
        name: Missing[str] = UNSET,
        description: MissingOrNullable[str] = UNSET,
    ) -> GuildTemplate:
        """Modify guild template.

        see https://discord.com/developers/docs/resources/guild-template#modify-guild-template
        """

        data = type_validate_python(
            ModifyGuildTemplateParams, {"name": name, "description": description}
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/templates/{template_code}",
            response=JsonResponse(GuildTemplate),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
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
