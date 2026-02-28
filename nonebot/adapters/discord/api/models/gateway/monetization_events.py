from __future__ import annotations

from ..http.monetization import Entitlement, Subscription


class EntitlementCreate(Entitlement):
    pass


class EntitlementUpdate(Entitlement):
    pass


class EntitlementDelete(Entitlement):
    pass


class SubscriptionCreate(Subscription):
    pass


class SubscriptionUpdate(Subscription):
    pass


class SubscriptionDelete(Subscription):
    pass
