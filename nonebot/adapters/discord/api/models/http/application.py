from __future__ import annotations

from pydantic import BaseModel

from ..common.application import (
    ActivityInstance,
    ActivityLocation,
    Application,
    ApplicationIntegrationTypeConfiguration,
    ApplicationRoleConnectionMetadata,
    InstallParams,
)
from ...types import (
    UNSET,
    ApplicationFlag,
    ApplicationIntegrationType,
    Missing,
    MissingOrNullable,
)


class EditCurrentApplicationParams(BaseModel):
    custom_install_url: Missing[str] = UNSET
    description: Missing[str] = UNSET
    role_connections_verification_url: Missing[str] = UNSET
    install_params: Missing[InstallParams] = UNSET
    integration_types_config: Missing[
        dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration]
    ] = UNSET
    flags: Missing[ApplicationFlag] = UNSET
    icon: MissingOrNullable[str] = UNSET
    cover_image: MissingOrNullable[str] = UNSET
    interactions_endpoint_url: Missing[str] = UNSET
    tags: Missing[list[str]] = UNSET
    event_webhooks_url: Missing[str] = UNSET
    event_webhooks_status: Missing[int] = UNSET
    event_webhooks_types: Missing[list[str]] = UNSET


__all__ = [
    "ActivityInstance",
    "ActivityLocation",
    "Application",
    "ApplicationIntegrationTypeConfiguration",
    "ApplicationRoleConnectionMetadata",
    "EditCurrentApplicationParams",
    "InstallParams",
]
