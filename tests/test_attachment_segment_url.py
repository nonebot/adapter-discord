from nonebot.adapters.discord.api.models import MessageGet
from nonebot.adapters.discord.message import Message, MessageSegment, parse_message

from nonebot.compat import type_validate_python
import pytest


def _build_message_payload() -> dict[str, object]:
    return {
        "id": "1",
        "channel_id": "100",
        "author": {
            "id": "2",
            "username": "tester",
            "discriminator": "0",
            "global_name": None,
            "avatar": None,
        },
        "content": "",
        "timestamp": "2026-02-14T00:00:00+00:00",
        "edited_timestamp": None,
        "tts": False,
        "mention_everyone": False,
        "mentions": [],
        "mention_roles": [],
        "attachments": [
            {
                "id": "10",
                "filename": "a.png",
                "size": 123,
                "url": "https://cdn.discordapp.com/attachments/1/10/a.png",
                "proxy_url": "https://media.discordapp.net/attachments/1/10/a.png",
            }
        ],
        "embeds": [],
        "pinned": False,
        "type": 0,
    }


def test_from_guild_message_preserves_attachment_url() -> None:
    message = Message.from_guild_message(
        type_validate_python(MessageGet, _build_message_payload())
    )

    attachment_segment = message["attachment"][0]

    assert (
        attachment_segment.data["url"]
        == "https://cdn.discordapp.com/attachments/1/10/a.png"
    )
    assert (
        attachment_segment.data["proxy_url"]
        == "https://media.discordapp.net/attachments/1/10/a.png"
    )


def test_sendable_rejects_url_only_attachment() -> None:
    message = Message()
    message.append(
        MessageSegment.attachment(
            "a.png", url="https://cdn.discordapp.com/attachments/1/10/a.png"
        )
    )

    with pytest.raises(ValueError, match=r"bot\.fetch_attachments\(message\)"):
        message.sendable()


def test_sendable_rejects_attachment_without_file_or_url() -> None:
    message = Message()
    message.append(MessageSegment.attachment("a.png"))

    with pytest.raises(ValueError, match="provide `content=`"):
        message.sendable()


def test_parse_message_raises_for_non_sendable_attachment() -> None:
    message = Message()
    message.append(
        MessageSegment.attachment(
            "a.png", url="https://cdn.discordapp.com/attachments/1/10/a.png"
        )
    )

    with pytest.raises(ValueError, match=r"bot\.fetch_attachments\(message\)"):
        parse_message(message)


def test_parse_message_keeps_file_attachment_upload_behavior() -> None:
    message = Message()
    message.append(
        MessageSegment.attachment(
            "a.png",
            content=b"binary",
            url="https://cdn.discordapp.com/attachments/1/10/a.png",
        )
    )

    payload = parse_message(message)

    assert "content" not in payload
    assert payload["attachments"][0].filename == "a.png"
    assert payload["files"][0].filename == "a.png"
