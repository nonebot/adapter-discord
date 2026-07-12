"""Interaction request conversion built on message-domain compiled parts."""

from .write import InteractionCallbackMessage
from ..message.conversion import OutboundMessageParts
from ..models import (
    AllowedMention,
    AttachmentSend,
    CreateFollowupMessageParams,
    File,
    MessageFlag,
    WebhookMessageEditParams,
)
from ...protocol import UNSET, Missing, MissingOrNullable, is_unset


def _attachment_lists(
    parts: OutboundMessageParts,
) -> tuple[Missing[list[AttachmentSend]], Missing[list[File]]]:
    if is_unset(parts.attachments):
        return UNSET, UNSET
    return (
        [part.attachment for part in parts.attachments],
        [part.file for part in parts.attachments],
    )


def to_interaction_callback(
    parts: OutboundMessageParts,
    *,
    tts: bool | None,
    allowed_mentions: AllowedMention | None,
    flags: MessageFlag | None,
) -> InteractionCallbackMessage:
    """Build initial interaction callback data without owning its lifecycle."""
    attachments, files = _attachment_lists(parts)
    request = InteractionCallbackMessage()
    if tts is not None:
        request["tts"] = tts
    if not is_unset(parts.content):
        request["content"] = parts.content
    if not is_unset(parts.embeds):
        request["embeds"] = list(parts.embeds)
    if allowed_mentions is not None:
        request["allowed_mentions"] = allowed_mentions
    if flags is not None:
        request["flags"] = flags
    if not is_unset(parts.components):
        request["components"] = list(parts.components)
    if not is_unset(attachments):
        request["attachments"] = attachments
    if not is_unset(parts.poll):
        request["poll"] = parts.poll
    if not is_unset(files):
        request["files"] = files
    return request


def to_followup_message(
    parts: OutboundMessageParts,
    *,
    tts: Missing[bool] = UNSET,
    allowed_mentions: Missing[AllowedMention] = UNSET,
    flags: Missing[MessageFlag] = UNSET,
) -> CreateFollowupMessageParams:
    """Build a followup webhook payload from compiled message parts."""

    attachments, files = _attachment_lists(parts)
    request = CreateFollowupMessageParams()
    if not is_unset(parts.content):
        request["content"] = parts.content
    if not is_unset(tts):
        request["tts"] = tts
    if not is_unset(parts.embeds):
        request["embeds"] = list(parts.embeds)
    if not is_unset(allowed_mentions):
        request["allowed_mentions"] = allowed_mentions
    if not is_unset(parts.components):
        request["components"] = list(parts.components)
    if not is_unset(files):
        request["files"] = files
    if not is_unset(attachments):
        request["attachments"] = attachments
    if not is_unset(flags):
        request["flags"] = flags
    if not is_unset(parts.poll):
        request["poll"] = parts.poll
    return request


def to_origin_edit(
    parts: OutboundMessageParts,
    *,
    flags: MissingOrNullable[MessageFlag] = UNSET,
    allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
) -> WebhookMessageEditParams:
    """Build an original/followup webhook edit payload from compiled parts."""

    attachments, files = _attachment_lists(parts)
    request = WebhookMessageEditParams()
    if not is_unset(parts.content):
        request["content"] = parts.content
    if not is_unset(parts.embeds):
        request["embeds"] = list(parts.embeds)
    if not is_unset(flags):
        request["flags"] = flags
    if not is_unset(allowed_mentions):
        request["allowed_mentions"] = allowed_mentions
    if not is_unset(parts.components):
        request["components"] = list(parts.components)
    if not is_unset(files):
        request["files"] = files
    if not is_unset(attachments):
        request["attachments"] = attachments
    if not is_unset(parts.poll):
        request["poll"] = parts.poll
    return request


__all__ = [
    "to_followup_message",
    "to_interaction_callback",
    "to_origin_edit",
]
