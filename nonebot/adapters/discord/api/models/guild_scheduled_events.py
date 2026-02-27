from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ..types import (
    UNSET,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventStatus,
    Missing,
    MissingOrNullable,
)

if TYPE_CHECKING:
    from ..model import GuildMember, RecurrenceRule, User


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
