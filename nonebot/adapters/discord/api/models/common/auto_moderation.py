from __future__ import annotations

from pydantic import BaseModel

from .snowflake import Snowflake
from ...types import (
    UNSET,
    AutoModerationActionType,
    AutoModerationRuleEventType,
    KeywordPresetType,
    Missing,
    TriggerType,
)


class AutoModerationRule(BaseModel):
    id: Snowflake
    guild_id: Snowflake
    name: str
    creator_id: Snowflake
    event_type: AutoModerationRuleEventType
    trigger_type: TriggerType
    trigger_metadata: TriggerMetadata
    actions: list[AutoModerationAction]
    enabled: bool
    exempt_roles: list[Snowflake]
    exempt_channels: list[Snowflake]


class TriggerMetadata(BaseModel):
    keyword_filter: Missing[list[str]] = UNSET
    regex_patterns: Missing[list[str]] = UNSET
    presets: Missing[list[KeywordPresetType]] = UNSET
    allow_list: Missing[list[str]] = UNSET
    mention_total_limit: Missing[int] = UNSET
    mention_raid_protection_enabled: Missing[bool] = UNSET


class AutoModerationAction(BaseModel):
    type: AutoModerationActionType
    metadata: Missing[AutoModerationActionMetadata] = UNSET


class AutoModerationActionMetadata(BaseModel):
    channel_id: Missing[Snowflake] = UNSET
    duration_seconds: Missing[int] = UNSET
    custom_message: Missing[str] = UNSET
