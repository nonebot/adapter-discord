"""Canonical gateway.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..models import ApplicationReady, UnavailableGuild, User

from .._model_support import (
    UNSET,
    ActivityAssetImage,
    BaseModel,
    Missing,
    MissingOrNullable,
    Snowflake,
)


class Gateway(BaseModel):
    """Get Gateway Response

    see https://discord.com/developers/docs/topics/gateway#get-gateway"""

    url: str


class GatewayBot(BaseModel):
    """Get Gateway Bot Response

    see https://discord.com/developers/docs/topics/gateway#get-gateway-bot"""

    url: str
    shards: int
    session_start_limit: SessionStartLimit


class SessionStartLimit(BaseModel):
    """Session start limit

    see https://discord.com/developers/docs/topics/gateway#session-start-limit-object"""

    total: int
    remaining: int
    reset_after: int
    max_concurrency: int


class Hello(BaseModel):
    """Hello Payload data

    see https://discord.com/developers/docs/topics/gateway-events#hello"""

    heartbeat_interval: int


class Ready(BaseModel):
    """Ready Payload data

    see https://discord.com/developers/docs/topics/gateway-events#ready"""

    v: int
    user: User
    guilds: list[UnavailableGuild]
    session_id: str
    resume_gateway_url: str
    shard: Missing[list[int]] = UNSET
    application: ApplicationReady


class ClientStatus(BaseModel):
    """Client Status

    see https://discord.com/developers/docs/topics/gateway-events#client-status-object
    """

    desktop: Missing[str] = UNSET
    mobile: Missing[str] = UNSET
    web: Missing[str] = UNSET


class ActivityTimestamps(BaseModel):
    """Activity Timestamps

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-timestamps
    """

    start: Missing[int] = UNSET
    end: Missing[int] = UNSET


class ActivityEmoji(BaseModel):
    """Activity Emoji

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-emoji
    """

    name: str
    id: Missing[Snowflake] = UNSET
    animated: Missing[bool] = UNSET


class ActivityParty(BaseModel):
    """Activity Party

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-party
    """

    id: Missing[str] = UNSET
    size: Missing[tuple[int, int]] = UNSET


class ActivityAssets(BaseModel):
    """Activity Assets

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-assets
    """

    large_image: Missing[ActivityAssetImage] = UNSET
    large_text: Missing[str] = UNSET
    small_image: Missing[ActivityAssetImage] = UNSET
    small_text: Missing[str] = UNSET


class ActivitySecrets(BaseModel):
    """Activity Secrets

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-secrets
    """

    join: Missing[str] = UNSET
    spectate: Missing[str] = UNSET
    match: Missing[str] = UNSET


class ActivityButtons(BaseModel):
    """Activity Buttons

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-buttons
    """

    label: str
    url: str


class ActivityInstance(BaseModel):
    """Activity Instance

    see https://discord.com/developers/docs/resources/application#get-application-activity-instance-activity-instance-object
    """

    application_id: Snowflake
    """Application ID"""
    instance_id: str
    """Activity Instance ID"""
    launch_id: Snowflake
    """Unique identifier for the launch"""
    location: ActivityLocation
    """The Location the instance is runnning in"""
    users: list[Snowflake]
    """The IDs of the Users currently connected to the instance"""


class ActivityLocation(BaseModel):
    """The Activity Location is an object that describes
    the location in which an activity instance is running.

    see https://discord.com/developers/docs/resources/application#get-application-activity-instance-activity-location-object
    """

    id: str
    """	The unique identifier for the location"""
    kind: Literal["gc", "pc"]
    """
    Enum describing kind of location

    'gc'	The Location is a Guild Channel\n
    'pc'	The Location is a Private Channel, such as a DM or GDM
    """
    channel_id: Snowflake
    guild_id: MissingOrNullable[Snowflake] = UNSET


__all__ = [
    "ActivityAssets",
    "ActivityButtons",
    "ActivityEmoji",
    "ActivityInstance",
    "ActivityLocation",
    "ActivityParty",
    "ActivitySecrets",
    "ActivityTimestamps",
    "ClientStatus",
    "Gateway",
    "GatewayBot",
    "Hello",
    "Ready",
    "SessionStartLimit",
]
