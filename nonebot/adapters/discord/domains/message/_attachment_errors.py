"""Shared diagnostics for unsendable attachment message segments."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...message import MessageSegment


def get_unsendable_attachment_message(index: int, attachment: "MessageSegment") -> str:
    """Explain how callers can make an attachment segment sendable."""
    if attachment.data.get("url") or attachment.data.get("proxy_url"):
        return (
            f"Attachment segment at index {index} is not sendable because file "
            "content is missing; call "
            "`await bot.fetch_attachments(message)` first"
        )
    return (
        f"Attachment segment at index {index} is not sendable because file "
        "content is missing; provide `content=` in "
        "MessageSegment.attachment(...)"
    )
