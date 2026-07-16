"""Canonical channel.gateway models."""

from .._model_support import (
    UNSET,
    BaseModel,
    ChannelType,
    Missing,
    MissingOrNullable,
    Snowflake,
    datetime,
)
from ..channel.read import Channel, ThreadMember


class ChannelCreate(Channel):
    """Channel Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-create"""


class ChannelUpdate(Channel):
    """Channel Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-update"""


class ChannelDelete(Channel):
    """Channel Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-delete"""


class ThreadCreate(Channel):
    """Thread Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-create"""

    newly_created: Missing[bool] = UNSET
    thread_member: Missing[ThreadMember] = UNSET


class ThreadUpdate(Channel):
    """Thread Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-update"""


class ThreadDelete(BaseModel):
    """Thread Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-delete"""

    id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    type: ChannelType


class ThreadListSync(BaseModel):
    """Thread List Sync Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-list-sync
    """

    guild_id: Snowflake
    channel_ids: Missing[list[Snowflake]] = UNSET
    threads: list[Channel]
    members: list[ThreadMember]


class ThreadMemberUpdate(ThreadMember):
    """Thread Member Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-member-update
    """

    guild_id: Snowflake


class ThreadMembersUpdate(BaseModel):
    """Thread Members Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-members-update
    """

    id: Snowflake
    guild_id: Snowflake
    member_count: int
    added_members: Missing[list[ThreadMember]] = UNSET
    removed_member_ids: Missing[list[Snowflake]] = UNSET


class ChannelPinsUpdate(BaseModel):
    """Channel Pins Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-pins-update"""

    guild_id: Missing[Snowflake] = UNSET
    channel_id: Snowflake
    last_pin_timestamp: Missing[datetime.datetime | None] = UNSET


__all__ = [
    "ChannelCreate",
    "ChannelDelete",
    "ChannelPinsUpdate",
    "ChannelUpdate",
    "ThreadCreate",
    "ThreadDelete",
    "ThreadListSync",
    "ThreadMemberUpdate",
    "ThreadMembersUpdate",
    "ThreadUpdate",
]
