from enum import IntEnum


class ButtonStyle(IntEnum):
    """Button styles.

    see https://discord.com/developers/docs/interactions/message-components#button-object-button-styles
    """

    Primary = 1
    """color: blurple, required field: custom_id"""
    Secondary = 2
    """color: grey, required field: custom_id"""
    Success = 3
    """color: green, required field: custom_id"""
    Danger = 4
    """color: red, required field: custom_id"""
    Link = 5
    """color: grey, navigates to a URL, required field: url"""
    Premium = 6
    """color: blurple, required field: sku_id"""


class ComponentType(IntEnum):
    """Component types.

    see https://discord.com/developers/docs/interactions/message-components#component-object-component-types
    """

    ActionRow = 1
    """Container for other components"""
    Button = 2
    """Button object"""
    StringSelect = 3
    """Select menu for picking from defined text options"""
    TextInput = 4
    """TextSegment input object"""
    UserInput = 5
    """Select menu for users"""
    RoleSelect = 6
    """Select menu for roles"""
    MentionableSelect = 7
    """Select menu for mentionables (users and roles)"""
    ChannelSelect = 8
    """Select menu for channels"""


class TextInputStyle(IntEnum):
    """TextSegment input style.

    see https://discord.com/developers/docs/interactions/message-components#text-input-object-text-input-styles
    """

    Short = 1
    """Single-line input"""
    Paragraph = 2
    """Multi-line input"""


__all__ = ["ButtonStyle", "ComponentType", "TextInputStyle"]
