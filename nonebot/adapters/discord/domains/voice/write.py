"""Canonical voice.write models."""

from typing_extensions import Required, TypedDict

from .types import StagePrivacyLevel
from .._model_support import Snowflake, datetime
from ...protocol import SnowflakeType


class ModifyCurrentUserVoiceStateParams(TypedDict, total=False):
    """Modify Current User Voice State Params.

    see https://discord.com/developers/docs/resources/voice#modify-current-user-voice-state
    """

    channel_id: Snowflake
    suppress: bool
    request_to_speak_timestamp: datetime.datetime | None


class ModifyUserVoiceStateParams(TypedDict, total=False):
    """Parameters for ``_api_modify_user_voice_state``."""

    channel_id: "SnowflakeType"
    suppress: bool


class CreateStageInstanceParams(TypedDict, total=False):
    """Parameters for ``_api_create_stage_instance``."""

    channel_id: Required["SnowflakeType"]
    topic: Required[str]
    privacy_level: "StagePrivacyLevel"
    send_start_notification: bool
    guild_scheduled_event_id: "SnowflakeType"


class ModifyStageInstanceParams(TypedDict, total=False):
    """Parameters for ``_api_modify_stage_instance``."""

    topic: str
    privacy_level: "StagePrivacyLevel"


__all__ = [
    "CreateStageInstanceParams",
    "ModifyCurrentUserVoiceStateParams",
    "ModifyStageInstanceParams",
    "ModifyUserVoiceStateParams",
]
