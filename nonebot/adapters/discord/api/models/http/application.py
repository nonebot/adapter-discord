from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from ..common.snowflake import Snowflake
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
    from ..common.teams import Team
    from ..common.user import User


# Application
# see https://discord.com/developers/docs/resources/application
class Application(BaseModel):
    """Application.

    see https://discord.com/developers/docs/resources/application#application-object
    """

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
    bot: Missing[User] = UNSET
    """Partial user object for the bot user associated with the app"""
    terms_of_service_url: Missing[str] = UNSET
    """the url of the app's terms of service"""
    privacy_policy_url: Missing[str] = UNSET
    """the url of the app's privacy policy"""
    owner: Missing[User] = UNSET
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
    guild: Missing[Guild] = UNSET
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
    interactions_endpoint_url: MissingOrNullable[str] = UNSET
    """Interactions endpoint URL for the app"""
    role_connections_verification_url: MissingOrNullable[str] = UNSET
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
        dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration]
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
    """\tthe permissions to request for the bot role"""


class ApplicationIntegrationTypeConfiguration(BaseModel):
    """Application Integration Type Configuration

    see https://discord.com/developers/docs/resources/application#application-object-application-integration-type-configuration-object
    """

    oauth2_install_params: Missing[InstallParams] = UNSET


class EditCurrentApplicationParams(BaseModel):
    """Edit Current Application Params.

    see https://discord.com/developers/docs/resources/application#edit-current-application
    """

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


class ActivityInstance(BaseModel):
    """Activity Instance

    see https://discord.com/developers/docs/resources/application#get-application-activity-instance-activity-instance-object
    """

    application_id: Snowflake
    """Application ID"""

    instance_id: str
    """Activity Instance ID"""

    launch_id: Snowflake
    """Unique identifier for the launch"""

    location: ActivityLocation
    """The Location the instance is runnning in"""

    users: list[Snowflake]
    """The IDs of the Users currently connected to the instance"""


class ActivityLocation(BaseModel):
    """The Activity Location is an object that describes
    the location in which an activity instance is running.

    see https://discord.com/developers/docs/resources/application#get-application-activity-instance-activity-location-object
    """

    id: str
    """The unique identifier for the location"""

    kind: Literal["gc", "pc"]
    """Enum describing kind of location

    'gc' The Location is a Guild Channel
    'pc' The Location is a Private Channel, such as a DM or GDM
    """

    channel_id: Snowflake
    guild_id: MissingOrNullable[Snowflake] = UNSET


# Application Role Connection Metadata
# see https://discord.com/developers/docs/resources/application-role-connection-metadata
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
