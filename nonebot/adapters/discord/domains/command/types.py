from __future__ import annotations

from enum import IntEnum


class ApplicationCommandOptionType(IntEnum):
    """Application Command Option Type

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type
    """

    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    """Any integer between -2^53 and 2^53"""
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    """Includes all channel types + categories"""
    ROLE = 8
    MENTIONABLE = 9
    """Includes users and roles"""
    NUMBER = 10
    """Any double between -2^53 and 2^53"""
    ATTACHMENT = 11
    """attachment object"""


class ApplicationCommandPermissionsType(IntEnum):
    """Application command permissions type.

    see https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-application-command-permission-type
    """

    ROLE = 1
    USER = 2
    CHANNEL = 3


class ApplicationCommandType(IntEnum):
    """Application Command Type

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-types
    """

    CHAT_INPUT = 1
    """Slash commands; a text-based command that shows up when a user types /"""
    USER = 2
    """A UI-based command that shows up when you right click or tap on a user"""
    MESSAGE = 3
    """A UI-based command that shows up when you right click or tap on a message"""


__all__ = [
    "ApplicationCommandOptionType",
    "ApplicationCommandPermissionsType",
    "ApplicationCommandType",
]
