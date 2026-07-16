"""Canonical interaction.read models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Component, InteractionCallbackData, ResolvedData

from .._model_support import (
    UNSET,
    ApplicationCommandOptionType,
    ApplicationCommandType,
    BaseModel,
    ComponentType,
    GuildFeature,
    InteractionCallbackType,
    Missing,
    Snowflake,
)


class InteractionGuild(BaseModel):
    """partial guild object for Interaction

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    id: Snowflake
    locale: Missing[str] = UNSET
    features: list[GuildFeature]


class ApplicationCommandData(BaseModel):
    """Sent in APPLICATION_COMMAND and APPLICATION_COMMAND_AUTOCOMPLETE interactions.

    *options can be partial when in response to APPLICATION_COMMAND_AUTOCOMPLETE

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-application-command-data-structure
    """

    id: Snowflake
    """the ID of the invoked command"""
    name: str
    """the name of the invoked command"""
    type: ApplicationCommandType
    """the type of the invoked command"""
    resolved: Missing["ResolvedData"] = UNSET
    """converted users + roles + channels + attachments"""
    options: Missing[list["ApplicationCommandInteractionDataOption"]] = UNSET
    """the params + values from the user"""
    guild_id: Missing[Snowflake] = UNSET
    """the id of the guild the command is registered to"""
    target_id: Missing[Snowflake] = UNSET
    """id of the user or message targeted by a user or message command"""


class MessageComponentData(BaseModel):
    """Message Component Data

    This is always present for select menu components

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-message-component-data-structure
    """

    custom_id: str
    """the custom_id of the component"""
    component_type: ComponentType
    """the type of the component"""
    values: Missing[list[str]] = UNSET
    """values the user selected in a select menu component"""
    resolved: Missing["ResolvedData"] = UNSET
    """resolved entities from selected options"""


class ModalSubmitData(BaseModel):
    """Modal Submit Data

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-modal-submit-data-structure
    """

    custom_id: str
    """the custom_id of the modal"""
    components: list["Component"]
    """the values submitted by the user"""


InteractionData = ApplicationCommandData | MessageComponentData | ModalSubmitData


class ApplicationCommandInteractionDataOption(BaseModel):
    """Application Command Interaction Data Option

    All options have names, and an option can either be a parameter and
    input value--in which case value will be set--or it can denote a subcommand or
    group--in which case it will contain a top-level key and another array of options.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-application-command-interaction-data-option-structure
    """

    name: str
    """Name of the parameter"""
    type: ApplicationCommandOptionType
    """Value of application command option type"""
    value: Missing[str | int | float | bool] = UNSET
    """Value of the option resulting from user input"""
    options: Missing[list["ApplicationCommandInteractionDataOption"]] = UNSET
    """Present if this option is a group or subcommand"""
    focused: Missing[bool] = UNSET
    """true if this option is the currently focused option for autocomplete"""


class InteractionResponse(BaseModel):
    """Interaction response.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object
    """

    type: InteractionCallbackType
    """the type of response"""
    data: Missing["InteractionCallbackData"] = UNSET
    """an optional response message"""


__all__ = [
    "ApplicationCommandData",
    "ApplicationCommandInteractionDataOption",
    "InteractionData",
    "InteractionGuild",
    "InteractionResponse",
    "MessageComponentData",
    "ModalSubmitData",
]
