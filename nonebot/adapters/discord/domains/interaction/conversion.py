"""Interaction request conversion built on message-domain compiled parts."""

from ..message.conversion import OutboundMessageParts
from ..models import (
    AllowedMention,
    AttachmentSend,
    ExecuteWebhookParams,
    File,
    InteractionCallbackMessage,
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
    return InteractionCallbackMessage(
        tts=tts,
        content=None if is_unset(parts.content) else parts.content,
        embeds=None if is_unset(parts.embeds) else list(parts.embeds),
        allowed_mentions=allowed_mentions,
        flags=flags,
        components=None if is_unset(parts.components) else list(parts.components),
        attachments=None if is_unset(attachments) else attachments,
        poll=None if is_unset(parts.poll) else parts.poll,
        files=None if is_unset(files) else files,
    )


def to_followup_message(
    parts: OutboundMessageParts,
    *,
    tts: Missing[bool] = UNSET,
    allowed_mentions: Missing[AllowedMention] = UNSET,
    flags: Missing[MessageFlag] = UNSET,
) -> ExecuteWebhookParams:
    """Build a followup webhook payload from compiled message parts."""

    attachments, files = _attachment_lists(parts)
    return ExecuteWebhookParams(
        content=parts.content,
        tts=tts,
        embeds=list(parts.embeds) if not is_unset(parts.embeds) else UNSET,
        allowed_mentions=allowed_mentions,
        components=(
            list(parts.components) if not is_unset(parts.components) else UNSET
        ),
        files=files,
        attachments=attachments,
        flags=flags,
        poll=parts.poll,
    )


def to_origin_edit(
    parts: OutboundMessageParts,
    *,
    flags: MissingOrNullable[MessageFlag] = UNSET,
    allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
) -> WebhookMessageEditParams:
    """Build an original/followup webhook edit payload from compiled parts."""

    attachments, files = _attachment_lists(parts)
    return WebhookMessageEditParams(
        content=parts.content,
        embeds=list(parts.embeds) if not is_unset(parts.embeds) else UNSET,
        flags=flags,
        allowed_mentions=allowed_mentions,
        components=(
            list(parts.components) if not is_unset(parts.components) else UNSET
        ),
        files=files,
        attachments=attachments,
        poll=parts.poll,
    )


__all__ = [
    "to_followup_message",
    "to_interaction_callback",
    "to_origin_edit",
]
