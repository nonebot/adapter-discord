from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ...types import UNSET, GuildMemberFlags, Missing, MissingOrNullable

if TYPE_CHECKING:
    from .user import AvatarDecorationData, User


class GuildMember(BaseModel):
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
