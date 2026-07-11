"""Canonical webhook.write models."""

from typing import TYPE_CHECKING

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

from .._model_support import (
    UNSET,
    BaseModel,
    MessageFlag,
    Missing,
    MissingOrNullable,
    Snowflake,
)


class WebhookMessageEditParams(BaseModel):
    """Edit Webhook Message Parameters.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/webhook#edit-webhook-message
    """

    content: MissingOrNullable[str] = UNSET
    embeds: MissingOrNullable[list["Embed"]] = UNSET
    flags: MissingOrNullable[MessageFlag] = UNSET
    allowed_mentions: MissingOrNullable["AllowedMention"] = UNSET
    components: MissingOrNullable[list["Component"]] = UNSET
    files: Missing[list["File"]] = UNSET
    attachments: MissingOrNullable[list["AttachmentSend"]] = UNSET
    poll: MissingOrNullable["PollRequest"] = UNSET


class CreateWebhookParams(BaseModel):
    """Create Webhook Params.

    see https://discord.com/developers/docs/resources/webhook#create-webhook
    """

    name: str
    avatar: MissingOrNullable[str] = UNSET


class ExecuteWebhookParams(BaseModel):
    """Execute Webhook Parameters

    see https://discord.com/developers/docs/resources/webhook#execute-webhook"""

    content: Missing[str] = UNSET
    username: Missing[str] = UNSET
    avatar_url: Missing[str] = UNSET
    tts: Missing[bool] = UNSET
    embeds: Missing[list["Embed"]] = UNSET
    allowed_mentions: Missing["AllowedMention"] = UNSET
    components: Missing[list["DirectComponent"]] = UNSET
    files: Missing[list["File"]] = UNSET
    attachments: Missing[list["AttachmentSend"]] = UNSET
    flags: Missing[MessageFlag] = UNSET
    thread_name: Missing[str] = UNSET
    applied_tags: Missing[list[Snowflake]] = UNSET
    poll: Missing["PollRequest"] = UNSET


__all__ = ["CreateWebhookParams", "ExecuteWebhookParams", "WebhookMessageEditParams"]
