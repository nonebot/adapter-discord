from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .embeds import (
        Embed,
        EmbedAuthor,
        EmbedField,
        EmbedFooter,
        EmbedImage,
        EmbedProvider,
        EmbedThumbnail,
        EmbedVideo,
    )
    from .messages import (
        AllowedMention,
        Attachment,
        AttachmentSend,
        ChannelMention,
        CountDetails,
        File,
        MessageActivity,
        MessageCall,
        MessageEditParams,
        MessageGet,
        MessageReference,
        MessageSend,
        MessageSnapshot,
        MessageSnapshotMessage,
        Reaction,
        RoleSubscriptionData,
        WebhookMessageEditParams,
    )
    from .oauth2 import AuthorizationResponse
    from .permissions import (
        CreateGuildRoleParams,
        ModifyGuildRoleParams,
        ModifyGuildRolePositionParams,
        Role,
        RoleColors,
        RoleTags,
    )
    from .snowflake import Snowflake, SnowflakeType
    from .teams import Team, TeamMember, TeamMemberUser
    from .user import (
        ApplicationRoleConnection,
        AvatarDecorationData,
        Connection,
        ModifyCurrentUserParams,
        User,
    )


__all__ = [
    "AllowedMention",
    "ApplicationRoleConnection",
    "Attachment",
    "AttachmentSend",
    "AuthorizationResponse",
    "AvatarDecorationData",
    "ChannelMention",
    "Connection",
    "CountDetails",
    "CreateGuildRoleParams",
    "Embed",
    "EmbedAuthor",
    "EmbedField",
    "EmbedFooter",
    "EmbedImage",
    "EmbedProvider",
    "EmbedThumbnail",
    "EmbedVideo",
    "File",
    "MessageActivity",
    "MessageCall",
    "MessageEditParams",
    "MessageGet",
    "MessageReference",
    "MessageSend",
    "MessageSnapshot",
    "MessageSnapshotMessage",
    "ModifyCurrentUserParams",
    "ModifyGuildRoleParams",
    "ModifyGuildRolePositionParams",
    "Reaction",
    "Role",
    "RoleColors",
    "RoleSubscriptionData",
    "RoleTags",
    "Snowflake",
    "SnowflakeType",
    "Team",
    "TeamMember",
    "TeamMemberUser",
    "User",
    "WebhookMessageEditParams",
]


_EXPORTS: dict[str, tuple[str, str]] = {
    "AllowedMention": (".messages", "AllowedMention"),
    "ApplicationRoleConnection": (".user", "ApplicationRoleConnection"),
    "Attachment": (".messages", "Attachment"),
    "AttachmentSend": (".messages", "AttachmentSend"),
    "AuthorizationResponse": (".oauth2", "AuthorizationResponse"),
    "AvatarDecorationData": (".user", "AvatarDecorationData"),
    "ChannelMention": (".messages", "ChannelMention"),
    "Connection": (".user", "Connection"),
    "CountDetails": (".messages", "CountDetails"),
    "CreateGuildRoleParams": (".permissions", "CreateGuildRoleParams"),
    "Embed": (".embeds", "Embed"),
    "EmbedAuthor": (".embeds", "EmbedAuthor"),
    "EmbedField": (".embeds", "EmbedField"),
    "EmbedFooter": (".embeds", "EmbedFooter"),
    "EmbedImage": (".embeds", "EmbedImage"),
    "EmbedProvider": (".embeds", "EmbedProvider"),
    "EmbedThumbnail": (".embeds", "EmbedThumbnail"),
    "EmbedVideo": (".embeds", "EmbedVideo"),
    "File": (".messages", "File"),
    "MessageActivity": (".messages", "MessageActivity"),
    "MessageCall": (".messages", "MessageCall"),
    "MessageEditParams": (".messages", "MessageEditParams"),
    "MessageGet": (".messages", "MessageGet"),
    "MessageReference": (".messages", "MessageReference"),
    "MessageSend": (".messages", "MessageSend"),
    "MessageSnapshot": (".messages", "MessageSnapshot"),
    "MessageSnapshotMessage": (".messages", "MessageSnapshotMessage"),
    "ModifyCurrentUserParams": (".user", "ModifyCurrentUserParams"),
    "ModifyGuildRoleParams": (".permissions", "ModifyGuildRoleParams"),
    "ModifyGuildRolePositionParams": (".permissions", "ModifyGuildRolePositionParams"),
    "Reaction": (".messages", "Reaction"),
    "Role": (".permissions", "Role"),
    "RoleColors": (".permissions", "RoleColors"),
    "RoleSubscriptionData": (".messages", "RoleSubscriptionData"),
    "RoleTags": (".permissions", "RoleTags"),
    "Snowflake": (".snowflake", "Snowflake"),
    "SnowflakeType": (".snowflake", "SnowflakeType"),
    "Team": (".teams", "Team"),
    "TeamMember": (".teams", "TeamMember"),
    "TeamMemberUser": (".teams", "TeamMemberUser"),
    "User": (".user", "User"),
    "WebhookMessageEditParams": (".messages", "WebhookMessageEditParams"),
}


def __getattr__(name: str) -> object:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError:
        raise AttributeError(name) from None

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
