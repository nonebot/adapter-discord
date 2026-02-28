from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ...types import UNSET, IntegrationExpireBehaviors, Missing

if TYPE_CHECKING:
    from .user import User


class IntegrationAccount(BaseModel):
    id: str
    name: str


class IntegrationApplication(BaseModel):
    id: Snowflake
    name: str
    icon: str | None = None
    description: str
    bot: Missing[User] = UNSET


class Integration(BaseModel):
    id: Snowflake
    name: str
    type: str
    enabled: bool
    syncing: Missing[bool] = UNSET
    role_id: Missing[Snowflake] = UNSET
    enable_emoticons: Missing[bool] = UNSET
    expire_behavior: Missing[IntegrationExpireBehaviors] = UNSET
    expire_grace_period: Missing[int] = UNSET
    user: Missing[User] = UNSET
    account: IntegrationAccount
    synced_at: Missing[datetime.datetime] = UNSET
    subscriber_count: Missing[int] = UNSET
    revoked: Missing[bool] = UNSET
    application: Missing[IntegrationApplication] = UNSET
    scopes: Missing[list[str]] = UNSET
