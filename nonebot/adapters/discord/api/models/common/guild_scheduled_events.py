from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ...types import (
    UNSET,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventRecurrenceRuleFrequency,
    GuildScheduledEventRecurrenceRuleMonth,
    GuildScheduledEventRecurrenceRuleWeekday,
    GuildScheduledEventStatus,
    Missing,
    MissingOrNullable,
)

if TYPE_CHECKING:
    from .guild_members import GuildMember
    from .user import User


class RecurrenceRule(BaseModel):
    start: datetime.datetime
    end: datetime.datetime | None = None
    frequency: GuildScheduledEventRecurrenceRuleFrequency
    interval: int
    by_weekday: list[GuildScheduledEventRecurrenceRuleWeekday] | None = None
    by_n_weekday: list[GuildScheduledEventRecurrenceRuleN_WeekdayStructure] | None = (
        None
    )
    by_month: list[GuildScheduledEventRecurrenceRuleMonth] | None = None
    by_month_day: int | None = None
    by_year_day: int | None = None
    count: int | None = None


class GuildScheduledEventRecurrenceRuleN_WeekdayStructure(BaseModel):  # noqa: N801
    n: int
    day: GuildScheduledEventRecurrenceRuleWeekday


class GuildScheduledEvent(BaseModel):
    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake | None = None
    creator_id: MissingOrNullable[Snowflake] = UNSET
    name: str
    description: MissingOrNullable[str] = UNSET
    scheduled_start_time: datetime.datetime
    scheduled_end_time: datetime.datetime | None = None
    privacy_level: GuildScheduledEventPrivacyLevel
    status: GuildScheduledEventStatus
    entity_type: GuildScheduledEventEntityType
    entity_id: Snowflake | None = None
    entity_metadata: GuildScheduledEventEntityMetadata | None = None
    creator: Missing[User] = UNSET
    user_count: Missing[int] = UNSET
    image: MissingOrNullable[str] = UNSET
    recurrence_rule: RecurrenceRule | None = None


class GuildScheduledEventEntityMetadata(BaseModel):
    location: Missing[str] = UNSET


class GuildScheduledEventUser(BaseModel):
    guild_scheduled_event_id: Snowflake
    user: User
    member: Missing[GuildMember] = UNSET
