from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ..types import (
    UNSET,
    ButtonStyle,
    ChannelType,
    ComponentType,
    Missing,
    TextInputStyle,
)

if TYPE_CHECKING:
    from ..model import Channel, GuildMember, Role, User


class ActionRow(BaseModel):
    """An Action Row is a non-interactive container
    component for other types of components.
    It has a type: 1 and a sub-array of components of other types.

    - You can have up to 5 Action Rows per message
    - An Action Row cannot contain another Action Row

    see https://discord.com/developers/docs/interactions/message-components#action-rows
    """

    type: ComponentType = Field(default=ComponentType.ActionRow)
    components: list[Button | SelectMenu | TextInput]


class ComponentEmoji(BaseModel):
    """partial emoji for Component.

    see https://discord.com/developers/docs/interactions/message-components#button-object
    """

    id: str | None = Field(...)
    """emoji id"""
    name: str | None = Field(...)
    """emoji name"""
    animated: Missing[bool] = UNSET
    """whether this emoji is animated"""


class Button(BaseModel):
    """Buttons come in a variety of styles to convey different types of actions.
    These styles also define what fields are valid for a button.

    - Non-link buttons must have a custom_id, and cannot have a url
    - Link buttons must have a url, and cannot have a custom_id
    - Link buttons do not send an interaction to your app when clicked

    see https://discord.com/developers/docs/interactions/message-components#button-object
    """

    type: Literal[ComponentType.Button] = Field(default=ComponentType.Button)
    """2 for a button"""
    style: ButtonStyle
    """A button style"""
    label: Missing[str] = UNSET
    """TextSegment that appears on the button; max 80 characters"""
    emoji: Missing[ComponentEmoji] = UNSET
    """emoji name, id, and animated"""
    custom_id: Missing[str] = UNSET
    """Developer-defined identifier for the button; max 100 characters"""
    sku_id: Missing[Snowflake] = UNSET
    """Identifier for a purchasable SKU, only
    available when using premium-style buttons"""
    url: Missing[str] = UNSET
    """URL for link-style buttons"""
    disabled: Missing[bool] = UNSET
    """Whether the button is disabled (defaults to false)"""


class SelectMenu(BaseModel):
    """Select menus are interactive components that allow users to
    select one or more options from a dropdown list in messages.

    - On desktop, clicking on a select menu opens a dropdown-style UI;
    - on mobile, tapping a select menu opens up a half-sheet with the options.

    Select menus support single-select and multi-select behavior,
    meaning you can prompt a user to choose just one item from a list,
    or multiple. When a user finishes making their choice(s) by clicking
    out of the dropdown or closing the half-sheet, your app will receive an interaction.

    - Select menus must be sent inside an Action Row
    - An Action Row can contain only one select menu
    - An Action Row containing a select menu cannot also contain buttons

    see https://discord.com/developers/docs/interactions/message-components#select-menu-object
    """

    type: Literal[
        ComponentType.StringSelect,
        ComponentType.UserInput,
        ComponentType.RoleSelect,
        ComponentType.MentionableSelect,
        ComponentType.ChannelSelect,
    ]
    """Type of select menu component"""
    custom_id: str
    """ID for the select menu; max 100 characters"""
    options: Missing[list[SelectOption]] = UNSET
    """Specified choices in a select menu
    (only required and available for string selects; max 25"""
    channel_types: Missing[list[ChannelType]] = UNSET
    """List of channel types to include in the channel select component"""
    placeholder: Missing[str] = UNSET
    """Placeholder text if nothing is selected; max 150 characters"""
    default_values: Missing[list[SelectDefaultValue]] = UNSET
    """List of default values for auto-populated select
    menu components; number of default values must be in
    the range defined by min_values and max_values"""
    min_values: Missing[int] = UNSET
    """Minimum number of items that must be chosen (defaults to 1); min 0, max 25"""
    max_values: Missing[int] = UNSET
    """Maximum number of items that can be chosen (defaults to 1); max 25"""
    disabled: Missing[bool] = UNSET
    """Whether select menu is disabled (defaults to false)"""


class SelectDefaultValue(BaseModel):
    """see https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-default-value-structure"""

    id: Snowflake
    """ID of a user, role, or channel"""
    type: Literal["user", "role", "channel"]
    """Type of value that `id` represents."""


class SelectOption(BaseModel):
    """Select Option of StringSelect Menu.

    see https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-option-structure
    """

    label: str
    """User-facing name of the option; max 100 characters"""
    value: str
    """Dev-defined value of the option; max 100 characters"""
    description: Missing[str] = UNSET
    """Additional description of the option; max 100 characters"""
    emoji: Missing[ComponentEmoji] = UNSET
    """emoji name, id, and animated"""
    default: Missing[bool] = UNSET
    """Will show this option as selected by default"""


class SelectMenuResolved(BaseModel):
    """The resolved object is included in interaction payloads for user, role,
    mentionable, and channel select menu components. resolved contains a nested object
    with additional details about the selected options with the key of the
    resource type—users, roles, channels, and members.

    see https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-menu-resolved-object
    """

    users: Missing[dict[Snowflake, User]] = UNSET
    roles: Missing[dict[Snowflake, Role]] = UNSET
    channels: Missing[dict[Snowflake, Channel]] = UNSET
    members: Missing[dict[Snowflake, GuildMember]] = UNSET


class TextInput(BaseModel):
    """TextSegment inputs are an interactive component that render on modals.
    They can be used to collect short-form or long-form text.

    see https://discord.com/developers/docs/interactions/message-components#text-inputs
    """

    type: Literal[ComponentType.TextInput] = Field(default=ComponentType.TextInput)
    """4 for a text input"""
    custom_id: str
    """Developer-defined identifier for the input; max 100 characters"""
    style: TextInputStyle
    """The TextSegment Input Style"""
    label: str
    """Label for this component; max 45 characters"""
    min_length: Missing[int] = UNSET
    """Minimum input length for a text input; min 0, max 4000"""
    max_length: Missing[int] = UNSET
    """Maximum input length for a text input; min 1, max 4000"""
    required: Missing[bool] = UNSET
    """\tWhether this component is required to be filled (defaults to true)"""
    value: Missing[str] = UNSET
    """Pre-filled value for this component; max 4000 characters"""
    placeholder: Missing[str] = UNSET
    """Custom placeholder text if the input is empty; max 100 characters"""


Component = ActionRow | Button | SelectMenu | TextInput
DirectComponent = ActionRow | TextInput
