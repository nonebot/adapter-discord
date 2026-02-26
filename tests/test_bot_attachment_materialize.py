from nonebot.adapters.discord.message import Message, MessageSegment, parse_message
from tests.fake.doubles import DummyAdapter, DummyBot

import pytest


def _build_bot(adapter: DummyAdapter) -> DummyBot:
    return DummyBot(adapter)


@pytest.mark.anyio
async def test_fetch_attachments_materializes_remote_attachment_to_file() -> None:
    adapter = DummyAdapter(content=b"image")
    bot = _build_bot(adapter)

    message = Message()
    message.append(MessageSegment.text("foo"))
    message.append(
        MessageSegment.attachment(
            "a.png", url="https://cdn.discordapp.com/attachments/1/10/a.png"
        )
    )

    fetched = await bot.fetch_attachments(message)
    payload = parse_message(fetched)

    assert message["attachment"][0].data["file"] is None
    assert payload["content"] == "foo"
    assert payload["attachments"][0].filename == "a.png"
    assert payload["files"][0].filename == "a.png"
    assert payload["files"][0].content == b"image"
    assert adapter.request_calls == 1


@pytest.mark.anyio
async def test_fetch_attachments_rejects_unsupported_host_by_default() -> None:
    adapter = DummyAdapter(content=b"image")
    bot = _build_bot(adapter)

    message = Message()
    message.append(MessageSegment.attachment("a.png", url="https://example.com/a.png"))

    with pytest.raises(ValueError, match="has no fetchable url/proxy_url"):
        await bot.fetch_attachments(message)
    assert adapter.request_calls == 0


@pytest.mark.anyio
async def test_fetch_attachments_supports_custom_allowed_hosts() -> None:
    adapter = DummyAdapter(content=b"image")
    bot = _build_bot(adapter)

    message = Message()
    message.append(MessageSegment.attachment("a.png", url="https://example.com/a.png"))

    fetched = await bot.fetch_attachments(message, allowed_hosts={"example.com"})
    payload = parse_message(fetched)

    assert payload["attachments"][0].filename == "a.png"
    assert payload["files"][0].content == b"image"
    assert adapter.request_calls == 1


@pytest.mark.anyio
async def test_fetch_attachments_honors_max_bytes_limit() -> None:
    adapter = DummyAdapter(content=b"123456")
    bot = _build_bot(adapter)

    message = Message()
    message.append(
        MessageSegment.attachment(
            "a.png", url="https://cdn.discordapp.com/attachments/1/10/a.png"
        )
    )

    with pytest.raises(ValueError, match="Failed to fetch attachment content"):
        await bot.fetch_attachments(message, max_bytes=5)


@pytest.mark.anyio
async def test_fetch_attachments_skip_error_keeps_message_unsendable() -> None:
    adapter = DummyAdapter(status_code=404, content=b"")
    bot = _build_bot(adapter)

    message = Message()
    message.append(
        MessageSegment.attachment(
            "a.png", url="https://cdn.discordapp.com/attachments/1/10/a.png"
        )
    )

    fetched = await bot.fetch_attachments(message, on_error="skip")

    with pytest.raises(ValueError, match=r"bot\.fetch_attachments\(message\)"):
        fetched.sendable()
    assert adapter.request_calls == 1
