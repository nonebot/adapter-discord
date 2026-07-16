from enum import IntEnum


class InteractionCallbackType(IntEnum):
    """Interaction callback type.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-type
    """

    PONG = 1
    """ACK a Ping"""
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    """respond to an interaction with a message"""
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    """ACK an interaction and edit a response later, the user sees a loading state"""
    DEFERRED_UPDATE_MESSAGE = 6
    """for components, ACK an interaction and edit the original message later;
    the user does not see a loading state"""
    UPDATE_MESSAGE = 7
    """for components, edit the message the component was attached to.
    Only valid for component-based interactions"""
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    """respond to an autocomplete interaction with suggested choices"""
    MODAL = 9
    """respond to an interaction with a popup modal.
    Not available for MODAL_SUBMIT and PING interactions."""


class InteractionContextType(IntEnum):
    """Interaction Context Type

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-context-types
    """

    GUILD = 0
    """Interaction can be used within servers"""
    BOT_DM = 1
    """Interaction can be used within DMs with the app's bot user"""
    PRIVATE_CHANNEL = 2
    """Interaction can be used within Group DMs and DMs other than the app's bot user"""


class InteractionType(IntEnum):
    """Interaction type.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
    """

    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


__all__ = ["InteractionCallbackType", "InteractionContextType", "InteractionType"]
