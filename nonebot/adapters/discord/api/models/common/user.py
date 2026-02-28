from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ...types import (
    UNSET,
    ConnectionServiceType,
    Missing,
    MissingOrNullable,
    PremiumType,
    UserFlags,
    VisibilityType,
)

if TYPE_CHECKING:
    from ..http.integrations import Integration


class User(BaseModel):
    """User

    see https://discord.com/developers/docs/resources/user#user-object
    """

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

    see https://discord.com/developers/docs/resources/user#connection-object
    """

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


class ApplicationRoleConnection(BaseModel):
    """Application Role Connection

    see https://discord.com/developers/docs/resources/user#application-role-connection-object
    """

    platform_name: str | None = Field(...)
    platform_username: str | None = Field(...)
    metadata: dict  # object


class ModifyCurrentUserParams(BaseModel):
    username: Missing[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET
