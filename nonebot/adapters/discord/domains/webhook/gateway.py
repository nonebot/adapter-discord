"""Canonical webhook.gateway models."""

from .._model_support import BaseModel, Snowflake


class WebhooksUpdate(BaseModel):
    """Webhooks Update Event Fields

    Sent when a guild channel's webhook is created, updated, or deleted.

    see https://discord.com/developers/docs/topics/gateway-events#webhooks-update
    """

    guild_id: Snowflake
    channel_id: Snowflake


__all__ = ["WebhooksUpdate"]
