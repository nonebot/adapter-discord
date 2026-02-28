from __future__ import annotations

import datetime

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ..common.voice import VoiceRegion, VoiceState
from ...types import UNSET, Missing, MissingOrNullable


class ModifyCurrentUserVoiceStateParams(BaseModel):
    channel_id: Missing[Snowflake] = UNSET
    suppress: Missing[bool] = UNSET
    request_to_speak_timestamp: MissingOrNullable[datetime.datetime] = UNSET


__all__ = [
    "ModifyCurrentUserVoiceStateParams",
    "VoiceRegion",
    "VoiceState",
]
