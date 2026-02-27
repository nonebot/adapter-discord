from __future__ import annotations

from pydantic import BaseModel

from .snowflake import Snowflake
from ..types import UNSET, Missing, MissingOrNullable, RoleFlag


class RoleColors(BaseModel):
    primary_color: int
    secondary_color: int | None = None
    tertiary_color: int | None = None


class RoleTags(BaseModel):
    bot_id: Missing[Snowflake] = UNSET
    integration_id: Missing[Snowflake] = UNSET
    premium_subscriber: Missing[None] = UNSET
    subscription_listing_id: Missing[Snowflake] = UNSET
    available_for_purchase: Missing[None] = UNSET
    guild_connections: Missing[None] = UNSET


class Role(BaseModel):
    id: Snowflake
    name: str
    color: int
    colors: Missing[RoleColors] = UNSET
    hoist: bool
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: Missing[RoleTags] = UNSET
    flags: Missing[RoleFlag] = UNSET
