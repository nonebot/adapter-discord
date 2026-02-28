from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from .interactions.application_commands import ApplicationCommand
from .snowflake import Snowflake
from ..types import UNSET, AuditLogEventType, Missing

if TYPE_CHECKING:
    from ..model import (
        AutoModerationRule,
        Channel,
        GuildScheduledEvent,
        Integration,
        User,
        Webhook,
    )


# Audit Log
# see https://discord.com/developers/docs/resources/audit-log
class AuditLog(BaseModel):
    """Audit Log.

    see https://discord.com/developers/docs/resources/audit-log#audit-log-object"""

    application_commands: list[ApplicationCommand]
    """List of application commands referenced in the audit log"""
    audit_log_entries: list[AuditLogEntry]
    """List of audit log entries, sorted from most to least recent"""
    auto_moderation_rules: list[AutoModerationRule]
    """List of auto moderation rules referenced in the audit log"""
    guild_scheduled_events: list[GuildScheduledEvent]
    """List of guild scheduled events referenced in the audit log"""
    integrations: list[Integration]  # partial integration object
    """List of partial integration objects"""
    threads: list[Channel]  # thread-specific channel objects
    """List of threads referenced in the audit log"""
    users: list[User]
    """List of users referenced in the audit log"""
    webhooks: list[Webhook]
    """List of webhooks referenced in the audit log"""


class AuditLogEntry(BaseModel):
    """Audit Log Entry

    see https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object
    """

    target_id: str | None = None
    """ID of the affected entity (webhook, user, role, etc.)"""
    changes: Missing[list[AuditLogChange]] = UNSET
    """Changes made to the target_id"""
    user_id: Snowflake | None = None
    """User or app that made the changes"""
    id: Snowflake
    """ID of the entry"""
    action_type: AuditLogEventType
    """Type of action that occurred"""
    options: Missing[OptionalAuditEntryInfo] = UNSET
    """Additional info for certain event types"""
    reason: Missing[str] = UNSET
    """Reason for the change (1-512 characters)"""


class OptionalAuditEntryInfo(BaseModel):
    """Optional Audit Entry Info

    see https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-optional-audit-entry-info
    """

    application_id: Missing[Snowflake] = UNSET
    """ID of the app whose permissions were targeted"""
    auto_moderation_rule_name: Missing[str] = UNSET
    """Name of the Auto Moderation rule that was triggered"""
    auto_moderation_rule_trigger_type: Missing[str] = UNSET
    """Trigger type of the Auto Moderation rule that was triggered"""
    channel_id: Missing[Snowflake] = UNSET
    """Channel in which the entities were targeted"""
    count: Missing[str] = UNSET
    """Number of entities that were targeted"""
    delete_member_days: Missing[str] = UNSET
    """Number of days after which inactive members were kicked"""
    id: Missing[Snowflake] = UNSET
    """ID of the overwritten entity"""
    members_removed: Missing[str] = UNSET
    """Number of members removed by the prune"""
    message_id: Missing[Snowflake] = UNSET
    """ID of the message that was targeted"""
    role_name: Missing[str] = UNSET
    """Name of the role if type is "0" (not present if type is "1")"""
    type: Missing[str] = UNSET
    """Type of overwritten entity - role ("0") or member ("1")"""
    integration_type: Missing[str] = UNSET
    """The type of integration which performed the action"""


class AuditLogChange(BaseModel):
    """Many audit log events include a changes array in their entry object.
    The structure for the individual changes varies based on the event type
    and its changed objects, so apps shouldn't depend on a single pattern
    of handling audit log events.

    see https://discord.com/developers/docs/resources/audit-log#audit-log-change-object
    """

    new_value: Missing[Any] = UNSET
    """New value of the key"""
    old_value: Missing[Any] = UNSET
    """Old value of the key"""
    key: str
    """Name of the changed entity, with a few exceptions"""


class AuditLogChangeException(BaseModel):
    """Audit Log Change Exception.

    see https://discord.com/developers/docs/resources/audit-log#audit-log-change-object-audit-log-change-exceptions
    """
