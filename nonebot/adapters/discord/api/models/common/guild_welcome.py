from __future__ import annotations

from pydantic import BaseModel

from .snowflake import Snowflake


class WelcomeScreen(BaseModel):
    description: str | None = None
    welcome_channels: list[WelcomeScreenChannel]


class WelcomeScreenChannel(BaseModel):
    channel_id: Snowflake
    description: str
    emoji_id: Snowflake | None = None
    emoji_name: str | None = None
