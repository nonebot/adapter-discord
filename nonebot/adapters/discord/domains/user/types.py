from __future__ import annotations

from enum import IntEnum, IntFlag

from .._enum import StrEnum


class ConnectionServiceType(StrEnum):
    """Connection service type.

    see https://discord.com/developers/docs/resources/user#connection-object-services"""

    Battle_net = "battlenet"
    Bungie_net = "bungie"
    Domain = "domain"
    eBay = "ebay"  # noqa: N815
    Epic_Games = "epicgames"
    Facebook = "facebook"
    GitHub = "github"
    Instagram = "instagram"
    League_of_Legends = "leagueoflegends"
    PayPal = "paypal"
    PlayStation_Network = "playstation"
    Reddit = "reddit"
    Riot_Games = "riotgames"
    Roblox = "roblox"
    Spotify = "spotify"
    Skype = "skype"
    Steam = "steam"
    TikTok = "tiktok"
    Twitch = "twitch"
    Twitter = "twitter"
    Xbox_Live = "xbox"
    YouTube = "youtube"


class PremiumType(IntEnum):
    """Premium types denote the level of premium a user has.
    Visit the Nitro page to learn more about the premium plans we currently offer.

    see https://discord.com/developers/docs/resources/user#user-object-premium-types"""

    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
    NITRO_BASIC = 3


class UserFlags(IntFlag):
    """User flags denote certain attributes about a user.
    These flags are only available to bots.

    see https://discord.com/developers/docs/resources/user#user-object-user-flags"""

    STAFF = 1 << 0
    """Discord Employee"""
    PARTNER = 1 << 1
    """Partnered Server Owner"""
    HYPESQUAD = 1 << 2
    """HypeSquad Events Member"""
    BUG_HUNTER_LEVEL_1 = 1 << 3
    """Bug Hunter Level 1"""
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    """House Bravery Member"""
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    """House Brilliance Member"""
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    """House Balance Member"""
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    """Early Nitro Supporter"""
    TEAM_PSEUDO_USER = 1 << 10
    """User is a team"""
    BUG_HUNTER_LEVEL_2 = 1 << 14
    """Bug Hunter Level 2"""
    VERIFIED_BOT = 1 << 16
    """Verified Bot"""
    VERIFIED_DEVELOPER = 1 << 17
    """Early Verified Bot Developer"""
    CERTIFIED_MODERATOR = 1 << 18
    """Moderator Programs Alumni"""
    BOT_HTTP_INTERACTIONS = 1 << 19
    """Bot uses only HTTP interactions and is shown in the online member list"""
    ACTIVE_DEVELOPER = 1 << 22
    """User is an Active Developer"""


class VisibilityType(IntEnum):
    """Visibility type.

    see https://discord.com/developers/docs/resources/user#connection-object-visibility-types
    """

    NONE = 0
    """invisible to everyone except the user themselves"""
    EVERYONE = 1
    """visible to everyone"""


__all__ = ["ConnectionServiceType", "PremiumType", "UserFlags", "VisibilityType"]
