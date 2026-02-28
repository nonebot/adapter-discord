from __future__ import annotations

from pydantic import BaseModel

from ..common.channels import (
    Channel,
    DefaultReaction,
    FollowedChannel,
    ForumTag,
    Overwrite,
    ThreadMember,
    ThreadMetadata,
)
from ..common.snowflake import Snowflake
from ...types import (
    UNSET,
    ChannelFlags,
    ChannelType,
    ForumLayoutTypes,
    Missing,
    MissingOrNullable,
    OverwriteType,
    SortOrderTypes,
    VideoQualityMode,
)


class PartialOverwrite(BaseModel):
    id: Snowflake
    type: OverwriteType
    allow: MissingOrNullable[str] = UNSET
    deny: MissingOrNullable[str] = UNSET


class ForumTagRequest(BaseModel):
    id: Missing[Snowflake] = UNSET
    name: str
    moderated: Missing[bool] = UNSET
    emoji_id: MissingOrNullable[Snowflake] = UNSET
    emoji_name: MissingOrNullable[str] = UNSET


class ArchivedThreadsResponse(BaseModel):
    threads: list[Channel]
    members: list[ThreadMember]
    has_more: bool


class ModifyChannelParams(BaseModel):
    name: Missing[str] = UNSET
    type: Missing[ChannelType] = UNSET
    position: MissingOrNullable[int] = UNSET
    topic: MissingOrNullable[str] = UNSET
    nsfw: MissingOrNullable[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET
    bitrate: MissingOrNullable[int] = UNSET
    user_limit: MissingOrNullable[int] = UNSET
    permission_overwrites: MissingOrNullable[list[PartialOverwrite]] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    rtc_region: MissingOrNullable[str] = UNSET
    video_quality_mode: MissingOrNullable[VideoQualityMode] = UNSET
    default_auto_archive_duration: MissingOrNullable[int] = UNSET
    flags: Missing[ChannelFlags] = UNSET
    available_tags: Missing[list[ForumTagRequest]] = UNSET
    default_reaction_emoji: MissingOrNullable[DefaultReaction] = UNSET
    default_thread_rate_limit_per_user: Missing[int] = UNSET
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    default_forum_layout: Missing[ForumLayoutTypes] = UNSET


class ModifyThreadParams(BaseModel):
    name: Missing[str] = UNSET
    archived: Missing[bool] = UNSET
    auto_archive_duration: Missing[int] = UNSET
    locked: Missing[bool] = UNSET
    invitable: Missing[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET
    flags: Missing[ChannelFlags] = UNSET
    applied_tags: Missing[list[Snowflake]] = UNSET


class StartThreadFromMessageParams(BaseModel):
    name: str
    auto_archive_duration: Missing[int] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET


class StartThreadWithoutMessageParams(BaseModel):
    name: str
    auto_archive_duration: Missing[int] = UNSET
    type: Missing[ChannelType] = UNSET
    invitable: Missing[bool] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET


class ModifyGuildChannelPositionParams(BaseModel):
    id: Snowflake
    position: MissingOrNullable[int] = UNSET
    lock_permissions: MissingOrNullable[bool] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET


class CreateGuildChannelParams(BaseModel):
    name: str
    type: ChannelType | None = None
    topic: str | None = None
    bitrate: int | None = None
    user_limit: int | None = None
    rate_limit_per_user: int | None = None
    position: int | None = None
    permission_overwrites: list[Overwrite] | None = None
    parent_id: Snowflake | None = None
    nsfw: bool | None = None
    rtc_region: str | None = None
    video_quality_mode: VideoQualityMode | None = None
    default_auto_archive_duration: int | None = None
    default_reaction_emoji: DefaultReaction | None = None
    available_tags: list[ForumTagRequest] | None = None
    default_sort_order: SortOrderTypes | None = None
    default_forum_layout: ForumLayoutTypes | None = None
    default_thread_rate_limit_per_user: int | None = None


class ListActiveGuildThreadsResponse(BaseModel):
    threads: list[Channel]
    members: list[ThreadMember]


__all__ = [
    "ArchivedThreadsResponse",
    "Channel",
    "CreateGuildChannelParams",
    "DefaultReaction",
    "FollowedChannel",
    "ForumTag",
    "ForumTagRequest",
    "ListActiveGuildThreadsResponse",
    "ModifyChannelParams",
    "ModifyGuildChannelPositionParams",
    "ModifyThreadParams",
    "Overwrite",
    "PartialOverwrite",
    "StartThreadFromMessageParams",
    "StartThreadWithoutMessageParams",
    "ThreadMember",
    "ThreadMetadata",
]
