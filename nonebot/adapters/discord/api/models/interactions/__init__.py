from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .application_commands import (
        AnyCommandOption,
        ApplicationCommand,
        ApplicationCommandBulkOverwriteParams,
        ApplicationCommandCreate,
        ApplicationCommandEditParams,
        ApplicationCommandOption,
        ApplicationCommandOptionChoice,
        ApplicationCommandPermissions,
        AttachmentOption,
        BooleanOption,
        ChannelOption,
        CommandOptionBase,
        GuildApplicationCommandPermissions,
        IntegerOption,
        MentionableOption,
        NumberOption,
        OptionChoice,
        RoleOption,
        StringOption,
        SubCommandGroupOption,
        SubCommandOption,
        UserOption,
    )
    from .interactions import (
        ApplicationCommandData,
        ApplicationCommandInteractionDataOption,
        InteractionCallbackAutocomplete,
        InteractionCallbackData,
        InteractionCallbackMessage,
        InteractionCallbackModal,
        InteractionData,
        InteractionGuild,
        InteractionResponse,
        MessageComponentData,
        MessageInteraction,
        MessageInteractionMetadata,
        ModalSubmitData,
        ResolvedData,
    )
    from .message_components import (
        ActionRow,
        Button,
        Component,
        ComponentEmoji,
        DirectComponent,
        SelectDefaultValue,
        SelectMenu,
        SelectMenuResolved,
        SelectOption,
        TextInput,
    )


__all__ = [
    "ActionRow",
    "AnyCommandOption",
    "ApplicationCommand",
    "ApplicationCommandBulkOverwriteParams",
    "ApplicationCommandCreate",
    "ApplicationCommandData",
    "ApplicationCommandEditParams",
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
    "InteractionCallbackAutocomplete",
    "InteractionCallbackData",
    "InteractionCallbackMessage",
    "InteractionCallbackModal",
    "InteractionData",
    "InteractionGuild",
    "InteractionResponse",
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


_EXPORTS: dict[str, tuple[str, str]] = {
    "ActionRow": (".message_components", "ActionRow"),
    "AnyCommandOption": (".application_commands", "AnyCommandOption"),
    "ApplicationCommand": (".application_commands", "ApplicationCommand"),
    "ApplicationCommandBulkOverwriteParams": (
        ".application_commands",
        "ApplicationCommandBulkOverwriteParams",
    ),
    "ApplicationCommandCreate": (".application_commands", "ApplicationCommandCreate"),
    "ApplicationCommandData": (".interactions", "ApplicationCommandData"),
    "ApplicationCommandEditParams": (
        ".application_commands",
        "ApplicationCommandEditParams",
    ),
    "ApplicationCommandInteractionDataOption": (
        ".interactions",
        "ApplicationCommandInteractionDataOption",
    ),
    "ApplicationCommandOption": (".application_commands", "ApplicationCommandOption"),
    "ApplicationCommandOptionChoice": (
        ".application_commands",
        "ApplicationCommandOptionChoice",
    ),
    "ApplicationCommandPermissions": (
        ".application_commands",
        "ApplicationCommandPermissions",
    ),
    "AttachmentOption": (".application_commands", "AttachmentOption"),
    "BooleanOption": (".application_commands", "BooleanOption"),
    "Button": (".message_components", "Button"),
    "ChannelOption": (".application_commands", "ChannelOption"),
    "CommandOptionBase": (".application_commands", "CommandOptionBase"),
    "Component": (".message_components", "Component"),
    "ComponentEmoji": (".message_components", "ComponentEmoji"),
    "DirectComponent": (".message_components", "DirectComponent"),
    "GuildApplicationCommandPermissions": (
        ".application_commands",
        "GuildApplicationCommandPermissions",
    ),
    "IntegerOption": (".application_commands", "IntegerOption"),
    "InteractionCallbackAutocomplete": (
        ".interactions",
        "InteractionCallbackAutocomplete",
    ),
    "InteractionCallbackData": (".interactions", "InteractionCallbackData"),
    "InteractionCallbackMessage": (
        ".interactions",
        "InteractionCallbackMessage",
    ),
    "InteractionCallbackModal": (".interactions", "InteractionCallbackModal"),
    "InteractionData": (".interactions", "InteractionData"),
    "InteractionGuild": (".interactions", "InteractionGuild"),
    "InteractionResponse": (".interactions", "InteractionResponse"),
    "MentionableOption": (".application_commands", "MentionableOption"),
    "MessageComponentData": (".interactions", "MessageComponentData"),
    "MessageInteraction": (".interactions", "MessageInteraction"),
    "MessageInteractionMetadata": (
        ".interactions",
        "MessageInteractionMetadata",
    ),
    "ModalSubmitData": (".interactions", "ModalSubmitData"),
    "NumberOption": (".application_commands", "NumberOption"),
    "OptionChoice": (".application_commands", "OptionChoice"),
    "ResolvedData": (".interactions", "ResolvedData"),
    "RoleOption": (".application_commands", "RoleOption"),
    "SelectDefaultValue": (".message_components", "SelectDefaultValue"),
    "SelectMenu": (".message_components", "SelectMenu"),
    "SelectMenuResolved": (".message_components", "SelectMenuResolved"),
    "SelectOption": (".message_components", "SelectOption"),
    "StringOption": (".application_commands", "StringOption"),
    "SubCommandGroupOption": (".application_commands", "SubCommandGroupOption"),
    "SubCommandOption": (".application_commands", "SubCommandOption"),
    "TextInput": (".message_components", "TextInput"),
    "UserOption": (".application_commands", "UserOption"),
}


def __getattr__(name: str) -> object:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError:
        raise AttributeError(name) from None

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
