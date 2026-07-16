"""Canonical command.write models."""

from typing import TYPE_CHECKING
from typing_extensions import Required

from .._model_support import OutboundTypedDict

if TYPE_CHECKING:
    from .read import ApplicationCommandPermissions
    from ..models import AnyCommandOption

from .._model_support import (
    ApplicationCommandType,
    ApplicationIntegrationType,
    InteractionContextType,
    Snowflake,
)


class ApplicationCommandCreate(OutboundTypedDict, total=False):
    """Application Command Create

    see https://discord.com/developers/docs/interactions/application-commands#create-global-application-command
    """

    name: Required[str]
    name_localizations: dict[str, str] | None
    description: str
    description_localizations: dict[str, str] | None
    options: "list[AnyCommandOption]"
    default_member_permissions: str | None
    dm_permission: bool | None
    default_permission: bool
    integration_types: list[ApplicationIntegrationType]
    contexts: list[InteractionContextType]
    type: ApplicationCommandType
    nsfw: bool


class ApplicationCommandBulkOverwriteParams(OutboundTypedDict, total=False):
    """Application Command Bulk Overwrite Params.

    see https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-global-application-commands
    """

    id: Snowflake
    type: ApplicationCommandType
    name: Required[str]
    name_localizations: dict[str, str] | None
    description: str | None
    description_localizations: dict[str, str] | None
    options: "list[AnyCommandOption] | None"
    default_member_permissions: str | None
    dm_permission: bool | None
    default_permission: bool | None
    nsfw: bool | None
    integration_types: list[ApplicationIntegrationType]
    contexts: list[InteractionContextType] | None


class ApplicationCommandEditParams(OutboundTypedDict, total=False):
    """Application Command Edit Params.

    see https://discord.com/developers/docs/interactions/application-commands#edit-global-application-command
    """

    name: str
    name_localizations: dict[str, str] | None
    description: str
    description_localizations: dict[str, str] | None
    options: "list[AnyCommandOption]"
    default_member_permissions: str | None
    dm_permission: bool | None
    default_permission: bool
    nsfw: bool
    integration_types: list[ApplicationIntegrationType]
    contexts: list[InteractionContextType]


class EditApplicationCommandPermissionsParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_edit_application_command_permissions``."""

    permissions: Required["list[ApplicationCommandPermissions]"]


__all__ = [
    "ApplicationCommandBulkOverwriteParams",
    "ApplicationCommandCreate",
    "ApplicationCommandEditParams",
    "EditApplicationCommandPermissionsParams",
]
