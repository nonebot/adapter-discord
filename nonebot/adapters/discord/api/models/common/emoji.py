from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ...types import UNSET, Missing

if TYPE_CHECKING:
    from .user import User


class Emoji(BaseModel):
    id: Snowflake | None = None
    name: str | None = None
    roles: Missing[list[Snowflake]] = UNSET
    user: Missing[User] = UNSET
    require_colons: Missing[bool] = UNSET
    managed: Missing[bool] = UNSET
    animated: Missing[bool] = UNSET
    available: Missing[bool] = UNSET


class ApplicationEmojis(BaseModel):
    items: list[Emoji]
