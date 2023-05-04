from typing import Any, Dict, Type, Union, Literal

from ..utils import json_dumps
from .model import MessageSend, ExecuteWebhookParams


def parse_data(
    data: Dict[str, Any], model_class: Type[Union[MessageSend, ExecuteWebhookParams]]
) -> Dict[Literal["files", "json"], Any]:
    model = model_class.parse_obj(data)
    payload = model.dict(exclude={"files"}, exclude_none=True)
    if model.files:
        multipart = {"payload_json": None}
        attachments: list[dict] = payload.pop("attachments", [])
        for index, file in enumerate(model.files):
            for attachment in attachments:
                if attachment["filename"] == file.filename:
                    attachment["id"] = str(index)
                    break
            multipart[f"file[{index}]"] = (file.filename, file.content)
        if attachments:
            payload["attachments"] = attachments
        multipart["payload_json"] = (None, json_dumps(payload), "application/json")
        return {"files": multipart}
    else:
        return {"json": payload}


def parse_forum_thread_message(
    data: Dict[str, Any]
) -> Dict[Literal["files", "json"], Any]:
    model = MessageSend.parse_obj(data)
    payload = {}
    content = model.dict(exclude={"files"}, exclude_none=True)
    if auto_archive_duration := data.pop("auto_archive_duration"):
        payload["auto_archive_duration"] = auto_archive_duration
    if rate_limit_per_user := data.pop("rate_limit_per_user"):
        payload["rate_limit_per_user"] = rate_limit_per_user
    if applied_tags := data.pop("applied_tags"):
        payload["applied_tags"] = applied_tags
    payload["message"] = content
    if model.files:
        multipart = {"payload_json": None}
        attachments: list[dict] = payload.pop("attachments", [])
        for index, file in enumerate(model.files):
            for attachment in attachments:
                if attachment["filename"] == file.filename:
                    attachment["id"] = str(index)
                    break
            multipart[f"file[{index}]"] = (file.filename, file.content)
        if attachments:
            payload["attachments"] = attachments
        multipart["payload_json"] = (None, json_dumps(payload), "application/json")
        return {"files": multipart}
    else:
        return {"json": payload}
