from __future__ import annotations

import datetime

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ..http.channels import Channel, ThreadMember
from ...types import UNSET, ChannelType, Missing, MissingOrNullable


class ChannelCreate(Channel):
    pass


class ChannelUpdate(Channel):
    pass


class ChannelDelete(Channel):
    pass


class ThreadCreate(Channel):
    newly_created: Missing[bool] = UNSET
    thread_member: Missing[ThreadMember] = UNSET


class ThreadUpdate(Channel):
    pass


class ThreadDelete(BaseModel):
    id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    type: ChannelType


class ThreadListSync(BaseModel):
    guild_id: Snowflake
    channel_ids: Missing[list[Snowflake]] = UNSET
    threads: list[Channel]
    members: list[ThreadMember]


class ThreadMemberUpdate(ThreadMember):
    guild_id: Snowflake


class ThreadMembersUpdate(BaseModel):
    id: Snowflake
    guild_id: Snowflake
    member_count: int
    added_members: Missing[list[ThreadMember]] = UNSET
    removed_member_ids: Missing[list[Snowflake]] = UNSET


class ChannelPinsUpdate(BaseModel):
    guild_id: Missing[Snowflake] = UNSET
    channel_id: Snowflake
    last_pin_timestamp: Missing[datetime.datetime | None] = UNSET
