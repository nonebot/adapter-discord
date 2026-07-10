"""Canonical voice.gateway models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Emoji

from .._model_support import (
    UNSET,
    AnimationType,
    BaseModel,
    Field,
    Missing,
    MissingOrNullable,
    Snowflake,
    datetime,
)
from ..voice.read import StageInstance, VoiceState


class VoiceStateUpdate(VoiceState):
    """Voice State Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#voice-state-update
    """


class VoiceChannelStatusUpdate(BaseModel):
    """Voice Channel Status Update Event Fields

    This gateway dispatch is observed in production but is not yet fully
    documented on Discord's public Gateway Events page.

    Field shape is based on:
    - https://github.com/discord/discord-api-docs/pull/6398
    - https://github.com/discord/discord-api-docs/pull/6400
    """

    id: Snowflake
    guild_id: Snowflake
    status: str | None = None


class VoiceChannelStartTimeUpdate(BaseModel):
    """Voice Channel Start Time Update Event Fields

    This gateway dispatch is observed in production but is not yet fully
    documented on Discord's public Gateway Events page.

    Field shape is based on observed payloads and community implementations.
    """

    id: Snowflake
    guild_id: Snowflake
    voice_start_time: datetime.datetime | None = None


class VoiceServerUpdate(BaseModel):
    """Voice Server Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#voice-server-update
    """

    token: str
    guild_id: Snowflake
    endpoint: str | None = Field(...)


class StageInstanceCreate(StageInstance):
    """Stage Instance Create Event Fields

    Sent when a Stage instance is created (i.e. the Stage is now "live").
    Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-create
    """


class StageInstanceUpdate(StageInstance):
    """Stage Instance Update Event Fields

    Sent when a Stage instance has been updated. Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-update
    """


class StageInstanceDelete(StageInstance):
    """Stage Instance Delete Event Fields

    Sent when a Stage instance has been deleted (i.e. the Stage has been closed).
    Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-delete
    """


class VoiceChannelEffectSend(BaseModel):
    """Voice Channel Effect Send Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#voice-channel-effect-send-voice-channel-effect-send-event-fields
    """

    channel_id: Snowflake
    guild_id: Snowflake
    user_id: Snowflake
    emoji: MissingOrNullable[Emoji] = UNSET
    animation_type: MissingOrNullable[AnimationType] = UNSET
    animation_id: Missing[int] = UNSET
    sound_id: Missing[Snowflake | int] = UNSET
    sound_volume: Missing[float] = UNSET


__all__ = [
    "StageInstanceCreate",
    "StageInstanceDelete",
    "StageInstanceUpdate",
    "VoiceChannelEffectSend",
    "VoiceChannelStartTimeUpdate",
    "VoiceChannelStatusUpdate",
    "VoiceServerUpdate",
    "VoiceStateUpdate",
]
