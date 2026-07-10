from __future__ import annotations

from enum import IntEnum, IntFlag


class ChannelFlags(IntFlag):
    """Channel flags.

    see https://discord.com/developers/docs/resources/channel#channel-object-channel-flags
    """

    PINNED = 1 << 1
    """this thread is pinned to the top of its parent GUILD_FORUM channel"""
    REQUIRE_TAG = 1 << 4
    """whether a tag is required to be specified
    when creating a thread in a GUILD_FORUM channel.
    Tags are specified in the applied_tags field."""
    HIDE_MEDIA_DOWNLOAD_OPTIONS = 1 << 15
    """when set hides the embedded media download options. Available only for
    media channels"""


class ChannelType(IntEnum):
    """Channel type.

    Type ANNOUNCEMENT_THREAD(10), PUBLIC_THREAD(11) and PRIVATE_THREAD(12) are only
    available in API v9 and above.

    The GUILD_MEDIA(16) channel type is still in active development.
    Avoid implementing any features that are not documented here, since they are
    subject to change without notice!

    see https://discord.com/developers/docs/resources/channel#channel-object-channel-types
    """

    GUILD_TEXT = 0
    """a text channel within a server"""
    DM = 1
    """a direct message between users"""
    GUILD_VOICE = 2
    """a voice channel within a server"""
    GROUP_DM = 3
    """a direct message between multiple users"""
    GUILD_CATEGORY = 4
    """an organizational category that contains up to 50 channels"""
    GUILD_ANNOUNCEMENT = 5
    """a channel that users can follow and crosspost
    into their own server (formerly news channels)"""
    ANNOUNCEMENT_THREAD = 10
    """a temporary sub-channel within a GUILD_ANNOUNCEMENT channel"""
    PUBLIC_THREAD = 11
    """a temporary sub-channel within a GUILD_TEXT or GUILD_FORUM channel"""
    PRIVATE_THREAD = 12
    """a temporary sub-channel within a GUILD_TEXT channel that is only viewable by
    those invited and those with the MANAGE_THREADS permission"""
    GUILD_STAGE_VOICE = 13
    """a voice channel for hosting events with an audience"""
    GUILD_DIRECTORY = 14
    """the channel in a hub containing the listed servers"""
    GUILD_FORUM = 15
    """Channel that can only contain threads"""
    GUILD_MEDIA = 16
    """Channel that can only contain threads, similar to GUILD_FORUM channels"""


class ForumLayoutTypes(IntEnum):
    """Forum layout types.

    see https://discord.com/developers/docs/resources/channel#channel-object-forum-layout-types
    """

    NOT_SET = 0
    """No default has been set for forum channel"""
    LIST_VIEW = 1
    """Display posts as a list"""
    GALLERY_VIEW = 2
    """Display posts as a collection of tiles"""


class OverwriteType(IntEnum):
    """Overwrite type.

    see https://discord.com/developers/docs/resources/channel#overwrite-object"""

    ROLE = 0
    MEMBER = 1


class SortOrderTypes(IntEnum):
    """Sort order types.

    see https://discord.com/developers/docs/resources/channel#channel-object-sort-order-types
    """

    LATEST_ACTIVITY = 0
    """Sort forum posts by activity"""
    CREATION_DATE = 1
    """Sort forum posts by creation time (from most recent to oldest)"""


class VideoQualityMode(IntEnum):
    """Video quality mode.

    see https://discord.com/developers/docs/resources/channel#channel-object-video-quality-modes
    """

    AUTO = 1
    """Discord chooses the quality for optimal performance"""
    FULL = 2
    """720p"""


__all__ = [
    "ChannelFlags",
    "ChannelType",
    "ForumLayoutTypes",
    "OverwriteType",
    "SortOrderTypes",
    "VideoQualityMode",
]
