from nonebot.adapters.discord.api import (
    ActionRow,
    Button,
    ButtonStyle,
    ComponentType,
    Embed,
    File,
    MessageReference,
    Poll,
    PollAnswer,
    PollMedia,
    PollRequest,
)
from nonebot.adapters.discord.message import Message, MessageSegment, parse_message

from nonebot.compat import type_validate_python
import pytest


def test_text_segment_from_dict() -> None:
    seg = type_validate_python(MessageSegment, {"type": "text", "data": {"text": "hi"}})
    assert seg.type == "text"
    assert str(seg) == "hi"


def test_embed_segment_from_dict() -> None:
    seg = type_validate_python(
        MessageSegment, {"type": "embed", "data": {"embed": {"title": "t"}}}
    )
    assert seg.type == "embed"
    assert isinstance(seg.data["embed"], Embed)


def test_reference_segment_from_dict() -> None:
    seg = type_validate_python(
        MessageSegment,
        {"type": "reference", "data": {"reference": {"message_id": "123"}}},
    )
    assert seg.type == "reference"
    assert isinstance(seg.data["reference"], MessageReference)
    assert int(seg.data["reference"].message_id) == 123


def test_attachment_segment_from_dict() -> None:
    seg = type_validate_python(
        MessageSegment,
        {
            "type": "attachment",
            "data": {
                "attachment": {"filename": "a.txt"},
                "file": {"filename": "a.txt", "content": b"data"},
            },
        },
    )
    assert seg.type == "attachment"
    assert seg.data["attachment"].filename == "a.txt"
    assert isinstance(seg.data["file"], File)


def test_component_segment_action_row_from_dict() -> None:
    seg = type_validate_python(
        MessageSegment,
        {
            "type": "component",
            "data": {
                "component": {
                    "type": int(ComponentType.ActionRow),
                    "components": [
                        {"type": 2, "style": 1, "custom_id": "x", "label": "X"},
                    ],
                }
            },
        },
    )
    assert seg.type == "component"
    assert int(seg.data["component"].type) == int(ComponentType.ActionRow)


def test_component_segment_text_input_from_dict() -> None:
    seg = type_validate_python(
        MessageSegment,
        {
            "type": "component",
            "data": {
                "component": {
                    "type": int(ComponentType.TextInput),
                    "custom_id": "modal_input",
                    "style": 1,
                    "label": "Title",
                }
            },
        },
    )
    assert seg.type == "component"
    assert int(seg.data["component"].type) == int(ComponentType.TextInput)


def test_poll_segment_from_dict() -> None:
    seg = type_validate_python(
        MessageSegment,
        {
            "type": "poll",
            "data": {
                "poll": {
                    "question": {"text": "Q"},
                    "answers": [{"poll_media": {"text": "A"}}],
                    "duration": 24,
                    "allow_multiselect": False,
                    "layout_type": 1,
                }
            },
        },
    )
    assert seg.type == "poll"
    assert seg.data["poll"].question.text == "Q"


def test_unknown_segment_type_raises() -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        type_validate_python(MessageSegment, {"type": "unknown", "data": {}})


def test_parse_message_integration() -> None:
    msg = Message()
    msg.append(MessageSegment.text("hi"))
    msg.append(MessageSegment.embed(Embed(title="t")))
    msg.append(MessageSegment.reference(123))
    msg.append(
        MessageSegment.component(
            ActionRow(
                components=[Button(style=ButtonStyle.Primary, custom_id="x", label="X")]
            )
        )
    )
    msg.append(MessageSegment.attachment("a.txt", content=b"x"))

    poll = Poll(
        question=PollMedia(text="Q"),
        answers=[PollAnswer(answer_id=1, poll_media=PollMedia(text="A"))],
        expiry=None,
        allow_multiselect=False,
        layout_type=1,
    )
    msg.append(MessageSegment.poll(poll))

    payload = parse_message(msg)
    assert payload["content"] == "hi"
    assert payload["embeds"][0].title == "t"
    assert int(payload["message_reference"].message_id) == 123
    assert int(payload["components"][0].type) == int(ComponentType.ActionRow)
    assert payload["attachments"][0].filename == "a.txt"
    assert payload["files"][0].content == b"x"
    assert isinstance(payload["poll"], PollRequest)
