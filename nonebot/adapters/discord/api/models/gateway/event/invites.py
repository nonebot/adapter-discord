from __future__ import annotations

import datetime
import warnings

from pydantic import BaseModel

from ...common.application import Application
from ...common.snowflake import Snowflake
from ...common.user import User
from ....types import UNSET, InviteTargetType, Missing


class InviteCreate(BaseModel):
    channel_id: Snowflake
    code: str
    created_at: datetime.datetime
    guild_id: Missing[Snowflake] = UNSET
    inviter: Missing[User] = UNSET
    max_age: int
    max_uses: int
    target_type: Missing[InviteTargetType] = UNSET
    target_user: Missing[User] = UNSET
    target_application: Missing[Application] = UNSET
    temporary: bool
    uses: int


class InviteDelete(BaseModel):
    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    code: str

    def __init__(self, **data) -> None:  # noqa: ANN003
        super().__init__(**data)
        warnings.warn(
            "InviteStageInstance is deprecated by Discord",
            DeprecationWarning,
            stacklevel=2,
        )


__all__ = ["InviteCreate", "InviteDelete"]
