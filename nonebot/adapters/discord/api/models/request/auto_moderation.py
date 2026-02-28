from __future__ import annotations

from pydantic import BaseModel

from ..common.auto_moderation import AutoModerationAction, TriggerMetadata
from ..common.snowflake import Snowflake
from ...types import AutoModerationRuleEventType, TriggerType


class CreateAndModifyAutoModerationRuleParams(BaseModel):
    name: str | None = None
    event_type: AutoModerationRuleEventType | None = None
    trigger_type: TriggerType | None = None
    trigger_metadata: TriggerMetadata | None = None
    actions: list[AutoModerationAction] | None = None
    enabled: bool | None = None
    exempt_roles: list[Snowflake] | None = None
    exempt_channels: list[Snowflake] | None = None


__all__ = ["CreateAndModifyAutoModerationRuleParams"]
