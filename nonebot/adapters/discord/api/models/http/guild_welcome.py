from __future__ import annotations

from pydantic import BaseModel

from ..common.guild_welcome import (
    WelcomeScreen,
    WelcomeScreenChannel,
)
from ...types import UNSET, MissingOrNullable


class ModifyGuildWelcomeScreenParams(BaseModel):
    enabled: MissingOrNullable[bool] = UNSET
    welcome_channels: MissingOrNullable[list[WelcomeScreenChannel]] = UNSET
    description: MissingOrNullable[str] = UNSET


__all__ = ["ModifyGuildWelcomeScreenParams", "WelcomeScreen", "WelcomeScreenChannel"]
