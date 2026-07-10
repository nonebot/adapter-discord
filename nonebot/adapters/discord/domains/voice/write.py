"""Canonical voice.write models."""

from __future__ import annotations

from .._model_support import (
    UNSET,
    BaseModel,
    Missing,
    MissingOrNullable,
    Snowflake,
    datetime,
)


class ModifyCurrentUserVoiceStateParams(BaseModel):
    """Modify Current User Voice State Params.

    see https://discord.com/developers/docs/resources/voice#modify-current-user-voice-state
    """

    channel_id: Missing[Snowflake] = UNSET
    suppress: Missing[bool] = UNSET
    request_to_speak_timestamp: MissingOrNullable[datetime.datetime] = UNSET


__all__ = ["ModifyCurrentUserVoiceStateParams"]
