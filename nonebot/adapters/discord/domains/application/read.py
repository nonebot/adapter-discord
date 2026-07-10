"""Canonical application.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Guild, User

from .._model_support import (
    UNSET,
    ApplicationFlag,
    ApplicationIntegrationType,
    ApplicationRoleConnectionMetadataType,
    BaseModel,
    EntitlementType,
    Field,
    MembershipState,
    Missing,
    MissingOrNullable,
    SKUFlag,
    SKUType,
    Snowflake,
    SubscriptionStatus,
    TeamMemberRoleType,
    datetime,
)


class Application(BaseModel):
    """Application.

    see https://discord.com/developers/docs/resources/application#application-object"""

    id: Snowflake
    """the id of the app"""
    name: str
    """the name of the app"""
    icon: str | None = None
    """the icon hash of the app"""
    description: str
    """the description of the app"""
    rpc_origins: Missing[list[str]] = UNSET
    """an array of rpc origin urls, if rpc is enabled"""
    bot_public: bool
    """when false only app owner can join the app's bot to guilds"""
    bot_require_code_grant: bool
    """when true the app's bot will only join upon completion
    of the full oauth2 code grant flow"""
    bot: Missing[User] = UNSET  # partial user object
    """Partial user object for the bot user associated with the app"""
    terms_of_service_url: Missing[str] = UNSET
    """the url of the app's terms of service"""
    privacy_policy_url: Missing[str] = UNSET
    """the url of the app's privacy policy"""
    owner: Missing[User] = UNSET  # partial user object
    """partial user object containing info on the owner of the application"""
    verify_key: str
    """the hex encoded key for verification in
    interactions and the GameSDK's GetTicket"""
    team: Team | None = None
    """if the application belongs to a team, this will
    be a list of the members of that team"""
    guild_id: Missing[Snowflake] = UNSET
    """if this application is a game sold on Discord,
    this field will be the guild to which it has been linked"""
    guild: Missing[Guild] = UNSET  # partial guild object
    """Partial object of the associated guild"""
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
    approximate_guild_count: Missing[int] = UNSET
    """Approximate count of guilds the app has been added to"""
    approximate_user_install_count: Missing[int] = UNSET
    """Approximate count of users that have installed the app"""
    redirect_uris: Missing[list[str]] = UNSET
    """Array of redirect URIs for the app"""
    interactions_endpoint_url: MissingOrNullable[str] = (
        UNSET  # return type not match the docs
    )
    """Interactions endpoint URL for the app"""
    role_connections_verification_url: MissingOrNullable[str] = (
        UNSET  # return type not match the docs
    )
    """Role connection verification URL for the app"""
    event_webhooks_url: MissingOrNullable[str] = UNSET
    """Event webhooks URL for the app to receive webhook events"""
    event_webhooks_status: Missing[int] = UNSET
    """Status indicating whether event webhooks are enabled"""
    event_webhooks_types: Missing[list[str]] = UNSET
    """List of webhook event types the app subscribes to"""
    tags: Missing[list[str]] = UNSET
    """up to 5 tags describing the content and functionality of the application"""
    install_params: Missing[InstallParams] = UNSET
    """settings for the application's default in-app authorization link, if enabled"""
    integration_types_config: Missing[
        dict[
            ApplicationIntegrationType,
            ApplicationIntegrationTypeConfiguration,
        ]
    ] = UNSET
    """Default scopes and permissions for each supported
    installation context. Value for each key is an integration
    type configuration object"""
    custom_install_url: Missing[str] = UNSET
    """the application's default custom authorization link, if enabled"""


class InstallParams(BaseModel):
    """Install params.

    see https://discord.com/developers/docs/resources/application#install-params-object
    """

    scopes: list[str]
    """the scopes to add the application to the server with"""
    permissions: str
    """	the permissions to request for the bot role"""


class ApplicationIntegrationTypeConfiguration(BaseModel):
    """Application Integration Type Configuration

    see https://discord.com/developers/docs/resources/application#application-object-application-integration-type-configuration-object
    """

    oauth2_install_params: Missing[InstallParams] = UNSET


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
    name_localizations: Missing[dict[str, str]] = UNSET
    """translations of the name"""
    description: str
    """description of the metadata field (1-200 characters)"""
    description_localizations: Missing[dict[str, str]] = UNSET
    """translations of the description"""


class ApplicationRoleConnection(BaseModel):
    """Application Role Connection

    see https://discord.com/developers/docs/resources/user#application-role-connection-object
    """

    platform_name: str | None = Field(...)
    platform_username: str | None = Field(...)
    metadata: dict  # object


class ApplicationReady(BaseModel):
    """partial application object for ready event.

    see https://discord.com/developers/docs/events/gateway-events#ready
    """

    id: str
    flags: int


class Team(BaseModel):
    """Team.

    see https://discord.com/developers/docs/topics/teams#data-models-team-object"""

    icon: str | None = Field(...)
    id: str
    members: list[TeamMember]
    name: str
    owner_user_id: Snowflake


class TeamMember(BaseModel):
    """Team member.

    see https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    membership_state: MembershipState
    team_id: Snowflake
    user: TeamMemberUser
    role: TeamMemberRoleType


class TeamMemberUser(BaseModel):
    """partial user object for TeamMember

    see https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    avatar: str | None = None
    discriminator: str
    id: Snowflake
    username: str


class AuthorizationResponse(BaseModel):
    """Get Current Authorization Information Response

    see https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
    """

    application: Application  # partial application object
    scopes: list[str]
    expires: datetime.datetime
    user: Missing[User] = UNSET


class Entitlement(BaseModel):
    """see https://discord.com/developers/docs/monetization/entitlements#entitlement-object"""

    id: Snowflake
    """ID of the entitlement"""
    sku_id: Snowflake
    """ID of the SKU"""
    application_id: Snowflake
    """ID of the parent application"""
    user_id: Missing[Snowflake] = UNSET
    """ID of the user that is granted access to the entitlement's sku"""
    type: EntitlementType
    """Type of entitlement"""
    deleted: bool
    """Entitlement was deleted"""
    starts_at: Missing[datetime.datetime] = UNSET
    """Start date at which the entitlement is valid.
    Not present when using test entitlements."""
    ends_at: Missing[datetime.datetime] = UNSET
    """Date at which the entitlement is no longer valid.
    Not present when using test entitlements."""
    guild_id: Missing[Snowflake] = UNSET
    """ID of the guild that is granted access to the entitlement's sku"""
    consumed: Missing[bool] = UNSET
    """For consumable items, whether or not the entitlement has been consumed"""


class SKU(BaseModel):
    """https://discord.com/developers/docs/resources/sku#sku-object"""

    id: Snowflake
    type: SKUType
    application_id: Snowflake
    name: str
    slug: str
    flags: SKUFlag
    dependent_sku_id: MissingOrNullable[Snowflake] = UNSET
    manifest_labels: MissingOrNullable[list[str]] = UNSET
    access_type: Missing[int] = UNSET
    features: Missing[list[str]] = UNSET
    release_date: MissingOrNullable[datetime.datetime] = UNSET
    premium: Missing[bool] = UNSET
    show_age_gate: Missing[bool] = UNSET


class Subscription(BaseModel):
    """https://discord.com/developers/docs/resources/subscription#subscription-object"""

    id: Snowflake
    user_id: Snowflake
    sku_ids: list[Snowflake]
    entitlement_ids: list[Snowflake]
    renewal_sku_ids: MissingOrNullable[list[Snowflake]] = UNSET
    current_period_start: datetime.datetime
    current_period_end: datetime.datetime
    status: SubscriptionStatus
    canceled_at: datetime.datetime | None = None
    country: Missing[str] = UNSET


__all__ = [
    "SKU",
    "Application",
    "ApplicationIntegrationTypeConfiguration",
    "ApplicationReady",
    "ApplicationRoleConnection",
    "ApplicationRoleConnectionMetadata",
    "AuthorizationResponse",
    "Entitlement",
    "InstallParams",
    "Subscription",
    "Team",
    "TeamMember",
    "TeamMemberUser",
]
