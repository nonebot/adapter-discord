from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ...types import UNSET, Missing, MissingOrNullable, WebhookType

if TYPE_CHECKING:
    from .user import User


class SourceGuild(BaseModel):
    id: Snowflake
    name: str
    icon: str | None = None


class SourceChannel(BaseModel):
    id: Snowflake
    name: str


class Webhook(BaseModel):
    id: Snowflake
    type: WebhookType
    guild_id: MissingOrNullable[Snowflake] = UNSET
    channel_id: Snowflake | None = Field(...)
    user: Missing[User] = UNSET
    name: str | None = Field(...)
    avatar: str | None = Field(...)
    token: Missing[str] = UNSET
    application_id: Snowflake | None = Field(...)
    source_guild: Missing[SourceGuild] = UNSET
    source_channel: Missing[SourceChannel] = UNSET
    url: Missing[str] = UNSET


__all__ = ["SourceChannel", "SourceGuild", "Webhook"]
