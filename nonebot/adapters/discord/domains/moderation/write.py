"""Canonical moderation.write models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import AutoModerationAction, TriggerMetadata

from .._model_support import (
    AutoModerationRuleEventType,
    BaseModel,
    Snowflake,
    TriggerType,
)


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


__all__ = ["CreateAndModifyAutoModerationRuleParams"]
