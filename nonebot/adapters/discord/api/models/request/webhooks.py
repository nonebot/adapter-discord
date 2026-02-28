from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .messages import AllowedMention, AttachmentSend, File
from ..common.snowflake import Snowflake
from ...types import UNSET, MessageFlag, Missing, MissingOrNullable

if TYPE_CHECKING:
    from .polls import PollRequest
    from ..common.embeds import Embed
    from ..interactions.message_components import Component, DirectComponent


class ExecuteWebhookParams(BaseModel):
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


class WebhookMessageEditParams(BaseModel):
    """Edit Webhook Message Parameters.

    All parameters are optional and nullable.

    see https://discord.com/developers/docs/resources/webhook#edit-webhook-message
    """

    content: MissingOrNullable[str] = UNSET
    embeds: MissingOrNullable[list[Embed]] = UNSET
    flags: MissingOrNullable[MessageFlag] = UNSET
    allowed_mentions: MissingOrNullable[AllowedMention] = UNSET
    components: MissingOrNullable[list[Component]] = UNSET
    files: Missing[list[File]] = UNSET
    attachments: MissingOrNullable[list[AttachmentSend]] = UNSET
    poll: MissingOrNullable[PollRequest] = UNSET


__all__ = [
    "CreateWebhookParams",
    "ExecuteWebhookParams",
    "WebhookMessageEditParams",
]
