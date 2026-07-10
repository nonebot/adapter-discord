"""Canonical gateway.write models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Activity, PresenceUpdate

from .._model_support import (
    UNSET,
    BaseModel,
    Field,
    Missing,
    Snowflake,
    UpdatePresenceStatusType,
)


class Identify(BaseModel):
    """Identify Payload data

    see https://discord.com/developers/docs/topics/gateway-events#identify"""

    token: str
    properties: IdentifyConnectionProperties
    compress: Missing[bool] = UNSET
    large_threshold: Missing[int] = UNSET
    shard: Missing[list[int]] = UNSET
    presence: Missing[PresenceUpdate] = UNSET
    intents: int


class IdentifyConnectionProperties(BaseModel):
    """Identify Connection Properties

    see https://discord.com/developers/docs/topics/gateway-events#identify-identify-connection-properties
    """

    os: str
    browser: str
    device: str


class Resume(BaseModel):
    """Resume Payload data

    see https://discord.com/developers/docs/topics/gateway-events#resume"""

    token: str
    session_id: str
    seq: int


class RequestGuildMembers(BaseModel):
    """Request Guild Members Payload data

    see https://discord.com/developers/docs/topics/gateway-events#request-guild-members
    """

    guild_id: Snowflake
    query: Missing[str] = UNSET
    limit: int
    presences: Missing[bool] = UNSET
    user_ids: Missing[Snowflake | list[Snowflake]] = UNSET
    nonce: Missing[str] = UNSET


class UpdateVoiceState(BaseModel):
    """Update Voice State Payload data

    see https://discord.com/developers/docs/topics/gateway-events#update-voice-state"""

    guild_id: Snowflake
    channel_id: Snowflake | None = Field(...)
    self_mute: bool
    self_deaf: bool


class UpdatePresence(BaseModel):
    """Update Presence Payload data

    see https://discord.com/developers/docs/topics/gateway-events#update-presence"""

    since: int | None = Field(...)
    activities: list[Activity]
    status: UpdatePresenceStatusType
    afk: bool


__all__ = [
    "Identify",
    "IdentifyConnectionProperties",
    "RequestGuildMembers",
    "Resume",
    "UpdatePresence",
    "UpdateVoiceState",
]
