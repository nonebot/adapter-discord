from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

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

if TYPE_CHECKING:
    from .guild_members import GuildMember
from ..common.user import User

# Channel
# see https://discord.com/developers/docs/resources/channel


class Channel(BaseModel):
    """Represents a guild or DM channel within Discord.

    see https://discord.com/developers/docs/resources/channel#channel-object"""

    id: Snowflake
    """the id of this channel"""
    type: ChannelType
    """the type of channel"""
    guild_id: Missing[Snowflake] = UNSET
    """the id of the guild (may be missing for some channel objects
    received over gateway guild dispatches)"""
    position: Missing[int] = UNSET
    """sorting position of the channel"""
    permission_overwrites: Missing[list[Overwrite]] = UNSET
    """explicit permission overwrites for members and roles"""
    name: MissingOrNullable[str] = UNSET
    """the name of the channel (1-100 characters)"""
    topic: MissingOrNullable[str] = UNSET
    """the channel topic (0-4096 characters for GUILD_FORUM channels,
    0-1024 characters for all others)"""
    nsfw: Missing[bool] = UNSET
    """whether the channel is nsfw"""
    last_message_id: MissingOrNullable[Snowflake] = UNSET
    """the id of the last message sent in this channel
    (or thread for GUILD_FORUM channels)
    (may not point to an existing or valid message or thread)"""
    bitrate: Missing[int] = UNSET
    """the bitrate (in bits) of the voice channel"""
    user_limit: Missing[int] = UNSET
    """the user limit of the voice channel"""
    rate_limit_per_user: Missing[int] = UNSET
    """amount of seconds a user has to wait before sending another message (0-21600);
    bots, as well as users with the permission manage_messages or
    manage_channel, are unaffected"""
    recipients: Missing[list[User]] = UNSET
    """the recipients of the DM"""
    icon: MissingOrNullable[str] = UNSET
    """icon hash of the group DM"""
    owner_id: Missing[Snowflake] = UNSET
    """id of the creator of the group DM or thread"""
    application_id: Missing[Snowflake] = UNSET
    """application id of the group DM creator if it is bot-created"""
    managed: Missing[bool] = UNSET
    """for group DM channels: whether the channel is managed
    by an application via the gdm.join OAuth2 scope"""
    parent_id: MissingOrNullable[Snowflake] = UNSET
    """for guild channels: id of the parent category for a channel
    (each parent category can contain up to 50 channels),
    for threads: id of the text channel this thread was created"""
    last_pin_timestamp: MissingOrNullable[datetime.datetime] = UNSET
    """when the last pinned message was pinned.
    This may be null in events such as GUILD_CREATE when a message is not pinned."""
    rtc_region: MissingOrNullable[str] = UNSET
    """voice region id for the voice channel, automatic when set to null"""
    video_quality_mode: Missing[VideoQualityMode] = UNSET
    """the camera video quality mode of the voice channel, 1 when not present"""
    message_count: Missing[int] = UNSET
    """number of messages (not including the initial message
    or deleted messages) in a thread."""
    member_count: Missing[int] = UNSET
    """an approximate count of users in a thread, stops counting at 50"""
    thread_metadata: Missing[ThreadMetadata] = UNSET
    """thread-specific fields not needed by other channels"""
    member: Missing[ThreadMember] = UNSET
    """thread member object for the current user, if they have joined the thread,
    only included on certain API endpoints"""
    default_auto_archive_duration: Missing[int] = UNSET
    """default duration, copied onto newly created threads, in minutes,
    threads will stop showing in the channel list after the specified
    period of inactivity, can be set to: 60, 1440, 4320, 10080"""
    permissions: Missing[str] = UNSET
    """computed permissions for the invoking user in the channel, including overwrites,
    only included when part of the resolved data received on a slash command interaction
    """
    flags: Missing[ChannelFlags] = UNSET
    """channel flags combined as a bitfield"""
    total_message_sent: Missing[int] = UNSET
    """number of messages ever sent in a thread, it's similar to message_count
    on message creation, but will not decrement the number when a message is deleted"""
    available_tags: Missing[list[ForumTag]] = UNSET
    """the set of tags that can be used in a GUILD_FORUM or a GUILD_MEDIA channel"""
    applied_tags: Missing[list[Snowflake]] = UNSET
    """the IDs of the set of tags that have been applied to a
    thread in a GUILD_FORUM or a GUILD_MEDIA channel"""
    default_reaction_emoji: MissingOrNullable[DefaultReaction] = UNSET
    """the emoji to show in the add reaction button on a
    thread in a GUILD_FORUM channel"""
    default_thread_rate_limit_per_user: Missing[int] = UNSET
    """the initial rate_limit_per_user to set on newly created threads in a channel.
    this field is copied to the thread at creation time and does not live update."""
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    """the default sort order type used to order posts in GUILD_FORUM channels.
    Defaults to null, which indicates a preferred sort order
    hasn't been set by a channel admin"""
    default_forum_layout: Missing[ForumLayoutTypes] = UNSET
    """the default forum layout view used to display posts in GUILD_FORUM channels.
    Defaults to 0, which indicates a layout view has not been set by a channel admin"""


class FollowedChannel(BaseModel):
    """Followed channel.

    see https://discord.com/developers/docs/resources/channel#followed-channel-object"""

    channel_id: Snowflake
    webhook_id: Snowflake


class Overwrite(BaseModel):
    """Overwrite.

    see https://discord.com/developers/docs/resources/channel#overwrite-object"""

    id: Snowflake
    type: OverwriteType
    allow: str
    deny: str


class PartialOverwrite(BaseModel):
    """Partial overwrite.

    Used in request payloads where `allow`/`deny` can be omitted or null.

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    id: Snowflake
    type: OverwriteType
    allow: MissingOrNullable[str] = UNSET
    deny: MissingOrNullable[str] = UNSET


class ThreadMetadata(BaseModel):
    """Thread metadata.

    see https://discord.com/developers/docs/resources/channel#thread-metadata-object"""

    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime.datetime
    locked: bool
    invitable: Missing[bool] = UNSET
    create_timestamp: MissingOrNullable[datetime.datetime] = UNSET


class ThreadMember(BaseModel):
    """Thread member.

    see https://discord.com/developers/docs/resources/channel#thread-member-object"""

    id: Missing[Snowflake] = UNSET
    user_id: Missing[Snowflake] = UNSET
    join_timestamp: datetime.datetime
    flags: int
    member: Missing[GuildMember] = UNSET


class DefaultReaction(BaseModel):
    """Default reaction.

    see https://discord.com/developers/docs/resources/channel#default-reaction-object"""

    emoji_id: str | None = None
    emoji_name: str | None = None


class ForumTag(BaseModel):
    """An object that represents a tag that is able to be applied
    to a thread in a GUILD_FORUM or GUILD_MEDIA channel.

    see https://discord.com/developers/docs/resources/channel#forum-tag-object"""

    id: Snowflake
    name: str
    moderated: bool
    emoji_id: Snowflake | None = None
    emoji_name: str | None = None


class ForumTagRequest(BaseModel):
    """Forum tag request.

    see https://discord.com/developers/docs/resources/channel#forum-tag-object"""

    id: Missing[Snowflake] = UNSET
    name: str
    moderated: Missing[bool] = UNSET
    emoji_id: MissingOrNullable[Snowflake] = UNSET
    emoji_name: MissingOrNullable[str] = UNSET


class ArchivedThreadsResponse(BaseModel):
    """Archived threads response.

    see https://discord.com/developers/docs/resources/channel#list-public-archived-threads-response-body
    """

    threads: list[Channel]
    members: list[ThreadMember]
    has_more: bool


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
