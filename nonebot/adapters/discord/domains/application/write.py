"""Canonical application.write models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import ApplicationIntegrationTypeConfiguration, InstallParams

from .._model_support import (
    UNSET,
    ApplicationFlag,
    ApplicationIntegrationType,
    BaseModel,
    Missing,
    MissingOrNullable,
)


class EditCurrentApplicationParams(BaseModel):
    """Edit Current Application Params.

    see https://discord.com/developers/docs/resources/application#edit-current-application
    """

    custom_install_url: Missing[str] = UNSET
    description: Missing[str] = UNSET
    role_connections_verification_url: Missing[str] = UNSET
    install_params: Missing["InstallParams"] = UNSET
    integration_types_config: Missing[
        dict[ApplicationIntegrationType, "ApplicationIntegrationTypeConfiguration"]
    ] = UNSET
    flags: Missing[ApplicationFlag] = UNSET
    icon: MissingOrNullable[str] = UNSET
    cover_image: MissingOrNullable[str] = UNSET
    interactions_endpoint_url: Missing[str] = UNSET
    tags: Missing[list[str]] = UNSET
    event_webhooks_url: Missing[str] = UNSET
    event_webhooks_status: Missing[int] = UNSET
    event_webhooks_types: Missing[list[str]] = UNSET


__all__ = ["EditCurrentApplicationParams"]
