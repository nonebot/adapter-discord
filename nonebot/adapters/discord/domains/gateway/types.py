from enum import IntEnum, IntFlag

from .._enum import StrEnum


class ActivityAssetImage(StrEnum):
    """Activity Asset Image

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-asset-image
    """

    ApplicationAsset = "Application Asset"
    """{application_asset_id} see https://discord.com/developers/docs/reference#image-formatting"""
    MediaProxyImage = "Media Proxy Image"
    """mp:{image_id}"""


class ActivityFlags(IntFlag):
    """Activity Flags

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-flags
    """

    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5
    PARTY_PRIVACY_FRIENDS = 1 << 6
    PARTY_PRIVACY_VOICE_CHANNEL = 1 << 7
    EMBEDDED = 1 << 8


class ActivityType(IntEnum):
    """Activity Type

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-types
    """

    Game = 0
    """Playing {name}"""
    Streaming = 1
    """Streaming {details}"""
    Listening = 2
    """Listening to {name}"""
    Watching = 3
    """Watching {name}"""
    Custom = 4
    """{emoji} {name}"""
    Competing = 5
    """	Competing in {name}"""


class PresenceStatus(StrEnum):
    """Presence Status

    see https://discord.com/developers/docs/topics/gateway-events#presence-update-presence-update-event-fields
    """

    ONLINE = "online"
    DND = "dnd"
    IDLE = "idle"
    OFFLINE = "offline"


class UpdatePresenceStatusType(StrEnum):
    """Update Presence Status type.

    see https://discord.com/developers/docs/topics/gateway-events#update-presence-status-types
    """

    online = "online"
    """Online"""
    dnd = "dnd"
    """Do Not Disturb"""
    idle = "idle"
    """AFK"""
    invisible = "invisible"
    """Invisible and shown as offline"""
    offline = "offline"
    """	Offline"""


__all__ = [
    "ActivityAssetImage",
    "ActivityFlags",
    "ActivityType",
    "PresenceStatus",
    "UpdatePresenceStatusType",
]
