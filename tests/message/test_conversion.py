from types import SimpleNamespace
import warnings

from nonebot.adapters import MessageTemplate
import nonebot.adapters.discord.commands.matcher as matcher_module
from nonebot.adapters.discord.commands.matcher import ApplicationCommandMatcher
from nonebot.adapters.discord.domains.interaction.conversion import (
    to_followup_message,
    to_interaction_callback,
    to_origin_edit,
)
from nonebot.adapters.discord.domains.message.conversion import (
    compile_message,
    to_legacy_kwargs,
    to_message_edit,
    to_message_send,
)
from nonebot.adapters.discord.domains.models import (
    ActionRow,
    Button,
    ButtonStyle,
    Embed,
    MessageFlag,
    Poll,
    PollAnswer,
    PollMedia,
)
from nonebot.adapters.discord.message import Message, MessageSegment, parse_message
from nonebot.adapters.discord.protocol import is_not_unset
from tests.fake.doubles import DummyBot

import pytest


def _poll() -> Poll:
    return Poll(
        question=PollMedia(text="question"),
        answers=[PollAnswer(answer_id=1, poll_media=PollMedia(text="answer"))],
        expiry=None,
        allow_multiselect=False,
        layout_type=1,
    )


def test_compile_message_preserves_parts_and_attachment_pairs() -> None:
    message = Message()
    message.append(MessageSegment.text("first "))
    message.append(MessageSegment.text("second"))
    message.append(MessageSegment.embed(Embed(title="first")))
    message.append(MessageSegment.embed(Embed(title="second")))
    message.append(MessageSegment.reference(1))
    message.append(MessageSegment.reference(2, fail_if_not_exists=False))
    message.append(
        MessageSegment.component(
            ActionRow(
                components=[Button(style=ButtonStyle.Primary, custom_id="x", label="X")]
            )
        )
    )
    message.append(MessageSegment.sticker(10))
    message.append(MessageSegment.sticker(11))
    message.append(MessageSegment.poll(_poll()))
    message.append(MessageSegment.attachment("same.txt", content=b"first"))
    message.append(MessageSegment.attachment("same.txt", content=b"second"))

    parts = compile_message(message)

    assert parts.content == "first second"
    assert is_not_unset(parts.embeds)
    assert is_not_unset(parts.message_reference)
    assert is_not_unset(parts.message_reference.message_id)
    assert is_not_unset(parts.sticker_ids)
    assert is_not_unset(parts.attachments)
    assert is_not_unset(parts.poll)
    assert [embed.title for embed in parts.embeds] == ["first", "second"]
    assert int(parts.message_reference.message_id) == 2
    assert parts.message_reference.fail_if_not_exists is False
    assert [int(sticker_id) for sticker_id in parts.sticker_ids] == [10, 11]
    assert parts.poll["question"].text == "question"
    assert [attachment.attachment.get("id") for attachment in parts.attachments] == [
        0,
        1,
    ]
    assert [attachment.file.content for attachment in parts.attachments] == [
        b"first",
        b"second",
    ]
    assert "id" not in message["attachment"][0].data["attachment"]

    send = to_message_send(parts, tts=False)
    assert "attachments" in send
    assert "files" in send
    attachments = send["attachments"]
    files = send["files"]
    assert attachments is not None
    assert files is not None
    assert [attachment.get("id") for attachment in attachments] == [0, 1]
    assert [file.content for file in files] == [b"first", b"second"]
    assert to_message_edit(parts).get("content") == "first second"


def test_legacy_kwargs_exactly_render_compiled_parts() -> None:
    message = Message(
        [
            MessageSegment.text("body"),
            MessageSegment.attachment("a.txt", content=b"payload"),
        ]
    )
    parts = compile_message(message)
    assert is_not_unset(parts.attachments)

    assert to_legacy_kwargs(parts) == {
        "content": "body",
        "files": [parts.attachments[0].file],
        "attachments": [message["attachment"][0].data["attachment"]],
    }


def test_compile_message_is_pure_and_rejects_unmaterialized_attachment() -> None:
    message = Message()
    message.append(MessageSegment.text("body"))
    message.append(
        MessageSegment.attachment(
            "remote.txt", url="https://cdn.discordapp.com/attachments/1/2/remote.txt"
        )
    )
    before = message.clone()

    with pytest.raises(ValueError, match=r"bot\.fetch_attachments\(message\)"):
        compile_message(message)

    assert message["attachment"][0].data == before["attachment"][0].data


def test_parse_message_warns_from_direct_compatibility_call() -> None:
    parts = compile_message("body")
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        assert parse_message("body") == to_legacy_kwargs(parts)

    assert len(captured) == 1
    assert captured[0].category is DeprecationWarning
    assert str(captured[0].message) == (
        "parse_message() is deprecated and will be removed in 2.0; pass Message "
        "to Bot.send/Bot.send_to or construct the raw request model explicitly"
    )
    assert vars(parse_message)["__deprecated__"] == str(captured[0].message)


def test_reference_preserves_false_and_falsey_identifiers() -> None:
    segment = MessageSegment.reference(
        0,
        channel_id=0,
        guild_id=0,
        fail_if_not_exists=False,
    )
    reference = segment.data["reference"]

    assert int(reference.message_id) == 0
    assert int(reference.channel_id) == 0
    assert int(reference.guild_id) == 0
    assert reference.fail_if_not_exists is False


def test_interaction_converters_preserve_compiled_values() -> None:
    parts = compile_message(MessageSegment.attachment("a.txt", content=b"data"))

    callback = to_interaction_callback(
        parts, tts=False, allowed_mentions=None, flags=None
    )
    followup = to_followup_message(parts)
    origin_edit = to_origin_edit(parts)

    callback_attachments = callback.get("attachments")
    callback_files = callback.get("files")
    assert callback_attachments is not None
    assert callback_files is not None
    assert "attachments" in followup
    assert "files" in followup
    origin_attachments = origin_edit.get("attachments")
    origin_files = origin_edit.get("files")
    followup_attachments = followup.get("attachments")
    followup_files = followup.get("files")
    assert origin_attachments is not None
    assert origin_files is not None
    assert followup_attachments is not None
    assert followup_files is not None
    assert callback_attachments[0].get("id") == 0
    assert callback_files[0].content == b"data"
    assert followup_attachments[0].get("id") == 0
    assert followup_files[0].content == b"data"
    assert origin_attachments[0].get("id") == 0
    assert origin_files[0].content == b"data"


@pytest.mark.anyio
async def test_bot_send_to_passes_typed_compiled_models(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bot = DummyBot()
    captured: dict[str, object] = {}

    async def create_message(**kwargs: object) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(bot, "create_message", create_message)

    await bot.send_to(
        42,
        Message(
            [
                MessageSegment.attachment("same.txt", content=b"first"),
                MessageSegment.attachment("same.txt", content=b"second"),
            ]
        ),
    )

    attachments = captured["attachments"]
    files = captured["files"]
    assert isinstance(attachments, list)
    assert isinstance(files, list)
    assert [attachment["id"] for attachment in attachments] == [0, 1]
    assert [file.content for file in files] == [b"first", b"second"]


@pytest.mark.anyio
async def test_matcher_template_helpers_format_before_typed_conversion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Response:
        message: object
        flags: MessageFlag | None

        async def followup_with_flags(
            self, message: object, *, flags: MessageFlag | None
        ) -> str:
            self.message = message
            self.flags = flags
            return "followup-result"

    response = Response()

    def new_context_value() -> object:
        return object()

    def matcher_context() -> SimpleNamespace:
        return SimpleNamespace(state={"name": "Discord"})

    def get_response(_event: object, _bot: object) -> Response:
        return response

    monkeypatch.setattr(
        matcher_module, "current_event", SimpleNamespace(get=new_context_value)
    )
    monkeypatch.setattr(
        matcher_module, "current_bot", SimpleNamespace(get=new_context_value)
    )
    monkeypatch.setattr(
        matcher_module, "current_matcher", SimpleNamespace(get=matcher_context)
    )
    monkeypatch.setattr(matcher_module, "get_command_response", get_response)

    with pytest.warns(
        DeprecationWarning,
        match=r"send_followup_msg\(\) is deprecated and will be removed in 2.0; inject CommandResponse and call response.followup\(\)",
    ):
        result = await ApplicationCommandMatcher.send_followup_msg(
            MessageTemplate("hello {name}")
        )

    assert result == "followup-result"
    assert response.message == "hello Discord"
    assert response.flags is None
