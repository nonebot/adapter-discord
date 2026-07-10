"""Canonical moderation.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import (
        ApplicationCommand,
        Channel,
        GuildScheduledEvent,
        Integration,
        User,
        Webhook,
    )

from .._model_support import (
    UNSET,
    Any,
    AuditLogEventType,
    AutoModerationActionType,
    AutoModerationRuleEventType,
    BaseModel,
    KeywordPresetType,
    Missing,
    Snowflake,
    TriggerType,
)


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


class AutoModerationRule(BaseModel):
    """Auto moderation rule.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object
    """

    id: Snowflake
    """the id of this rule"""
    guild_id: Snowflake
    """the id of the guild which this rule belongs to"""
    name: str
    """the rule name"""
    creator_id: Snowflake
    """	the user which first created this rule"""
    event_type: AutoModerationRuleEventType
    """the rule event type"""
    trigger_type: TriggerType
    """the rule trigger type"""
    trigger_metadata: TriggerMetadata
    """the rule trigger metadata"""
    actions: list[AutoModerationAction]
    """the actions which will execute when the rule is triggered"""
    enabled: bool
    """whether the rule is enabled"""
    exempt_roles: list[Snowflake]
    """the role ids that should not be affected by the rule (Maximum of 20)"""
    exempt_channels: list[Snowflake]
    """the channel ids that should not be affected by the rule (Maximum of 50)"""


class TriggerMetadata(BaseModel):
    """Additional data used to determine whether a rule should be triggered.
    Different fields are relevant based on the value of trigger_type.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-trigger-metadata
    """

    keyword_filter: Missing[list[str]] = UNSET
    """substrings which will be searched for in content (Maximum of 1000)"""
    regex_patterns: Missing[list[str]] = UNSET
    """regular expression patterns which will be matched
    against content (Maximum of 10)"""
    presets: Missing[list[KeywordPresetType]] = UNSET
    """the internally pre-defined wordsets which will be searched for in content"""
    allow_list: Missing[list[str]] = UNSET
    """substrings which should not trigger the rule (Maximum of 100 or 1000)"""
    mention_total_limit: Missing[int] = UNSET
    """total number of unique role and user mentions allowed
    per message (Maximum of 50)"""
    mention_raid_protection_enabled: Missing[bool] = UNSET
    """whether to automatically detect mention raids"""


class AutoModerationAction(BaseModel):
    """Auto moderation action.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object
    """

    type: AutoModerationActionType
    """the type of action"""
    metadata: Missing[AutoModerationActionMetadata] = UNSET
    """additional metadata needed during execution for this specific action type"""


class AutoModerationActionMetadata(BaseModel):
    """Auto moderation action metadata.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-action-metadata
    """

    channel_id: Missing[Snowflake] = UNSET
    """channel to which user content should be logged"""
    duration_seconds: Missing[int] = UNSET
    """	timeout duration in seconds"""
    custom_message: Missing[str] = UNSET
    """additional explanation that will be shown to members
    whenever their message is blocked"""


class BulkBan(BaseModel):
    """bulk ban response

    see https://discord.com/developers/docs/resources/guild#bulk-guild-ban-bulk-ban-response
    """

    banned_users: list[Snowflake]
    """list of user ids, that were successfully banned"""
    failed_users: list[Snowflake]
    """list of user ids, that were not banned"""


__all__ = [
    "AuditLog",
    "AuditLogChange",
    "AuditLogChangeException",
    "AuditLogEntry",
    "AutoModerationAction",
    "AutoModerationActionMetadata",
    "AutoModerationRule",
    "BulkBan",
    "OptionalAuditEntryInfo",
    "TriggerMetadata",
]
