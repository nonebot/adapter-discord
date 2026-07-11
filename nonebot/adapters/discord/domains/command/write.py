"""Canonical command.write models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import AnyCommandOption

from .._model_support import (
    UNSET,
    ApplicationCommandType,
    ApplicationIntegrationType,
    BaseModel,
    InteractionContextType,
    Missing,
    MissingOrNullable,
    Snowflake,
)


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


__all__ = [
    "ApplicationCommandBulkOverwriteParams",
    "ApplicationCommandCreate",
    "ApplicationCommandEditParams",
]
