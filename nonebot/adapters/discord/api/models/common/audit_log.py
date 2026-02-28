from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ..interactions.application_commands import ApplicationCommand
from ...types import UNSET, AuditLogEventType, Missing

if TYPE_CHECKING:
    from .auto_moderation import AutoModerationRule
    from .channels import Channel
    from .guild_scheduled_events import GuildScheduledEvent
    from .integrations import Integration
    from .user import User
    from ..http.webhooks import Webhook


class AuditLog(BaseModel):
    application_commands: list[ApplicationCommand]
    audit_log_entries: list[AuditLogEntry]
    auto_moderation_rules: list[AutoModerationRule]
    guild_scheduled_events: list[GuildScheduledEvent]
    integrations: list[Integration]
    threads: list[Channel]
    users: list[User]
    webhooks: list[Webhook]


class AuditLogEntry(BaseModel):
    target_id: str | None = None
    changes: Missing[list[AuditLogChange]] = UNSET
    user_id: Snowflake | None = None
    id: Snowflake
    action_type: AuditLogEventType
    options: Missing[OptionalAuditEntryInfo] = UNSET
    reason: Missing[str] = UNSET


class OptionalAuditEntryInfo(BaseModel):
    application_id: Missing[Snowflake] = UNSET
    auto_moderation_rule_name: Missing[str] = UNSET
    auto_moderation_rule_trigger_type: Missing[str] = UNSET
    channel_id: Missing[Snowflake] = UNSET
    count: Missing[str] = UNSET
    delete_member_days: Missing[str] = UNSET
    id: Missing[Snowflake] = UNSET
    members_removed: Missing[str] = UNSET
    message_id: Missing[Snowflake] = UNSET
    role_name: Missing[str] = UNSET
    type: Missing[str] = UNSET
    integration_type: Missing[str] = UNSET


class AuditLogChange(BaseModel):
    new_value: Missing[object] = UNSET
    old_value: Missing[object] = UNSET
    key: str


class AuditLogChangeException(BaseModel):
    pass
