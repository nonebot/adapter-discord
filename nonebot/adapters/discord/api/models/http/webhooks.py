from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from ..common.snowflake import Snowflake
from ..interactions.message_components import DirectComponent
from ...types import UNSET, MessageFlag, Missing, MissingOrNullable, WebhookType

if TYPE_CHECKING:
    from .polls import PollRequest
    from ..common.embeds import Embed
    from ..common.messages import AllowedMention, AttachmentSend, File
    from ..common.user import User


class SourceGuild(BaseModel):
    """partial guild object for Webhook.source_guild

    see https://discord.com/developers/docs/resources/webhook#webhook-object-example-channel-follower-webhook
    """

    id: Snowflake
    name: str
    icon: str | None = None


class SourceChannel(BaseModel):
    """partial channel object for Webhook.source_channel

    see https://discord.com/developers/docs/resources/webhook#webhook-object-example-channel-follower-webhook
    """

    id: Snowflake
    name: str


class Webhook(BaseModel):
    """Used to represent a webhook.

    see https://discord.com/developers/docs/resources/webhook#webhook-object
    """

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


class ExecuteWebhookParams(BaseModel):
    """Execute Webhook Parameters

    see https://discord.com/developers/docs/resources/webhook#execute-webhook
    """

    content: Missing[str] = UNSET
    username: Missing[str] = UNSET
    avatar_url: Missing[str] = UNSET
    tts: Missing[bool] = UNSET
    embeds: Missing[list[Embed]] = UNSET
    allowed_mentions: Missing[AllowedMention] = UNSET
    components: Missing[list[DirectComponent]] = UNSET
    files: Missing[list[File]] = UNSET
    attachments: Missing[list[AttachmentSend]] = UNSET
    flags: Missing[MessageFlag] = UNSET
    thread_name: Missing[str] = UNSET
    applied_tags: Missing[list[Snowflake]] = UNSET


class CreateWebhookParams(BaseModel):
    name: str
    avatar: MissingOrNullable[str] = UNSET
    poll: Missing[PollRequest] = UNSET
