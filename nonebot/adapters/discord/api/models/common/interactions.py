from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Literal, TypeAlias, TypeVar

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ...types import (
    UNSET,
    ApplicationCommandOptionType,
    ApplicationCommandPermissionsType,
    ApplicationCommandType,
    ApplicationIntegrationType,
    ButtonStyle,
    ChannelType,
    ComponentType,
    GuildFeature,
    InteractionContextType,
    InteractionType,
    Missing,
    MissingOrNullable,
    TextInputStyle,
)

if TYPE_CHECKING:
    from .channels import Channel
    from .guild_members import GuildMember
    from .messages import Attachment, MessageGet
    from .permissions import Role
    from .user import User

T = TypeVar("T", str, int, float)


class ApplicationCommand(BaseModel):
    id: Snowflake
    type: Missing[ApplicationCommandType] = UNSET
    application_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    name: str
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    description: Missing[str] = UNSET
    description_localizations: MissingOrNullable[dict[str, str]] = UNSET
    options: MissingOrNullable[list[ApplicationCommandOption]] = UNSET
    default_member_permissions: str | None = Field(...)
    dm_permission: Missing[bool] = UNSET
    default_permission: MissingOrNullable[bool] = UNSET
    nsfw: Missing[bool] = UNSET
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    contexts: MissingOrNullable[list[InteractionContextType]] = UNSET
    version: Snowflake


class CommandOptionBase(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    name_localizations: dict[str, str] | None = None
    description: str
    description_localizations: dict[str, str] | None = None


class ApplicationCommandOption(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    description: Missing[str] = UNSET
    description_localizations: MissingOrNullable[dict[str, str]] = UNSET
    required: Missing[bool] = UNSET
    choices: Missing[list[ApplicationCommandOptionChoice]] = UNSET
    options: MissingOrNullable[list[ApplicationCommandOption]] = UNSET
    channel_types: Missing[list[ChannelType]] = UNSET
    min_value: Missing[int | float] = UNSET
    max_value: Missing[int | float] = UNSET
    min_length: Missing[int] = UNSET
    max_length: Missing[int] = UNSET
    autocomplete: Missing[bool] = UNSET


class OptionChoice(BaseModel, Generic[T]):
    name: str
    name_localizations: dict[str, str] | None = None
    value: T


class SubCommandOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.SUB_COMMAND, init=False
    )
    options: (
        list[
            IntegerOption
            | StringOption
            | BooleanOption
            | UserOption
            | ChannelOption
            | RoleOption
            | MentionableOption
            | NumberOption
            | AttachmentOption
        ]
        | None
    ) = None


class SubCommandGroupOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.SUB_COMMAND_GROUP, init=False
    )
    options: list[SubCommandOption] | None = None


class IntegerOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.INTEGER, init=False
    )
    choices: list[OptionChoice[int]] | None = None
    min_value: int | None = None
    max_value: int | None = None
    autocomplete: bool | None = None
    required: bool = False


class StringOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.STRING, init=False
    )
    choices: list[OptionChoice[str]] | None = None
    min_length: int | None = None
    max_length: int | None = None
    autocomplete: bool | None = None
    required: bool = False


class BooleanOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.BOOLEAN, init=False
    )
    required: bool = False


class UserOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.USER, init=False
    )
    required: bool = False


class ChannelOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.CHANNEL, init=False
    )
    channel_types: list[ChannelType] | None = None
    required: bool = False


class RoleOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.ROLE, init=False
    )
    required: bool = False


class MentionableOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.MENTIONABLE, init=False
    )
    required: bool = False


class NumberOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.NUMBER, init=False
    )
    choices: list[OptionChoice[float]] | None = None
    min_value: float | None = None
    required: bool = False


class AttachmentOption(CommandOptionBase):
    type: ApplicationCommandOptionType = Field(
        ApplicationCommandOptionType.ATTACHMENT, init=False
    )
    required: bool = False


AnyCommandOption: TypeAlias = (
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
    name: str
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    value: str | int | float


class GuildApplicationCommandPermissions(BaseModel):
    id: Snowflake
    application_id: Snowflake
    guild_id: Snowflake
    permissions: list[ApplicationCommandPermissions]


class ApplicationCommandPermissions(BaseModel):
    id: Snowflake
    type: ApplicationCommandPermissionsType
    permission: bool


class ActionRow(BaseModel):
    type: ComponentType = Field(default=ComponentType.ActionRow)
    components: list[Button | SelectMenu | TextInput]


class ComponentEmoji(BaseModel):
    id: str | None = Field(...)
    name: str | None = Field(...)
    animated: Missing[bool] = UNSET


class Button(BaseModel):
    type: Literal[ComponentType.Button] = Field(default=ComponentType.Button)
    style: ButtonStyle
    label: Missing[str] = UNSET
    emoji: Missing[ComponentEmoji] = UNSET
    custom_id: Missing[str] = UNSET
    sku_id: Missing[Snowflake] = UNSET
    url: Missing[str] = UNSET
    disabled: Missing[bool] = UNSET


class SelectMenu(BaseModel):
    type: Literal[
        ComponentType.StringSelect,
        ComponentType.UserInput,
        ComponentType.RoleSelect,
        ComponentType.MentionableSelect,
        ComponentType.ChannelSelect,
    ]
    custom_id: str
    options: Missing[list[SelectOption]] = UNSET
    channel_types: Missing[list[ChannelType]] = UNSET
    placeholder: Missing[str] = UNSET
    default_values: Missing[list[SelectDefaultValue]] = UNSET
    min_values: Missing[int] = UNSET
    max_values: Missing[int] = UNSET
    disabled: Missing[bool] = UNSET


class SelectDefaultValue(BaseModel):
    id: Snowflake
    type: Literal["user", "role", "channel"]


class SelectOption(BaseModel):
    label: str
    value: str
    description: Missing[str] = UNSET
    emoji: Missing[ComponentEmoji] = UNSET
    default: Missing[bool] = UNSET


class SelectMenuResolved(BaseModel):
    users: Missing[dict[Snowflake, User]] = UNSET
    roles: Missing[dict[Snowflake, Role]] = UNSET
    channels: Missing[dict[Snowflake, Channel]] = UNSET
    members: Missing[dict[Snowflake, GuildMember]] = UNSET


class TextInput(BaseModel):
    type: Literal[ComponentType.TextInput] = Field(default=ComponentType.TextInput)
    custom_id: str
    style: TextInputStyle
    label: str
    min_length: Missing[int] = UNSET
    max_length: Missing[int] = UNSET
    required: Missing[bool] = UNSET
    value: Missing[str] = UNSET
    placeholder: Missing[str] = UNSET


Component: TypeAlias = ActionRow | Button | SelectMenu | TextInput
DirectComponent: TypeAlias = ActionRow | TextInput


class InteractionGuild(BaseModel):
    id: Snowflake
    locale: Missing[str] = UNSET
    features: list[GuildFeature]


class ApplicationCommandData(BaseModel):
    id: Snowflake
    name: str
    type: ApplicationCommandType
    resolved: Missing[ResolvedData] = UNSET
    options: Missing[list[ApplicationCommandInteractionDataOption]] = UNSET
    guild_id: Missing[Snowflake] = UNSET
    target_id: Missing[Snowflake] = UNSET


class MessageComponentData(BaseModel):
    custom_id: str
    component_type: ComponentType
    values: Missing[list[str]] = UNSET
    resolved: Missing[ResolvedData] = UNSET


class ModalSubmitData(BaseModel):
    custom_id: str
    components: list[Component]


InteractionData: TypeAlias = (
    ApplicationCommandData | MessageComponentData | ModalSubmitData
)


class ResolvedData(BaseModel):
    users: Missing[dict[Snowflake, User]] = UNSET
    members: Missing[dict[Snowflake, GuildMember]] = UNSET
    roles: Missing[dict[Snowflake, Role]] = UNSET
    channels: Missing[dict[Snowflake, Channel]] = UNSET
    messages: Missing[dict[Snowflake, MessageGet]] = UNSET
    attachments: Missing[dict[Snowflake, Attachment]] = UNSET


class ApplicationCommandInteractionDataOption(BaseModel):
    name: str
    type: ApplicationCommandOptionType
    value: Missing[str | int | float | bool] = UNSET
    options: Missing[list[ApplicationCommandInteractionDataOption]] = UNSET
    focused: Missing[bool] = UNSET


class MessageInteraction(BaseModel):
    id: Snowflake
    type: InteractionType
    name: str
    user: User
    member: Missing[GuildMember] = UNSET


class MessageInteractionMetadata(BaseModel):
    id: Snowflake
    type: InteractionType
    user: User
    authorizing_integration_owners: dict[
        ApplicationIntegrationType, Snowflake | Literal["0"]
    ]
    original_response_message_id: Missing[Snowflake] = UNSET
    interacted_message_id: Missing[Snowflake] = UNSET
    triggering_interaction_metadata: Missing[MessageInteractionMetadata] = UNSET


__all__ = [
    "ActionRow",
    "AnyCommandOption",
    "ApplicationCommand",
    "ApplicationCommandData",
    "ApplicationCommandInteractionDataOption",
    "ApplicationCommandOption",
    "ApplicationCommandOptionChoice",
    "ApplicationCommandPermissions",
    "AttachmentOption",
    "BooleanOption",
    "Button",
    "ChannelOption",
    "CommandOptionBase",
    "Component",
    "ComponentEmoji",
    "DirectComponent",
    "GuildApplicationCommandPermissions",
    "IntegerOption",
    "InteractionData",
    "InteractionGuild",
    "MentionableOption",
    "MessageComponentData",
    "MessageInteraction",
    "MessageInteractionMetadata",
    "ModalSubmitData",
    "NumberOption",
    "OptionChoice",
    "ResolvedData",
    "RoleOption",
    "SelectDefaultValue",
    "SelectMenu",
    "SelectMenuResolved",
    "SelectOption",
    "StringOption",
    "SubCommandGroupOption",
    "SubCommandOption",
    "TextInput",
    "UserOption",
]
