"""Canonical user.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Integration

from .._model_support import (
    UNSET,
    BaseModel,
    ConnectionServiceType,
    Field,
    Missing,
    MissingOrNullable,
    PremiumType,
    Snowflake,
    UserFlags,
    VisibilityType,
)


class User(BaseModel):
    """User

    see https://discord.com/developers/docs/resources/user#user-object"""

    id: Snowflake
    username: str
    discriminator: str
    global_name: str | None = None
    avatar: str | None = Field(...)
    bot: Missing[bool] = UNSET
    system: Missing[bool] = UNSET
    mfa_enabled: Missing[bool] = UNSET
    banner: MissingOrNullable[str] = UNSET
    accent_color: MissingOrNullable[int] = UNSET
    locale: Missing[str] = UNSET
    verified: Missing[bool] = UNSET
    email: MissingOrNullable[str] = UNSET
    flags: Missing[int] = UNSET
    premium_type: Missing[PremiumType] = UNSET
    public_flags: Missing[UserFlags] = UNSET
    avatar_decoration_data: MissingOrNullable[AvatarDecorationData] = UNSET


class AvatarDecorationData(BaseModel):
    """Avatar Decoration Data

    see https://discord.com/developers/docs/resources/user#avatar-decoration-data-object
    """

    asset: str
    sku_id: Snowflake


class Connection(BaseModel):
    """Connection

    see https://discord.com/developers/docs/resources/user#connection-object"""

    id: str
    name: str
    type: ConnectionServiceType
    revoked: Missing[bool] = UNSET
    integrations: Missing[list[Integration]] = UNSET  # partial server integrations
    verified: bool
    friend_sync: bool
    show_activity: bool
    two_way_link: bool
    visibility: VisibilityType


__all__ = ["AvatarDecorationData", "Connection", "User"]
