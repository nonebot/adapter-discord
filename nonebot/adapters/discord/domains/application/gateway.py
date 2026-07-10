"""Canonical application.gateway models."""

from __future__ import annotations

from ..application.read import Entitlement, Subscription


class EntitlementCreate(Entitlement):
    """Entitlement Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-create"""


class EntitlementUpdate(Entitlement):
    """Entitlement Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-update"""


class EntitlementDelete(Entitlement):
    """Entitlement Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-delete"""


class SubscriptionCreate(Subscription):
    """Subscription Create Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#subscription-create"""


class SubscriptionUpdate(Subscription):
    """Subscription Update Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#subscription-update"""


class SubscriptionDelete(Subscription):
    """Subscription Delete Event Fields

    see https://discord.com/developers/docs/topics/gateway-events#subscription-delete"""


__all__ = [
    "EntitlementCreate",
    "EntitlementDelete",
    "EntitlementUpdate",
    "SubscriptionCreate",
    "SubscriptionDelete",
    "SubscriptionUpdate",
]
