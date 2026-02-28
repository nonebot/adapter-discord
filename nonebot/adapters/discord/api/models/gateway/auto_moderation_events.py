from __future__ import annotations

from pydantic import BaseModel, Field

from ..common.snowflake import Snowflake
from ..http.auto_moderation import AutoModerationAction, AutoModerationRule
from ...types import UNSET, Missing, TriggerType


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
