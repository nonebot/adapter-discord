import datetime
import inspect
import sys
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Union,
    final,
)

from pydantic import (
    BaseModel as PydanticBaseModel,
    Field,
)
from pydantic.generics import GenericModel

from .types import *

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, DictStrAny, MappingIntStrAny

T = TypeVar("T", str, int, float)


class BaseModel(PydanticBaseModel):
    def dict(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> "DictStrAny":
        data = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        # exclude UNSET
        if exclude_unset or exclude_none:
            data = {key: value for key, value in data.items() if value is not UNSET}
        return data


@final
class Snowflake(int):
    """Snowflake is a type of discord uniquely identifiable descriptors.

    It can be treated as a regular `int` for most purposes.

    see https://discord.com/developers/docs/reference#snowflakes"""

    __slots__ = ()

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any):
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        if not isinstance(value, int):
            raise TypeError(f"{value!r} is not int or str of int")
        return cls(value)

    @property
    def timestamp(self) -> int:
        """Milliseconds since Discord Epoch,
        the first second of 2015 or 1420070400000.

        """
        return (self >> 22) + 1420070400000

    @property
    def create_at(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(
            self.timestamp / 1000, datetime.timezone.utc
        )

    @property
    def internal_worker_id(self) -> int:
        return (self & 0x3E0000) >> 17

    @property
    def internal_process_id(self) -> int:
        return (self & 0x1F000) >> 12

    @property
    def increment(self) -> int:
        """For every ID that is generated on that process, this number is incremented"""
        return self & 0xFFF

    @classmethod
    def from_data(
        cls, timestamp: int, worker_id: int, process_id: int, increment: int
    ) -> "Snowflake":
        """Convert the pieces of info that comprise an ID into a Snowflake.
        Args:
            timestamp (int): Milliseconds timestamp.
            worker_id: worker_id
            process_id: process_id
            increment: increment
        """
        return cls(
            (timestamp - 1420070400000) << 22
            | (worker_id << 17)
            | (process_id << 12)
            | increment
        )

    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> "Snowflake":
        """Get a Snowflake from a datetime object."""
        return cls.from_data(int(dt.timestamp() * 1000), 0, 0, 0)


SnowflakeType = Union[Snowflake, int]
"""Snowflake or int"""


# Application Commands
# see https://discord.com/developers/docs/interactions/application-commands


class ApplicationCommand(BaseModel):
    """Application Command

    default_permission will soon be deprecated.
    You can instead set default_member_permissions to "0"
    to disable the command for everyone except admins by default,
    and/or set dm_permission to false to disable globally-scoped
    commands inside of DMs with your app

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object
    """

    id: Snowflake
    """Unique ID of command"""
    type: Missing[ApplicationCommandType] = UNSET
    """Type of command, defaults to 1"""
    application_id: Snowflake
    """ID of the parent application"""
    guild_id: Missing[Snowflake] = UNSET
    """Guild ID of the command, if not global"""
    name: str
    """Name of command, 1-32 characters"""
    name_localizations: MissingOrNullable[Dict[str, str]] = UNSET
    """Localization dictionary for name field.
    Values follow the same restrictions as name"""
    description: Missing[str] = UNSET
    """Description for CHAT_INPUT commands, 1-100 characters.
    Empty string for USER and MESSAGE commands"""
    description_localizations: MissingOrNullable[Dict[str, str]] = UNSET
    """Localization dictionary for description field.
    Values follow the same restrictions as description"""
    options: MissingOrNullable[List["ApplicationCommandOption"]] = UNSET
    """Parameters for the command, max of 25"""
    default_member_permissions: Optional[str] = Field(...)
    """Set of permissions represented as a bit set"""
    dm_permission: Missing[bool] = UNSET
    """Indicates whether the command is available in DMs with the app,
    only for globally-scoped commands.By default, commands are visible."""
    default_permission: MissingOrNullable[bool] = UNSET
    """Not recommended for use as field will soon be deprecated.
    Indicates whether the command is enabled by default
    when the app is added to a guild, defaults to true"""
    nsfw: Missing[bool] = UNSET
    """Indicates whether the command is age-restricted, defaults to false"""
    version: Snowflake
    """Autoincrementing version identifier updated during substantial record changes"""


class ApplicationCommandCreate(BaseModel):
    type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT
    name: str
    name_localizations: Optional[Dict[str, str]] = None
    description: Optional[str] = None
    description_localizations: Optional[Dict[str, str]] = None
    options: Optional[List["AnyCommandOption"]] = None
    default_member_permissions: Optional[str] = None
    dm_permission: Optional[bool] = None
    default_permission: Optional[bool] = None
    nsfw: Optional[bool] = None


class CommandOptionBase(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    name_localizations: Optional[Dict[str, str]] = None
    description: str
    description_localizations: Optional[Dict[str, str]] = None


class ApplicationCommandOption(CommandOptionBase):
    """Application Command Option

    Required options must be listed before optional options

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType
    """Type of option"""
    name: str
    """1-32 character name"""
    name_localizations: MissingOrNullable[Dict[str, str]] = UNSET
    """Localization dictionary for the name field.
    Values follow the same restrictions as name"""
    description: Missing[str] = UNSET
    """1-100 character description"""
    description_localizations: MissingOrNullable[Dict[str, str]] = UNSET
    """Localization dictionary for the description field.
    Values follow the same restrictions as description"""
    required: Missing[bool] = UNSET
    """If the parameter is required or optional--default false"""
    choices: Missing[List["ApplicationCommandOptionChoice"]] = UNSET
    """Choices for STRING, INTEGER,
    and NUMBER types for the user to pick from, max 25"""
    options: MissingOrNullable[List["ApplicationCommandOption"]] = UNSET
    """If the option is a subcommand or subcommand group type,
    these nested options will be the parameters"""
    channel_types: Missing[List[ChannelType]] = UNSET
    """	If the option is a channel type,
    the channels shown will be restricted to these types"""
    min_value: Missing[Union[int, float]] = UNSET
    """If the option is an INTEGER or NUMBER type, the minimum value permitted"""
    max_value: Missing[Union[int, float]] = UNSET
    """If the option is an INTEGER or NUMBER type, the maximum value permitted"""
    min_length: Missing[int] = UNSET
    """For option type STRING,
    the minimum allowed length (minimum of 0, maximum of 6000)"""
    max_length: Missing[int] = UNSET
    """For option type STRING,
    the maximum allowed length (minimum of 1, maximum of 6000)"""
    autocomplete: Missing[bool] = UNSET
    """If autocomplete interactions are enabled for
    this STRING, INTEGER, or NUMBER type option"""


class OptionChoice(GenericModel, Generic[T]):
    name: str
    name_localizations: Optional[Dict[str, str]] = None
    value: T


class SubCommandOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.SUB_COMMAND] = Field(
        ApplicationCommandOptionType.SUB_COMMAND, init=False
    )
    options: Optional[
        List[
            Union[
                "IntegerOption",
                "StringOption",
                "BooleanOption",
                "UserOption",
                "ChannelOption",
                "RoleOption",
                "MentionableOption",
                "NumberOption",
                "AttachmentOption",
            ]
        ]
    ] = None


class SubCommandGroupOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.SUB_COMMAND_GROUP] = Field(
        ApplicationCommandOptionType.SUB_COMMAND_GROUP, init=False
    )
    options: Optional[List[SubCommandOption]] = None


class IntegerOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.INTEGER] = Field(
        ApplicationCommandOptionType.INTEGER, init=False
    )
    choices: Optional[List[OptionChoice[int]]] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    autocomplete: Optional[bool] = None
    required: bool = False


class StringOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.STRING] = Field(
        ApplicationCommandOptionType.STRING, init=False
    )
    choices: Optional[List[OptionChoice[str]]] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    autocomplete: Optional[bool] = None
    required: bool = False


class BooleanOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.BOOLEAN] = Field(
        ApplicationCommandOptionType.BOOLEAN, init=False
    )
    required: bool = False


class UserOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.USER] = Field(
        ApplicationCommandOptionType.USER, init=False
    )
    required: bool = False


class ChannelOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.CHANNEL] = Field(
        ApplicationCommandOptionType.CHANNEL, init=False
    )
    channel_types: Optional[List[ChannelType]] = None
    required: bool = False


class RoleOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.ROLE] = Field(
        ApplicationCommandOptionType.ROLE, init=False
    )
    required: bool = False


class MentionableOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.MENTIONABLE] = Field(
        ApplicationCommandOptionType.MENTIONABLE, init=False
    )
    required: bool = False


class NumberOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.NUMBER] = Field(
        ApplicationCommandOptionType.NUMBER, init=False
    )
    choices: Optional[List[OptionChoice[float]]] = None
    min_value: Optional[float] = None
    required: bool = False


class AttachmentOption(CommandOptionBase):
    type: Literal[ApplicationCommandOptionType.ATTACHMENT] = Field(
        ApplicationCommandOptionType.ATTACHMENT, init=False
    )
    required: bool = False


AnyCommandOption = Union[
    SubCommandGroupOption,
    SubCommandOption,
    IntegerOption,
    StringOption,
    UserOption,
    ChannelOption,
    RoleOption,
    MentionableOption,
    NumberOption,
    BooleanOption,
    AttachmentOption,
]


class ApplicationCommandOptionChoice(BaseModel):
    """Application Command Option Choice

    If you specify choices for an option,
    they are the only valid values for a user to pick

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
    """

    name: str
    """1-100 character choice name"""
    name_localizations: MissingOrNullable[Dict[str, str]] = UNSET
    """Localization dictionary for the name field.
    Values follow the same restrictions as name"""
    value: Union[str, int, float]
    """Value for the choice, up to 100 characters if string.
    Type of value depends on the option type that the choice belongs to."""


class GuildApplicationCommandPermissions(BaseModel):
    """Guild Application Command Permissions

    When the id field is the application ID instead of a command ID,
    the permissions apply to all commands that do not contain explicit overwrites.

    see https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-guild-application-command-permissions-structure
    """

    id: Snowflake
    """ID of the command or the application ID"""
    application_id: Snowflake
    """ID of the application the command belongs to"""
    guild_id: Snowflake
    """ID of the guild"""
    permissions: List["ApplicationCommandPermissions"]
    """Permissions for the command in the guild, max of 100"""


class ApplicationCommandPermissions(BaseModel):
    """Application command permissions.

    Application command permissions allow you to enable or
    disable commands for specific users, roles, or channels within a guild.

    see https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-guild-application-command-permissions-structure
    """

    id: Snowflake
    """ID of the role, user, or channel. It can also be a permission constant"""
    type: ApplicationCommandPermissionsType
    """application command permission type"""
    permission: bool
    """true to allow, false, to disallow"""


# Message Components
# see https://discord.com/developers/docs/interactions/message-components


class ActionRow(BaseModel):
    """An Action Row is a non-interactive container
    component for other types of components.
    It has a type: 1 and a sub-array of components of other types.

    - You can have up to 5 Action Rows per message
    - An Action Row cannot contain another Action Row

    see https://discord.com/developers/docs/interactions/message-components#action-rows
    """

    type: ComponentType = Field(default=ComponentType.ActionRow, const=True)
    components: List[Union["Button", "SelectMenu", "TextInput"]]


class ComponentEmoji(BaseModel):
    """partial emoji for Component.

    see https://discord.com/developers/docs/interactions/message-components#button-object
    """

    id: Optional[str] = Field(...)
    """emoji id"""
    name: Optional[str] = Field(...)
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

    type: Literal[ComponentType.Button] = Field(
        default=ComponentType.Button, const=True
    )
    """2 for a button"""
    style: ButtonStyle
    """A button style"""
    label: Missing[str] = UNSET
    """TextSegment that appears on the button; max 80 characters"""
    emoji: Missing[ComponentEmoji] = UNSET
    """emoji name, id, and animated"""
    custom_id: Missing[str] = UNSET
    """Developer-defined identifier for the button; max 100 characters"""
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
    options: Missing[List["SelectOption"]] = UNSET
    """Specified choices in a select menu
    (only required and available for string selects; max 25"""
    channel_types: Missing[List[ChannelType]] = UNSET
    """List of channel types to include in the channel select component"""
    placeholder: Missing[str] = UNSET
    """Placeholder text if nothing is selected; max 150 characters"""
    min_values: Missing[int] = UNSET
    """Minimum number of items that must be chosen (defaults to 1); min 0, max 25"""
    max_values: Missing[int] = UNSET
    """Maximum number of items that can be chosen (defaults to 1); max 25"""
    disabled: Missing[bool] = UNSET
    """Whether select menu is disabled (defaults to false)"""
    resolved: Missing["SelectMenuResolved"] = UNSET
    """Resolved values for user, role, and channel selects,
    can be returned only by the payload, but cannot be set actively"""


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

    users: Missing[Dict[Snowflake, "User"]] = UNSET
    roles: Missing[Dict[Snowflake, "Role"]] = UNSET
    channels: Missing[Dict[Snowflake, "Channel"]] = UNSET
    members: Missing[Dict[Snowflake, "GuildMember"]] = UNSET


class TextInput(BaseModel):
    """TextSegment inputs are an interactive component that render on modals.
    They can be used to collect short-form or long-form text.

    see https://discord.com/developers/docs/interactions/message-components#text-inputs
    """

    type: Literal[ComponentType.TextInput] = Field(
        default=ComponentType.TextInput, const=True
    )
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
    """	Whether this component is required to be filled (defaults to true)"""
    value: Missing[str] = UNSET
    """Pre-filled value for this component; max 4000 characters"""
    placeholder: Missing[str] = UNSET
    """Custom placeholder text if the input is empty; max 100 characters"""


Component = Union[ActionRow, Button, SelectMenu, TextInput]
DirectComponent = Union[ActionRow, TextInput]


# Receiving and Responding
# see https://discord.com/developers/docs/interactions/receiving-and-responding


class Interaction(BaseModel):
    """An Interaction is the message that your application receives
    when a user uses an application command or a message component.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    id: Snowflake
    """ID of the interaction"""
    application_id: Snowflake
    """ID of the application this interaction is for"""
    type: InteractionType
    """Type of interaction"""
    data: Missing["InteractionData"] = UNSET
    """Interaction data payload
    This is always present on application command, message component,
    and modal submit interaction types.
    It is optional for future-proofing against new interaction types"""
    guild_id: Missing[Snowflake] = UNSET
    """Guild that the interaction was sent from"""
    channel: Missing["Channel"] = UNSET
    """Channel that the interaction was sent from"""
    channel_id: Missing[Snowflake] = UNSET
    """Channel that the interaction was sent from"""
    member: Missing["GuildMember"] = UNSET
    """Guild member data for the invoking user, including permissions"""
    user: Missing["User"] = UNSET
    """User object for the invoking user, if invoked in a DM"""
    token: str
    """Continuation token for responding to the interaction"""
    version: int
    """Read-only property, always 1"""
    message: Missing["MessageGet"] = UNSET
    """For components, the message they were attached to"""
    app_permissions: Missing[str] = UNSET
    """Bitwise set of permissions the app or bot has within the
    channel the interaction was sent from"""
    locale: Missing[str] = UNSET
    """Selected language of the invoking user"""
    guild_locale: Missing[str] = UNSET
    """Guild's preferred locale, if invoked in a guild"""


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
    options: Missing[List["ApplicationCommandInteractionDataOption"]] = UNSET
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
    values: Missing[List[str]] = UNSET
    """values the user selected in a select menu component"""


class ModalSubmitData(BaseModel):
    """Modal Submit Data

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-modal-submit-data-structure
    """

    custom_id: str
    """the custom_id of the modal"""
    components: List[Component]
    """the values submitted by the user"""


InteractionData = Union[ApplicationCommandData, MessageComponentData, ModalSubmitData]
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

    users: Missing[Dict[Snowflake, "User"]] = UNSET
    """the ids and User objects"""
    members: Missing[Dict[Snowflake, "GuildMember"]] = UNSET
    """the ids and partial Member objects"""
    roles: Missing[Dict[Snowflake, "Role"]] = UNSET
    """the ids and Role objects"""
    channels: Missing[Dict[Snowflake, "Channel"]] = UNSET
    """the ids and partial Channel objects"""
    messages: Missing[Dict[Snowflake, "MessageGet"]] = UNSET
    """the ids and partial Message objects"""
    attachments: Missing[Dict[Snowflake, "Attachment"]] = UNSET
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
    value: Missing[Union[str, int, float, bool]] = UNSET
    """Value of the option resulting from user input"""
    options: Missing[List["ApplicationCommandInteractionDataOption"]] = UNSET
    """Present if this option is a group or subcommand"""
    focused: Missing[bool] = UNSET
    """true if this option is the currently focused option for autocomplete"""


class MessageInteraction(BaseModel):
    """Message interaction.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    id: Snowflake
    """ID of the interaction"""
    type: InteractionType
    """Type of interaction"""
    name: str
    """Name of the application command, including subcommands and subcommand groups"""
    user: "User"
    """User who invoked the interaction"""
    member: Missing["GuildMember"] = UNSET
    """Member who invoked the interaction in the guild"""


class InteractionResponse(BaseModel):
    """Interaction response.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object
    """

    type: InteractionCallbackType
    """the type of response"""
    data: Missing["InteractionCallbackData"] = UNSET
    """an optional response message"""


class InteractionCallbackMessage(BaseModel):
    """Interaction callback message.

    Not all message fields are currently supported.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    tts: Optional[bool] = None
    """is the response TTS"""
    content: Optional[str] = None
    """message content"""
    embeds: Optional[List["Embed"]] = None
    """supports up to 10 embeds"""
    allowed_mentions: Optional["AllowedMention"] = None
    """allowed mentions object"""
    flags: Optional[MessageFlag] = None
    """message flags combined as a bitfield
    (only SUPPRESS_EMBEDS and EPHEMERAL can be set)"""
    components: Optional[List[Component]] = None
    """message components"""
    attachments: Optional[List["AttachmentSend"]] = None
    """attachment objects with filename and description.
    See Uploading Files for details."""

    files: Optional[List["File"]] = None


class InteractionCallbackAutocomplete(BaseModel):
    """Interaction callback Autocomplete.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: List[ApplicationCommandOptionChoice]
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
    components: List[Component]
    """between 1 and 5 (inclusive) components that make up the modal"""


InteractionCallbackData = Union[
    InteractionCallbackMessage,
    InteractionCallbackAutocomplete,
    InteractionCallbackModal,
]
"""see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-data-structure"""


# Application
# see https://discord.com/developers/docs/resources/application


class Application(BaseModel):
    """Application.

    see https://discord.com/developers/docs/resources/application#application-object"""

    id: Snowflake
    """the id of the app"""
    name: str
    """the name of the app"""
    icon: Optional[str]
    """the icon hash of the app"""
    description: str
    """the description of the app"""
    rpc_origins: Missing[List[str]] = UNSET
    """an array of rpc origin urls, if rpc is enabled"""
    bot_public: bool
    """when false only app owner can join the app's bot to guilds"""
    bot_require_code_grant: bool
    """when true the app's bot will only join upon completion
    of the full oauth2 code grant flow"""
    terms_of_service_url: Missing[str] = UNSET
    """the url of the app's terms of service"""
    privacy_policy_url: Missing[str] = UNSET
    """the url of the app's privacy policy"""
    owner: Missing["User"] = UNSET  # partial user object
    """partial user object containing info on the owner of the application"""
    verify_key: str
    """the hex encoded key for verification in
    interactions and the GameSDK's GetTicket"""
    team: Optional["Team"]
    """if the application belongs to a team, this will
    be a list of the members of that team"""
    guild_id: Missing[Snowflake] = UNSET
    """if this application is a game sold on Discord,
    this field will be the guild to which it has been linked"""
    primary_sku_id: Missing[Snowflake] = UNSET
    """if this application is a game sold on Discord,
    this field will be the id of the "Game SKU" that is created, if exists"""
    slug: Missing[str] = UNSET
    """if this application is a game sold on Discord,
    this field will be the URL slug that links to the store page"""
    cover_image: Missing[str] = UNSET
    """the application's default rich presence invite cover image hash"""
    flags: Missing[ApplicationFlag] = UNSET
    """the application's public flags"""
    tags: Missing[List[str]] = UNSET
    """up to 5 tags describing the content and functionality of the application"""
    install_params: Missing["InstallParams"] = UNSET
    """settings for the application's default in-app authorization link, if enabled"""
    custom_install_url: Missing[str] = UNSET
    """the application's default custom authorization link, if enabled"""
    role_connections_verification_url: Missing[str] = UNSET
    """the application's role connection verification entry point,
    which when configured will render the app as a verification method
    in the guild role verification configuration"""


class InstallParams(BaseModel):
    """Install params.

    see https://discord.com/developers/docs/resources/application#install-params-object
    """

    scopes: List[str]
    """the scopes to add the application to the server with"""
    permissions: str
    """	the permissions to request for the bot role"""


# Application Role Connection Metadata
# see https://discord.com/developers/docs/resources/application-role-connection-metadata


class ApplicationRoleConnectionMetadata(BaseModel):
    """Application Role Connection Metadata.

    see https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object
    """

    type: ApplicationRoleConnectionMetadataType
    """type of metadata value"""
    key: str
    """dictionary key for the metadata field
    (must be a-z, 0-9, or _ characters; 1-50 characters)"""
    name: str
    """name of the metadata field (1-100 characters)"""
    name_localizations: Missing[Dict[str, str]] = UNSET
    """translations of the name"""
    description: str
    """description of the metadata field (1-200 characters)"""
    description_localizations: Missing[Dict[str, str]] = UNSET
    """translations of the description"""


# Audit Log
# see https://discord.com/developers/docs/resources/audit-log


class AuditLog(BaseModel):
    """Audit Log.

    see https://discord.com/developers/docs/resources/audit-log#audit-log-object"""

    application_commands: List[ApplicationCommand]
    """List of application commands referenced in the audit log"""
    audit_log_entries: List["AuditLogEntry"]
    """List of audit log entries, sorted from most to least recent"""
    auto_moderation_rules: List["AutoModerationRule"]
    """List of auto moderation rules referenced in the audit log"""
    guild_scheduled_events: List["GuildScheduledEvent"]
    """List of guild scheduled events referenced in the audit log"""
    integrations: List["Integration"]  # partial integration object
    """List of partial integration objects"""
    threads: List["Channel"]  # thread-specific channel objects
    """List of threads referenced in the audit log"""
    users: List["User"]
    """List of users referenced in the audit log"""
    webhooks: List["Webhook"]
    """List of webhooks referenced in the audit log"""


class AuditLogEntry(BaseModel):
    """Audit Log Entry

    see https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object
    """

    target_id: Optional[str]
    """ID of the affected entity (webhook, user, role, etc.)"""
    changes: Missing[List["AuditLogChange"]] = UNSET
    """Changes made to the target_id"""
    user_id: Optional[Snowflake]
    """User or app that made the changes"""
    id: Snowflake
    """ID of the entry"""
    action_type: AuditLogEventType
    """Type of action that occurred"""
    options: Missing["OptionalAuditEntryInfo"] = UNSET
    """Additional info for certain event types"""
    reason: Missing[str] = UNSET
    """Reason for the change (1-512 characters)"""


class OptionalAuditEntryInfo(BaseModel):
    """Optional Audit Entry Info

    see https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-optional-audit-entry-info
    """

    application_id: Snowflake
    """ID of the app whose permissions were targeted"""
    auto_moderation_rule_name: str
    """Name of the Auto Moderation rule that was triggered"""
    auto_moderation_rule_trigger_type: str
    """Trigger type of the Auto Moderation rule that was triggered"""
    channel_id: Snowflake
    """Channel in which the entities were targeted"""
    count: str
    """Number of entities that were targeted"""
    delete_member_days: str
    """Number of days after which inactive members were kicked"""
    id: Snowflake
    """ID of the overwritten entity"""
    members_removed: str
    """Number of members removed by the prune"""
    message_id: Snowflake
    """ID of the message that was targeted"""
    role_name: str
    """Name of the role if type is "0" (not present if type is "1")"""
    type: str
    """Type of overwritten entity - role ("0") or member ("1")"""


class AuditLogChange(BaseModel):
    """Many audit log events include a changes array in their entry object.
    The structure for the individual changes varies based on the event type
    and its changed objects, so apps shouldn't depend on a single pattern
    of handling audit log events.

    see https://discord.com/developers/docs/resources/audit-log#audit-log-change-object
    """

    new_value: Missing[Any] = UNSET
    """New value of the key"""
    old_value: Missing[Any] = UNSET
    """Old value of the key"""
    key: str
    """Name of the changed entity, with a few exceptions"""


class AuditLogChangeException(BaseModel):
    """Audit Log Change Exception.

    see https://discord.com/developers/docs/resources/audit-log#audit-log-change-object-audit-log-change-exceptions
    """


# Auto Moderation
# see https://discord.com/developers/docs/resources/auto-moderation


class AutoModerationRule(BaseModel):
    """Auto moderation rule.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object
    """

    id: Snowflake
    """the id of this rule"""
    guild_id: Snowflake
    """the id of the guild which this rule belongs to"""
    name: str
    """the rule name"""
    creator_id: Snowflake
    """	the user which first created this rule"""
    event_type: AutoModerationRuleEventType
    """the rule event type"""
    trigger_type: TriggerType
    """the rule trigger type"""
    trigger_metadata: "TriggerMetadata"
    """the rule trigger metadata"""
    actions: List["AutoModerationAction"]
    """the actions which will execute when the rule is triggered"""
    enabled: bool
    """whether the rule is enabled"""
    exempt_roles: List[Snowflake]
    """the role ids that should not be affected by the rule (Maximum of 20)"""
    exempt_channels: List[Snowflake]
    """the channel ids that should not be affected by the rule (Maximum of 50)"""


class TriggerMetadata(BaseModel):
    """Additional data used to determine whether a rule should be triggered.
    Different fields are relevant based on the value of trigger_type.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-trigger-metadata
    """

    keyword_filter: List[str]
    """substrings which will be searched for in content (Maximum of 1000)"""
    regex_patterns: List[str]
    """regular expression patterns which will be matched
    against content (Maximum of 10)"""
    presets: List[KeywordPresetType]
    """the internally pre-defined wordsets which will be searched for in content"""
    allow_list: List[str]
    """substrings which should not trigger the rule (Maximum of 100 or 1000)"""
    mention_total_limit: int
    """total number of unique role and user mentions allowed
    per message (Maximum of 50)"""


class AutoModerationAction(BaseModel):
    """Auto moderation action.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object
    """

    type: AutoModerationActionType
    """the type of action"""
    metadata: Missing["AutoModerationActionMetadata"] = UNSET
    """additional metadata needed during execution for this specific action type"""


class AutoModerationActionMetadata(BaseModel):
    """Auto moderation action metadata.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-action-metadata
    """

    channel_id: Snowflake
    """channel to which user content should be logged"""
    duration_seconds: int
    """	timeout duration in seconds"""
    custom_message: Missing[str] = UNSET
    """additional explanation that will be shown to members
    whenever their message is blocked"""


class CreateAndModifyAutoModerationRuleParams(BaseModel):
    """Create and modify Auto Moderation Rule Params.

    see https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
    """

    name: Optional[str]
    event_type: Optional[AutoModerationRuleEventType]
    trigger_type: Optional[TriggerType]
    trigger_metadata: Optional[TriggerMetadata]
    actions: Optional[List[AutoModerationAction]]
    enabled: Optional[bool]
    exempt_roles: Optional[List[Snowflake]]
    exempt_channels: Optional[List[Snowflake]]


# Channel
# see https://discord.com/developers/docs/resources/channel


class Channel(BaseModel):
    """Represents a guild or DM channel within Discord.

    see https://discord.com/developers/docs/resources/channel#channel-object"""

    id: Snowflake
    """the id of this channel"""
    type: ChannelType
    """the type of channel"""
    guild_id: Missing[Snowflake] = UNSET
    """the id of the guild (may be missing for some channel objects
    received over gateway guild dispatches)"""
    position: Missing[int] = UNSET
    """sorting position of the channel"""
    permission_overwrites: Missing[List["Overwrite"]] = UNSET
    """explicit permission overwrites for members and roles"""
    name: MissingOrNullable[str] = UNSET
    """the name of the channel (1-100 characters)"""
    topic: MissingOrNullable[str] = UNSET
    """the channel topic (0-4096 characters for GUILD_FORUM channels,
    0-1024 characters for all others)"""
    nsfw: Missing[bool] = UNSET
    """whether the channel is nsfw"""
    last_message_id: MissingOrNullable[Snowflake] = UNSET
    """the id of the last message sent in this channel
    (or thread for GUILD_FORUM channels)
    (may not point to an existing or valid message or thread)"""
    bitrate: Missing[int] = UNSET
    """the bitrate (in bits) of the voice channel"""
    user_limit: Missing[int] = UNSET
    """the user limit of the voice channel"""
    rate_limit_per_user: Missing[int] = UNSET
    """amount of seconds a user has to wait before sending another message (0-21600);
    bots, as well as users with the permission manage_messages or
    manage_channel, are unaffected"""
    recipients: Missing[List["User"]] = UNSET
    """the recipients of the DM"""
    icon: MissingOrNullable[str] = UNSET
    """icon hash of the group DM"""
    owner_id: Missing[Snowflake] = UNSET
    """id of the creator of the group DM or thread"""
    application_id: Missing[Snowflake] = UNSET
    """application id of the group DM creator if it is bot-created"""
    managed: Missing[bool] = UNSET
    """for group DM channels: whether the channel is managed
    by an application via the gdm.join OAuth2 scope"""
    parent_id: MissingOrNullable[Snowflake] = UNSET
    """for guild channels: id of the parent category for a channel
    (each parent category can contain up to 50 channels),
    for threads: id of the text channel this thread was created"""
    last_pin_timestamp: MissingOrNullable[str] = UNSET
    """when the last pinned message was pinned.
    This may be null in events such as GUILD_CREATE when a message is not pinned."""
    rtc_region: MissingOrNullable[str] = UNSET
    """voice region id for the voice channel, automatic when set to null"""
    video_quality_mode: Missing[VideoQualityMode] = UNSET
    """the camera video quality mode of the voice channel, 1 when not present"""
    message_count: Missing[int] = UNSET
    """number of messages (not including the initial message
    or deleted messages) in a thread."""
    member_count: Missing[int] = UNSET
    """an approximate count of users in a thread, stops counting at 50"""
    thread_metadata: Missing["ThreadMetadata"] = UNSET
    """thread-specific fields not needed by other channels"""
    member: Missing["ThreadMember"] = UNSET
    """thread member object for the current user, if they have joined the thread,
    only included on certain API endpoints"""
    default_auto_archive_duration: Missing[int] = UNSET
    """default duration, copied onto newly created threads, in minutes,
    threads will stop showing in the channel list after the specified
    period of inactivity, can be set to: 60, 1440, 4320, 10080"""
    permissions: Missing[str] = UNSET
    """computed permissions for the invoking user in the channel, including overwrites,
    only included when part of the resolved data received on a slash command interaction
    """
    flags: Missing[ChannelFlags] = UNSET
    """channel flags combined as a bitfield"""
    total_message_sent: Missing[int] = UNSET
    """number of messages ever sent in a thread, it's similar to message_count
    on message creation, but will not decrement the number when a message is deleted"""
    available_tags: Missing[List["ForumTag"]] = UNSET
    """the set of tags that can be used in a GUILD_FORUM channel"""
    applied_tags: Missing[List[Snowflake]] = UNSET
    """the IDs of the set of tags that have been applied to a
    thread in a GUILD_FORUM channel"""
    default_reaction_emoji: MissingOrNullable["DefaultReaction"] = UNSET
    """the emoji to show in the add reaction button on a
    thread in a GUILD_FORUM channel"""
    default_thread_rate_limit_per_user: Missing[int] = UNSET
    """the initial rate_limit_per_user to set on newly created threads in a channel.
    this field is copied to the thread at creation time and does not live update."""
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    """the default sort order type used to order posts in GUILD_FORUM channels.
    Defaults to null, which indicates a preferred sort order
    hasn't been set by a channel admin"""
    default_forum_layout: Missing[ForumLayoutTypes] = UNSET
    """the default forum layout view used to display posts in GUILD_FORUM channels.
    Defaults to 0, which indicates a layout view has not been set by a channel admin"""


class MessageGet(BaseModel):
    """Message

    see https://discord.com/developers/docs/resources/channel#message-object"""

    id: Snowflake
    channel_id: Snowflake
    author: "User"
    content: str
    timestamp: datetime.datetime
    edited_timestamp: Optional[datetime.datetime] = Field(...)
    tts: bool
    mention_everyone: bool
    mentions: List["User"]
    mention_roles: List[str]
    mention_channels: Missing[List["ChannelMention"]] = UNSET
    attachments: List["Attachment"]
    embeds: List["Embed"]
    reactions: Missing[List["Reaction"]] = UNSET
    nonce: Missing[Union[int, str]] = UNSET
    pinned: bool
    webhook_id: Missing[Snowflake] = UNSET
    type: MessageType
    activity: Missing["MessageActivity"] = UNSET
    application: Missing[Application] = UNSET
    application_id: Missing[Snowflake] = UNSET
    message_reference: Missing["MessageReference"] = UNSET
    flags: Missing[MessageFlag] = UNSET
    referenced_message: MissingOrNullable["MessageGet"] = UNSET
    interaction: Missing[MessageInteraction] = UNSET
    thread: Missing[Channel] = UNSET
    components: Missing[List[DirectComponent]] = UNSET
    sticker_items: Missing[List["StickerItem"]] = UNSET
    stickers: Missing[List["Sticker"]] = UNSET
    position: Missing[int] = UNSET
    role_subscription_data: Missing["RoleSubscriptionData"] = UNSET


class MessageActivity(BaseModel):
    """Message activity.

    see https://discord.com/developers/docs/resources/channel#message-object-message-activity-structure
    """

    type: MessageActivityType
    party_id: Optional[str]


class MessageReference(BaseModel):
    """Message reference.

    see https://discord.com/developers/docs/resources/channel#message-reference-object
    """

    message_id: Missing[Snowflake] = UNSET
    """id of the originating message"""
    channel_id: Missing[Snowflake] = UNSET
    """id of the originating message's channel.
    channel_id is optional when creating a reply,
    but will always be present when receiving an
    event/response that includes this data model."""
    guild_id: Missing[Snowflake] = UNSET
    """id of the originating message's guild"""
    fail_if_not_exists: Missing[bool] = UNSET
    """when sending, whether to error if the referenced
    message doesn't exist instead of sending
    as a normal (non-reply) message, default true"""


class FollowedChannel(BaseModel):
    """Followed channel.

    see https://discord.com/developers/docs/resources/channel#followed-channel-object"""

    channel_id: Snowflake
    webhook_id: Snowflake


class Reaction(BaseModel):
    """Reaction.

    see https://discord.com/developers/docs/resources/channel#reaction-object"""

    count: int
    me: bool
    emoji: "Emoji"


class Overwrite(BaseModel):
    """Overwrite.

    see https://discord.com/developers/docs/resources/channel#overwrite-object"""

    id: str
    type: OverwriteType
    allow: str
    deny: str


class ThreadMetadata(BaseModel):
    """Thread metadata.

    see https://discord.com/developers/docs/resources/channel#thread-metadata-object"""

    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: Optional[bool]
    create_timestamp: Optional[str]


class ThreadMember(BaseModel):
    """Thread member.

    see https://discord.com/developers/docs/resources/channel#thread-member-object"""

    id: Optional[str]
    user_id: Optional[str]
    join_timestamp: str
    flags: int
    member: Optional["GuildMember"]


class DefaultReaction(BaseModel):
    """Default reaction.

    see https://discord.com/developers/docs/resources/channel#default-reaction-object"""

    emoji_id: Optional[str]
    emoji_name: Optional[str]


class ForumTag(BaseModel):
    """An object that represents a tag that is able to be applied
    to a thread in a GUILD_FORUM channel.

    see https://discord.com/developers/docs/resources/channel#forum-tag-object"""

    id: Snowflake
    name: str
    moderated: bool
    emoji_id: MissingOrNullable[Snowflake] = UNSET
    emoji_name: Optional[str]


class Embed(BaseModel):
    """Embed

    see https://discord.com/developers/docs/resources/channel#embed-object"""

    title: Missing[str] = UNSET
    type: Missing[EmbedTypes] = UNSET
    description: Missing[str] = UNSET
    url: Missing[str] = UNSET
    timestamp: Missing[str] = UNSET
    color: Missing[int] = UNSET
    footer: Missing["EmbedFooter"] = UNSET
    image: Missing["EmbedImage"] = UNSET
    thumbnail: Missing["EmbedThumbnail"] = UNSET
    video: Missing["EmbedVideo"] = UNSET
    provider: Missing["EmbedProvider"] = UNSET
    author: Missing["EmbedAuthor"] = UNSET
    fields: Missing[List["EmbedField"]] = UNSET


class EmbedThumbnail(BaseModel):
    """Embed thumbnail.

    see https://discord.com/developers/docs/resources/channel#embed-object-embed-thumbnail-structure
    """

    url: str
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedVideo(BaseModel):
    """Embed video.

    see https://discord.com/developers/docs/resources/channel#embed-object-embed-video-structure
    """

    url: Missing[str] = UNSET
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedImage(BaseModel):
    """Embed image.

    see https://discord.com/developers/docs/resources/channel#embed-object-embed-image-structure
    """

    url: str
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedProvider(BaseModel):
    """Embed provider.

    see https://discord.com/developers/docs/resources/channel#embed-object-embed-provider-structure
    """

    name: Missing[str] = UNSET
    url: Missing[str] = UNSET


class EmbedAuthor(BaseModel):
    """Embed author.

    see https://discord.com/developers/docs/resources/channel#embed-object-embed-author-structure
    """

    name: str
    url: Missing[str] = UNSET
    icon_url: Missing[str] = UNSET
    proxy_icon_url: Missing[str] = UNSET


class EmbedFooter(BaseModel):
    """Embed footer.

    see https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
    """

    text: str
    icon_url: Missing[str] = UNSET
    proxy_icon_url: Missing[str] = UNSET


class EmbedField(BaseModel):
    """Embed field.

    see https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
    """

    name: str
    value: str
    inline: Missing[bool] = UNSET


class Attachment(BaseModel):
    """Attachment

    see https://discord.com/developers/docs/resources/channel#attachment-object"""

    id: str
    filename: str
    description: Missing[str] = UNSET
    content_type: Missing[str] = UNSET
    size: int
    url: str
    proxy_url: str
    height: MissingOrNullable[int] = UNSET
    width: MissingOrNullable[int] = UNSET
    ephemeral: MissingOrNullable[bool] = UNSET
    duration_secs: Missing[float] = UNSET
    waveform: Missing[str] = UNSET


class ChannelMention(BaseModel):
    """Channel mention.

    see https://discord.com/developers/docs/resources/channel#channel-mention-object"""

    id: str
    guild_id: str
    type: ChannelType
    name: str


class AllowedMention(BaseModel):
    """The allowed mention field allows for more granular control over
    mentions without various hacks to the message
    content. This will always validate against message content to avoid
    phantom pings (e.g. to ping everyone, you must
    still have @everyone in the message content),
    and check against user/bot permissions.

    see https://discord.com/developers/docs/resources/channel#allowed-mentions-object"""

    parse: List[AllowedMentionType]
    """An array of allowed mention types to parse from the content."""
    roles: List[Snowflake]
    """Array of role_ids to mention (Max size of 100)"""
    users: List[Snowflake]
    """	Array of user_ids to mention (Max size of 100)"""
    replied_user: bool
    """For replies, whether to mention the author of the message
    being replied to (default false)"""


class RoleSubscriptionData(BaseModel):
    """Role subscription data.

    see https://discord.com/developers/docs/resources/channel#role-subscription-data-object
    """

    role_subscription_listing_id: str
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool


class ArchivedThreadsResponse(BaseModel):
    """Archived threads response.

    see https://discord.com/developers/docs/resources/channel#list-public-archived-threads-response-body
    """

    threads: List[Channel]
    members: List[ThreadMember]
    has_more: bool


class File(BaseModel):
    content: bytes
    filename: str


class AttachmentSend(BaseModel):
    """Attachment Send

    see https://discord.com/developers/docs/resources/channel#attachment-object"""

    filename: str
    description: Optional[str]


class MessageSend(BaseModel):
    """Message Send

    see https://discord.com/developers/docs/resources/channel#create-message"""

    content: Optional[str]
    nonce: Optional[Union[int, str]]
    tts: Optional[bool]
    embeds: Optional[List[Embed]]
    allowed_mentions: Optional[AllowedMention]
    message_reference: Optional[MessageReference]
    components: Optional[List[DirectComponent]]
    sticker_ids: Optional[List[Snowflake]]
    files: Optional[List[File]]
    attachments: Optional[List[AttachmentSend]]
    flags: Optional[MessageFlag]


class ModifyChannelParams(BaseModel):
    """Modify Channel Params

    see https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    name: Optional[str]
    type: Optional[ChannelType]
    position: Optional[int]
    topic: Optional[str]
    nsfw: Optional[bool]
    rate_limit_per_user: Optional[int]
    bitrate: Optional[int]
    user_limit: Optional[int]
    permission_overwrites: Optional[List[Overwrite]]
    parent_id: Optional[Snowflake]
    rtc_region: Optional[str]
    video_quality_mode: Optional[VideoQualityMode]
    default_auto_archive_duration: Optional[int]
    flags: Optional[ChannelFlags]
    available_tags: Optional[List[ForumTag]]
    default_reaction_emoji: Optional[DefaultReaction]
    default_thread_rate_limit_per_user: Optional[int]
    default_sort_order: Optional[SortOrderTypes]
    default_forum_layout: Optional[ForumLayoutTypes]


# Emoji
# see https://discord.com/developers/docs/resources/emoji


class Emoji(BaseModel):
    """Emoji Object

    see https://discord.com/developers/docs/resources/emoji#emoji-object"""

    id: Optional[str]
    """emoji id"""
    name: Optional[str]
    """emoji name(can be null only in reaction emoji objects)"""
    roles: Missing[List[Snowflake]] = UNSET
    """roles allowed to use this emoji"""
    user: Missing["User"] = UNSET
    """user that created this emoji"""
    require_colons: Missing[bool] = UNSET
    """whether this emoji must be wrapped in colons"""
    managed: Missing[bool] = UNSET
    """whether this emoji is managed"""
    animated: Missing[bool] = UNSET
    """whether this emoji is animated"""
    available: Missing[bool] = UNSET
    """whether this emoji can be used, may be false due to loss of Server Boosts"""


# Guild
# see https://discord.com/developers/docs/resources/guild
class Guild(BaseModel):
    """Guild

    see https://discord.com/developers/docs/resources/guild#guild-object"""

    id: Snowflake
    name: str
    icon: Optional[str] = Field(...)
    icon_hash: MissingOrNullable[str] = UNSET
    splash: Optional[str] = Field(...)
    discovery_splash: Optional[str]
    owner: Missing[bool] = UNSET
    owner_id: Snowflake
    permissions: Missing[str] = UNSET
    region: MissingOrNullable[str] = UNSET
    afk_channel_id: Optional[Snowflake] = Field(...)
    afk_timeout: int
    widget_enabled: Missing[bool] = UNSET
    widget_channel_id: MissingOrNullable[Snowflake] = UNSET
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    roles: List["Role"]
    emojis: List[Emoji]
    features: List[GuildFeature]
    mfa_level: MFALevel
    application_id: Optional[Snowflake] = Field(...)
    system_channel_id: Optional[Snowflake] = Field(...)
    system_channel_flags: SystemChannelFlags
    rules_channel_id: Optional[Snowflake] = Field(...)
    max_presences: Optional[int] = Field(...)
    max_members: Optional[int] = Field(...)
    vanity_url_code: Optional[str] = Field(...)
    description: Optional[str] = Field(...)
    banner: Optional[str] = Field(...)
    premium_tier: PremiumTier
    premium_subscription_count: Optional[int] = Field(...)
    preferred_locale: str
    public_updates_channel_id: Optional[Snowflake] = Field(...)
    max_video_channel_users: Missing[int] = UNSET
    max_stage_video_channel_users: Missing[int] = UNSET
    approximate_member_count: Missing[int] = UNSET
    approximate_presence_count: Missing[int] = UNSET
    welcome_screen: Missing["WelcomeScreen"] = UNSET
    nsfw_level: GuildNSFWLevel
    stickers: Missing[List["Sticker"]] = UNSET
    premium_progress_bar_enabled: bool


class CurrentUserGuild(BaseModel):
    """partial guild object for Get Current User Guilds API

    see https://discord.com/developers/docs/resources/user#get-current-user-guilds"""

    id: Snowflake
    name: str
    icon: Optional[str] = Field(...)
    owner: Missing[bool] = UNSET
    permissions: Missing[str] = UNSET
    features: List[GuildFeature]


class UnavailableGuild(BaseModel):
    """Unavailable Guild

    see https://discord.com/developers/docs/resources/guild#unavailable-guild-object"""

    id: Snowflake
    unavailable: Literal[True]


class GuildPreview(BaseModel):
    """Guild Preview

    see https://discord.com/developers/docs/resources/guild#guild-preview-object"""

    id: Snowflake
    name: str
    icon: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    emojis: List[Emoji]
    features: List[GuildFeature]
    approximate_member_count: int
    approximate_presence_count: int
    description: Optional[str]
    stickers: List["Sticker"]


class GuildWidgetSettings(BaseModel):
    """Guild Widget Settings

    see https://discord.com/developers/docs/resources/guild#guild-widget-settings-object
    """

    enabled: bool
    channel_id: Optional[Snowflake]


class GuildWidget(BaseModel):
    """Guild Widget

    see https://discord.com/developers/docs/resources/guild#guild-widget-object"""

    id: Snowflake
    name: str
    instant_invite: Optional[str]
    channels: List["Channel"]  # partial channel objects
    members: List["User"]  # partial user objects
    presence_count: int


class GuildMember(BaseModel):
    """Guild Member

    see https://discord.com/developers/docs/resources/guild#guild-member-object"""

    user: Missing["User"] = UNSET
    nick: MissingOrNullable[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    roles: List[Snowflake]
    joined_at: datetime.datetime
    premium_since: MissingOrNullable[datetime.datetime] = UNSET
    deaf: Missing[bool] = UNSET
    mute: Missing[bool] = UNSET
    flags: GuildMemberFlags
    pending: Missing[bool] = UNSET
    permissions: Missing[str] = UNSET
    communication_disabled_until: MissingOrNullable[datetime.datetime] = UNSET


class Integration(BaseModel):
    """Integration

    see https://discord.com/developers/docs/resources/guild#integration-object"""

    id: Snowflake
    name: str
    type: str
    enabled: bool
    syncing: Missing[bool] = UNSET
    role_id: Missing[Snowflake] = UNSET
    enable_emoticons: Missing[bool] = UNSET
    expire_behavior: Missing[IntegrationExpireBehaviors] = UNSET
    expire_grace_period: Missing[int] = UNSET
    user: Missing["User"] = UNSET
    account: Optional["IntegrationAccount"]
    synced_at: Missing[datetime.datetime] = UNSET
    subscriber_count: Missing[int] = UNSET
    revoked: Missing[bool] = UNSET
    application: Missing["IntegrationApplication"] = UNSET
    scopes: Missing[List[str]] = UNSET  # TODO: OAuth2 scopes


class IntegrationAccount(BaseModel):
    """Integration Account

    see https://discord.com/developers/docs/resources/guild#integration-account-object
    """

    id: str
    name: str


class IntegrationApplication(BaseModel):
    """Integration Application

    see https://discord.com/developers/docs/resources/guild#integration-application-object
    """

    id: Snowflake
    name: str
    icon: Optional[str]
    description: str
    bot: Missing["User"] = UNSET


class Ban(BaseModel):
    """Ban

    see https://discord.com/developers/docs/resources/guild#ban-object"""

    reason: Optional[str]
    user: "User"


class WelcomeScreen(BaseModel):
    """Welcome screen.

    see https://discord.com/developers/docs/resources/guild#welcome-screen-object"""

    description: Optional[str]
    welcome_channels: List["WelcomeScreenChannel"]


class WelcomeScreenChannel(BaseModel):
    """Welcome screen channel.

    see https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-channel-structure
    """

    channel_id: Snowflake
    description: str
    emoji_id: Optional[Snowflake]
    emoji_name: Optional[str]


class GuildOnboarding(BaseModel):
    """Guild onboarding.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object"""

    guild_id: Snowflake
    prompts: List["OnboardingPrompt"]
    default_channel_ids: List[Snowflake]
    enabled: bool


class OnboardingPrompt(BaseModel):
    """Onboarding prompt.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-prompt-structure
    """

    id: Snowflake
    type: OnboardingPromptType
    options: List["OnboardingPromptOption"]
    title: str
    single_select: bool
    required: bool
    in_onboarding: bool


class OnboardingPromptOption(BaseModel):
    """Onboarding prompt option.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-prompt-option-structure
    """

    id: Snowflake
    channel_ids: List[Snowflake]
    role_ids: List[Snowflake]
    emoji: Emoji
    title: str
    description: Optional[str]


class MembershipScreening(BaseModel):
    """Membership screening.

    see https://discord.com/developers/docs/resources/guild#membership-screening-object
    """


class CreateGuildParams(BaseModel):
    """Create Guild Params

    see https://discord.com/developers/docs/resources/guild#create-guild"""

    name: str
    region: Optional[str]
    icon: Optional[str]
    verification_level: Optional[VerificationLevel]
    default_message_notifications: Optional[DefaultMessageNotificationLevel]
    explicit_content_filter: Optional[ExplicitContentFilterLevel]
    roles: Optional[List["Role"]]
    channels: Optional[List[Channel]]
    afk_channel_id: Optional[Snowflake]
    afk_timeout: Optional[int]
    system_channel_id: Optional[Snowflake]
    system_channel_flags: Optional[SystemChannelFlags]


class ModifyGuildParams(BaseModel):
    """Modify Guild Params

    see https://discord.com/developers/docs/resources/guild#modify-guild"""

    name: str
    region: Optional[str]
    verification_level: Optional[VerificationLevel]
    default_message_notifications: Optional[DefaultMessageNotificationLevel]
    explicit_content_filter: Optional[ExplicitContentFilterLevel]
    afk_channel_id: Optional[Snowflake]
    afk_timeout: Optional[int]
    icon: Optional[str]
    owner_id: Optional[Snowflake]
    splash: Optional[str]
    discovery_splash: Optional[str]
    banner: Optional[str]
    system_channel_id: Optional[Snowflake]
    system_channel_flags: Optional[SystemChannelFlags]
    rules_channel_id: Optional[Snowflake]
    public_updates_channel_id: Optional[Snowflake]
    preferred_locale: Optional[str]
    features: Optional[List[GuildFeature]]
    description: Optional[str]
    premium_progress_bar_enabled: Optional[bool]


class CreateGuildChannelParams(BaseModel):
    """Create Guild Channel Params

    see https://discord.com/developers/docs/resources/guild#create-guild-channel"""

    name: str
    type: Optional[ChannelType]
    topic: Optional[str]
    bitrate: Optional[int]
    user_limit: Optional[int]
    rate_limit_per_user: Optional[int]
    position: Optional[int]
    permission_overwrites: Optional[List["Overwrite"]]
    parent_id: Optional[Snowflake]
    nsfw: Optional[bool]
    rtc_region: Optional[str]
    video_quality_mode: Optional[VideoQualityMode]
    default_auto_archive_duration: Optional[int]
    default_reaction_emoji: Optional[DefaultReaction]
    available_tags: Optional[List[ForumTag]]
    default_sort_order: Optional[SortOrderTypes]


class ListActiveGuildThreadsResponse(BaseModel):
    """List Active Guild Threads Response

    see https://discord.com/developers/docs/resources/guild#list-active-guild-threads"""

    threads: List[Channel]
    members: List[ThreadMember]


class ModifyGuildWelcomeScreenParams(BaseModel):
    """Modify Guild Welcome Screen Params

    see https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
    """

    enabled: Optional[bool]
    welcome_channels: Optional[List[WelcomeScreenChannel]]
    description: Optional[str]


# Guild Scheduled Event
# see https://discord.com/developers/docs/resources/guild-scheduled-event


class GuildScheduledEvent(BaseModel):
    """Guild Scheduled Event

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object
    """

    id: Snowflake
    guild_id: Snowflake
    channel_id: Optional[Snowflake]
    creator_id: MissingOrNullable[Snowflake] = UNSET
    name: str
    description: MissingOrNullable[str] = UNSET
    scheduled_start_time: datetime.datetime
    scheduled_end_time: Optional[datetime.datetime]
    privacy_level: GuildScheduledEventPrivacyLevel
    status: GuildScheduledEventStatus
    entity_type: GuildScheduledEventEntityType
    entity_id: Optional[Snowflake]
    entity_metadata: Optional["GuildScheduledEventEntityMetadata"]
    creator: Missing["User"] = UNSET
    user_count: Missing[int] = UNSET
    image: MissingOrNullable[str] = UNSET


class GuildScheduledEventEntityMetadata(BaseModel):
    """Guild Scheduled Event Entity Metadata

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: Missing[str] = UNSET


class GuildScheduledEventUser(BaseModel):
    """Guild Scheduled Event User

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-user-object
    """

    guild_scheduled_event_id: Snowflake
    user: "User"
    member: Missing[GuildMember] = UNSET


class CreateGuildScheduledEventParams(BaseModel):
    """Create Guild Scheduled Event Params

    see https://discord.com/developers/docs/resources/guild-scheduled-event#create-guild-scheduled-event-json-params
    """

    channel_id: Optional[Snowflake]
    entity_metadata: Optional[GuildScheduledEventEntityMetadata]
    name: str
    privacy_level: GuildScheduledEventPrivacyLevel
    scheduled_start_time: datetime.datetime  # ISO8601 timestamp
    scheduled_end_time: Optional[datetime.datetime]  # ISO8601 timestamp
    description: Optional[str]
    entity_type: GuildScheduledEventEntityType
    image: Optional[str]


class ModifyGuildScheduledEventParams(BaseModel):
    """Modify Guild Scheduled Event Params

    see https://discord.com/developers/docs/resources/guild-scheduled-event#modify-guild-scheduled-event-json-params
    """

    channel_id: Optional[Snowflake]
    entity_metadata: Optional[GuildScheduledEventEntityMetadata]
    name: Optional[str]
    privacy_level: Optional[GuildScheduledEventPrivacyLevel]
    scheduled_start_time: Optional[datetime.datetime]  # ISO8601 timestamp
    scheduled_end_time: Optional[datetime.datetime]  # ISO8601 timestamp
    description: Optional[str]
    entity_type: Optional[GuildScheduledEventEntityType]
    status: Optional[GuildScheduledEventStatus]
    image: Optional[str]


# Guild Template
# see https://discord.com/developers/docs/resources/guild-template
class GuildTemplate(BaseModel):
    """Guild Template

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object
    """

    code: str
    name: str
    description: Optional[str]
    usage_count: int
    creator_id: str
    creator: "User"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    source_guild_id: Snowflake
    serialized_source_guild: "Guild"  # partial guild object
    is_dirty: Optional[bool]


# Invite
# see https://discord.com/developers/docs/resources/invite
class Invite(BaseModel):
    """Invite

    see https://discord.com/developers/docs/resources/invite#invite-object"""

    code: str
    guild: Missing[Guild] = UNSET  # partial guild object
    channel: Optional[Channel] = Field(...)  # partial channel object
    inviter: Missing["User"] = UNSET
    target_type: Missing["InviteTargetType"] = UNSET
    target_user: Missing["User"] = UNSET
    # partial application object
    target_application: Missing["Application"] = UNSET
    approximate_presence_count: Missing[int] = UNSET
    approximate_member_count: Missing[int] = UNSET
    expires_at: Missing[datetime.datetime] = UNSET
    stage_instance: Missing["StageInstance"] = UNSET
    guild_scheduled_event: Missing["GuildScheduledEvent"] = UNSET


class InviteMetadata(BaseModel):
    """Invite Metadata

    see https://discord.com/developers/docs/resources/invite#invite-metadata-object"""

    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: datetime.datetime


class InviteStageInstance(BaseModel):
    """Invite Stage Instance

    see https://discord.com/developers/docs/resources/invite#invite-stage-instance-object
    """

    members: List[GuildMember]  # partial guild member objects
    participant_count: int
    speaker_count: int
    topic: str


# Stage Instance
# see https://discord.com/developers/docs/resources/stage-instance


class StageInstance(BaseModel):
    """Stage Instance

    see https://discord.com/developers/docs/resources/stage-instance#stage-instance-object
    """

    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: StagePrivacyLevel
    discoverable_disabled: bool
    guild_scheduled_event_id: Optional[Snowflake]


# Sticker
# see https://discord.com/developers/docs/resources/sticker
class Sticker(BaseModel):
    """Sticker Object

    see https://discord.com/developers/docs/resources/sticker#sticker-object"""

    id: Snowflake
    pack_id: Missing[Snowflake] = UNSET
    name: str
    description: Optional[str] = Field(...)
    tags: str
    asset: Missing[str] = UNSET
    type: StickerType
    format_type: StickerFormatType
    available: Missing[bool] = UNSET
    guild_id: Missing[Snowflake] = UNSET
    user: Missing["User"] = UNSET
    sort_value: Missing[int] = UNSET


class StickerItem(BaseModel):
    """Sticker item.

    see https://discord.com/developers/docs/resources/sticker#sticker-item-object"""

    id: Snowflake
    name: str
    format_type: StickerFormatType


class StickerPack(BaseModel):
    """Sticker pack.

    see https://discord.com/developers/docs/resources/sticker#sticker-pack-object"""

    id: Snowflake
    stickers: List[Sticker]
    name: str
    sku_id: Snowflake
    cover_sticker_id: Missing[Snowflake] = UNSET
    description: str
    banner_asset_id: Missing[Snowflake] = UNSET


# User
# see https://discord.com/developers/docs/resources/user
class User(BaseModel):
    """User

    see https://discord.com/developers/docs/resources/user#user-object"""

    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str] = Field(...)
    bot: Missing[bool] = UNSET
    system: Missing[bool] = UNSET
    mfa_enabled: Missing[bool] = UNSET
    banner: MissingOrNullable[str] = UNSET
    accent_color: MissingOrNullable[int] = UNSET
    locale: Missing[str] = UNSET
    verified: Missing[bool] = UNSET
    email: MissingOrNullable[str] = UNSET
    flags: Missing[int] = UNSET
    premium_type: Missing[PremiumType] = UNSET
    public_flags: Missing[UserFlags] = UNSET


class Connection(BaseModel):
    """Connection

    see https://discord.com/developers/docs/resources/user#connection-object"""

    id: str
    name: str
    type: ConnectionServiceType
    revoked: Missing[bool] = UNSET
    integrations: Missing[List["Integration"]] = UNSET
    verified: bool
    friend_sync: bool
    show_activity: bool
    two_way_link: bool
    visibility: VisibilityType


class ApplicationRoleConnection(BaseModel):
    """Application Role Connection

    see https://discord.com/developers/docs/resources/user#application-role-connection-object
    """

    platform_name: Optional[str] = Field(...)
    platform_username: Optional[str] = Field(...)
    metadata: dict  # object


# Voice
# see https://discord.com/developers/docs/resources/voice
class VoiceState(BaseModel):
    """Voice State

    see https://discord.com/developers/docs/resources/voice#voice-state-object"""

    guild_id: Missing[Snowflake] = UNSET
    channel_id: Optional[Snowflake] = Field(...)
    user_id: Snowflake
    member: Missing[GuildMember] = UNSET
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: Missing[bool] = UNSET
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: Optional[datetime.datetime] = Field(...)


class VoiceRegion(BaseModel):
    """Voice Region

    see https://discord.com/developers/docs/resources/voice#voice-region-object"""

    id: str
    name: str
    optimal: bool
    deprecated: bool
    custom: bool


# Webhook
# see https://discord.com/developers/docs/resources/webhook
class Webhook(BaseModel):
    """Used to represent a webhook.

    see https://discord.com/developers/docs/resources/webhook#webhook-object"""

    id: Snowflake
    type: WebhookType
    guild_id: MissingOrNullable[Snowflake] = UNSET
    channel_id: Optional[Snowflake] = Field(...)
    user: Missing[User] = UNSET
    name: Optional[str] = Field(...)
    avatar: Optional[str] = Field(...)
    token: Missing[str] = UNSET
    application_id: Optional[Snowflake] = Field(...)
    source_guild: MissingOrNullable[Guild] = UNSET  # partial guild object
    # partial channel object
    source_channel: MissingOrNullable[Channel] = UNSET
    url: Missing[str] = UNSET


class ExecuteWebhookParams(BaseModel):
    """Execute Webhook Parameters

    see https://discord.com/developers/docs/resources/webhook#execute-webhook"""

    content: Optional[str] = None
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    tts: Optional[bool] = None
    embeds: Optional[List[Embed]] = None
    allowed_mentions: Optional[AllowedMention] = None
    components: Optional[List[DirectComponent]] = None
    files: Optional[List[File]] = None
    attachments: Optional[List[AttachmentSend]] = None
    flags: Optional[MessageFlag] = None
    thread_name: Optional[str] = None


# gateway
# see https://discord.com/developers/docs/topics/gateway


class Gateway(BaseModel):
    """Get Gateway Response

    see https://discord.com/developers/docs/topics/gateway#get-gateway"""

    url: str


class GatewayBot(BaseModel):
    """Get Gateway Bot Response

    see https://discord.com/developers/docs/topics/gateway#get-gateway-bot"""

    url: str
    shards: int
    session_start_limit: "SessionStartLimit"


class SessionStartLimit(BaseModel):
    """Session start limit

    see https://discord.com/developers/docs/topics/gateway#session-start-limit-object"""

    total: int
    remaining: int
    reset_after: int
    max_concurrency: int


# gateway events
# see https://discord.com/developers/docs/topics/gateway-events
class Identify(BaseModel):
    """Identify Payload data

    see https://discord.com/developers/docs/topics/gateway-events#identify"""

    token: str
    properties: "IdentifyConnectionProperties"
    compress: Missing[bool] = UNSET
    large_threshold: Missing[int] = UNSET
    shard: Missing[List[int]] = UNSET
    presence: Missing["PresenceUpdate"] = UNSET
    intents: int


class IdentifyConnectionProperties(BaseModel):
    """Identify Connection Properties

    see https://discord.com/developers/docs/topics/gateway-events#identify-identify-connection-properties
    """

    os: str
    browser: str
    device: str


class Resume(BaseModel):
    """Resume Payload data

    see https://discord.com/developers/docs/topics/gateway-events#resume"""

    token: str
    session_id: str
    seq: int


class RequestGuildMembers(BaseModel):
    """Request Guild Members Payload data

    see https://discord.com/developers/docs/topics/gateway-events#request-guild-members
    """

    guild_id: Snowflake
    query: Missing[str] = UNSET
    limit: int
    presences: Missing[bool] = UNSET
    user_ids: Missing[Union[Snowflake, List[Snowflake]]] = UNSET
    nonce: Missing[str] = UNSET


class UpdateVoiceState(BaseModel):
    """Update Voice State Payload data

    see https://discord.com/developers/docs/topics/gateway-events#update-voice-state"""

    guild_id: Snowflake
    channel_id: Optional[Snowflake] = Field(...)
    self_mute: bool
    self_deaf: bool


class UpdatePresence(BaseModel):
    """Update Presence Payload data

    see https://discord.com/developers/docs/topics/gateway-events#update-presence"""

    since: Optional[int] = Field(...)
    activities: List["Activity"]
    status: UpdatePresenceStatusType
    afk: bool


class Hello(BaseModel):
    """Hello Payload data

    see https://discord.com/developers/docs/topics/gateway-events#hello"""

    heartbeat_interval: int


class ApplicationReady(BaseModel):
    """partial application object for ready event."""

    id: str
    flags: int


class Ready(BaseModel):
    """Ready Payload data

    see https://discord.com/developers/docs/topics/gateway-events#ready"""

    v: int
    user: User
    guilds: List[UnavailableGuild]
    session_id: str
    resume_gateway_url: str
    shard: Missing[List[int]] = UNSET
    application: ApplicationReady


class AutoModerationRuleCreate(AutoModerationRule):
    """Auto Moderation Rule Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-create
    """


class AutoModerationRuleUpdate(AutoModerationRule):
    """Auto Moderation Rule Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-update
    """


class AutoModerationRuleDelete(AutoModerationRule):
    """Auto Moderation Rule Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-delete
    """


class AutoModerationActionExecution(BaseModel):
    """Auto Moderation Action Execution Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-action-execution
    """

    guild_id: Snowflake
    action: AutoModerationAction
    rule_id: Snowflake
    rule_trigger_type: TriggerType
    user_id: Snowflake
    channel_id: Missing[Snowflake] = UNSET
    message_id: Missing[Snowflake] = UNSET
    alert_system_message_id: Missing[Snowflake] = UNSET
    content: str
    matched_keyword: Optional[str] = Field(...)
    matched_content: Optional[str] = Field(...)


class ChannelCreate(Channel):
    """Channel Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-create"""


class ChannelUpdate(Channel):
    """Channel Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-update"""


class ChannelDelete(Channel):
    """Channel Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-delete"""


class ThreadCreate(Channel):
    """Thread Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-create"""

    newly_created: Missing[bool] = UNSET
    thread_member: Missing[ThreadMember] = UNSET


class ThreadUpdate(Channel):
    """Thread Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-update"""


class ThreadDelete(BaseModel):
    """Thread Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-delete"""

    id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    type: ChannelType


class ThreadListSync(BaseModel):
    """Thread List Sync Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-list-sync-thread-list-sync-event
    """

    guild_id: Snowflake
    channel_ids: Missing[List[Snowflake]] = UNSET
    threads: List[Channel]
    members: List[ThreadMember]


class ThreadMemberUpdate(ThreadMember):
    """Thread Member Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-member-update
    """

    guild_id: Snowflake


class ThreadMembersUpdate(BaseModel):
    """Thread Members Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#thread-members-update-thread-members-update-event
    """

    id: Snowflake
    guild_id: Snowflake
    member_count: int
    added_members: Missing[List[ThreadMember]] = UNSET
    removed_member_ids: Missing[List[Snowflake]] = UNSET


class ChannelPinsUpdate(BaseModel):
    """Channel Pins Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#channel-pins-update"""

    guild_id: Missing[Snowflake] = UNSET
    channel_id: Snowflake
    last_pin_timestamp: Missing[Optional[datetime.datetime]] = UNSET


class GuildCreate(BaseModel):
    """Guild Create Event's Guild inner can be either Guild or UnavailableGuild

    see https://discord.com/developers/docs/topics/gateway-events#guild-create"""

    id: Snowflake
    unavailable: Missing[bool] = UNSET
    name: Missing[str] = UNSET
    icon: MissingOrNullable[str] = UNSET
    icon_hash: MissingOrNullable[str] = UNSET
    splash: MissingOrNullable[str] = UNSET
    discovery_splash: MissingOrNullable[str] = UNSET
    owner: Missing[bool] = UNSET
    owner_id: Missing[Snowflake] = UNSET
    permissions: Missing[str] = UNSET
    region: MissingOrNullable[str] = UNSET
    afk_channel_id: MissingOrNullable[Snowflake] = UNSET
    afk_timeout: Missing[int] = UNSET
    widget_enabled: Missing[bool] = UNSET
    widget_channel_id: MissingOrNullable[Snowflake] = UNSET
    verification_level: Missing[VerificationLevel] = UNSET
    default_message_notifications: Missing[DefaultMessageNotificationLevel] = UNSET
    explicit_content_filter: Missing[ExplicitContentFilterLevel] = UNSET
    roles: Missing[List["Role"]] = UNSET
    emojis: Missing[List[Emoji]] = UNSET
    features: Missing[List[GuildFeature]] = UNSET
    mfa_level: Missing[MFALevel] = UNSET
    application_id: MissingOrNullable[Snowflake] = UNSET
    system_channel_id: MissingOrNullable[Snowflake] = UNSET
    system_channel_flags: Missing[SystemChannelFlags] = UNSET
    rules_channel_id: MissingOrNullable[Snowflake] = UNSET
    max_presences: MissingOrNullable[int] = UNSET
    max_members: MissingOrNullable[int] = UNSET
    vanity_url_code: MissingOrNullable[str] = UNSET
    description: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET
    premium_tier: Missing[PremiumTier] = UNSET
    premium_subscription_count: MissingOrNullable[int] = UNSET
    preferred_locale: Missing[str] = UNSET
    public_updates_channel_id: MissingOrNullable[Snowflake] = UNSET
    max_video_channel_users: Missing[int] = UNSET
    max_stage_video_channel_users: Missing[int] = UNSET
    approximate_member_count: Missing[int] = UNSET
    approximate_presence_count: Missing[int] = UNSET
    welcome_screen: Missing[WelcomeScreen] = UNSET
    nsfw_level: Missing[GuildNSFWLevel] = UNSET
    stickers: Missing[List[Sticker]] = UNSET
    premium_progress_bar_enabled: Missing[bool] = UNSET
    joined_at: Missing[str] = UNSET
    large: Missing[bool] = UNSET
    member_count: Missing[int] = UNSET
    voice_states: Missing[List["VoiceState"]] = UNSET
    members: Missing[List["GuildMember"]] = UNSET
    channels: Missing[List["Channel"]] = UNSET
    threads: Missing[List["Channel"]] = UNSET
    presences: Missing[
        List["PresenceUpdate"]
    ] = UNSET  # partial presence update objects
    stage_instances: Missing[List["StageInstance"]] = UNSET
    guild_scheduled_events: Missing[List["GuildScheduledEvent"]] = UNSET


class GuildUpdate(Guild):
    """Guild Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-update"""


class GuildDelete(UnavailableGuild):
    """Guild Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-delete"""


class GuildAuditLogEntryCreate(AuditLogEntry):
    """Guild Audit Log Entry Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-audit-log-entry-create
    """


class GuildBanAdd(BaseModel):
    """Guild Ban Add Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-ban-add"""

    guild_id: Snowflake
    user: User


class GuildBanRemove(BaseModel):
    """Guild Ban Remove Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-ban-remove"""

    guild_id: Snowflake
    user: User


class GuildEmojisUpdate(BaseModel):
    """Guild Emojis Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-emojis-update"""

    guild_id: Snowflake
    emojis: List[Emoji]


class GuildStickersUpdate(BaseModel):
    """Guild Stickers Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-stickers-update
    """

    guild_id: Snowflake
    stickers: List[Sticker]


class GuildIntegrationsUpdate(BaseModel):
    """Guild Integrations Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-integrations-update
    """

    guild_id: Snowflake


class GuildMemberAdd(GuildMember):
    """Guild Member Add Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-add"""

    guild_id: Snowflake


class GuildMemberRemove(BaseModel):
    """Guild Member Remove Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-remove"""

    guild_id: Snowflake
    user: User


class GuildMemberUpdate(BaseModel):
    """Guild Member Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-update"""

    guild_id: Snowflake
    roles: List[Snowflake]
    user: User
    nick: MissingOrNullable[str] = UNSET
    joined_at: Optional[datetime.datetime] = Field(...)
    premium_since: MissingOrNullable[datetime.datetime] = UNSET
    deaf: Missing[bool] = UNSET
    mute: Missing[bool] = UNSET
    pending: Missing[bool] = UNSET
    communication_disabled_until: MissingOrNullable[datetime.datetime] = UNSET


class GuildMembersChunk(BaseModel):
    """Guild Members Chunk Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-members-chunk"""

    guild_id: Snowflake
    members: List[GuildMember]
    chunk_index: int
    chunk_count: int
    not_found: Missing[List[Snowflake]] = UNSET
    presences: Missing[List["PresenceUpdate"]] = UNSET
    nonce: Missing[str] = UNSET


class GuildRoleCreate(BaseModel):
    """Guild Role Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-create"""

    guild_id: Snowflake
    role: "Role"


class GuildRoleUpdate(BaseModel):
    """Guild Role Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-update"""

    guild_id: Snowflake
    role: "Role"


class GuildRoleDelete(BaseModel):
    """Guild Role Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-delete"""

    guild_id: Snowflake
    role_id: Snowflake


class GuildScheduledEventCreate(GuildScheduledEvent):
    """Guild Scheduled Event Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-create
    """


class GuildScheduledEventUpdate(GuildScheduledEvent):
    """Guild Scheduled Event Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-update
    """


class GuildScheduledEventDelete(GuildScheduledEvent):
    """Guild Scheduled Event Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-delete
    """


class GuildScheduledEventUserAdd(BaseModel):
    """Guild Scheduled Event User Add Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-add-guild-scheduled-event-user-add-event-fields
    """

    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


class GuildScheduledEventUserRemove(BaseModel):
    """Guild Scheduled Event User Remove Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-remove-guild-scheduled-event-user-remove-event-fields
    """

    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


class IntegrationCreate(Integration):
    """Integration Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#integration-create"""

    guild_id: Snowflake


class IntegrationUpdate(Integration):
    """Integration Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#integration-update"""

    guild_id: Snowflake


class IntegrationDelete(BaseModel):
    """Integration Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#integration-delete"""

    id: Snowflake
    guild_id: Snowflake
    application_id: Missing[Snowflake] = UNSET


class InviteCreate(BaseModel):
    """Invite Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#invite-create"""

    channel_id: Snowflake
    code: str
    created_at: datetime.datetime
    guild_id: Missing[Snowflake] = UNSET
    inviter: Missing[User] = UNSET
    max_age: int
    max_uses: int
    target_type: Missing[InviteTargetType] = UNSET
    target_user: Missing[User] = UNSET
    target_application: Missing[Application] = UNSET
    temporary: bool
    uses: int


class InviteDelete(BaseModel):
    """Invite Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#invite-delete"""

    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    code: str


class MessageCreate(MessageGet):
    """Message Create Event Fields

    Sent when a message is created. The inner payload is a message object

    see https://discord.com/developers/docs/topics/gateway-events#message-create
    """

    guild_id: Missing[Snowflake] = UNSET
    member: Missing[GuildMember] = UNSET  # partial member object
    mentions: List[User]


class MessageUpdate(MessageGet):
    """Message Update Event Fields

    Unlike creates, message updates may contain only a subset of the full
    message object payload(but will always contain an ID and channel_id).

    see https://discord.com/developers/docs/topics/gateway-events#message-update
    """

    guild_id: Missing[str] = UNSET
    member: Missing[GuildMember] = UNSET
    mentions: Missing[List[User]] = UNSET
    id: Snowflake
    channel_id: Snowflake
    author: Missing["User"] = UNSET
    content: Missing[str] = UNSET
    timestamp: Missing[datetime.datetime] = UNSET
    edited_timestamp: MissingOrNullable[datetime.datetime] = UNSET
    tts: Missing[bool] = UNSET
    mention_everyone: Missing[bool] = UNSET
    mention_roles: Missing[List[str]] = UNSET
    mention_channels: Missing[List["ChannelMention"]] = UNSET
    attachments: Missing[List["Attachment"]] = UNSET
    embeds: Missing[List["Embed"]] = UNSET
    reactions: Missing[List["Reaction"]] = UNSET
    nonce: Missing[Union[int, str]] = UNSET
    pinned: Missing[bool] = UNSET
    webhook_id: Missing[Snowflake] = UNSET
    type: Missing[MessageType] = UNSET
    activity: Missing["MessageActivity"] = UNSET
    application: Missing[Application] = UNSET
    application_id: Missing[Snowflake] = UNSET
    message_reference: Missing["MessageReference"] = UNSET
    flags: Missing[MessageFlag] = UNSET
    referenced_message: MissingOrNullable["MessageGet"] = UNSET
    interaction: Missing[MessageInteraction] = UNSET
    thread: Missing[Channel] = UNSET
    components: Missing[List[DirectComponent]] = UNSET
    sticker_items: Missing[List["StickerItem"]] = UNSET
    stickers: Missing[List["Sticker"]] = UNSET
    position: Missing[int] = UNSET
    role_subscription_data: Missing["RoleSubscriptionData"] = UNSET


class MessageDelete(BaseModel):
    """Message Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#message-delete
    """

    id: Snowflake
    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET


class MessageDeleteBulk(BaseModel):
    """Message Delete Bulk Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#message-delete-bulk
    """

    ids: List[Snowflake]
    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET


class MessageReactionAdd(BaseModel):
    """Message Reaction Add Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-add
    """

    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    member: Missing[GuildMember] = UNSET
    emoji: Emoji  # partial emoji object


class MessageReactionRemove(BaseModel):
    """Message Reaction Remove Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove
    """

    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    emoji: Emoji  # partial emoji object


class MessageReactionRemoveAll(BaseModel):
    """Message Reaction Remove Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-all
    """

    channel_id: Snowflake
    message_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET


class MessageReactionRemoveEmoji(BaseModel):
    """Message Reaction Remove Emoji Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-emoji
    """

    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    message_id: Snowflake
    emoji: Emoji  # partial emoji object


class PresenceUpdateUser(User):
    """Presence Update User Fields

    see https://discord.com/developers/docs/topics/gateway-events#presence-update"""

    id: Snowflake
    username: Missing[str] = UNSET
    discriminator: Missing[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    bot: Missing[bool] = UNSET
    system: Missing[bool] = UNSET
    mfa_enabled: Missing[bool] = UNSET
    banner: MissingOrNullable[str] = UNSET
    accent_color: MissingOrNullable[int] = UNSET
    locale: Missing[str] = UNSET
    verified: Missing[bool] = UNSET
    email: MissingOrNullable[str] = UNSET
    flags: Missing[int] = UNSET
    premium_type: Missing[PremiumType] = UNSET
    public_flags: Missing[UserFlags] = UNSET


class PresenceUpdate(BaseModel):
    """Presence Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#presence-update
    """

    user: PresenceUpdateUser
    guild_id: Missing[Snowflake] = UNSET
    status: PresenceStatus
    activities: List["Activity"]
    client_status: "ClientStatus"


class ClientStatus(BaseModel):
    """Client Status

    see https://discord.com/developers/docs/topics/gateway-events#client-status-object
    """

    desktop: Missing[str] = UNSET
    mobile: Missing[str] = UNSET
    web: Missing[str] = UNSET


class Activity(BaseModel):
    """Activity

    see https://discord.com/developers/docs/topics/gateway-events#activity-object"""

    name: str
    type: ActivityType
    url: MissingOrNullable[str] = UNSET
    created_at: int
    timestamps: Missing["ActivityTimestamps"] = UNSET
    application_id: Missing[Snowflake] = UNSET
    details: MissingOrNullable[str] = UNSET
    state: MissingOrNullable[str] = UNSET
    emoji: MissingOrNullable["ActivityEmoji"] = UNSET
    party: Missing["ActivityParty"] = UNSET
    assets: Missing["ActivityAssets"] = UNSET
    secrets: Missing["ActivitySecrets"] = UNSET
    instance: Missing[bool] = UNSET
    flags: Missing[ActivityFlags] = UNSET
    buttons: Missing[List["ActivityButtons"]] = UNSET


class ActivityTimestamps(BaseModel):
    """Activity Timestamps

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-types
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
    size: Missing[Tuple[int, int]] = UNSET


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


class TypingStart(BaseModel):
    """Typing Start Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#typing-start
    """

    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    user_id: Snowflake
    timestamp: datetime.datetime
    member: Missing[GuildMember] = UNSET


class UserUpdate(User):
    """User Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#user-update"""


class VoiceStateUpdate(VoiceState):
    """Voice State Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#voice-state-update
    """


class VoiceServerUpdate(BaseModel):
    """Voice Server Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#voice-server-update
    """

    token: str
    guild_id: Snowflake
    endpoint: Optional[str] = Field(...)


class WebhooksUpdate(BaseModel):
    """Webhooks Update Event Fields

    Sent when a guild channel's webhook is created, updated, or deleted.

    see https://discord.com/developers/docs/topics/gateway-events#webhooks-update
    """

    guild_id: Snowflake
    channel_id: Snowflake


class InteractionCreate(Interaction):
    """Interaction Create Event Fields

    Sent when a user uses an Application Command or Message Component.
    Inner payload is an Interaction.

    see https://discord.com/developers/docs/topics/gateway-events#interaction-create
    """


class StageInstanceCreate(StageInstance):
    """Stage Instance Create Event Fields

    Sent when a Stage instance is created (i.e. the Stage is now "live").
    Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-create
    """


class StageInstanceUpdate(StageInstance):
    """Stage Instance Update Event Fields

    Sent when a Stage instance has been updated. Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-update
    """


class StageInstanceDelete(StageInstance):
    """Stage Instance Delete Event Fields

    Sent when a Stage instance has been deleted (i.e. the Stage has been closed).
    Inner payload is a Stage instance

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-delete
    """


# Permissions
# see https://discord.com/developers/docs/topics/permissions
class Role(BaseModel):
    """Role

    see https://discord.com/developers/docs/topics/permissions#role-object"""

    id: Snowflake
    name: str
    color: int
    hoist: bool
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: Missing["RoleTags"] = UNSET


class RoleTags(BaseModel):
    """Role tags.

    see https://discord.com/developers/docs/topics/permissions#role-object-role-tags-structure
    """

    bot_id: Missing[Snowflake] = UNSET
    integration_id: Missing[Snowflake] = UNSET
    premium_subscriber: Missing[None] = UNSET
    subscription_listing_id: Missing[Snowflake] = UNSET
    available_for_purchase: Missing[None] = UNSET
    guild_connections: Missing[None] = UNSET


# Teams
# see https://discord.com/developers/docs/topics/teams
class Team(BaseModel):
    """Team.

    see https://discord.com/developers/docs/topics/teams#data-models-team-object"""

    icon: Optional[str] = Field(...)
    id: str
    members: List["TeamMember"]
    name: str
    owner_user_id: Snowflake


class TeamMember(BaseModel):
    """Team member.

    see https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    membership_state: MembershipState
    permissions: List[str]
    team_id: Snowflake
    user: "TeamMemberUser"


class TeamMemberUser(BaseModel):
    """partial user object for TeamMember"""

    avatar: Optional[str]
    discriminator: str
    id: Snowflake
    username: str


class AuthorizationResponse(BaseModel):
    """Get Current Authorization Information Response

    see https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
    """

    application: Application  # partial application object
    scopes: List[str]
    expires: datetime.datetime
    user: Missing[User] = UNSET


for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, BaseModel):
        obj.update_forward_refs()

__all__ = [
    "BaseModel",
    "Snowflake",
    "SnowflakeType",
    "ApplicationCommand",
    "ApplicationCommandCreate",
    "CommandOptionBase",
    "OptionChoice",
    "SubCommandOption",
    "SubCommandGroupOption",
    "IntegerOption",
    "StringOption",
    "BooleanOption",
    "UserOption",
    "ChannelOption",
    "RoleOption",
    "MentionableOption",
    "NumberOption",
    "AttachmentOption",
    "AnyCommandOption",
    "ApplicationCommandOption",
    "ApplicationCommandOptionChoice",
    "GuildApplicationCommandPermissions",
    "ApplicationCommandPermissions",
    "ActionRow",
    "ComponentEmoji",
    "Button",
    "SelectMenu",
    "SelectOption",
    "SelectMenuResolved",
    "TextInput",
    "Component",
    "DirectComponent",
    "Interaction",
    "ApplicationCommandData",
    "MessageComponentData",
    "ModalSubmitData",
    "InteractionData",
    "ResolvedData",
    "ApplicationCommandInteractionDataOption",
    "MessageInteraction",
    "InteractionResponse",
    "InteractionCallbackMessage",
    "InteractionCallbackAutocomplete",
    "InteractionCallbackModal",
    "InteractionCallbackData",
    "Application",
    "InstallParams",
    "ApplicationRoleConnectionMetadata",
    "AuditLog",
    "AuditLogEntry",
    "OptionalAuditEntryInfo",
    "AuditLogChange",
    "AuditLogChangeException",
    "AutoModerationRule",
    "TriggerMetadata",
    "AutoModerationAction",
    "AutoModerationActionMetadata",
    "CreateAndModifyAutoModerationRuleParams",
    "Channel",
    "MessageGet",
    "MessageActivity",
    "MessageReference",
    "FollowedChannel",
    "Reaction",
    "Overwrite",
    "ThreadMetadata",
    "ThreadMember",
    "DefaultReaction",
    "ForumTag",
    "Embed",
    "EmbedThumbnail",
    "EmbedVideo",
    "EmbedImage",
    "EmbedProvider",
    "EmbedAuthor",
    "EmbedFooter",
    "EmbedField",
    "Attachment",
    "ChannelMention",
    "AllowedMention",
    "RoleSubscriptionData",
    "ArchivedThreadsResponse",
    "File",
    "AttachmentSend",
    "MessageSend",
    "ModifyChannelParams",
    "Emoji",
    "Guild",
    "CurrentUserGuild",
    "UnavailableGuild",
    "GuildPreview",
    "GuildWidgetSettings",
    "GuildWidget",
    "GuildMember",
    "Integration",
    "IntegrationAccount",
    "IntegrationApplication",
    "Ban",
    "WelcomeScreen",
    "WelcomeScreenChannel",
    "GuildOnboarding",
    "OnboardingPrompt",
    "OnboardingPromptOption",
    "MembershipScreening",
    "CreateGuildParams",
    "ModifyGuildParams",
    "CreateGuildChannelParams",
    "ListActiveGuildThreadsResponse",
    "ModifyGuildWelcomeScreenParams",
    "GuildScheduledEvent",
    "GuildScheduledEventEntityMetadata",
    "GuildScheduledEventUser",
    "CreateGuildScheduledEventParams",
    "ModifyGuildScheduledEventParams",
    "GuildTemplate",
    "Invite",
    "InviteMetadata",
    "InviteStageInstance",
    "StageInstance",
    "Sticker",
    "StickerItem",
    "StickerPack",
    "User",
    "Connection",
    "ApplicationRoleConnection",
    "VoiceState",
    "VoiceRegion",
    "Webhook",
    "ExecuteWebhookParams",
    "Gateway",
    "GatewayBot",
    "SessionStartLimit",
    "Identify",
    "IdentifyConnectionProperties",
    "Resume",
    "RequestGuildMembers",
    "UpdateVoiceState",
    "UpdatePresence",
    "Hello",
    "ApplicationReady",
    "Ready",
    "AutoModerationRuleCreate",
    "AutoModerationRuleUpdate",
    "AutoModerationRuleDelete",
    "AutoModerationActionExecution",
    "ChannelCreate",
    "ChannelUpdate",
    "ChannelDelete",
    "ThreadCreate",
    "ThreadUpdate",
    "ThreadDelete",
    "ThreadListSync",
    "ThreadMemberUpdate",
    "ThreadMembersUpdate",
    "ChannelPinsUpdate",
    "GuildCreate",
    "GuildUpdate",
    "GuildDelete",
    "GuildAuditLogEntryCreate",
    "GuildBanAdd",
    "GuildBanRemove",
    "GuildEmojisUpdate",
    "GuildStickersUpdate",
    "GuildIntegrationsUpdate",
    "GuildMemberAdd",
    "GuildMemberRemove",
    "GuildMemberUpdate",
    "GuildMembersChunk",
    "GuildRoleCreate",
    "GuildRoleUpdate",
    "GuildRoleDelete",
    "GuildScheduledEventCreate",
    "GuildScheduledEventUpdate",
    "GuildScheduledEventDelete",
    "GuildScheduledEventUserAdd",
    "GuildScheduledEventUserRemove",
    "IntegrationCreate",
    "IntegrationUpdate",
    "IntegrationDelete",
    "InviteCreate",
    "InviteDelete",
    "MessageCreate",
    "MessageCreate",
    "MessageUpdate",
    "MessageDelete",
    "MessageDeleteBulk",
    "MessageReactionAdd",
    "MessageReactionRemove",
    "MessageReactionRemoveAll",
    "MessageReactionRemoveEmoji",
    "PresenceUpdateUser",
    "PresenceUpdate",
    "ClientStatus",
    "Activity",
    "ActivityTimestamps",
    "ActivityEmoji",
    "ActivityParty",
    "ActivityAssets",
    "ActivitySecrets",
    "ActivityButtons",
    "TypingStart",
    "UserUpdate",
    "VoiceStateUpdate",
    "VoiceServerUpdate",
    "WebhooksUpdate",
    "InteractionCreate",
    "StageInstanceCreate",
    "StageInstanceUpdate",
    "StageInstanceDelete",
    "Role",
    "RoleTags",
    "Team",
    "TeamMember",
    "TeamMemberUser",
    "AuthorizationResponse",
]
