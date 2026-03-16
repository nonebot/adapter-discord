from datetime import datetime, timezone
import json

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
from nonebot.adapters.discord.serialization import encode_prepared_request
from nonebot.adapters.discord.utils import omit_unset


def _assert_transport_datetime(actual: str, expected: datetime) -> None:
    assert datetime.fromisoformat(actual.replace("Z", "+00:00")) == expected


def test_parse_data_keeps_explicit_null() -> None:
    payload = encode_prepared_request(parse_data({"content": None}, MessageEditParams))[
        "json"
    ]
    assert payload == {"content": None}


def test_parse_data_omits_unset() -> None:
    payload = encode_prepared_request(
        parse_data({"content": UNSET}, MessageEditParams)
    )["json"]
    assert payload == {}


def test_omit_unset_filters_unset_in_list() -> None:
    payload = omit_unset({"arr": [1, UNSET, {"a": UNSET, "b": 2}]})
    assert payload == {"arr": [1, {"b": 2}]}


def test_parse_data_message_send_omits_unset_fields() -> None:
    payload = encode_prepared_request(parse_data({}, MessageSend))["json"]
    assert payload == {}


def test_parse_data_execute_webhook_omits_unset_fields() -> None:
    payload = encode_prepared_request(parse_data({}, ExecuteWebhookParams))["json"]
    assert payload == {}


def test_parse_data_serializes_embed_timestamp() -> None:
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)
    payload = encode_prepared_request(
        parse_data(
            {"embeds": [Embed(timestamp=timestamp)]},
            MessageSend,
        )
    )["json"]

    _assert_transport_datetime(payload["embeds"][0]["timestamp"], timestamp)


def test_parse_data_multipart_keeps_null_attachments() -> None:
    res = encode_prepared_request(
        parse_data(
            {
                "files": [File(content=b"1", filename="a.txt")],
                "attachments": None,
            },
            MessageEditParams,
        )
    )
    multipart = res["files"]
    _, payload_json, _ = multipart["payload_json"]
    payload = json.loads(payload_json)
    assert payload["attachments"] is None


def test_parse_data_multipart_maps_attachment_id() -> None:
    res = encode_prepared_request(
        parse_data(
            {
                "files": [File(content=b"1", filename="a.txt")],
                "attachments": [{"filename": "a.txt"}],
            },
            MessageEditParams,
        )
    )
    multipart = res["files"]
    _, payload_json, _ = multipart["payload_json"]
    payload = json.loads(payload_json)
    assert payload["attachments"][0]["id"] == 0


def test_parse_data_keeps_action_row_type_for_components() -> None:
    payload = encode_prepared_request(
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
    )["json"]
    assert "content" not in payload
    assert int(payload["components"][0]["type"]) == int(ComponentType.ActionRow)


def test_parse_forum_thread_message_keeps_name() -> None:
    payload = encode_prepared_request(
        parse_forum_thread_message({"name": "thread-name", "content": "hello"})
    )["json"]
    assert payload["name"] == "thread-name"


def test_parse_forum_thread_message_without_content() -> None:
    payload = encode_prepared_request(
        parse_forum_thread_message({"name": "thread-name"})
    )["json"]
    assert payload["message"] == {}


def test_parse_forum_thread_message_serializes_embed_timestamp_in_multipart() -> None:
    timestamp = datetime(2026, 3, 14, 12, 0, tzinfo=timezone.utc)
    res = encode_prepared_request(
        parse_forum_thread_message(
            {
                "name": "thread-name",
                "files": [File(content=b"1", filename="a.txt")],
                "embeds": [Embed(timestamp=timestamp)],
            }
        )
    )
    multipart = res["files"]
    _, payload_json, _ = multipart["payload_json"]
    payload = json.loads(payload_json)

    _assert_transport_datetime(payload["message"]["embeds"][0]["timestamp"], timestamp)


def test_parse_forum_thread_message_maps_message_attachment_id() -> None:
    res = encode_prepared_request(
        parse_forum_thread_message(
            {
                "name": "thread-name",
                "files": [File(content=b"1", filename="a.txt")],
                "attachments": [{"filename": "a.txt"}],
            }
        )
    )
    multipart = res["files"]
    _, payload_json, _ = multipart["payload_json"]
    payload = json.loads(payload_json)
    assert payload["message"]["attachments"][0]["id"] == 0
