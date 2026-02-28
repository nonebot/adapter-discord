from __future__ import annotations

from pydantic import BaseModel

from ..common.permissions import RoleColors
from ..common.snowflake import Snowflake
from ...types import UNSET, Missing, MissingOrNullable


class ModifyGuildRoleParams(BaseModel):
    name: MissingOrNullable[str] = UNSET
    permissions: MissingOrNullable[str] = UNSET
    color: MissingOrNullable[int] = UNSET
    colors: Missing[RoleColors] = UNSET
    hoist: MissingOrNullable[bool] = UNSET
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET
    mentionable: MissingOrNullable[bool] = UNSET


class CreateGuildRoleParams(BaseModel):
    name: Missing[str] = UNSET
    permissions: Missing[str] = UNSET
    color: Missing[int] = UNSET
    colors: Missing[RoleColors] = UNSET
    hoist: Missing[bool] = UNSET
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET
    mentionable: Missing[bool] = UNSET


class ModifyGuildRolePositionParams(BaseModel):
    id: Snowflake
    position: MissingOrNullable[int] = UNSET
