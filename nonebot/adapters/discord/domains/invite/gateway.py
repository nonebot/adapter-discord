"""Canonical invite.gateway models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Application, User

from .._model_support import (
    UNSET,
    BaseModel,
    InviteTargetType,
    Missing,
    Snowflake,
    datetime,
)


class InviteCreate(BaseModel):
    """Invite Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#invite-create"""

    channel_id: Snowflake
    code: str
    created_at: datetime.datetime
    guild_id: Missing[Snowflake] = UNSET
    inviter: Missing["User"] = UNSET
    max_age: int
    max_uses: int
    target_type: Missing[InviteTargetType] = UNSET
    target_user: Missing["User"] = UNSET
    target_application: Missing["Application"] = UNSET  # partial application object
    temporary: bool
    uses: int


class InviteDelete(BaseModel):
    """Invite Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#invite-delete"""

    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    code: str


__all__ = ["InviteCreate", "InviteDelete"]
