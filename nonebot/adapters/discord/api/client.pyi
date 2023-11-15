import datetime
from typing import Literal, overload

from .model import *
from .types import *

class ApiClient:
    async def get_global_application_commands(
        self, *, application_id: SnowflakeType, with_localizations: bool | None = ...
    ) -> list[ApplicationCommand]: ...
    async def create_global_application_command(
        self,
        *,
        application_id: SnowflakeType,
        name: str,
        name_localizations: dict[str, str] | None = ...,
        description: str | None = ...,
        description_localizations: dict[str, str] | None = ...,
        options: list[ApplicationCommandOption] | None = ...,
        default_member_permissions: str | None = ...,
        dm_permission: bool | None = ...,
        default_permission: bool | None = ...,
        type: ApplicationCommandType | None = ...,
        nsfw: bool | None = ...,
    ) -> ApplicationCommand: ...
    async def get_global_application_command(
        self, *, application_id: SnowflakeType, command_id: SnowflakeType
    ) -> ApplicationCommand: ...
    async def edit_global_application_command(
        self,
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
        name: str | None = ...,
        name_localizations: dict[str, str] | None = ...,
        description: str | None = ...,
        description_localizations: dict[str, str] | None = ...,
        options: list[ApplicationCommandOption] | None = ...,
        default_member_permissions: str | None = ...,
        dm_permission: bool | None = ...,
        default_permission: bool | None = ...,
        nsfw: bool | None = ...,
    ) -> ApplicationCommand: ...
    async def _delete_global_application_command(
        self,
        *,
        application_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> None: ...
    async def bulk_overwrite_global_application_commands(
        self, *, application_id: SnowflakeType, commands: list[ApplicationCommandCreate]
    ) -> list[ApplicationCommand]: ...
    async def get_guild_application_commands(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        with_localizations: bool | None = ...,
    ) -> list[ApplicationCommand]: ...
    async def create_guild_application_command(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        name: str,
        name_localizations: dict[str, str] | None = ...,
        description: str | None = ...,
        description_localizations: dict[str, str] | None = ...,
        options: list[ApplicationCommandOption] | None = ...,
        default_member_permissions: str | None = ...,
        default_permission: bool | None = ...,
        type: ApplicationCommandType | None = ...,
        nsfw: bool | None = ...,
    ) -> ApplicationCommand: ...
    async def get_guild_application_command(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> ApplicationCommand: ...
    async def edit_guild_application_command(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        name: str | None = ...,
        name_localizations: dict[str, str] | None = ...,
        description: str | None = ...,
        description_localizations: dict[str, str] | None = ...,
        options: list[ApplicationCommandOption] | None = ...,
        default_member_permissions: str | None = ...,
        default_permission: bool | None = ...,
        nsfw: bool | None = ...,
    ) -> ApplicationCommand: ...
    async def delete_guild_application_command(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> None: ...
    async def bulk_overwrite_guild_application_commands(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        commands: list[ApplicationCommandCreate],
    ) -> list[ApplicationCommand]: ...
    async def get_guild_application_command_permissions(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
    ) -> GuildApplicationCommandPermissions: ...
    async def get_application_command_permissions(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
    ) -> GuildApplicationCommandPermissions: ...
    async def edit_application_command_permissions(
        self,
        *,
        application_id: SnowflakeType,
        guild_id: SnowflakeType,
        command_id: SnowflakeType,
        permissions: list[ApplicationCommandPermissions],
    ) -> GuildApplicationCommandPermissions: ...
    async def create_interaction_response(
        self,
        *,
        interaction_id: SnowflakeType,
        interaction_token: str,
        response: InteractionResponse,
    ) -> None: ...
    async def get_origin_interaction_response(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = ...,
    ) -> MessageGet: ...
    async def edit_origin_interaction_response(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = ...,
        content: str | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[Component] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
    ) -> MessageGet: ...
    async def delete_origin_interaction_response(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
    ) -> None: ...
    async def create_followup_message(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        content: str | None = ...,
        tts: bool | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[Component] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
        flags: int | None = ...,
        thread_name: str | None = ...,
    ) -> MessageGet: ...
    async def get_followup_message(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
    ) -> MessageGet: ...
    async def edit_followup_message(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = ...,
        content: str | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[Component] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
    ) -> MessageGet: ...
    async def delete_followup_message(
        self,
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
    ) -> None: ...
    async def get_current_application(
        self, *, application_id: SnowflakeType
    ) -> Application: ...
    async def get_application_role_connection_metadata_records(
        self, *, application_id: SnowflakeType
    ) -> list[ApplicationRoleConnectionMetadata]:
        """get application role connection metadata records

        see https://discord.com/developers/docs/resources/application-role-connection-metadata#get-application-role-connection-metadata-records
        """
        ...

    async def update_application_role_connection_metadata_records(
        self, *, application_id: SnowflakeType
    ) -> list[ApplicationRoleConnectionMetadata]:
        """get application role connection metadata records

        see https://discord.com/developers/docs/resources/application-role-connection-metadata#get-application-role-connection-metadata-records
        """
        ...

    async def get_guild_audit_log(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = ...,
        action_type: AuditLogEventType | None = ...,
        before: SnowflakeType | None = ...,
        after: SnowflakeType | None = ...,
        limit: int | None = ...,
    ) -> AuditLog:
        """get guild audit log

        see https://discord.com/developers/docs/resources/audit-log#get-guild-audit-log
        """
        ...

    async def list_auto_moderation_rules_for_guild(
        self, *, guild_id: SnowflakeType
    ) -> list[AutoModerationRule]:
        """list auto moderation rules for guild

        see https://discord.com/developers/docs/resources/auto-moderation#list-auto-moderation-rules-for-guild
        """
        ...

    async def get_auto_moderation_rule(
        self, *, guild_id: SnowflakeType, rule_id: SnowflakeType
    ) -> AutoModerationRule:
        """get auto moderation rule

        see https://discord.com/developers/docs/resources/auto-moderation#get-auto-moderation-rule
        """
        ...

    async def create_auto_moderation_rule(
        self, *, guild_id: SnowflakeType, **data
    ) -> AutoModerationRule:
        """create auto moderation rule

        see https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
        """
        ...

    async def modify_auto_moderation_rule(
        self,
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: TriggerType,
        trigger_metadata: TriggerMetadata | None = ...,
        actions: list[AutoModerationAction] = ...,
        enabled: bool | None = ...,
        exempt_roles: list[SnowflakeType] = ...,
        exempt_channels: list[SnowflakeType] = ...,
        reason: str | None = ...,
    ) -> AutoModerationRule:
        """modify auto moderation rule

        see https://discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule
        """
        ...

    async def delete_auto_moderation_rule(
        self,
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """delete auto moderation rule

        see https://discord.com/developers/docs/resources/auto-moderation#delete-auto-moderation-rule
        """
        ...

    async def get_channel(self, *, channel_id: SnowflakeType) -> Channel:
        """get channel

        see https://discord.com/developers/docs/resources/channel#get-channel"""
        ...

    async def modify_DM(
        self,
        *,
        channel_id: SnowflakeType,
        name: str = ...,
        icon: bytes = ...,
        reason: str | None = ...,
    ) -> Channel:
        """modify DM

        see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-group-dm
        """
        ...

    async def modify_channel(
        self,
        *,
        channel_id: SnowflakeType,
        name: str | None = ...,
        type: ChannelType | None = ...,
        position: int | None = ...,
        topic: str | None = ...,
        nsfw: bool | None = ...,
        rate_limit_per_user: int | None = ...,
        bitrate: int | None = ...,
        user_limit: int | None = ...,
        permission_overwrites: list[Overwrite] | None = ...,
        parent_id: SnowflakeType | None = ...,
        rtc_region: str | None = ...,
        video_quality_mode: VideoQualityMode | None = ...,
        default_auto_archive_duration: int | None = ...,
        flags: ChannelFlags | None = ...,
        available_tags: list[ForumTag] | None = ...,
        default_reaction_emoji: DefaultReaction | None = ...,
        default_thread_rate_limit_per_user: int | None = ...,
        default_sort_order: SortOrderTypes | None = ...,
        default_forum_layout: ForumLayoutTypes | None = ...,
        reason: str | None = ...,
    ) -> Channel:
        """modify channel

        see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
        """
        ...

    async def modify_thread(
        self,
        *,
        channel_id: SnowflakeType,
        name: str = ...,
        archived: bool = ...,
        auto_archive_duration: int = ...,
        locked: bool = ...,
        invitable: bool = ...,
        rate_limit_per_user: int | None = ...,
        flags: ChannelFlags | None = ...,
        applied_tags: list[SnowflakeType] | None = ...,
        reason: str | None = ...,
    ) -> Channel:
        """modify thread

        see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-thread
        """
        ...

    async def delete_channel(
        self, *, channel_id: SnowflakeType, reason: str | None = ...
    ) -> Channel:
        """delete channel

        see https://discord.com/developers/docs/resources/channel#deleteclose-channel"""
        ...

    async def get_channel_messages(
        self,
        *,
        channel_id: SnowflakeType,
        around: SnowflakeType | None = ...,
        before: SnowflakeType | None = ...,
        after: SnowflakeType | None = ...,
        limit: int | None = ...,
    ) -> list[MessageGet]:
        """get channel messages

        see https://discord.com/developers/docs/resources/channel#get-channel-messages
        """
        ...

    async def get_channel_message(
        self, *, channel_id: SnowflakeType, message_id: SnowflakeType
    ) -> MessageGet:
        """get channel message

        see https://discord.com/developers/docs/resources/channel#get-channel-message"""
        ...

    async def create_message(
        self,
        *,
        channel_id: SnowflakeType,
        content: str | None = ...,
        nonce: int | str | None = ...,
        tts: bool | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        message_reference: MessageReference | None = ...,
        components: list[DirectComponent] | None = ...,
        sticker_ids: list[SnowflakeType] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
        flags: MessageFlag | None = ...,
    ) -> MessageGet:
        """create message

        see https://discord.com/developers/docs/resources/channel#create-message
        """
        ...

    async def crosspost_message(
        self, *, channel_id: SnowflakeType, message_id: SnowflakeType
    ) -> MessageGet:
        """crosspost message

        see https://discord.com/developers/docs/resources/channel#crosspost-message"""
        ...

    async def create_reaction(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """create reaction

        see https://discord.com/developers/docs/resources/channel#create-reaction"""
        ...

    async def delete_own_reaction(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """delete own reaction

        see https://discord.com/developers/docs/resources/channel#delete-own-reaction"""
        ...

    async def delete_user_reaction(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        user_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """delete user reaction

        see https://discord.com/developers/docs/resources/channel#delete-user-reaction
        """
        ...

    async def get_reactions(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
        after: SnowflakeType | None = ...,
        limit: int | None = ...,
    ) -> list[User]:
        """get reactions

        see https://discord.com/developers/docs/resources/channel#get-reactions"""
        ...

    async def delete_all_reactions(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> None:
        """

        see https://discord.com/developers/docs/resources/channel#delete-all-reactions
        """
        ...

    async def delete_all_reactions_for_emoji(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """

        see https://discord.com/developers/docs/resources/channel#delete-all-reactions
        """
        ...

    async def edit_message(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        content: str | None = ...,
        embeds: list[Embed] | None = ...,
        flags: MessageFlag | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[DirectComponent] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
    ) -> MessageGet:
        """see https://discord.com/developers/docs/resources/channel#edit-message"""
        ...

    async def delete_message(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#delete-message"""
        ...

    async def bulk_delete_message(
        self,
        *,
        channel_id: SnowflakeType,
        messages: list[SnowflakeType],
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#bulk-delete-messages"""
        ...

    async def edit_channel_permissions(
        self,
        *,
        channel_id: SnowflakeType,
        overwrite_id: SnowflakeType,
        allow: str | None = ...,
        deny: str | None = ...,
        type: OverwriteType | None = ...,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#edit-channel-permissions"""
        ...

    async def get_channel_invites(self, *, channel_id: SnowflakeType) -> list[Invite]:
        """https://discord.com/developers/docs/resources/channel#get-channel-invites"""
        ...

    async def create_channel_invite(
        self,
        *,
        channel_id: SnowflakeType,
        max_age: int | None = ...,
        max_uses: int | None = ...,
        temporary: bool | None = ...,
        unique: bool | None = ...,
        target_type: int | None = ...,
        target_user_id: SnowflakeType | None = ...,
        target_application_id: SnowflakeType | None = ...,
        reason: str | None = ...,
    ) -> Invite:
        """https://discord.com/developers/docs/resources/channel#create-channel-invite"""
        ...

    async def delete_channel_permission(
        self,
        *,
        channel_id: SnowflakeType,
        overwrite_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#delete-channel-permission"""
        ...

    async def follow_announcement_channel(
        self, *, channel_id: SnowflakeType, webhook_channel_id: SnowflakeType = ...
    ) -> FollowedChannel:
        """https://discord.com/developers/docs/resources/channel#follow-news-channel"""
        ...

    async def trigger_typing_indicator(self, *, channel_id: SnowflakeType) -> None:
        """https://discord.com/developers/docs/resources/channel#trigger-typing-indicator"""
        ...

    async def get_pinned_messages(
        self, *, channel_id: SnowflakeType
    ) -> list[MessageGet]:
        """https://discord.com/developers/docs/resources/channel#get-pinned-messages"""
        ...

    async def pin_message(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#add-pinned-channel-message"""
        ...

    async def unpin_message(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#delete-pinned-channel-message"""
        ...

    async def group_DM_add_recipient(
        self,
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
        access_token: str = ...,
        nick: str = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#group-dm-add-recipient"""
        ...

    async def group_DM_remove_recipient(
        self, *, channel_id: SnowflakeType, user_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#group-dm-remove-recipient"""
        ...

    async def start_thread_from_message(
        self,
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        name: str = ...,
        auto_archive_duration: int | None = ...,
        rate_limit_per_user: int | None = ...,
        reason: str | None = ...,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#start-thread-with-message"""
        ...

    async def start_thread_without_message(
        self,
        *,
        channel_id: SnowflakeType,
        name: str = ...,
        auto_archive_duration: int | None = ...,
        type: ChannelType | None = ...,
        invitable: bool | None = ...,
        rate_limit_per_user: int | None = ...,
        reason: str | None = ...,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#start-thread-without-message"""
        ...

        # TODO: Returns a channel, with a nested message object, on success

    async def start_thread_in_forum_channel(
        self,
        *,
        channel_id: SnowflakeType,
        name: str = ...,
        auto_archive_duration: int | None = ...,
        rate_limit_per_user: int | None = ...,
        applied_tags: list[SnowflakeType] | None = ...,
        content: str | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[DirectComponent] | None = ...,
        sticker_ids: list[SnowflakeType] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
        flags: MessageFlag | None = ...,
        reason: str | None = ...,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/channel#start-thread-in-forum-channel"""
        ...

    async def join_thread(self, *, channel_id: SnowflakeType) -> None:
        """https://discord.com/developers/docs/resources/channel#join-thread"""
        ...

    async def add_thread_member(
        self, *, channel_id: SnowflakeType, user_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#add-thread-member"""
        ...

    async def leave_thread(self, *, channel_id: SnowflakeType) -> None:
        """https://discord.com/developers/docs/resources/channel#leave-thread"""
        ...

    async def remove_thread_member(
        self, *, channel_id: SnowflakeType, user_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/channel#remove-thread-member"""
        ...

    async def get_thread_member(
        self,
        *,
        channel_id: SnowflakeType,
        user_id: SnowflakeType,
        with_member: bool | None = ...,
    ) -> ThreadMember:
        """https://discord.com/developers/docs/resources/channel#get-thread-member"""
        ...

    async def list_thread_members(
        self,
        *,
        channel_id: SnowflakeType,
        with_member: bool | None = ...,
        after: SnowflakeType | None = ...,
        limit: int | None = ...,
    ) -> list[ThreadMember]:
        """https://discord.com/developers/docs/resources/channel#list-thread-members"""
        ...

    async def list_public_archived_threads(
        self,
        *,
        channel_id: SnowflakeType,
        before: datetime.datetime | None = ...,
        limit: int | None = ...,
    ) -> ArchivedThreadsResponse:
        """https://discord.com/developers/docs/resources/channel#list-public-archived-threads"""
        ...

    async def list_private_archived_threads(
        self,
        *,
        channel_id: SnowflakeType,
        before: datetime.datetime | None = ...,
        limit: int | None = ...,
    ) -> ArchivedThreadsResponse:
        """https://discord.com/developers/docs/resources/channel#list-private-archived-threads"""
        ...

    async def list_joined_private_archived_threads(
        self,
        *,
        channel_id: SnowflakeType,
        before: datetime.datetime | None = ...,
        limit: int | None = ...,
    ) -> ArchivedThreadsResponse:
        """https://discord.com/developers/docs/resources/channel#list-joined-private-archived-threads"""
        ...

    async def list_guild_emojis(self, *, guild_id: SnowflakeType) -> list[Emoji]:
        """https://discord.com/developers/docs/resources/emoji#list-guild-emojis"""
        ...

    async def get_guild_emoji(
        self, *, guild_id: SnowflakeType, emoji_id: SnowflakeType
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#get-guild-emoji"""
        ...

    async def create_guild_emoji(
        self,
        *,
        guild_id: SnowflakeType,
        name: str = ...,
        image: str = ...,
        roles: list[SnowflakeType] = ...,
        reason: str | None = ...,
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#create-guild-emoji"""
        ...

    async def modify_guild_emoji(
        self,
        *,
        guild_id: SnowflakeType,
        emoji_id: str,
        name: str = ...,
        roles: list[SnowflakeType] | None = ...,
        reason: str | None = ...,
    ) -> Emoji:
        """https://discord.com/developers/docs/resources/emoji#modify-guild-emoji"""
        ...

    async def delete_guild_emoji(
        self, *, guild_id: SnowflakeType, emoji_id: str, reason: str | None = ...
    ) -> None:
        """https://discord.com/developers/docs/resources/emoji#delete-guild-emoji"""
        ...

    async def create_guild(
        self,
        *,
        name: str = ...,
        region: str | None = ...,
        icon: str | None = ...,
        verification_level: VerificationLevel | None = ...,
        default_message_notifications: DefaultMessageNotificationLevel | None = ...,
        explicit_content_filter: ExplicitContentFilterLevel | None = ...,
        roles: list[Role] | None = ...,
        channels: list[Channel] | None = ...,
        afk_channel_id: Snowflake | None = ...,
        afk_timeout: int | None = ...,
        system_channel_id: Snowflake | None = ...,
        system_channel_flags: SystemChannelFlags | None = ...,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild#create-guild"""
        ...

    async def get_guild(
        self, *, guild_id: SnowflakeType, with_counts: bool | None = ...
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild#get-guild"""
        ...

    async def get_guild_preview(self, *, guild_id: SnowflakeType) -> GuildPreview:
        """https://discord.com/developers/docs/resources/guild#get-guild-preview"""
        ...

    async def modify_guild(
        self,
        *,
        guild_id: SnowflakeType,
        name: str = ...,
        region: str | None = ...,
        verification_level: VerificationLevel | None = ...,
        default_message_notifications: DefaultMessageNotificationLevel | None = ...,
        explicit_content_filter: ExplicitContentFilterLevel | None = ...,
        afk_channel_id: Snowflake | None = ...,
        afk_timeout: int | None = ...,
        icon: str | None = ...,
        owner_id: Snowflake | None = ...,
        splash: str | None = ...,
        discovery_splash: str | None = ...,
        banner: str | None = ...,
        system_channel_id: Snowflake | None = ...,
        system_channel_flags: SystemChannelFlags | None = ...,
        rules_channel_id: Snowflake | None = ...,
        public_updates_channel_id: Snowflake | None = ...,
        preferred_locale: str | None = ...,
        features: list[GuildFeature] | None = ...,
        description: str | None = ...,
        premium_progress_bar_enabled: bool | None = ...,
        reason: str | None = ...,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild#modify-guild"""
        ...

    async def delete_guild(self, *, guild_id: SnowflakeType) -> None:
        """https://discord.com/developers/docs/resources/guild#delete-guild"""
        ...

    async def get_guild_channels(self, *, guild_id: SnowflakeType) -> list[Channel]:
        """https://discord.com/developers/docs/resources/guild#get-guild-channels"""
        ...

    async def create_guild_channel(
        self,
        *,
        guild_id: SnowflakeType,
        name: str = ...,
        type: ChannelType | None = ...,
        topic: str | None = ...,
        bitrate: int | None = ...,
        user_limit: int | None = ...,
        rate_limit_per_user: int | None = ...,
        position: int | None = ...,
        permission_overwrites: list[Overwrite] | None = ...,
        parent_id: Snowflake | None = ...,
        nsfw: bool | None = ...,
        rtc_region: str | None = ...,
        video_quality_mode: VideoQualityMode | None = ...,
        default_auto_archive_duration: int | None = ...,
        default_reaction_emoji: DefaultReaction | None = ...,
        available_tags: list[ForumTag] | None = ...,
        default_sort_order: SortOrderTypes | None = ...,
        reason: str | None = ...,
    ) -> Channel:
        """https://discord.com/developers/docs/resources/guild#create-guild-channel"""
        ...

    async def modify_guild_channel_positions(
        self,
        *,
        guild_id: SnowflakeType,
        id: SnowflakeType = ...,
        position: int | None = ...,
        lock_permissions: bool | None = ...,
        parent_id: SnowflakeType | None = ...,
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions"""
        ...

    async def list_active_guild_threads(
        self, *, guild_id: SnowflakeType
    ) -> ListActiveGuildThreadsResponse:
        """https://discord.com/developers/docs/resources/guild#list-active-guild-threads"""
        ...

    async def get_guild_member(
        self, *, guild_id: SnowflakeType, user_id: SnowflakeType
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#get-guild-member"""
        ...

    async def list_guild_members(
        self,
        *,
        guild_id: SnowflakeType,
        limit: int | None = ...,
        after: SnowflakeType | None = ...,
    ) -> list[GuildMember]:
        """https://discord.com/developers/docs/resources/guild#list-guild-members"""
        ...

    async def search_guild_members(
        self,
        *,
        guild_id: SnowflakeType,
        query: str | None = ...,
        limit: int | None = ...,
    ) -> list[GuildMember]:
        """https://discord.com/developers/docs/resources/guild#search-guild-members"""
        ...

    async def add_guild_member(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        access_token: str = ...,
        nick: str | None = ...,
        roles: list[SnowflakeType] | None = ...,
        mute: bool | None = ...,
        deaf: bool | None = ...,
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#add-guild-member"""
        ...

    async def modify_guild_member(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        nick: str | None = ...,
        roles: list[SnowflakeType] | None = ...,
        mute: bool | None = ...,
        deaf: bool | None = ...,
        channel_id: SnowflakeType | None = ...,
        communication_disabled_until: datetime.datetime | None = ...,
        flags: GuildMemberFlags | None = ...,
        reason: str | None = ...,
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#modify-guild-member"""
        ...

    async def modify_current_member(
        self,
        *,
        guild_id: SnowflakeType,
        nick: str | None = ...,
        reason: str | None = ...,
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#modify-current-member"""
        ...

    async def modify_current_user_nick(
        self,
        *,
        guild_id: SnowflakeType,
        nick: str | None = ...,
        reason: str | None = ...,
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/guild#modify-current-user-nick"""
        ...

    async def add_guild_member_role(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: str | None = ...,
    ):
        """https://discord.com/developers/docs/resources/guild#add-guild-member-role"""
        ...

    async def remove_guild_member_role(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: str | None = ...,
    ):
        """https://discord.com/developers/docs/resources/guild#remove-guild-member-role"""
        ...

    async def remove_guild_member(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: str | None = ...,
    ):
        """https://discord.com/developers/docs/resources/guild#remove-guild-member"""
        ...

    async def get_guild_bans(
        self,
        *,
        guild_id: SnowflakeType,
        limit: int | None = ...,
        before: SnowflakeType | None = ...,
        after: SnowflakeType | None = ...,
    ) -> list[Ban]:
        """https://discord.com/developers/docs/resources/guild#get-guild-bans"""
        ...

    async def get_guild_ban(
        self, *, guild_id: SnowflakeType, user_id: SnowflakeType
    ) -> Ban:
        """https://discord.com/developers/docs/resources/guild#get-guild-ban"""
        ...

    async def create_guild_ban(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        delete_message_days: int | None = ...,
        delete_message_seconds: int | None = ...,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#create-guild-ban"""
        ...

    async def remove_guild_ban(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#remove-guild-ban"""
        ...

    async def get_guild_roles(self, *, guild_id: SnowflakeType) -> list[Role]:
        """https://discord.com/developers/docs/resources/guild#get-guild-roles"""
        ...

    async def create_guild_role(
        self,
        *,
        guild_id: SnowflakeType,
        name: str | None = ...,
        permissions: str | None = ...,
        color: int | None = ...,
        hoist: bool | None = ...,
        icon: str | None = ...,
        unicode_emoji: str | None = ...,
        mentionable: bool | None = ...,
        reason: str | None = ...,
    ) -> Role:
        """https://discord.com/developers/docs/resources/guild#create-guild-role"""
        ...

    async def modify_guild_role_positions(
        self,
        *,
        guild_id: SnowflakeType,
        id: SnowflakeType,
        position: int | None = ...,
        reason: str | None = ...,
    ) -> list[Role]:
        """https://discord.com/developers/docs/resources/guild#modify-guild-role-positions"""
        ...

    async def modify_guild_role(
        self,
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
        name: str | None = ...,
        permissions: str | None = ...,
        color: int | None = ...,
        hoist: bool | None = ...,
        icon: str | None = ...,
        unicode_emoji: str | None = ...,
        mentionable: bool | None = ...,
        reason: str | None = ...,
    ) -> Role:
        """https://discord.com/developers/docs/resources/guild#modify-guild-role"""
        ...

    async def modify_guild_MFA_level(
        self, *, guild_id: SnowflakeType, level: int, reason: str | None = ...
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#modify-guild-mfa-level"""
        ...

    async def delete_guild_role(
        self,
        *,
        guild_id: SnowflakeType,
        role_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#delete-guild-role"""
        ...

    async def get_guild_prune_count(
        self, *, guild_id: SnowflakeType, days: int, include_roles: list[SnowflakeType]
    ) -> dict[Literal["pruned"], int]:
        """https://discord.com/developers/docs/resources/guild#get-guild-prune-count"""
        ...

    async def begin_guild_prune(
        self,
        *,
        guild_id: SnowflakeType,
        days: int | None = ...,
        compute_prune_count: bool | None = ...,
        include_roles: list[SnowflakeType] | None = ...,
        reason: str | None = ...,
    ) -> dict[Literal["pruned"], int]:
        """https://discord.com/developers/docs/resources/guild#begin-guild-prune"""
        ...

    async def get_guild_voice_regions(
        self, *, guild_id: SnowflakeType
    ) -> list[VoiceRegion]:
        """https://discord.com/developers/docs/resources/guild#get-guild-voice-regions"""
        ...

    async def get_guild_invites(self, *, guild_id: SnowflakeType) -> list[Invite]:
        """https://discord.com/developers/docs/resources/guild#get-guild-invites"""
        ...

    async def get_guild_integrations(
        self, *, guild_id: SnowflakeType
    ) -> list[Integration]:
        """https://discord.com/developers/docs/resources/guild#get-guild-integrations"""
        ...

    async def delete_guild_integration(
        self,
        *,
        guild_id: SnowflakeType,
        integration_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#delete-guild-integration"""
        ...

    async def get_guild_widget_settings(
        self, *, guild_id: SnowflakeType
    ) -> GuildWidgetSettings:
        """https://discord.com/developers/docs/resources/guild#get-guild-widget-settings"""
        ...

    async def modify_guild_widget(
        self,
        *,
        guild_id: SnowflakeType,
        enabled: bool | None = ...,
        channel_id: SnowflakeType | None = ...,
        reason: str | None = ...,
    ) -> GuildWidget:
        """https://discord.com/developers/docs/resources/guild#modify-guild-widget"""
        ...

    async def get_guild_widget(self, *, guild_id: SnowflakeType) -> GuildWidget:
        """https://discord.com/developers/docs/resources/guild#get-guild-widget"""
        ...

    async def get_guild_vanity_url(self, *, guild_id: SnowflakeType) -> Invite:
        """https://discord.com/developers/docs/resources/guild#get-guild-vanity-url"""
        ...

    async def get_guild_widget_image(
        self,
        *,
        guild_id: SnowflakeType,
        style: (
            Literal["shield", "banner1", "banner2", "banner3", "banner4"] | None
        ) = ...,
    ) -> str:
        """https://discord.com/developers/docs/resources/guild#get-guild-widget-image"""
        ...

    async def get_guild_welcome_screen(
        self, *, guild_id: SnowflakeType
    ) -> WelcomeScreen:
        """https://discord.com/developers/docs/resources/guild#get-guild-welcome-screen"""
        ...

    async def modify_guild_welcome_screen(
        self,
        *,
        guild_id: SnowflakeType,
        enabled: bool | None = ...,
        welcome_channels: list[WelcomeScreenChannel] | None = ...,
        description: str | None = ...,
        reason: str | None = ...,
    ) -> WelcomeScreen:
        """https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen"""
        ...

    async def get_guild_onboarding(self, *, guild_id: SnowflakeType) -> GuildOnboarding:
        """https://discord.com/developers/docs/resources/guild#get-guild-onboarding"""
        ...

    async def modify_current_user_voice_state(
        self,
        *,
        guild_id: SnowflakeType,
        channel_id: SnowflakeType | None = ...,
        suppress: bool | None = ...,
        request_to_speak_timestamp: datetime.datetime | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#modify-current-user-voice-state"""
        ...

    async def modify_user_voice_state(
        self,
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        channel_id: SnowflakeType,
        suppress: bool | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/guild#modify-user-voice-state"""
        ...

    async def list_scheduled_events_for_guild(
        self, *, guild_id: SnowflakeType, with_user_count: bool | None = ...
    ) -> list[GuildScheduledEvent]:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#list-scheduled-events-for-guild"""
        ...

    async def create_guild_schedule_event(
        self,
        *,
        guild_id: SnowflakeType,
        channel_id: Snowflake | None = ...,
        entity_metadata: GuildScheduledEventEntityMetadata | None = ...,
        name: str,
        privacy_level: GuildScheduledEventPrivacyLevel,
        scheduled_start_time: datetime.datetime,
        scheduled_end_time: datetime.datetime | None = ...,
        description: str | None = ...,
        entity_type: GuildScheduledEventEntityType,
        image: str | None = ...,
        reason: str | None = ...,
    ) -> GuildScheduledEvent:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event"""
        ...

    async def get_guild_scheduled_event(
        self,
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        with_user_count: bool | None = ...,
    ) -> GuildScheduledEvent:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event"""
        ...

    async def modify_guild_scheduled_event(
        self,
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        channel_id: Snowflake | None = ...,
        entity_metadata: GuildScheduledEventEntityMetadata | None = ...,
        name: str | None = ...,
        privacy_level: GuildScheduledEventPrivacyLevel | None = ...,
        scheduled_start_time: datetime.datetime | None = ...,
        scheduled_end_time: datetime.datetime | None = ...,
        description: str | None = ...,
        entity_type: GuildScheduledEventEntityType | None = ...,
        status: GuildScheduledEventStatus | None = ...,
        image: str | None = ...,
        reason: str | None = ...,
    ) -> GuildScheduledEvent:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event"""
        ...

    async def delete_guild_scheduled_event(
        self, *, guild_id: SnowflakeType, event_id: SnowflakeType
    ) -> None:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#delete-guild-scheduled-event"""
        ...

    async def get_guild_scheduled_event_users(
        self,
        *,
        guild_id: SnowflakeType,
        event_id: SnowflakeType,
        limit: int | None = ...,
        with_member: bool | None = ...,
        before: SnowflakeType | None = ...,
        after: SnowflakeType | None = ...,
    ) -> list[GuildScheduledEventUser]:
        """https://discord.com/developers/docs/resources/guild-scheduled-event#get-guild-scheduled-event-users"""
        ...

    async def get_guild_template(self, *, template_code: str) -> GuildTemplate:
        """https://discord.com/developers/docs/resources/guild-template#get-guild-template"""
        ...

    async def create_guild_from_guild_template(
        self, *, template_code: str, name: str, icon: str | None = ...
    ) -> Guild:
        """https://discord.com/developers/docs/resources/guild-template#create-guild-from-template"""
        ...

    async def get_guild_templates(
        self, *, guild_id: SnowflakeType
    ) -> list[GuildTemplate]:
        """https://discord.com/developers/docs/resources/guild-template#get-guild-templates"""
        ...

    async def create_guild_template(
        self, *, guild_id: SnowflakeType, name: str, description: str | None = ...
    ) -> GuildTemplate:
        """https://discord.com/developers/docs/resources/guild-template#create-guild-template"""
        ...

    async def sync_guild_template(
        self, *, guild_id: SnowflakeType, template_code: str
    ) -> GuildTemplate:
        """https://discord.com/developers/docs/resources/guild-template#sync-guild-template"""
        ...

    async def modify_guild_template(
        self,
        *,
        guild_id: SnowflakeType,
        template_code: str,
        name: str | None = ...,
        description: str | None = ...,
    ) -> GuildTemplate:
        """https://discord.com/developers/docs/resources/guild-template#modify-guild-template"""
        ...

    async def delete_guild_template(
        self, *, guild_id: SnowflakeType, template_code: str
    ) -> None:
        """https://discord.com/developers/docs/resources/guild-template#delete-guild-template"""
        ...

    async def get_invite(
        self,
        *,
        invite_code: str,
        with_counts: bool | None = ...,
        with_expiration: bool | None = ...,
        guild_scheduled_event_id: SnowflakeType | None = ...,
    ) -> Invite:
        """https://discord.com/developers/docs/resources/invite#get-invite"""
        ...

    async def delete_invite(
        self, *, invite_code: str, reason: str | None = ...
    ) -> Invite:
        """https://discord.com/developers/docs/resources/invite#delete-invite"""
        ...

    async def create_stage_instance(
        self,
        *,
        channel_id: SnowflakeType,
        topic: str,
        privacy_level: StagePrivacyLevel | None = ...,
        send_start_notification: bool | None = ...,
        reason: str | None = ...,
    ) -> StageInstance:
        """https://discord.com/developers/docs/resources/stage-instance#create-stage-instance"""
        ...

    async def get_stage_instance(
        self, *, channel_id: SnowflakeType
    ) -> StageInstance | None:
        """https://discord.com/developers/docs/resources/stage-instance#get-stage-instance"""
        ...

    async def modify_stage_instance(
        self,
        *,
        channel_id: SnowflakeType,
        topic: str | None = ...,
        privacy_level: StagePrivacyLevel | None = ...,
        reason: str | None = ...,
    ) -> StageInstance:
        """https://discord.com/developers/docs/resources/stage-instance#modify-stage-instance"""
        ...

    async def delete_stage_instance(
        self, *, channel_id: SnowflakeType, reason: str | None = ...
    ) -> None:
        """https://discord.com/developers/docs/resources/stage-instance#delete-stage-instance"""
        ...

    async def get_sticker(self, *, sticker_id: SnowflakeType) -> Sticker:
        """https://discord.com/developers/docs/resources/sticker#get-sticker"""
        ...

    async def list_nitro_sticker_packs(self) -> list[StickerPack]:
        """https://discord.com/developers/docs/resources/sticker#list-nitro-sticker-packs"""
        ...

    async def list_guild_stickers(self, *, guild_id: SnowflakeType) -> list[Sticker]:
        """https://discord.com/developers/docs/resources/sticker#list-guild-stickers"""
        ...

    async def get_guild_sticker(
        self, *, guild_id: SnowflakeType, sticker_id: SnowflakeType
    ) -> Sticker:
        """https://discord.com/developers/docs/resources/sticker#get-guild-sticker"""
        ...
    # async def create_guild_sticker(self,
    #                                *,
    #                                guild_id: SnowflakeType,
    #                                name: str,
    #                                description: str,
    #                                tags: str,
    #                                file: File,
    #                                reason: Optional[str] = ...) -> Sticker:
    #     """https://discord.com/developers/docs/resources/sticker#create-guild-sticker"""
    #     ...
    async def modify_guild_sticker(
        self,
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
        name: str | None = ...,
        description: str | None = ...,
        tags: str | None = ...,
        reason: str | None = ...,
    ) -> Sticker:
        """https://discord.com/developers/docs/resources/sticker#modify-guild-sticker"""
        ...

    async def delete_guild_sticker(
        self,
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
        reason: str | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/sticker#delete-guild-sticker"""
        ...

    async def get_current_user(self) -> User:
        """https://discord.com/developers/docs/resources/user#get-current-user"""
        ...

    async def get_user(self, *, user_id: SnowflakeType) -> User:
        """https://discord.com/developers/docs/resources/user#get-user"""
        ...

    async def modify_current_user(
        self, *, username: str | None = ..., avatar: str | None = ...
    ) -> User:
        """https://discord.com/developers/docs/resources/user#modify-current-user"""
        ...

    async def get_current_user_guilds(
        self,
        *,
        before: SnowflakeType | None = ...,
        after: SnowflakeType | None = ...,
        limit: int | None = ...,
    ) -> list[CurrentUserGuild]:
        """https://discord.com/developers/docs/resources/user#get-current-user-guilds"""
        ...

    async def get_current_user_guild_member(
        self, *, guild_id: SnowflakeType
    ) -> GuildMember:
        """https://discord.com/developers/docs/resources/user#get-current-user-guild-member"""
        ...

    async def leave_guild(self, *, guild_id: SnowflakeType) -> None:
        """https://discord.com/developers/docs/resources/user#leave-guild"""
        ...

    async def create_DM(self, *, recipient_id: SnowflakeType) -> Channel:
        """https://discord.com/developers/docs/resources/user#create-dm"""
        ...

    async def create_group_DM(
        self, *, access_tokens: list[str], nicks: dict[SnowflakeType, str]
    ) -> Channel:
        """https://discord.com/developers/docs/resources/user#create-group-dm"""
        ...

    async def get_user_connections(self) -> list[Connection]:
        """https://discord.com/developers/docs/resources/user#get-user-connections"""
        ...

    async def get_user_application_role_connection(
        self, *, application_id: SnowflakeType
    ) -> ApplicationRoleConnection:
        """https://discord.com/developers/docs/resources/user#get-user-application-connections"""
        ...

    async def update_user_application_role_connection(
        self,
        *,
        application_id: SnowflakeType,
        platform_name: str | None = ...,
        platform_username: str | None = ...,
        metadata: ApplicationRoleConnectionMetadata | None = ...,
    ) -> ApplicationRoleConnection:
        """https://discord.com/developers/docs/resources/user#modify-current-user"""
        ...

    async def list_voice_regions(self) -> list[VoiceRegion]:
        """https://discord.com/developers/docs/resources/voice#list-voice-regions"""
        ...

    async def create_webhook(
        self,
        *,
        channel_id: SnowflakeType,
        name: str,
        avatar: str | None = ...,
        reason: str | None = ...,
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#create-webhook"""
        ...

    async def get_channel_webhooks(self, *, channel_id: SnowflakeType) -> list[Webhook]:
        """https://discord.com/developers/docs/resources/webhook#get-channel-webhooks"""
        ...

    async def get_guild_webhooks(self, *, guild_id: SnowflakeType) -> list[Webhook]:
        """https://discord.com/developers/docs/resources/webhook#get-guild-webhooks"""
        ...

    async def get_webhook(self, *, webhook_id: SnowflakeType) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#get-webhook"""
        ...

    async def get_webhook_with_token(
        self, *, webhook_id: SnowflakeType, token: str
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#get-webhook-with-token"""
        ...

    async def modify_webhook(
        self,
        *,
        webhook_id: SnowflakeType,
        name: str | None = ...,
        avatar: str | None = ...,
        channel_id: SnowflakeType | None = ...,
        reason: str | None = ...,
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#modify-webhook"""
        ...

    async def modify_webhook_with_token(
        self,
        *,
        webhook_id: SnowflakeType,
        token: str,
        name: str | None = ...,
        avatar: str | None = ...,
    ) -> Webhook:
        """https://discord.com/developers/docs/resources/webhook#modify-webhook-with-token"""
        ...

    async def delete_webhook(
        self, *, webhook_id: SnowflakeType, reason: str | None = ...
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#delete-webhook"""
        ...

    async def delete_webhook_with_token(
        self, *, webhook_id: SnowflakeType, token: str
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#delete-webhook-with-token"""
        ...

    @overload
    async def execute_webhook(
        self,
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: Literal[False] | None = ...,
        thread_id: SnowflakeType | None = ...,
        content: str | None = ...,
        username: str | None = ...,
        avatar_url: str | None = ...,
        tts: bool | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[Component] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
        flags: int | None = ...,
        thread_name: str | None = ...,
        **data,
    ) -> None: ...
    @overload
    async def execute_webhook(
        self,
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: Literal[True] = ...,
        thread_id: SnowflakeType | None = ...,
        content: str | None = ...,
        username: str | None = ...,
        avatar_url: str | None = ...,
        tts: bool | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[Component] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
        flags: int | None = ...,
        thread_name: str | None = ...,
        **data,
    ) -> MessageGet: ...
    async def execute_webhook(
        self,
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: bool | None = ...,
        thread_id: SnowflakeType | None = ...,
        content: str | None = ...,
        username: str | None = ...,
        avatar_url: str | None = ...,
        tts: bool | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[Component] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
        flags: int | None = ...,
        thread_name: str | None = ...,
        **data,
    ) -> MessageGet | None:
        """https://discord.com/developers/docs/resources/webhook#execute-webhook"""
        ...

    async def execute_slack_compatible_webhook(
        self,
        *,
        webhook_id: SnowflakeType,
        token: str,
        thread_id: SnowflakeType | None = ...,
        wait: bool | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#execute-slackcompatible-webhook"""
        ...

    async def execute_github_compatible_webhook(
        self,
        *,
        webhook_id: SnowflakeType,
        token: str,
        thread_id: SnowflakeType | None = ...,
        wait: bool | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#execute-githubcompatible-webhook"""
        ...

    async def get_webhook_message(
        self,
        *,
        webhook_id: SnowflakeType,
        token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = ...,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/webhook#get-webhook-message"""
        ...

    async def edit_webhook_message(
        self,
        *,
        webhook_id: SnowflakeType,
        webhook_token: str,
        thread_id: SnowflakeType | None = ...,
        content: str | None = ...,
        embeds: list[Embed] | None = ...,
        allowed_mentions: AllowedMention | None = ...,
        components: list[Component] | None = ...,
        files: list[File] | None = ...,
        attachments: list[AttachmentSend] | None = ...,
    ) -> MessageGet:
        """https://discord.com/developers/docs/resources/webhook#edit-webhook-message"""
        ...

    async def delete_webhook_message(
        self,
        *,
        webhook_id: SnowflakeType,
        token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = ...,
    ) -> None:
        """https://discord.com/developers/docs/resources/webhook#delete-webhook-message"""
        ...

    async def get_gateway(self) -> Gateway:
        """https://discord.com/developers/docs/topics/gateway#get-gateway"""
        ...

    async def get_gateway_bot(self) -> GatewayBot:
        """https://discord.com/developers/docs/topics/gateway#get-gateway-bot"""
        ...

    async def get_current_bot_application_information(self) -> Application:
        """https://discord.com/developers/docs/resources/user#get-current-application-information"""
        ...

    async def get_current_authorization_information(self) -> AuthorizationResponse:
        """https://discord.com/developers/docs/resources/user#get-current-authorization-information"""
        ...
