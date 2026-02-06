import json

from nonebot.adapters.discord.api.model import File, MessageEditParams
from nonebot.adapters.discord.api.types import UNSET
from nonebot.adapters.discord.api.utils import parse_data


def test_parse_data_keeps_explicit_null() -> None:
    payload = parse_data({"content": None}, MessageEditParams)["json"]
    assert payload == {"content": None}


def test_parse_data_omits_unset() -> None:
    payload = parse_data({"content": UNSET}, MessageEditParams)["json"]
    assert payload == {}


def test_parse_data_multipart_keeps_null_attachments() -> None:
    res = parse_data(
        {
            "files": [File(content=b"1", filename="a.txt")],
            "attachments": None,
        },
        MessageEditParams,
    )
    multipart = res["files"]
    _, payload_json, _ = multipart["payload_json"]
    payload = json.loads(payload_json)
    assert payload["attachments"] is None


def test_parse_data_multipart_maps_attachment_id() -> None:
    res = parse_data(
        {
            "files": [File(content=b"1", filename="a.txt")],
            "attachments": [{"filename": "a.txt"}],
        },
        MessageEditParams,
    )
    multipart = res["files"]
    _, payload_json, _ = multipart["payload_json"]
    payload = json.loads(payload_json)
    assert payload["attachments"][0]["id"] == 0
