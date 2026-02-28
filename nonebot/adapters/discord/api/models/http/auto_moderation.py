from __future__ import annotations

from pydantic import BaseModel, Field

from ..common.snowflake import Snowflake
from ...types import (
    UNSET,
    AutoModerationActionType,
    AutoModerationRuleEventType,
    KeywordPresetType,
    Missing,
    TriggerType,
)


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
    """\tthe user which first created this rule"""
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
    """\ttimeout duration in seconds"""
    custom_message: Missing[str] = UNSET
    """additional explanation that will be shown to members
    whenever their message is blocked"""


class CreateAndModifyAutoModerationRuleParams(BaseModel):
    """Create and modify Auto Moderation Rule Params.

    see https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
    """

    name: str | None = None
    event_type: AutoModerationRuleEventType | None = None
    trigger_type: TriggerType | None = None
    trigger_metadata: TriggerMetadata | None = None
    actions: list[AutoModerationAction] | None = None
    enabled: bool | None = None
    exempt_roles: list[Snowflake] | None = None
    exempt_channels: list[Snowflake] | None = None


class AutoModerationRuleCreate(AutoModerationRule):
    pass


class AutoModerationRuleUpdate(AutoModerationRule):
    pass


class AutoModerationRuleDelete(AutoModerationRule):
    pass


class AutoModerationActionExecution(BaseModel):
    guild_id: Snowflake
    action: AutoModerationAction
    rule_id: Snowflake
    rule_trigger_type: TriggerType
    user_id: Snowflake
    channel_id: Missing[Snowflake] = UNSET
    message_id: Missing[Snowflake] = UNSET
    alert_system_message_id: Missing[Snowflake] = UNSET
    content: str
    matched_keyword: str | None = Field(...)
    matched_content: str | None = Field(...)
