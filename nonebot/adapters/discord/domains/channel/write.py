"""Canonical channel.write models."""

from typing import TYPE_CHECKING
from typing_extensions import Required

from .._model_support import OutboundTypedDict

if TYPE_CHECKING:
    from .types import OverwriteType
    from ..invite.types import InviteTargetType
    from ..models import (
        DefaultReaction,
        ForumTagRequest,
        PartialOverwrite,
    )
    from ...protocol import SnowflakeType

from .._model_support import (
    ChannelFlags,
    ChannelType,
    ForumLayoutTypes,
    Snowflake,
    SortOrderTypes,
    VideoQualityMode,
)


class ModifyChannelParams(OutboundTypedDict, total=False):
    """Modify Channel Params

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    # JSON Params (Guild channel)
    # see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    name: str
    type: ChannelType
    position: int | None
    topic: str | None
    nsfw: bool | None
    rate_limit_per_user: int | None
    bitrate: int | None
    user_limit: int | None
    permission_overwrites: "list[PartialOverwrite] | None"
    parent_id: Snowflake | None
    rtc_region: str | None
    video_quality_mode: VideoQualityMode | None
    default_auto_archive_duration: int | None
    flags: ChannelFlags
    available_tags: "list[ForumTagRequest]"
    default_reaction_emoji: "DefaultReaction | None"
    default_thread_rate_limit_per_user: int
    default_sort_order: SortOrderTypes | None
    default_forum_layout: ForumLayoutTypes


class ModifyThreadParams(OutboundTypedDict, total=False):
    """Modify Thread Params.

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-thread
    """

    name: str
    archived: bool
    auto_archive_duration: int
    locked: bool
    invitable: bool
    rate_limit_per_user: int | None
    flags: ChannelFlags
    applied_tags: list[Snowflake]


class StartThreadFromMessageParams(OutboundTypedDict, total=False):
    """Start Thread From Message Params.

    see https://discord.com/developers/docs/resources/channel#start-thread-from-message
    """

    name: Required[str]
    auto_archive_duration: int
    rate_limit_per_user: int | None


class StartThreadWithoutMessageParams(OutboundTypedDict, total=False):
    """Start Thread Without Message Params.

    see https://discord.com/developers/docs/resources/channel#start-thread-without-message
    """

    name: Required[str]
    auto_archive_duration: int
    type: ChannelType
    invitable: bool
    rate_limit_per_user: int | None


class ModifyGuildChannelPositionParams(OutboundTypedDict, total=False):
    """Modify Guild Channel Position Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions
    """

    id: Required[Snowflake]
    position: int | None
    lock_permissions: bool | None
    parent_id: Snowflake | None


class ModifyDMParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_modify_DM``."""

    name: str
    icon: bytes


class EditChannelPermissionsParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_edit_channel_permissions``."""

    allow: str
    deny: str
    type: Required["OverwriteType"]


class CreateChannelInviteParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_create_channel_invite``."""

    max_age: int
    max_uses: int
    temporary: bool
    unique: bool
    target_type: "InviteTargetType"
    target_user_id: "SnowflakeType"
    target_application_id: "SnowflakeType"
    role_ids: "list[SnowflakeType]"


class FollowAnnouncementChannelParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_follow_announcement_channel``."""

    webhook_channel_id: Required["SnowflakeType"]


class AddGroupDMRecipientParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_group_DM_add_recipient``."""

    access_token: Required[str]
    nick: Required[str]


__all__ = [
    "AddGroupDMRecipientParams",
    "CreateChannelInviteParams",
    "EditChannelPermissionsParams",
    "FollowAnnouncementChannelParams",
    "ModifyChannelParams",
    "ModifyDMParams",
    "ModifyGuildChannelPositionParams",
    "ModifyThreadParams",
    "StartThreadFromMessageParams",
    "StartThreadWithoutMessageParams",
]
