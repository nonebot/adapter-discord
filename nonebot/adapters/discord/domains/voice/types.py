from __future__ import annotations

from enum import IntEnum


class AnimationType(IntEnum):
    """Animation Type

    see https://discord.com/developers/docs/topics/gateway-events#voice-channel-effect-send-animation-types
    """

    PREMIUM = 0
    """A fun animation, sent by a Nitro subscriber"""
    BASIC = 1
    """The standard animation"""


class StagePrivacyLevel(IntEnum):
    """Stage Privacy Level

    see https://discord.com/developers/docs/resources/stage-instance#stage-instance-object-privacy-level
    """

    PUBLIC = 1
    """The Stage instance is visible publicly. (deprecated)"""
    GUILD_ONLY = 2
    """The Stage instance is visible to only guild members."""


__all__ = ["AnimationType", "StagePrivacyLevel"]
