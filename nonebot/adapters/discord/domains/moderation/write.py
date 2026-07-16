"""Canonical moderation.write models."""

from typing import TYPE_CHECKING
from typing_extensions import Required

from .._model_support import OutboundTypedDict

if TYPE_CHECKING:
    from ..models import AutoModerationAction, TriggerMetadata

from .._model_support import AutoModerationRuleEventType, TriggerType
from ...protocol import SnowflakeType


class CreateAutoModerationRuleParams(OutboundTypedDict, total=False):
    """Create Auto Moderation Rule Params.

    see https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
    """

    name: Required[str]
    event_type: Required[AutoModerationRuleEventType]
    trigger_type: Required[TriggerType]
    trigger_metadata: "TriggerMetadata"
    actions: Required["list[AutoModerationAction]"]
    enabled: bool
    exempt_roles: list[SnowflakeType]
    exempt_channels: list[SnowflakeType]


class ModifyAutoModerationRuleParams(OutboundTypedDict, total=False):
    """Modify Auto Moderation Rule Params.

    see https://discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule
    """

    name: str
    event_type: AutoModerationRuleEventType
    trigger_metadata: "TriggerMetadata"
    actions: "list[AutoModerationAction]"
    enabled: bool
    exempt_roles: list[SnowflakeType]
    exempt_channels: list[SnowflakeType]


__all__ = ["CreateAutoModerationRuleParams", "ModifyAutoModerationRuleParams"]
