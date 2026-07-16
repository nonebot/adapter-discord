"""Canonical channel.write models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import DefaultReaction, ForumTagRequest, PartialOverwrite

from .._model_support import (
    UNSET,
    BaseModel,
    ChannelFlags,
    ChannelType,
    ForumLayoutTypes,
    Missing,
    MissingOrNullable,
    Snowflake,
    SortOrderTypes,
    VideoQualityMode,
)


class ModifyChannelParams(BaseModel):
    """Modify Channel Params

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    # JSON Params (Guild channel)
    # see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    name: Missing[str] = UNSET
    type: Missing[ChannelType] = UNSET
    position: MissingOrNullable[int] = UNSET
    topic: MissingOrNullable[str] = UNSET
    nsfw: MissingOrNullable[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET
    bitrate: MissingOrNullable[int] = UNSET
    user_limit: MissingOrNullable[int] = UNSET
    permission_overwrites: MissingOrNullable[list["PartialOverwrite"]] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    rtc_region: MissingOrNullable[str] = UNSET
    video_quality_mode: MissingOrNullable[VideoQualityMode] = UNSET
    default_auto_archive_duration: MissingOrNullable[int] = UNSET
    flags: Missing[ChannelFlags] = UNSET
    available_tags: Missing[list["ForumTagRequest"]] = UNSET
    default_reaction_emoji: MissingOrNullable["DefaultReaction"] = UNSET
    default_thread_rate_limit_per_user: Missing[int] = UNSET
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    default_forum_layout: Missing[ForumLayoutTypes] = UNSET


class ModifyThreadParams(BaseModel):
    """Modify Thread Params.

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-thread
    """

    name: Missing[str] = UNSET
    archived: Missing[bool] = UNSET
    auto_archive_duration: Missing[int] = UNSET
    locked: Missing[bool] = UNSET
    invitable: Missing[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET
    flags: Missing[ChannelFlags] = UNSET
    applied_tags: Missing[list[Snowflake]] = UNSET


class StartThreadFromMessageParams(BaseModel):
    """Start Thread From Message Params.

    see https://discord.com/developers/docs/resources/channel#start-thread-from-message
    """

    name: str
    auto_archive_duration: Missing[int] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET


class StartThreadWithoutMessageParams(BaseModel):
    """Start Thread Without Message Params.

    see https://discord.com/developers/docs/resources/channel#start-thread-without-message
    """

    name: str
    auto_archive_duration: Missing[int] = UNSET
    type: Missing[ChannelType] = UNSET
    invitable: Missing[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET


class ModifyGuildChannelPositionParams(BaseModel):
    """Modify Guild Channel Position Params.

    see https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions
    """

    id: Snowflake
    position: MissingOrNullable[int] = UNSET
    lock_permissions: MissingOrNullable[bool] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET


__all__ = [
    "ModifyChannelParams",
    "ModifyGuildChannelPositionParams",
    "ModifyThreadParams",
    "StartThreadFromMessageParams",
    "StartThreadWithoutMessageParams",
]
