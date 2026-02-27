from typing import TYPE_CHECKING, Generic, TypeVar

from nonebot.compat import PYDANTIC_V2
from pydantic import BaseModel, Field

if PYDANTIC_V2 or TYPE_CHECKING:
    GenericModel = BaseModel
else:
    from pydantic.generics import GenericModel

from .snowflake import Snowflake
from ..types import (
    UNSET,
    ApplicationCommandOptionType,
    ApplicationCommandPermissionsType,
    ApplicationCommandType,
    ApplicationIntegrationType,
    ChannelType,
    InteractionContextType,
    Missing,
    MissingOrNullable,
)

T = TypeVar("T", str, int, float)


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
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    """Localization dictionary for name field.
    Values follow the same restrictions as name"""
    description: Missing[str] = UNSET
    """Description for CHAT_INPUT commands, 1-100 characters.
    Empty string for USER and MESSAGE commands"""
    description_localizations: MissingOrNullable[dict[str, str]] = UNSET
    """Localization dictionary for description field.
    Values follow the same restrictions as description"""
    options: MissingOrNullable[list["ApplicationCommandOption"]] = UNSET
    """Parameters for the command, max of 25"""
    default_member_permissions: str | None = Field(...)
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
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    """Installation contexts where the command is available,
    only for globally-scoped commands. Defaults to your
    app's configured contexts"""
    contexts: MissingOrNullable[list[InteractionContextType]] = UNSET
    """Interaction context(s) where the command can be used,
    only for globally-scoped commands. By default, all
    interaction context types included for new commands."""
    version: Snowflake
    """Autoincrementing version identifier updated during substantial record changes"""


class ApplicationCommandCreate(BaseModel):
    """Application Command Create

    see https://discord.com/developers/docs/interactions/application-commands#create-global-application-command
    """

    name: str
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    description: Missing[str] = UNSET
    description_localizations: MissingOrNullable[dict[str, str]] = UNSET
    options: Missing[list["AnyCommandOption"]] = UNSET
    default_member_permissions: MissingOrNullable[str] = UNSET
    dm_permission: MissingOrNullable[bool] = UNSET
    default_permission: Missing[bool] = UNSET
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    contexts: Missing[list[InteractionContextType]] = UNSET
    type: Missing[ApplicationCommandType] = UNSET
    nsfw: Missing[bool] = UNSET


class ApplicationCommandBulkOverwriteParams(BaseModel):
    """Application Command Bulk Overwrite Params.

    see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-global-application-commands
    """

    id: Missing[Snowflake] = UNSET
    type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT
    name: str
    name_localizations: dict[str, str] | None = None
    description: str | None = None
    description_localizations: dict[str, str] | None = None
    options: list["AnyCommandOption"] | None = None
    default_member_permissions: str | None = None
    dm_permission: bool | None = None
    default_permission: bool | None = None
    nsfw: bool | None = None
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    contexts: MissingOrNullable[list[InteractionContextType]] = UNSET


class ApplicationCommandEditParams(BaseModel):
    """Application Command Edit Params.

    see https://discord.com/developers/docs/interactions/application-commands#edit-global-application-command
    """

    name: Missing[str] = UNSET
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    description: Missing[str] = UNSET
    description_localizations: MissingOrNullable[dict[str, str]] = UNSET
    options: Missing[list["AnyCommandOption"]] = UNSET
    default_member_permissions: MissingOrNullable[str] = UNSET
    dm_permission: MissingOrNullable[bool] = UNSET
    default_permission: Missing[bool] = UNSET
    nsfw: Missing[bool] = UNSET
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    contexts: Missing[list[InteractionContextType]] = UNSET


class CommandOptionBase(BaseModel):
    """Application Command Option Base

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType
    name: str
    name_localizations: dict[str, str] | None = None
    description: str
    description_localizations: dict[str, str] | None = None


class ApplicationCommandOption(BaseModel):
    """Application Command Option

    Required options must be listed before optional options.

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType
    """Type of option"""
    name: str
    """1-32 character name"""
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    """Localization dictionary for the name field.
    Values follow the same restrictions as name"""
    description: Missing[str] = UNSET
    """1-100 character description"""
    description_localizations: MissingOrNullable[dict[str, str]] = UNSET
    """Localization dictionary for the description field.
    Values follow the same restrictions as description"""
    required: Missing[bool] = UNSET
    """If the parameter is required or optional--default false"""
    choices: Missing[list["ApplicationCommandOptionChoice"]] = UNSET
    """Choices for STRING, INTEGER,
    and NUMBER types for the user to pick from, max 25"""
    options: MissingOrNullable[list["ApplicationCommandOption"]] = UNSET
    """If the option is a subcommand or subcommand group type,
    these nested options will be the parameters"""
    channel_types: Missing[list[ChannelType]] = UNSET
    """If the option is a channel type,
    the channels shown will be restricted to these types"""
    min_value: Missing[int | float] = UNSET
    """If the option is an INTEGER or NUMBER type, the minimum value permitted"""
    max_value: Missing[int | float] = UNSET
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
    """Application Command Option Choice

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
    """

    name: str
    name_localizations: dict[str, str] | None = None
    value: T


class SubCommandOption(CommandOptionBase):
    """Sub Command Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.SUB_COMMAND, init=False
    )
    options: (
        list[
            "IntegerOption | StringOption | BooleanOption | UserOption| ChannelOption | RoleOption | MentionableOption | NumberOption | AttachmentOption"
        ]
        | None
    ) = None


class SubCommandGroupOption(CommandOptionBase):
    """Sub Command Group Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.SUB_COMMAND_GROUP, init=False
    )
    options: list[SubCommandOption] | None = None


class IntegerOption(CommandOptionBase):
    """Integer Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.INTEGER, init=False
    )
    choices: list[OptionChoice[int]] | None = None
    min_value: int | None = None
    max_value: int | None = None
    autocomplete: bool | None = None
    required: bool = False


class StringOption(CommandOptionBase):
    """String Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.STRING, init=False
    )
    choices: list[OptionChoice[str]] | None = None
    min_length: int | None = None
    max_length: int | None = None
    autocomplete: bool | None = None
    required: bool = False


class BooleanOption(CommandOptionBase):
    """Boolean Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.BOOLEAN, init=False
    )
    required: bool = False


class UserOption(CommandOptionBase):
    """User Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.USER, init=False
    )
    required: bool = False


class ChannelOption(CommandOptionBase):
    """Channel Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.CHANNEL, init=False
    )
    channel_types: list[ChannelType] | None = None
    required: bool = False


class RoleOption(CommandOptionBase):
    """Role Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.ROLE, init=False
    )
    required: bool = False


class MentionableOption(CommandOptionBase):
    """Mentionable Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.MENTIONABLE, init=False
    )
    required: bool = False


class NumberOption(CommandOptionBase):
    """Number Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.NUMBER, init=False
    )
    choices: list[OptionChoice[float]] | None = None
    min_value: float | None = None
    required: bool = False


class AttachmentOption(CommandOptionBase):
    """Attachment Option

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.ATTACHMENT, init=False
    )
    required: bool = False


AnyCommandOption = (
    SubCommandGroupOption
    | SubCommandOption
    | IntegerOption
    | StringOption
    | UserOption
    | ChannelOption
    | RoleOption
    | MentionableOption
    | NumberOption
    | BooleanOption
    | AttachmentOption
)


class ApplicationCommandOptionChoice(BaseModel):
    """Application Command Option Choice

    If you specify choices for an option,
    they are the only valid values for a user to pick

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
    """

    name: str
    """1-100 character choice name"""
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    """Localization dictionary for the name field.
    Values follow the same restrictions as name"""
    value: str | int | float
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
    permissions: list["ApplicationCommandPermissions"]
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
