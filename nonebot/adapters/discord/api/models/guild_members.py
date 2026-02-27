from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ..types import UNSET, GuildMemberFlags, Missing, MissingOrNullable

if TYPE_CHECKING:
    from ..model import AvatarDecorationData, User


class GuildMember(BaseModel):
    """Guild Member

    see https://discord.com/developers/docs/resources/guild#guild-member-object"""

    user: Missing[User] = UNSET
    nick: MissingOrNullable[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    roles: list[Snowflake]
    joined_at: datetime.datetime
    premium_since: MissingOrNullable[datetime.datetime] = UNSET
    deaf: Missing[bool] = UNSET
    mute: Missing[bool] = UNSET
    flags: GuildMemberFlags
    pending: Missing[bool] = UNSET
    permissions: Missing[str] = UNSET
    communication_disabled_until: MissingOrNullable[datetime.datetime] = UNSET
    avatar_decoration_data: MissingOrNullable[AvatarDecorationData] = UNSET


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
