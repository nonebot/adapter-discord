"""Canonical webhook.write models."""

from typing import TYPE_CHECKING
from typing_extensions import Required

from .._model_support import OutboundTypedDict

if TYPE_CHECKING:
    from ..models import (
        AllowedMention,
        AttachmentSend,
        Component,
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

    content: str | None
    username: str | None
    avatar_url: str | None
    tts: bool | None
    embeds: "list[Embed] | None"
    allowed_mentions: "AllowedMention | None"
    components: "list[Component] | None"
    files: "list[File] | None"
    attachments: "list[AttachmentSend] | None"
    flags: int | None
    thread_name: str | None
    applied_tags: list[Snowflake] | None
    poll: "PollRequest | None"


class ModifyWebhookParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_modify_webhook``."""

    name: str
    avatar: "str | None"
    channel_id: "SnowflakeType"


class ModifyWebhookWithTokenParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_modify_webhook_with_token``."""

    name: str
    avatar: "str | None"


__all__ = [
    "CreateWebhookParams",
    "ExecuteWebhookParams",
    "ModifyWebhookParams",
    "ModifyWebhookWithTokenParams",
    "WebhookMessageEditParams",
]
