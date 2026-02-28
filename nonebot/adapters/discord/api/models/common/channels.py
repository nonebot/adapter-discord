from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
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

if TYPE_CHECKING:
    from .guild_members import GuildMember
    from .user import User


class Channel(BaseModel):
    id: Snowflake
    type: ChannelType
    guild_id: Missing[Snowflake] = UNSET
    position: Missing[int] = UNSET
    permission_overwrites: Missing[list[Overwrite]] = UNSET
    name: MissingOrNullable[str] = UNSET
    topic: MissingOrNullable[str] = UNSET
    nsfw: Missing[bool] = UNSET
    last_message_id: MissingOrNullable[Snowflake] = UNSET
    bitrate: Missing[int] = UNSET
    user_limit: Missing[int] = UNSET
    rate_limit_per_user: Missing[int] = UNSET
    recipients: Missing[list[User]] = UNSET
    icon: MissingOrNullable[str] = UNSET
    owner_id: Missing[Snowflake] = UNSET
    application_id: Missing[Snowflake] = UNSET
    managed: Missing[bool] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    last_pin_timestamp: MissingOrNullable[datetime.datetime] = UNSET
    rtc_region: MissingOrNullable[str] = UNSET
    video_quality_mode: Missing[VideoQualityMode] = UNSET
    message_count: Missing[int] = UNSET
    member_count: Missing[int] = UNSET
    thread_metadata: Missing[ThreadMetadata] = UNSET
    member: Missing[ThreadMember] = UNSET
    default_auto_archive_duration: Missing[int] = UNSET
    permissions: Missing[str] = UNSET
    flags: Missing[ChannelFlags] = UNSET
    total_message_sent: Missing[int] = UNSET
    available_tags: Missing[list[ForumTag]] = UNSET
    applied_tags: Missing[list[Snowflake]] = UNSET
    default_reaction_emoji: MissingOrNullable[DefaultReaction] = UNSET
    default_thread_rate_limit_per_user: Missing[int] = UNSET
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    default_forum_layout: Missing[ForumLayoutTypes] = UNSET


class FollowedChannel(BaseModel):
    channel_id: Snowflake
    webhook_id: Snowflake


class Overwrite(BaseModel):
    id: Snowflake
    type: OverwriteType
    allow: str
    deny: str


class ThreadMetadata(BaseModel):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime.datetime
    locked: bool
    invitable: Missing[bool] = UNSET
    create_timestamp: MissingOrNullable[datetime.datetime] = UNSET


class ThreadMember(BaseModel):
    id: Missing[Snowflake] = UNSET
    user_id: Missing[Snowflake] = UNSET
    join_timestamp: datetime.datetime
    flags: int
    member: Missing[GuildMember] = UNSET


class DefaultReaction(BaseModel):
    emoji_id: str | None = None
    emoji_name: str | None = None


class ForumTag(BaseModel):
    id: Snowflake
    name: str
    moderated: bool
    emoji_id: Snowflake | None = None
    emoji_name: str | None = None
