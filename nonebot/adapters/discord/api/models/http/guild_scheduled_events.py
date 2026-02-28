from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..common.snowflake import Snowflake
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
    from ..common.user import User


class RecurrenceRule(BaseModel):
    """Discord's recurrence rule is a subset of the behaviors defined
    in the iCalendar RFC and implemented by python's dateutil rrule

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object
    """

    start: datetime.datetime
    """Starting time of the recurrence interval"""

    end: datetime.datetime | None = None
    """Ending time of the recurrence interval"""

    frequency: GuildScheduledEventRecurrenceRuleFrequency
    """How often the event occurs"""

    interval: int
    """The spacing between the events, defined by frequency. For example,
    frecency of WEEKLY and an interval of 2 would be "every-other week"""

    by_weekday: list[GuildScheduledEventRecurrenceRuleWeekday] | None = None
    """Set of specific days within a week for the event to recur on"""

    by_n_weekday: list[GuildScheduledEventRecurrenceRuleN_WeekdayStructure] | None = (
        None
    )
    """List of specific days within a specific week (1-5) to recur on"""

    by_month: list[GuildScheduledEventRecurrenceRuleMonth] | None = None
    """Set of specific months to recur on"""

    by_month_day: int | None = None
    """Set of specific dates within a month to recur on"""

    by_year_day: int | None = None
    """Set of days within a year to recur on (1-364)"""

    count: int | None = None
    """The total amount of times that the event is allowed to recur before stopping"""


class GuildScheduledEventRecurrenceRuleN_WeekdayStructure(BaseModel):  # noqa: N801
    """Guild Scheduled Event Recurrence Rule - N_Weekday Structure

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object-guild-scheduled-event-recurrence-rule-nweekday-structure
    """

    n: int
    """The week to reoccur on. 1 - 5"""

    day: GuildScheduledEventRecurrenceRuleWeekday
    """The day within the week to reoccur on"""


class GuildScheduledEvent(BaseModel):
    """Guild Scheduled Event

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object
    """

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
    """Guild Scheduled Event Entity Metadata

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: Missing[str] = UNSET


class GuildScheduledEventUser(BaseModel):
    """Guild Scheduled Event User

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-user-object
    """

    guild_scheduled_event_id: Snowflake
    user: User
    member: Missing[GuildMember] = UNSET


class CreateGuildScheduledEventParams(BaseModel):
    """Create Guild Scheduled Event Params

    see https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event-json-params
    """

    channel_id: Snowflake | None = None
    entity_metadata: GuildScheduledEventEntityMetadata | None = None
    name: str
    privacy_level: GuildScheduledEventPrivacyLevel
    scheduled_start_time: datetime.datetime  # ISO8601 timestamp
    scheduled_end_time: datetime.datetime | None = None  # ISO8601 timestamp
    description: str | None = None
    entity_type: GuildScheduledEventEntityType
    image: str | None = None
    recurrence_rule: RecurrenceRule | None = None


class ModifyGuildScheduledEventParams(BaseModel):
    """Modify Guild Scheduled Event Params

    see https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event-json-params
    """

    channel_id: MissingOrNullable[Snowflake] = UNSET
    entity_metadata: MissingOrNullable[GuildScheduledEventEntityMetadata] = UNSET
    name: Missing[str] = UNSET
    privacy_level: Missing[GuildScheduledEventPrivacyLevel] = UNSET
    scheduled_start_time: Missing[datetime.datetime] = UNSET  # ISO8601 timestamp
    scheduled_end_time: Missing[datetime.datetime] = UNSET  # ISO8601 timestamp
    description: MissingOrNullable[str] = UNSET
    entity_type: Missing[GuildScheduledEventEntityType] = UNSET
    status: Missing[GuildScheduledEventStatus] = UNSET
    image: Missing[str] = UNSET
    recurrence_rule: MissingOrNullable[RecurrenceRule] = UNSET
