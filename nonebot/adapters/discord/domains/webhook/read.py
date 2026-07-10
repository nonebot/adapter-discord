"""Canonical webhook.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import User

from .._model_support import (
    UNSET,
    BaseModel,
    Field,
    Missing,
    MissingOrNullable,
    Snowflake,
    WebhookType,
)


class SourceGuild(BaseModel):
    """partial guild object for Webhook.source_guild

    see https://discord.com/developers/docs/resources/webhook#webhook-object-example-channel-follower-webhook
    """

    id: Snowflake
    name: str
    icon: str | None = None


class SourceChannel(BaseModel):
    """partial channel object for Webhook.source_channel

    see https://discord.com/developers/docs/resources/webhook#webhook-object-example-channel-follower-webhook"""

    id: Snowflake
    name: str


class Webhook(BaseModel):
    """Used to represent a webhook.

    see https://discord.com/developers/docs/resources/webhook#webhook-object"""

    id: Snowflake
    type: WebhookType
    guild_id: MissingOrNullable[Snowflake] = UNSET
    channel_id: Snowflake | None = Field(...)
    user: Missing[User] = UNSET
    name: str | None = Field(...)
    avatar: str | None = Field(...)
    token: Missing[str] = UNSET
    application_id: Snowflake | None = Field(...)
    source_guild: Missing[SourceGuild] = UNSET
    source_channel: Missing[SourceChannel] = UNSET
    url: Missing[str] = UNSET


__all__ = ["SourceChannel", "SourceGuild", "Webhook"]
