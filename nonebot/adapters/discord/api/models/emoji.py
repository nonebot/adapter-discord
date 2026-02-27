from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ..types import UNSET, Missing

if TYPE_CHECKING:
    from ..model import User


class Emoji(BaseModel):
    """Emoji Object

    see https://discord.com/developers/docs/resources/emoji#emoji-object
    """

    id: Snowflake | None = None
    """emoji id"""
    name: str | None = None
    """emoji name(can be null only in reaction emoji objects)"""
    roles: Missing[list[Snowflake]] = UNSET
    """roles allowed to use this emoji"""
    user: Missing[User] = UNSET
    """user that created this emoji"""
    require_colons: Missing[bool] = UNSET
    """whether this emoji must be wrapped in colons"""
    managed: Missing[bool] = UNSET
    """whether this emoji is managed"""
    animated: Missing[bool] = UNSET
    """whether this emoji is animated"""
    available: Missing[bool] = UNSET
    """whether this emoji can be used, may be false due to loss of Server Boosts"""


class ApplicationEmojis(BaseModel):
    """a list of emoji objects for the given application under the items key.

    see https://discord.com/developers/docs/resources/emoji#list-application-emojis
    """

    items: list[Emoji]
