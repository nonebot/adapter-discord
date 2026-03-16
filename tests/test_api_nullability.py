from datetime import datetime, timezone
import json
from typing import Any

from nonebot.adapters.discord.api import (
    ActionRow,
    ComponentType,
    SelectMenu,
    SelectOption,
)
from nonebot.adapters.discord.api.model import (
    Embed,
    ExecuteWebhookParams,
    File,
    MessageEditParams,
    MessageSend,
)
from nonebot.adapters.discord.api.types import UNSET
from nonebot.adapters.discord.api.utils import parse_data, parse_forum_thread_message
from nonebot.adapters.discord.serialization import (
    PreparedRequest,
    encode_prepared_request,
)
from nonebot.adapters.discord.utils import omit_unset


def _json_payload(prepared: PreparedRequest) -> dict[str, Any]:
    encoded = encode_prepared_request(prepared)
    assert "json" in encoded
    return encoded["json"]


def _payload_json_text(prepared: PreparedRequest) -> str:
    encoded = encode_prepared_request(prepared)
    assert "files" in encoded
    payload_json = encoded["files"]["payload_json"]
    assert isinstance(payload_json, tuple)
    assert len(payload_json) >= 2
    payload_body = payload_json[1]
    assert isinstance(payload_body, (bytes, str))
    return payload_body.decode() if isinstance(payload_body, bytes) else payload_body


def _assert_transport_datetime(actual: str, expected: datetime) -> None:
    assert datetime.fromisoformat(actual.replace("Z", "+00:00")) == expected


def test_parse_data_keeps_explicit_null() -> None:
    payload = _json_payload(parse_data({"content": None}, MessageEditParams))
    assert payload == {"content": None}


def test_parse_data_omits_unset() -> None:
    payload = _json_payload(parse_data({"content": UNSET}, MessageEditParams))
    assert payload == {}


def test_omit_unset_filters_unset_in_list() -> None:
    payload = omit_unset({"arr": [1, UNSET, {"a": UNSET, "b": 2}]})
    assert payload == {"arr": [1, {"b": 2}]}


def test_parse_data_message_send_omits_unset_fields() -> None:
    payload = _json_payload(parse_data({}, MessageSend))
    assert payload == {}


def test_parse_data_execute_webhook_omits_unset_fields() -> None:
    payload = _json_payload(parse_data({}, ExecuteWebhookParams))
    assert payload == {}


def test_parse_data_serializes_embed_timestamp() -> None:
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)
    payload = _json_payload(
        parse_data(
            {"embeds": [Embed(timestamp=timestamp)]},
            MessageSend,
        )
    )

    _assert_transport_datetime(payload["embeds"][0]["timestamp"], timestamp)


def test_parse_data_multipart_keeps_null_attachments() -> None:
    payload = json.loads(
        _payload_json_text(
            parse_data(
                {
                    "files": [File(content=b"1", filename="a.txt")],
                    "attachments": None,
                },
                MessageEditParams,
            )
        )
    )
    assert payload["attachments"] is None


def test_parse_data_multipart_maps_attachment_id() -> None:
    payload = json.loads(
        _payload_json_text(
            parse_data(
                {
                    "files": [File(content=b"1", filename="a.txt")],
                    "attachments": [{"filename": "a.txt"}],
                },
                MessageEditParams,
            )
        )
    )
    assert payload["attachments"][0]["id"] == 0


def test_parse_data_keeps_action_row_type_for_components() -> None:
    payload = _json_payload(
        parse_data(
            {
                "components": [
                    ActionRow(
                        components=[
                            SelectMenu(
                                type=ComponentType.StringSelect,
                                custom_id="menu",
                                options=[SelectOption(label="A", value="a")],
                            )
                        ]
                    )
                ]
            },
            MessageSend,
        )
    )
    assert "content" not in payload
    assert int(payload["components"][0]["type"]) == int(ComponentType.ActionRow)


def test_parse_forum_thread_message_keeps_name() -> None:
    payload = _json_payload(
        parse_forum_thread_message({"name": "thread-name", "content": "hello"})
    )
    assert payload["name"] == "thread-name"


def test_parse_forum_thread_message_without_content() -> None:
    payload = _json_payload(parse_forum_thread_message({"name": "thread-name"}))
    assert payload["message"] == {}


def test_parse_forum_thread_message_serializes_embed_timestamp_in_multipart() -> None:
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)
    payload = json.loads(
        _payload_json_text(
            parse_forum_thread_message(
                {
                    "name": "thread-name",
                    "files": [File(content=b"1", filename="a.txt")],
                    "embeds": [Embed(timestamp=timestamp)],
                }
            )
        )
    )

    _assert_transport_datetime(payload["message"]["embeds"][0]["timestamp"], timestamp)


def test_parse_forum_thread_message_maps_message_attachment_id() -> None:
    payload = json.loads(
        _payload_json_text(
            parse_forum_thread_message(
                {
                    "name": "thread-name",
                    "files": [File(content=b"1", filename="a.txt")],
                    "attachments": [{"filename": "a.txt"}],
                }
            )
        )
    )
    assert payload["message"]["attachments"][0]["id"] == 0
