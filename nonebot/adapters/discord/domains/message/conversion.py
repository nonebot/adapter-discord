"""Pure conversion from NoneBot message segments to canonical Discord requests."""

from dataclasses import dataclass
from typing import Any, cast
from typing_extensions import NotRequired, TypedDict, Unpack

from ._attachment_errors import get_unsendable_attachment_message
from ..models import (
    AllowedMention,
    AttachmentSend,
    DirectComponent,
    Embed,
    File,
    MessageEditParams,
    MessageFlag,
    MessageReference,
    MessageSend,
    Poll,
    PollAnswerRequest,
    PollRequest,
)
from ...message import Message, MessageSegment
from ...protocol import UNSET, Missing, MissingOrNullable, Snowflake, is_unset


@dataclass(frozen=True, slots=True)
class OutboundAttachment:
    """One upload and its metadata, kept together to preserve pairing."""

    attachment: AttachmentSend
    file: File


@dataclass(frozen=True, slots=True)
class OutboundMessageParts:
    """The segment-derived portion of an outbound Discord message."""

    content: Missing[str] = UNSET
    embeds: Missing[tuple[Embed, ...]] = UNSET
    message_reference: Missing[MessageReference] = UNSET
    components: Missing[tuple[DirectComponent, ...]] = UNSET
    sticker_ids: Missing[tuple[Snowflake, ...]] = UNSET
    poll: Missing[PollRequest] = UNSET
    attachments: Missing[tuple[OutboundAttachment, ...]] = UNSET


class MessageSendOptions(TypedDict):
    """Keyword options for adding create-message fields to compiled parts."""

    nonce: NotRequired[Missing[int | str]]
    enforce_nonce: NotRequired[Missing[bool]]
    tts: NotRequired[Missing[bool]]
    allowed_mentions: NotRequired[Missing[AllowedMention]]
    flags: NotRequired[Missing[MessageFlag]]


def _copy_attachment_with_id(attachment: AttachmentSend, index: int) -> AttachmentSend:
    """Return upload metadata with its unambiguous multipart index assigned."""

    if hasattr(attachment, "model_copy"):
        return attachment.model_copy(update={"id": index})
    return attachment.copy(update={"id": index})


def _to_message(message: Message | MessageSegment | str) -> Message:
    if isinstance(message, str):
        return Message(MessageSegment.text(message))
    if isinstance(message, Message):
        return message
    return Message(message)


def _to_poll_request(poll: Poll | PollRequest) -> PollRequest:
    if isinstance(poll, PollRequest):
        return poll
    return PollRequest(
        question=poll.question,
        answers=[
            PollAnswerRequest(poll_media=answer.poll_media) for answer in poll.answers
        ],
        allow_multiselect=poll.allow_multiselect,
        layout_type=poll.layout_type,
    )


def compile_message(message: Message | MessageSegment | str) -> OutboundMessageParts:
    """Compile segments without I/O or changing the caller's message object."""

    source = _to_message(message)
    content = source.extract_content() or UNSET

    embed_segments = source["embed"] or ()
    embeds: Missing[tuple[Embed, ...]] = (
        tuple(segment.data["embed"] for segment in embed_segments)
        if embed_segments
        else UNSET
    )

    reference_segments = source["reference"] or ()
    message_reference: Missing[MessageReference] = (
        reference_segments[-1].data["reference"] if reference_segments else UNSET
    )

    component_segments = source["component"] or ()
    components: Missing[tuple[DirectComponent, ...]] = (
        tuple(segment.data["component"] for segment in component_segments)
        if component_segments
        else UNSET
    )

    sticker_segments = source["sticker"] or ()
    sticker_ids: Missing[tuple[Snowflake, ...]] = (
        tuple(segment.data["id"] for segment in sticker_segments)
        if sticker_segments
        else UNSET
    )

    poll_segments = source["poll"] or ()
    poll: Missing[PollRequest] = (
        _to_poll_request(poll_segments[-1].data["poll"]) if poll_segments else UNSET
    )

    attachment_segments = source["attachment"] or ()
    compiled_attachments: list[OutboundAttachment] = []
    for index, segment in enumerate(attachment_segments):
        file = segment.data["file"]
        if file is None:
            raise ValueError(get_unsendable_attachment_message(index, segment))
        compiled_attachments.append(
            OutboundAttachment(
                attachment=_copy_attachment_with_id(segment.data["attachment"], index),
                file=file,
            )
        )
    attachments: Missing[tuple[OutboundAttachment, ...]] = (
        tuple(compiled_attachments) if compiled_attachments else UNSET
    )

    return OutboundMessageParts(
        content=content,
        embeds=embeds,
        message_reference=message_reference,
        components=components,
        sticker_ids=sticker_ids,
        poll=poll,
        attachments=attachments,
    )


def _attachment_lists(
    parts: OutboundMessageParts,
) -> tuple[Missing[list[AttachmentSend]], Missing[list[File]]]:
    if is_unset(parts.attachments):
        return UNSET, UNSET
    return (
        [part.attachment for part in parts.attachments],
        [part.file for part in parts.attachments],
    )


def _legacy_attachment(attachment: AttachmentSend) -> AttachmentSend:
    """Drop the compiler-only multipart index for the legacy raw payload."""

    if hasattr(attachment, "model_copy"):
        return attachment.model_copy(update={"id": UNSET})
    return attachment.copy(update={"id": UNSET})


def to_message_send(
    parts: OutboundMessageParts, **options: Unpack[MessageSendOptions]
) -> MessageSend:
    """Add create-message options to compiled parts."""
    nonce = cast("Missing[int | str]", options.get("nonce", UNSET))
    enforce_nonce = cast("Missing[bool]", options.get("enforce_nonce", UNSET))
    tts = cast("Missing[bool]", options.get("tts", UNSET))
    allowed_mentions = cast(
        "Missing[AllowedMention]", options.get("allowed_mentions", UNSET)
    )
    flags = cast("Missing[MessageFlag]", options.get("flags", UNSET))

    attachments, files = _attachment_lists(parts)
    return MessageSend(
        content=parts.content,
        nonce=nonce,
        enforce_nonce=enforce_nonce,
        tts=tts,
        embeds=list(parts.embeds) if not is_unset(parts.embeds) else UNSET,
        allowed_mentions=allowed_mentions,
        message_reference=parts.message_reference,
        components=(
            list(parts.components) if not is_unset(parts.components) else UNSET
        ),
        sticker_ids=(
            list(parts.sticker_ids) if not is_unset(parts.sticker_ids) else UNSET
        ),
        files=files,
        attachments=attachments,
        flags=flags,
        poll=parts.poll,
    )


def to_message_edit(
    parts: OutboundMessageParts,
    *,
    flags: MissingOrNullable[MessageFlag] = UNSET,
) -> MessageEditParams:
    """Add edit-message options to compiled parts."""

    attachments, files = _attachment_lists(parts)
    return MessageEditParams(
        content=parts.content,
        embeds=list(parts.embeds) if not is_unset(parts.embeds) else UNSET,
        flags=flags,
        components=(
            list(parts.components) if not is_unset(parts.components) else UNSET
        ),
        files=files,
        attachments=attachments,
        sticker_ids=(
            list(parts.sticker_ids) if not is_unset(parts.sticker_ids) else UNSET
        ),
        poll=parts.poll,
    )


def to_legacy_kwargs(parts: OutboundMessageParts) -> dict[str, Any]:
    """Render the 1.x ``parse_message`` result from typed compiled parts."""

    result: dict[str, Any] = {}
    if not is_unset(parts.content):
        result["content"] = parts.content
    if not is_unset(parts.embeds):
        result["embeds"] = list(parts.embeds)
    if not is_unset(parts.message_reference):
        result["message_reference"] = parts.message_reference
    if not is_unset(parts.components):
        result["components"] = list(parts.components)
    if not is_unset(parts.sticker_ids):
        result["sticker_ids"] = list(parts.sticker_ids)
    if not is_unset(parts.poll):
        result["poll"] = parts.poll
    if not is_unset(parts.attachments):
        result["files"] = [part.file for part in parts.attachments]
        result["attachments"] = [
            _legacy_attachment(part.attachment) for part in parts.attachments
        ]
    return result


__all__ = [
    "OutboundAttachment",
    "OutboundMessageParts",
    "compile_message",
    "to_legacy_kwargs",
    "to_message_edit",
    "to_message_send",
]
