from __future__ import annotations

import datetime

from pydantic import BaseModel

from ..common.guild_scheduled_events import (
    GuildScheduledEvent,
    GuildScheduledEventEntityMetadata,
    GuildScheduledEventRecurrenceRuleN_WeekdayStructure,
    GuildScheduledEventUser,
    RecurrenceRule,
)
from ..common.snowflake import Snowflake
from ...types import (
    UNSET,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventStatus,
    Missing,
    MissingOrNullable,
)


class CreateGuildScheduledEventParams(BaseModel):
    channel_id: Snowflake | None = None
    entity_metadata: GuildScheduledEventEntityMetadata | None = None
    name: str
    privacy_level: GuildScheduledEventPrivacyLevel
    scheduled_start_time: datetime.datetime
    scheduled_end_time: datetime.datetime | None = None
    description: str | None = None
    entity_type: GuildScheduledEventEntityType
    image: str | None = None
    recurrence_rule: RecurrenceRule | None = None


class ModifyGuildScheduledEventParams(BaseModel):
    channel_id: MissingOrNullable[Snowflake] = UNSET
    entity_metadata: MissingOrNullable[GuildScheduledEventEntityMetadata] = UNSET
    name: Missing[str] = UNSET
    privacy_level: Missing[GuildScheduledEventPrivacyLevel] = UNSET
    scheduled_start_time: Missing[datetime.datetime] = UNSET
    scheduled_end_time: Missing[datetime.datetime] = UNSET
    description: MissingOrNullable[str] = UNSET
    entity_type: Missing[GuildScheduledEventEntityType] = UNSET
    status: Missing[GuildScheduledEventStatus] = UNSET
    image: Missing[str] = UNSET
    recurrence_rule: MissingOrNullable[RecurrenceRule] = UNSET


__all__ = [
    "CreateGuildScheduledEventParams",
    "GuildScheduledEvent",
    "GuildScheduledEventEntityMetadata",
    "GuildScheduledEventRecurrenceRuleN_WeekdayStructure",
    "GuildScheduledEventUser",
    "ModifyGuildScheduledEventParams",
    "RecurrenceRule",
]
