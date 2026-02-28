from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from .snowflake import Snowflake
from ...types import (
    UNSET,
    ApplicationFlag,
    ApplicationIntegrationType,
    ApplicationRoleConnectionMetadataType,
    Missing,
    MissingOrNullable,
)

if TYPE_CHECKING:
    from .guilds import Guild
    from .teams import Team
    from .user import User


class Application(BaseModel):
    id: Snowflake
    name: str
    icon: str | None = None
    description: str
    rpc_origins: Missing[list[str]] = UNSET
    bot_public: bool
    bot_require_code_grant: bool
    bot: Missing[User] = UNSET
    terms_of_service_url: Missing[str] = UNSET
    privacy_policy_url: Missing[str] = UNSET
    owner: Missing[User] = UNSET
    verify_key: str
    team: Team | None = None
    guild_id: Missing[Snowflake] = UNSET
    guild: Missing[Guild] = UNSET
    primary_sku_id: Missing[Snowflake] = UNSET
    slug: Missing[str] = UNSET
    cover_image: Missing[str] = UNSET
    flags: Missing[ApplicationFlag] = UNSET
    approximate_guild_count: Missing[int] = UNSET
    approximate_user_install_count: Missing[int] = UNSET
    redirect_uris: Missing[list[str]] = UNSET
    interactions_endpoint_url: MissingOrNullable[str] = UNSET
    role_connections_verification_url: MissingOrNullable[str] = UNSET
    event_webhooks_url: MissingOrNullable[str] = UNSET
    event_webhooks_status: Missing[int] = UNSET
    event_webhooks_types: Missing[list[str]] = UNSET
    tags: Missing[list[str]] = UNSET
    install_params: Missing[InstallParams] = UNSET
    integration_types_config: Missing[
        dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration]
    ] = UNSET
    custom_install_url: Missing[str] = UNSET


class InstallParams(BaseModel):
    scopes: list[str]
    permissions: str


class ApplicationIntegrationTypeConfiguration(BaseModel):
    oauth2_install_params: Missing[InstallParams] = UNSET


class ActivityInstance(BaseModel):
    application_id: Snowflake
    instance_id: str
    launch_id: Snowflake
    location: ActivityLocation
    users: list[Snowflake]


class ActivityLocation(BaseModel):
    id: str
    kind: Literal["gc", "pc"]
    channel_id: Snowflake
    guild_id: MissingOrNullable[Snowflake] = UNSET


class ApplicationRoleConnectionMetadata(BaseModel):
    type: ApplicationRoleConnectionMetadataType
    key: str
    name: str
    name_localizations: Missing[dict[str, str]] = UNSET
    description: str
    description_localizations: Missing[dict[str, str]] = UNSET
