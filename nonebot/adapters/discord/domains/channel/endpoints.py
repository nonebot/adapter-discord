import base64
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Annotated
from typing_extensions import Unpack

from .read import (
    ArchivedThreadsResponse,
    Channel,
    FollowedChannel,
    ThreadMember,
)
from .types import (
    ChannelType,
)
from .write import (
    AddGroupDMRecipientParams,
    CreateChannelInviteParams,
    EditChannelPermissionsParams,
    FollowAnnouncementChannelParams,
    ModifyChannelParams,
    ModifyDMParams,
    ModifyThreadParams,
    StartThreadFromMessageParams,
    StartThreadInForumChannelParams,
    StartThreadWithoutMessageParams,
)
from ..invite.read import Invite
from ..invite.types import InviteTargetType
from ..message.read import File, MessageGet
from ...api.validation import (
    Range,
    validate,
    validate_outbound_value,
)
from ...protocol import SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    MultipartBody,
    PreparedBody,
    RestCall,
    _bool_query,
)
from ...transport.serialization import encode_json_text

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


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


class ChannelEndpointMixin:
    async def _api_get_channel(
        self: "AdapterProtocol", bot: "Bot", *, channel_id: SnowflakeType
    ) -> Channel:
        """Get a channel by ID.

        see https://discord.com/developers/docs/resources/channel#get-channel
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_DM(  # noqa: N802
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyDMParams],
    ) -> Channel:
        """Update a Group DM channel's settings.

        see https://discord.com/developers/docs/resources/channel#modify-channel
        """
        fields = validate_outbound_value(ModifyDMParams, fields)
        name = fields.get("name")
        icon = fields.get("icon")

        data = {
            "name": name,
            "icon": _encode_image_data_uri(image=icon) if icon is not None else None,
        }
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_channel(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyChannelParams],
    ) -> Channel:
        """Update a channel's settings.

        see https://discord.com/developers/docs/resources/channel#modify-channel
        """
        fields = validate_outbound_value(ModifyChannelParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_thread(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyThreadParams],
    ) -> Channel:
        """Update a thread's settings.

        see https://discord.com/developers/docs/resources/channel#modify-channel
        """
        fields = validate_outbound_value(ModifyThreadParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_channel(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
    ) -> Channel:
        """Delete or close a channel.

        see https://discord.com/developers/docs/resources/channel#delete/close-channel
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_edit_channel_permissions(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        overwrite_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[EditChannelPermissionsParams],
    ) -> None:
        """Edit channel permissions.

        see https://discord.com/developers/docs/resources/channel#edit-channel-permissions
        """
        fields = validate_outbound_value(EditChannelPermissionsParams, fields)
        call = RestCall(
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/permissions/{overwrite_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_get_channel_invites(
        self: "AdapterProtocol", bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[Invite]:
        """Get channel invites.

        see https://discord.com/developers/docs/resources/channel#get-channel-invites
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/invites",
            response=JsonResponse(list[Invite]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_channel_invite(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        target_users_file: File | None = None,
        reason: str | None = None,
        **fields: Unpack[CreateChannelInviteParams],
    ) -> Invite:
        """Create channel invite.

        see https://discord.com/developers/docs/resources/channel#create-channel-invite
        """
        fields = validate_outbound_value(CreateChannelInviteParams, fields)
        max_age = fields.get("max_age")
        max_uses = fields.get("max_uses")
        temporary = fields.get("temporary")
        unique = fields.get("unique")
        target_type = fields.get("target_type")
        target_user_id = fields.get("target_user_id")
        target_application_id = fields.get("target_application_id")
        role_ids = fields.get("role_ids")

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
                "payload_json": (None, encode_json_text(payload), "application/json"),
            }
            call = RestCall(
                method="POST",
                url=self.base_url / f"channels/{channel_id}/invites",
                response=JsonResponse(Invite),
                auth=BotAuth(bot.bot_info),
                body=MultipartBody(multipart),
                audit_reason=reason or None,
            )
        else:
            call = RestCall(
                method="POST",
                url=self.base_url / f"channels/{channel_id}/invites",
                response=JsonResponse(Invite),
                auth=BotAuth(bot.bot_info),
                body=JsonBody(payload),
                audit_reason=reason or None,
            )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_channel_permission(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        overwrite_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete channel permission.

        see https://discord.com/developers/docs/resources/channel#delete-channel-permission
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/permissions/{overwrite_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_follow_announcement_channel(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[FollowAnnouncementChannelParams],
    ) -> FollowedChannel:
        """Follow announcement channel.

        see https://discord.com/developers/docs/resources/channel#follow-announcement-channel
        """
        fields = validate_outbound_value(FollowAnnouncementChannelParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/followers",
            response=JsonResponse(FollowedChannel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_trigger_typing_indicator(
        self: "AdapterProtocol", bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """Trigger typing indicator.

        see https://discord.com/developers/docs/resources/channel#trigger-typing-indicator
        """

        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/typing",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_get_pinned_messages(
        self: "AdapterProtocol", bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[MessageGet]:
        """Get pinned messages.

        see https://discord.com/developers/docs/resources/message#get-channel-pins
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/messages/pins",
            response=JsonResponse(list[MessageGet]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_pin_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Pin message.

        see https://discord.com/developers/docs/resources/message#pin-message
        """

        call = RestCall(
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/messages/pins/{message_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_unpin_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Unpin message.

        see https://discord.com/developers/docs/resources/message#unpin-message
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/messages/pins/{message_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_group_DM_add_recipient(  # noqa: N802
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
        **fields: Unpack[AddGroupDMRecipientParams],
    ) -> None:
        """Group DM add recipient.

        see https://discord.com/developers/docs/resources/channel#group-dm-add-recipient
        """
        fields = validate_outbound_value(AddGroupDMRecipientParams, fields)
        call = RestCall(
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/recipients/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_group_DM_remove_recipient(  # noqa: N802
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """Group DM remove recipient.

        see https://discord.com/developers/docs/resources/channel#group-dm-remove-recipient
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/recipients/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_start_thread_from_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[StartThreadFromMessageParams],
    ) -> Channel:
        """Start thread from message.

        see https://discord.com/developers/docs/resources/channel#start-thread-from-message
        """
        fields = validate_outbound_value(StartThreadFromMessageParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}/threads",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_start_thread_without_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[StartThreadWithoutMessageParams],
    ) -> Channel:
        """Start thread without message.

        see https://discord.com/developers/docs/resources/channel#start-thread-without-message
        """
        fields = validate_outbound_value(StartThreadWithoutMessageParams, fields)
        channel_type = fields.get("type")
        if channel_type is not None and channel_type not in (
            ChannelType.ANNOUNCEMENT_THREAD,
            ChannelType.PUBLIC_THREAD,
            ChannelType.PRIVATE_THREAD,
        ):
            msg = "type must be ANNOUNCEMENT_THREAD, PUBLIC_THREAD or PRIVATE_THREAD"
            raise ValueError(msg)

        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/threads",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_start_thread_in_forum_channel(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[StartThreadInForumChannelParams],
    ) -> Channel:
        """Start thread in forum or media channel.

        see https://discord.com/developers/docs/resources/channel#start-thread-in-forum-or-media-channel
        """
        fields = validate_outbound_value(StartThreadInForumChannelParams, fields)
        name = fields.pop("name")
        request_files = fields.pop("files", None)
        payload: dict[str, object] = {"name": name}
        for key in ("auto_archive_duration", "rate_limit_per_user", "applied_tags"):
            value = fields.pop(key, None)
            if value is not None:
                payload[key] = value
        payload["message"] = {
            key: value for key, value in fields.items() if value is not None
        }
        params = PreparedBody(
            payload,
            files=request_files or None,
            attachment_owner_path=("message",),
        )

        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/threads",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=params,
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_join_thread(
        self: "AdapterProtocol", bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """Join thread.

        see https://discord.com/developers/docs/resources/channel#join-thread
        """

        call = RestCall(
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/thread-members/@me",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_add_thread_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """Add thread member.

        see https://discord.com/developers/docs/resources/channel#add-thread-member
        """

        call = RestCall(
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_leave_thread(
        self: "AdapterProtocol", bot: "Bot", *, channel_id: SnowflakeType
    ) -> None:
        """Leave thread.

        see https://discord.com/developers/docs/resources/channel#leave-thread
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/thread-members/@me",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_remove_thread_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> None:
        """Remove thread member.

        see https://discord.com/developers/docs/resources/channel#remove-thread-member
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_get_thread_member(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
        with_member: bool | None = None,
    ) -> ThreadMember:
        """Get thread member.

        see https://discord.com/developers/docs/resources/channel#get-thread-member
        """

        params = {"with_member": _bool_query(value=with_member)}
        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/thread-members/{user_id}",
            response=JsonResponse(ThreadMember),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_list_thread_members(
        self: "AdapterProtocol",
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

        params = {
            "with_member": _bool_query(value=with_member),
            "after": after,
            "limit": limit,
        }
        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/thread-members",
            response=JsonResponse(list[ThreadMember]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_public_archived_threads(
        self: "AdapterProtocol",
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

        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/threads/archived/public",
            response=JsonResponse(ArchivedThreadsResponse),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_private_archived_threads(
        self: "AdapterProtocol",
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

        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/threads/archived/private",
            response=JsonResponse(ArchivedThreadsResponse),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_joined_private_archived_threads(
        self: "AdapterProtocol",
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

        call = RestCall(
            method="GET",
            url=self.base_url
            / f"channels/{channel_id}/users/@me/threads/archived/private",
            response=JsonResponse(ArchivedThreadsResponse),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["ChannelEndpointMixin"]
