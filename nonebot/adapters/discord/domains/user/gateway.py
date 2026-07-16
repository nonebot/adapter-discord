"""Canonical user.gateway models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Activity, AvatarDecorationData, ClientStatus

from .._model_support import (
    UNSET,
    BaseModel,
    Missing,
    MissingOrNullable,
    PremiumType,
    PresenceStatus,
    Snowflake,
    UserFlags,
)
from ..user.read import User


class PresenceUpdateUser(BaseModel):
    """Presence Update User Fields

    see https://discord.com/developers/docs/topics/gateway-events#presence-update"""

    id: Snowflake
    username: Missing[str] = UNSET
    discriminator: Missing[str] = UNSET
    global_name: MissingOrNullable[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
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
    avatar_decoration_data: MissingOrNullable["AvatarDecorationData"] = UNSET


class PresenceUpdate(BaseModel):
    """Presence Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#presence-update
    """

    user: PresenceUpdateUser
    guild_id: Snowflake
    status: PresenceStatus
    activities: list["Activity"]
    client_status: "ClientStatus"


class UserUpdate(User):
    """User Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#user-update"""


__all__ = ["PresenceUpdate", "PresenceUpdateUser", "UserUpdate"]
