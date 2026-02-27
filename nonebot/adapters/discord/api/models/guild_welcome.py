from __future__ import annotations

from pydantic import BaseModel

from .snowflake import Snowflake
from ..types import UNSET, MissingOrNullable


class WelcomeScreen(BaseModel):
    description: str | None = None
    welcome_channels: list[WelcomeScreenChannel]


class WelcomeScreenChannel(BaseModel):
    channel_id: Snowflake
    description: str
    emoji_id: Snowflake | None = None
    emoji_name: str | None = None


class ModifyGuildWelcomeScreenParams(BaseModel):
    enabled: MissingOrNullable[bool] = UNSET
    welcome_channels: MissingOrNullable[list[WelcomeScreenChannel]] = UNSET
    description: MissingOrNullable[str] = UNSET
