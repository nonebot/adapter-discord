"""Canonical application.write models."""

from typing import TYPE_CHECKING, Literal
from typing_extensions import Required

from .._model_support import OutboundTypedDict

if TYPE_CHECKING:
    from ..models import ApplicationIntegrationTypeConfiguration, InstallParams

from .._model_support import ApplicationFlag, ApplicationIntegrationType


class EditCurrentApplicationParams(OutboundTypedDict, total=False):
    """Edit Current Application Params.

    see https://discord.com/developers/docs/resources/application#edit-current-application
    """

    custom_install_url: str
    description: str
    role_connections_verification_url: str
    install_params: "InstallParams"
    integration_types_config: (
        "dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration]"
    )
    flags: ApplicationFlag
    icon: str | None
    cover_image: str | None
    interactions_endpoint_url: str
    tags: list[str]
    event_webhooks_url: str
    event_webhooks_status: int
    event_webhooks_types: list[str]


class CreateTestEntitlementParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_create_test_entitlement``."""

    sku_id: Required[str]
    owner_id: Required[str]
    owner_type: Required["Literal[1, 2]"]


__all__ = [
    "CreateTestEntitlementParams",
    "EditCurrentApplicationParams",
]
