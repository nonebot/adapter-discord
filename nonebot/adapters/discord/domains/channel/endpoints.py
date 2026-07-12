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
    StartThreadWithoutMessageParams,
)
from ..component.read import DirectComponent
from ..invite.read import Invite
from ..invite.types import InviteTargetType
from ..message.read import AllowedMention, Embed, File, MessageGet
from ..message.types import MessageFlag
from ..message.write import (
    AttachmentSend,
    MessageSend,
)
from ...api.validation import (
    Range,
    validate,
    validate_outbound_value,
)
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
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
        name = fields.get("name", UNSET)
        channel_type = fields.get("type", UNSET)
        position = fields.get("position", UNSET)
        topic = fields.get("topic", UNSET)
        nsfw = fields.get("nsfw", UNSET)
        rate_limit_per_user = fields.get("rate_limit_per_user", UNSET)
        bitrate = fields.get("bitrate", UNSET)
        user_limit = fields.get("user_limit", UNSET)
        permission_overwrites = fields.get("permission_overwrites", UNSET)
        parent_id = fields.get("parent_id", UNSET)
        rtc_region = fields.get("rtc_region", UNSET)
        video_quality_mode = fields.get("video_quality_mode", UNSET)
        default_auto_archive_duration = fields.get(
            "default_auto_archive_duration", UNSET
        )
        flags = fields.get("flags", UNSET)
        available_tags = fields.get("available_tags", UNSET)
        default_reaction_emoji = fields.get("default_reaction_emoji", UNSET)
        default_thread_rate_limit_per_user = fields.get(
            "default_thread_rate_limit_per_user", UNSET
        )
        default_sort_order = fields.get("default_sort_order", UNSET)
        default_forum_layout = fields.get("default_forum_layout", UNSET)

        data = {
            "name": name,
            "type": channel_type,
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
        data = validate_outbound_value(
            ModifyChannelParams,
            {key: value for key, value in data.items() if value is not UNSET},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields.get("name", UNSET)
        archived = fields.get("archived", UNSET)
        auto_archive_duration = fields.get("auto_archive_duration", UNSET)
        locked = fields.get("locked", UNSET)
        invitable = fields.get("invitable", UNSET)
        rate_limit_per_user = fields.get("rate_limit_per_user", UNSET)
        flags = fields.get("flags", UNSET)
        applied_tags = fields.get("applied_tags", UNSET)

        data = validate_outbound_value(
            ModifyThreadParams,
            {
                key: value
                for key, value in {
                    "name": name,
                    "archived": archived,
                    "auto_archive_duration": auto_archive_duration,
                    "locked": locked,
                    "invitable": invitable,
                    "rate_limit_per_user": rate_limit_per_user,
                    "flags": flags,
                    "applied_tags": applied_tags,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        allow = fields.get("allow")
        deny = fields.get("deny")
        overwrite_type = fields["type"]

        data = {
            "allow": allow,
            "deny": deny,
            "type": overwrite_type,
        }
        call = RestCall(
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/permissions/{overwrite_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
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
        webhook_channel_id = fields["webhook_channel_id"]

        data = {"webhook_channel_id": webhook_channel_id}
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/followers",
            response=JsonResponse(FollowedChannel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        access_token = fields["access_token"]
        nick = fields["nick"]

        data = {"access_token": access_token, "nick": nick}
        call = RestCall(
            method="PUT",
            url=self.base_url / f"channels/{channel_id}/recipients/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields["name"]
        auto_archive_duration = fields.get("auto_archive_duration", UNSET)
        rate_limit_per_user = fields.get("rate_limit_per_user", UNSET)

        data = validate_outbound_value(
            StartThreadFromMessageParams,
            {
                key: value
                for key, value in {
                    "name": name,
                    "auto_archive_duration": auto_archive_duration,
                    "rate_limit_per_user": rate_limit_per_user,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}/threads",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields["name"]
        auto_archive_duration = fields.get("auto_archive_duration", UNSET)
        channel_type = fields.get("type", UNSET)
        invitable = fields.get("invitable", UNSET)
        rate_limit_per_user = fields.get("rate_limit_per_user", UNSET)
        if channel_type is not UNSET and channel_type not in (
            ChannelType.ANNOUNCEMENT_THREAD,
            ChannelType.PUBLIC_THREAD,
            ChannelType.PRIVATE_THREAD,
        ):
            msg = "type must be ANNOUNCEMENT_THREAD, PUBLIC_THREAD or PRIVATE_THREAD"
            raise ValueError(msg)

        data = validate_outbound_value(
            StartThreadWithoutMessageParams,
            {
                key: value
                for key, value in {
                    "name": name,
                    "auto_archive_duration": auto_archive_duration,
                    "type": channel_type,
                    "invitable": invitable,
                    "rate_limit_per_user": rate_limit_per_user,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/threads",
            response=JsonResponse(Channel),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_start_thread_in_forum_channel(  # noqa: PLR0913
        self: "AdapterProtocol",
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
        message_payload = dict(
            validate_outbound_value(
                MessageSend,
                {
                    key: value
                    for key, value in data.items()
                    if key
                    not in {
                        "name",
                        "auto_archive_duration",
                        "rate_limit_per_user",
                        "applied_tags",
                    }
                    and value is not None
                    and value is not UNSET
                },
            )
        )
        request_files = message_payload.pop("files", None)
        payload: dict[str, object] = {"name": name, "message": message_payload}
        for key in ("auto_archive_duration", "rate_limit_per_user", "applied_tags"):
            value = data[key]
            if value is not UNSET and value is not None:
                payload[key] = value
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
