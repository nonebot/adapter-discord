"""Canonical emoji.read models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import User

from .._model_support import UNSET, BaseModel, Missing, Snowflake


class Emoji(BaseModel):
    """Emoji Object

    see https://discord.com/developers/docs/resources/emoji#emoji-object"""

    id: Snowflake | None = None
    """emoji id"""
    name: str | None = None
    """emoji name(can be null only in reaction emoji objects)"""
    roles: Missing[list[Snowflake]] = UNSET
    """roles allowed to use this emoji"""
    user: Missing["User"] = UNSET
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

    see https://discord.com/developers/docs/resources/emoji#list-application-emojis"""

    items: list[Emoji]


__all__ = ["ApplicationEmojis", "Emoji"]
