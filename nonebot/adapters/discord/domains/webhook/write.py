"""Canonical webhook.write models."""

from typing import TYPE_CHECKING
from typing_extensions import Required

from .._model_support import OutboundTypedDict

if TYPE_CHECKING:
    from ..models import (
        AllowedMention,
        AttachmentSend,
        Component,
        DirectComponent,
        Embed,
        File,
        PollRequest,
    )
    from ...protocol import SnowflakeType

from .._model_support import MessageFlag, Snowflake


class WebhookMessageEditParams(OutboundTypedDict, total=False):
    """Edit Webhook Message Parameters.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/webhook#edit-webhook-message
    """

    content: str | None
    embeds: "list[Embed] | None"
    flags: MessageFlag | None
    allowed_mentions: "AllowedMention | None"
    components: "list[Component] | None"
    files: "list[File]"
    attachments: "list[AttachmentSend] | None"
    poll: "PollRequest | None"


class CreateWebhookParams(OutboundTypedDict, total=False):
    """Create Webhook Params.

    see https://discord.com/developers/docs/resources/webhook#create-webhook
    """

    name: Required[str]
    avatar: str | None


class ExecuteWebhookParams(OutboundTypedDict, total=False):
    """Execute Webhook Parameters

    see https://discord.com/developers/docs/resources/webhook#execute-webhook"""

    content: str
    username: str
    avatar_url: str
    tts: bool
    embeds: "list[Embed]"
    allowed_mentions: "AllowedMention"
    components: "list[DirectComponent]"
    files: "list[File]"
    attachments: "list[AttachmentSend]"
    flags: MessageFlag
    thread_name: str
    applied_tags: list[Snowflake]
    poll: "PollRequest"


class ModifyWebhookParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_modify_webhook``."""

    name: str
    avatar: "str | None"
    channel_id: "SnowflakeType"


__all__ = [
    "CreateWebhookParams",
    "ExecuteWebhookParams",
    "ModifyWebhookParams",
    "WebhookMessageEditParams",
]
