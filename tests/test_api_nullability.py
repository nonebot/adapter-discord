from importlib import import_module
import json

api_model = import_module("nonebot.adapters.discord.api.model")
api_types = import_module("nonebot.adapters.discord.api.types")
api_utils = import_module("nonebot.adapters.discord.api.utils")
discord_utils = import_module("nonebot.adapters.discord.utils")

File = api_model.File
ExecuteWebhookParams = api_model.ExecuteWebhookParams
MessageSend = api_model.MessageSend
MessageEditParams = api_model.MessageEditParams
UNSET = api_types.UNSET
parse_data = api_utils.parse_data
parse_forum_thread_message = api_utils.parse_forum_thread_message
omit_unset = discord_utils.omit_unset


def test_parse_data_keeps_explicit_null() -> None:
    payload = parse_data({"content": None}, MessageEditParams)["json"]
    assert payload == {"content": None}


def test_parse_data_omits_unset() -> None:
    payload = parse_data({"content": UNSET}, MessageEditParams)["json"]
    assert payload == {}


def test_omit_unset_filters_unset_in_list() -> None:
    payload = omit_unset({"arr": [1, UNSET, {"a": UNSET, "b": 2}]})
    assert payload == {"arr": [1, {"b": 2}]}


def test_parse_data_message_send_omits_unset_fields() -> None:
    payload = parse_data({}, MessageSend)["json"]
    assert payload == {}


def test_parse_data_execute_webhook_omits_unset_fields() -> None:
    payload = parse_data({}, ExecuteWebhookParams)["json"]
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


def test_parse_data_keeps_action_row_type_for_components() -> None:
    api = import_module("nonebot.adapters.discord.api")
    action_row = api.ActionRow
    component_type = api.ComponentType
    select_menu = api.SelectMenu
    select_option = api.SelectOption

    payload = parse_data(
        {
            "components": [
                action_row(
                    components=[
                        select_menu(
                            type=component_type.StringSelect,
                            custom_id="menu",
                            options=[select_option(label="A", value="a")],
                        )
                    ]
                )
            ]
        },
        MessageSend,
    )["json"]
    assert "content" not in payload
    assert int(payload["components"][0]["type"]) == int(component_type.ActionRow)


def test_parse_forum_thread_message_keeps_name() -> None:
    payload = parse_forum_thread_message({"name": "thread-name", "content": "hello"})[
        "json"
    ]
    assert payload["name"] == "thread-name"


def test_parse_forum_thread_message_without_content() -> None:
    payload = parse_forum_thread_message({"name": "thread-name"})["json"]
    assert payload["message"] == {}


def test_parse_forum_thread_message_maps_message_attachment_id() -> None:
    res = parse_forum_thread_message(
        {
            "name": "thread-name",
            "files": [File(content=b"1", filename="a.txt")],
            "attachments": [{"filename": "a.txt"}],
        }
    )
    multipart = res["files"]
    _, payload_json, _ = multipart["payload_json"]
    payload = json.loads(payload_json)
    assert payload["message"]["attachments"][0]["id"] == 0
