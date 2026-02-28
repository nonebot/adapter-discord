from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from .application_commands import ApplicationCommandOptionChoice
from .message_components import Component
from ..snowflake import Snowflake
from ...types import (
    UNSET,
    ApplicationCommandOptionType,
    ApplicationCommandType,
    ApplicationIntegrationType,
    ComponentType,
    GuildFeature,
    InteractionCallbackType,
    InteractionType,
    MessageFlag,
    Missing,
)

if TYPE_CHECKING:
    from .. import (
        AllowedMention,
        Attachment,
        AttachmentSend,
        Channel,
        Embed,
        File,
        GuildMember,
        MessageGet,
        PollRequest,
        Role,
        User,
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
    resolved: Missing[ResolvedData] = UNSET
    """converted users + roles + channels + attachments"""
    options: Missing[list[ApplicationCommandInteractionDataOption]] = UNSET
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
    resolved: Missing[ResolvedData] = UNSET
    """resolved entities from selected options"""


class ModalSubmitData(BaseModel):
    """Modal Submit Data

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-modal-submit-data-structure
    """

    custom_id: str
    """the custom_id of the modal"""
    components: list[Component]
    """the values submitted by the user"""


InteractionData = ApplicationCommandData | MessageComponentData | ModalSubmitData
"""While the data field is guaranteed to be present for all interaction
types besides PING, its structure will vary.
The following tables detail the inner data payload for each interaction type.

see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data"""


class ResolvedData(BaseModel):
    """Resolved Data

    If data for a Member is included,
    data for its corresponding User will also be included.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """

    users: Missing[dict[Snowflake, User]] = UNSET
    """the ids and User objects"""
    members: Missing[dict[Snowflake, GuildMember]] = UNSET
    """the ids and partial Member objects"""
    roles: Missing[dict[Snowflake, Role]] = UNSET
    """the ids and Role objects"""
    channels: Missing[dict[Snowflake, Channel]] = UNSET
    """the ids and partial Channel objects"""
    messages: Missing[dict[Snowflake, MessageGet]] = UNSET
    """the ids and partial Message objects"""
    attachments: Missing[dict[Snowflake, Attachment]] = UNSET
    """the ids and attachment objects"""


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
    options: Missing[list[ApplicationCommandInteractionDataOption]] = UNSET
    """Present if this option is a group or subcommand"""
    focused: Missing[bool] = UNSET
    """true if this option is the currently focused option for autocomplete"""


class MessageInteraction(BaseModel):
    """Message interaction.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object
    """

    id: Snowflake
    """ID of the interaction"""
    type: InteractionType
    """Type of interaction"""
    name: str
    """Name of the application command, including subcommands and subcommand groups"""
    user: User
    """User who invoked the interaction"""
    member: Missing[GuildMember] = UNSET
    """Member who invoked the interaction in the guild"""


class MessageInteractionMetadata(BaseModel):
    """Message Interaction Metadata

    Metadata about the interaction, including the source of the interaction and relevant server and user IDs.

    see https://discord.com/developers/docs/resources/message#message-interaction-metadata-object
    """

    id: Snowflake
    """ID of the interaction"""
    type: InteractionType
    """Type of interaction"""
    user: User
    """User who triggered the interaction"""
    authorizing_integration_owners: dict[
        ApplicationIntegrationType, Snowflake | Literal["0"]
    ]
    """IDs for installation context(s) related to an interaction.
    Details in Authorizing Integration Owners Object"""
    original_response_message_id: Missing[Snowflake] = UNSET
    """ID of the original response message, present only on follow-up messages"""
    interacted_message_id: Missing[Snowflake] = UNSET
    """ID of the message that contained interactive component,
    present only on messages created from component interactions"""
    triggering_interaction_metadata: Missing[MessageInteractionMetadata] = UNSET
    """Metadata for the interaction that was used to open the modal,
    present only on modal submit interactions"""


class InteractionResponse(BaseModel):
    """Interaction response.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object
    """

    type: InteractionCallbackType
    """the type of response"""
    data: Missing[InteractionCallbackData] = UNSET
    """an optional response message"""


class InteractionCallbackMessage(BaseModel):
    """Interaction callback message.

    Not all message fields are currently supported.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    tts: bool | None = None
    """is the response TTS"""
    content: str | None = None
    """message content"""
    embeds: list[Embed] | None = None
    """supports up to 10 embeds"""
    allowed_mentions: AllowedMention | None = None
    """allowed mentions object"""
    flags: MessageFlag | None = None
    """message flags combined as a bitfield
    (only SUPPRESS_EMBEDS and EPHEMERAL can be set)"""
    components: list[Component] | None = None
    """message components"""
    attachments: list[AttachmentSend] | None = None
    """attachment objects with filename and description.
    See Uploading Files for details."""
    poll: PollRequest | None = None
    """Details about the poll"""
    files: list[File] | None = None


class InteractionCallbackAutocomplete(BaseModel):
    """Interaction callback Autocomplete.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: list[ApplicationCommandOptionChoice]
    """autocomplete choices (max of 25 choices)"""


class InteractionCallbackModal(BaseModel):
    """Interaction callback modal.

    Support for components in modals is currently limited to type 4 (Text Input).

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-modal
    """

    custom_id: str
    """a developer-defined identifier for the modal, max 100 characters"""
    title: str
    """the title of the popup modal, max 45 characters"""
    components: list[Component]
    """between 1 and 5 (inclusive) components that make up the modal"""


InteractionCallbackData = (
    InteractionCallbackMessage
    | InteractionCallbackAutocomplete
    | InteractionCallbackModal
)
"""see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-data-structure"""
