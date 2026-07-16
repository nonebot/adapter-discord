from enum import IntEnum, IntFlag

from .._enum import StrEnum


class ApplicationFlag(IntFlag):
    """Application flags.

    see https://discord.com/developers/docs/resources/application#application-object-application-flags
    """

    APPLICATION_AUTO_MODERATION_RULE_CREATE_BADGE = 1 << 6
    """Indicates if an app uses the Auto Moderation API"""
    GATEWAY_PRESENCE = 1 << 12
    """Intent required for bots in 100 or more servers
    to receive presence_update events"""
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    """Intent required for bots in under 100 servers to receive presence_update events,
    found on the Bot page in your app's settings"""
    GATEWAY_GUILD_MEMBERS = 1 << 14
    """Intent required for bots in 100 or more servers to
    receive member-related events like guild_member_add.
    See the list of member-related events under GUILD_MEMBERS"""
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    """Intent required for bots in under 100 servers to receive member-related events
    like guild_member_add, found on the Bot page in your app's settings.
    See the list of member-related events under GUILD_MEMBERS"""
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    """Indicates unusual growth of an app that prevents verification"""
    EMBEDDED = 1 << 17
    """Indicates if an app is embedded within the
    Discord client (currently unavailable publicly)"""
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    """Intent required for bots in 100 or more servers to receive message content"""
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    """Intent required for bots in under 100 servers to receive message content,
    found on the Bot page in your app's settings"""
    APPLICATION_COMMAND_BADGE = 1 << 23
    """Indicates if an app has registered global application commands"""


class ApplicationIntegrationType(IntEnum):
    """Application Integration Type

    see https://discord.com/developers/docs/resources/application#application-object-application-integration-types
    """

    GUILD_INSTALL = 0
    """App is installable to servers"""
    USER_INSTALL = 1
    """App is installable to users"""


class ApplicationRoleConnectionMetadataType(IntEnum):
    """Application role connection metadata type.

    see https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object-application-role-connection-metadata-type
    """

    INTEGER_LESS_THAN_OR_EQUAL = 1
    """the metadata value (integer) is less than or equal
    to the guild's configured value (integer)"""
    INTEGER_GREATER_THAN_OR_EQUAL = 2
    """the metadata value (integer) is greater than or equal
    to the guild's configured value (integer)"""
    INTEGER_EQUAL = 3
    """the metadata value (integer) is equal to the
    guild's configured value (integer)"""
    INTEGER_NOT_EQUAL = 4
    """	the metadata value (integer) is not equal to the
    guild's configured value (integer)"""
    DATETIME_LESS_THAN_OR_EQUAL = 5
    """	the metadata value (ISO8601 string) is less than or equal
    to the guild's configured value (integer; days before current date)"""
    DATETIME_GREATER_THAN_OR_EQUAL = 6
    """the metadata value (ISO8601 string) is greater than or equal
    to the guild's configured value (integer; days before current date)"""
    BOOLEAN_EQUAL = 7
    """the metadata value (integer) is equal to the
    guild's configured value (integer; 1)"""
    BOOLEAN_NOT_EQUAL = 8
    """the metadata value (integer) is not equal to the
    guild's configured value (integer; 1)"""


class EntitlementType(IntEnum):
    """Entitlement Types

    see https://discord.com/developers/docs/monetization/entitlements#entitlement-object-entitlement-types
    """

    PURCHASE = 1
    """Entitlement was purchased by user"""
    PREMIUM_SUBSCRIPTION = 2
    """Entitlement for Discord Nitro subscription"""
    DEVELOPER_GIFT = 3
    """Entitlement was gifted by developer"""
    TEST_MODE_PURCHASE = 4
    """Entitlement was purchased by a dev in application test mode"""
    FREE_PURCHASE = 5
    """Entitlement was granted when the SKU was free"""
    USER_GIFT = 6
    """Entitlement was gifted by another user"""
    PREMIUM_PURCHASE = 7
    """Entitlement was claimed by user for free as a Nitro Subscriber"""
    APPLICATION_SUBSCRIPTION = 8
    """Entitlement was purchased as an app subscription"""


class MembershipState(IntEnum):
    """Membership state.

    see https://discord.com/developers/docs/topics/teams#data-models-membership-state-enum
    """

    INVITED = 1
    ACCEPTED = 2


class SKUFlag(IntFlag):
    """SKUFlag

    see https://discord.com/developers/docs/resources/sku#sku-object-sku-flags
    """

    AVAILABLE = 1 << 2
    """SKU is available for purchase"""
    GUILD_SUBSCRIPTION = 1 << 7
    """Recurring SKU that can be purchased by a user and applied
    to a single server. Grants access to every user in that server."""
    USER_SUBSCRIPTION = 1 << 8
    """Recurring SKU purchased by a user for themselves.
    Grants access to the purchasing user in every server."""


class SKUType(IntEnum):
    """SKU Type

    see https://discord.com/developers/docs/resources/sku#sku-object-sku-types
    """

    DURABLE = 2
    """Durable one-time purchase"""
    CONSUMABLE = 3
    """Consumable one-time purchase"""
    SUBSCRIPTION = 5
    """Represents a recurring subscription"""
    SUBSCRIPTION_GROUP = 6
    """System-generated group for each SUBSCRIPTION SKU created"""


class SubscriptionStatus(IntEnum):
    """Subscription Statuses

    see https://discord.com/developers/docs/resources/subscription#subscription-statuses
    """

    ACTIVE = 0
    """Subscription is active and scheduled to renew."""
    ENDING = 1
    """Subscription is active but will not renew."""
    INACTIVE = 2
    """Subscription is inactive and not being charged."""


class TeamMemberRoleType(StrEnum):
    """Team Member Role Types

    see https://discord.com/developers/docs/topics/teams#team-member-roles"""

    Admin = "admin"
    """Admins have similar access as owners, except they cannot take
    destructive actions on the team or team-owned apps."""
    Developer = "developer"
    """Developers can access information about team-owned apps,
    like the client secret or public key. They can also take limited
    actions on team-owned apps, like configuring interaction endpoints or
    resetting the bot token. Members with the Developer role cannot manage
    the team or its members, or take destructive actions on team-owned apps."""
    Read_only = "read_only"
    """Read-only members can access information about a team and
    any team-owned apps. Some examples include getting the IDs of
    applications and exporting payout records. Members can also
    invite bots associated with team-owned apps that are marked private."""


__all__ = [
    "ApplicationFlag",
    "ApplicationIntegrationType",
    "ApplicationRoleConnectionMetadataType",
    "EntitlementType",
    "MembershipState",
    "SKUFlag",
    "SKUType",
    "SubscriptionStatus",
    "TeamMemberRoleType",
]
