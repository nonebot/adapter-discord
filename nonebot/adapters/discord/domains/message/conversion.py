"""Pure conversion from NoneBot message segments to canonical Discord requests."""

from dataclasses import dataclass
from typing import Any
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
from ...api.validation import validate_outbound_value
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

    nonce: NotRequired[int | str]
    enforce_nonce: NotRequired[bool]
    tts: NotRequired[bool]
    allowed_mentions: NotRequired[AllowedMention]
    flags: NotRequired[MessageFlag]


def _copy_attachment_with_id(attachment: AttachmentSend, index: int) -> AttachmentSend:
    """Return upload metadata with its unambiguous multipart index assigned."""

    copied = AttachmentSend(**attachment)
    copied["id"] = index
    return copied


def _to_message(message: Message | MessageSegment | str) -> Message:
    if isinstance(message, str):
        return Message(MessageSegment.text(message))
    if isinstance(message, Message):
        return message
    return Message(message)


def _to_poll_request(poll: Poll | PollRequest) -> PollRequest:
    if not isinstance(poll, Poll):
        return validate_outbound_value(PollRequest, poll)
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

    copied = AttachmentSend(**attachment)
    copied.pop("id", None)
    return copied


def to_message_send(  # noqa: C901, PLR0912
    parts: OutboundMessageParts, **options: Unpack[MessageSendOptions]
) -> MessageSend:
    """Add create-message options to compiled parts."""
    attachments, files = _attachment_lists(parts)
    request = MessageSend()
    if not is_unset(parts.content):
        request["content"] = parts.content
    if not is_unset(parts.embeds):
        request["embeds"] = list(parts.embeds)
    if not is_unset(parts.message_reference):
        request["message_reference"] = parts.message_reference
    if not is_unset(parts.components):
        request["components"] = list(parts.components)
    if not is_unset(parts.sticker_ids):
        request["sticker_ids"] = list(parts.sticker_ids)
    if not is_unset(parts.poll):
        request["poll"] = parts.poll
    if not is_unset(attachments):
        request["attachments"] = attachments
    if not is_unset(files):
        request["files"] = files
    if "nonce" in options:
        request["nonce"] = options["nonce"]
    if "enforce_nonce" in options:
        request["enforce_nonce"] = options["enforce_nonce"]
    if "tts" in options:
        request["tts"] = options["tts"]
    if "allowed_mentions" in options:
        request["allowed_mentions"] = options["allowed_mentions"]
    if "flags" in options:
        request["flags"] = options["flags"]
    return request


def to_message_edit(
    parts: OutboundMessageParts,
    *,
    flags: MissingOrNullable[MessageFlag] = UNSET,
) -> MessageEditParams:
    """Add edit-message options to compiled parts."""

    attachments, files = _attachment_lists(parts)
    request = MessageEditParams()
    if not is_unset(parts.content):
        request["content"] = parts.content
    if not is_unset(parts.embeds):
        request["embeds"] = list(parts.embeds)
    if not is_unset(parts.components):
        request["components"] = list(parts.components)
    if not is_unset(parts.sticker_ids):
        request["sticker_ids"] = list(parts.sticker_ids)
    if not is_unset(parts.poll):
        request["poll"] = parts.poll
    if not is_unset(attachments):
        request["attachments"] = attachments
    if not is_unset(files):
        request["files"] = files
    if not is_unset(flags):
        request["flags"] = flags
    return request


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
