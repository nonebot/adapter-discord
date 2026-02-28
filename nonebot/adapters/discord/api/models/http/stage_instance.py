from __future__ import annotations

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ...types import StagePrivacyLevel


class StageInstance(BaseModel):
    """Stage Instance

    see https://discord.com/developers/docs/resources/stage-instance#stage-instance-object
    """

    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: StagePrivacyLevel
    discoverable_disabled: bool
    guild_scheduled_event_id: Snowflake | None = None
