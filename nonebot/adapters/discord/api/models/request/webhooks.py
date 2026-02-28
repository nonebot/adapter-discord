from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .messages import AllowedMention, AttachmentSend, File
from ...types import UNSET, MessageFlag, Missing, MissingOrNullable

if TYPE_CHECKING:
    from ..common.embeds import Embed
    from ..http.polls import PollRequest
    from ..interactions.message_components import Component


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
