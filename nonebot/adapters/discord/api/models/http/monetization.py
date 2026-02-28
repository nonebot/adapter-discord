from __future__ import annotations

import datetime

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ...types import (
    UNSET,
    EntitlementType,
    Missing,
    MissingOrNullable,
    SKUFlag,
    SKUType,
    SubscriptionStatus,
)


class Entitlement(BaseModel):
    id: Snowflake
    sku_id: Snowflake
    application_id: Snowflake
    user_id: Missing[Snowflake] = UNSET
    type: EntitlementType
    deleted: bool
    starts_at: Missing[datetime.datetime] = UNSET
    ends_at: Missing[datetime.datetime] = UNSET
    guild_id: Missing[Snowflake] = UNSET
    consumed: Missing[bool] = UNSET


class SKU(BaseModel):
    id: Snowflake
    type: SKUType
    application_id: Snowflake
    name: str
    slug: str
    flags: SKUFlag
    dependent_sku_id: MissingOrNullable[Snowflake] = UNSET
    manifest_labels: MissingOrNullable[list[str]] = UNSET
    access_type: Missing[int] = UNSET
    features: Missing[list[str]] = UNSET
    release_date: MissingOrNullable[datetime.datetime] = UNSET
    premium: Missing[bool] = UNSET
    show_age_gate: Missing[bool] = UNSET


class Subscription(BaseModel):
    id: Snowflake
    user_id: Snowflake
    sku_ids: list[Snowflake]
    entitlement_ids: list[Snowflake]
    renewal_sku_ids: MissingOrNullable[list[Snowflake]] = UNSET
    current_period_start: datetime.datetime
    current_period_end: datetime.datetime
    status: SubscriptionStatus
    canceled_at: datetime.datetime | None = None
    country: Missing[str] = UNSET
