from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ..types import UNSET, Missing, UpdatePresenceStatusType

if TYPE_CHECKING:
    from ..model import Activity, PresenceUpdate, UnavailableGuild, User


class Identify(BaseModel):
    """Identify Payload data

    see https://discord.com/developers/docs/topics/gateway-events#identify
    """

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

    see https://discord.com/developers/docs/topics/gateway-events#resume
    """

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

    see https://discord.com/developers/docs/topics/gateway-events#update-voice-state
    """

    guild_id: Snowflake
    channel_id: Snowflake | None = Field(...)
    self_mute: bool
    self_deaf: bool


class UpdatePresence(BaseModel):
    """Update Presence Payload data

    see https://discord.com/developers/docs/topics/gateway-events#update-presence
    """

    since: int | None = Field(...)
    activities: list[Activity]
    status: UpdatePresenceStatusType
    afk: bool


class Hello(BaseModel):
    """Hello Payload data

    see https://discord.com/developers/docs/topics/gateway-events#hello
    """

    heartbeat_interval: int


class ApplicationReady(BaseModel):
    """partial application object for ready event.

    see https://discord.com/developers/docs/events/gateway-events#ready
    """

    id: str
    flags: int


class Ready(BaseModel):
    """Ready Payload data

    see https://discord.com/developers/docs/topics/gateway-events#ready
    """

    v: int
    user: User
    guilds: list[UnavailableGuild]
    session_id: str
    resume_gateway_url: str
    shard: Missing[list[int]] = UNSET
    application: ApplicationReady
