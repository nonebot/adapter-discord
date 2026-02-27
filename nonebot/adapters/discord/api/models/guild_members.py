from __future__ import annotations

import datetime

from pydantic import BaseModel

from .snowflake import Snowflake
from ..types import UNSET, GuildMemberFlags, MissingOrNullable


class ModifyGuildMemberParams(BaseModel):
    nick: MissingOrNullable[str] = UNSET
    roles: MissingOrNullable[list[Snowflake]] = UNSET
    mute: MissingOrNullable[bool] = UNSET
    deaf: MissingOrNullable[bool] = UNSET
    channel_id: MissingOrNullable[Snowflake] = UNSET
    communication_disabled_until: MissingOrNullable[datetime.datetime] = UNSET
    flags: MissingOrNullable[GuildMemberFlags] = UNSET


class ModifyCurrentMemberParams(BaseModel):
    nick: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    bio: MissingOrNullable[str] = UNSET
