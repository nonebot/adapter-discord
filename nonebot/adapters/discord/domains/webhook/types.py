from __future__ import annotations

from enum import IntEnum


class WebhookType(IntEnum):
    """Webhook type.

    see https://discord.com/developers/docs/resources/webhook#webhook-object-webhook-types
    """

    Incoming = 1
    """	Incoming Webhooks can post messages to channels with a generated token"""
    Channel_Follower = 2
    """	Channel Follower Webhooks are internal webhooks used with Channel
    Following to post new messages into channels"""
    Application = 3
    """Application webhooks are webhooks used with Interactions"""


__all__ = ["WebhookType"]
