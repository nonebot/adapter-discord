"""Canonical voice.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import GuildMember

from .._model_support import (
    UNSET,
    BaseModel,
    Field,
    Missing,
    Snowflake,
    StagePrivacyLevel,
    datetime,
)


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


class VoiceState(BaseModel):
    """Voice State

    see https://discord.com/developers/docs/resources/voice#voice-state-object"""

    guild_id: Missing[Snowflake] = UNSET
    channel_id: Snowflake | None = Field(...)
    user_id: Snowflake
    member: Missing[GuildMember] = UNSET
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: Missing[bool] = UNSET
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: datetime.datetime | None = Field(...)


class VoiceRegion(BaseModel):
    """Voice Region

    see https://discord.com/developers/docs/resources/voice#voice-region-object"""

    id: str
    name: str
    optimal: bool
    deprecated: bool
    custom: bool


__all__ = ["StageInstance", "VoiceRegion", "VoiceState"]
