import json
from typing import Any, Literal, Union

from nonebot.compat import type_validate_python

from .model import (
    ExecuteWebhookParams,
    InteractionCallbackMessage,
    InteractionResponse,
    MessageEditParams,
    MessageSend,
    WebhookMessageEditParams,
)
from .types import UNSET
from ..utils import model_dump


def omit_unset(data: Any) -> Any:  # noqa: ANN401
    """Recursively omit fields whose value is exactly ``UNSET``.

    Notes:
    - Keep ``None`` as-is to allow explicitly sending JSON ``null``.
    - This helper is intended for handles that build request payloads via
      plain ``dict``/``list`` instead of Pydantic models.
    """

    if isinstance(data, dict):
        return data.__class__(
            (k, omit_unset(v)) for k, v in data.items() if v is not UNSET
        )
    if isinstance(data, (list, tuple, set)):
        return data.__class__(omit_unset(i) for i in data if i is not UNSET)
    return data


def parse_data(
    data: dict[str, Any],
    model_class: type[
        Union[
            ExecuteWebhookParams,
            MessageEditParams,
            MessageSend,
            WebhookMessageEditParams,
        ]
    ],
) -> dict[Literal["files", "json"], Any]:
    model = type_validate_python(model_class, data)
    payload: dict[str, Any] = model_dump(model, exclude={"files"}, exclude_unset=True)
    files = getattr(model, "files", None)
    if files is not None and files is not UNSET and len(files) > 0:
        multipart: dict[str, Any] = {}
        attachments = payload.get("attachments", [])
        if isinstance(attachments, list):
            attachments = payload.pop("attachments", [])
        for index, file in enumerate(files):
            if isinstance(attachments, list):
                for attachment in attachments:
                    if attachment.get("filename") == file.filename:
                        attachment["id"] = index
                        break
            multipart[f"files[{index}]"] = (file.filename, file.content)
        if isinstance(attachments, list) and attachments:
            payload["attachments"] = attachments
        multipart["payload_json"] = (None, json.dumps(payload), "application/json")
        return {"files": multipart}
    return {"json": payload}


def parse_forum_thread_message(
    data: dict[str, Any],
) -> dict[Literal["files", "json"], Any]:
    model = type_validate_python(MessageSend, data)
    payload: dict[str, Any] = {}
    content: dict[str, Any] = model_dump(model, exclude={"files"}, exclude_none=True)
    auto_archive_duration = data.pop("auto_archive_duration", UNSET)
    if auto_archive_duration is not UNSET and auto_archive_duration is not None:
        payload["auto_archive_duration"] = auto_archive_duration
    rate_limit_per_user = data.pop("rate_limit_per_user", UNSET)
    if rate_limit_per_user is not UNSET:
        payload["rate_limit_per_user"] = rate_limit_per_user
    applied_tags = data.pop("applied_tags", UNSET)
    if applied_tags is not UNSET and applied_tags is not None:
        payload["applied_tags"] = applied_tags
    payload["message"] = content
    if model.files:
        multipart: dict[str, Any] = {"payload_json": None}
        attachments: list[dict] = payload.pop("attachments", [])
        for index, file in enumerate(model.files):
            for attachment in attachments:
                if attachment["filename"] == file.filename:
                    attachment["id"] = index
                    break
            multipart[f"files[{index}]"] = (file.filename, file.content)
        if attachments:
            payload["attachments"] = attachments
        multipart["payload_json"] = (None, json.dumps(payload), "application/json")
        return {"files": multipart}
    return {"json": payload}


def parse_interaction_response(
    response: InteractionResponse,
) -> dict[Literal["files", "json"], Any]:
    payload: dict[str, Any] = model_dump(response, exclude_none=True)
    if response.data and isinstance(response.data, InteractionCallbackMessage):
        payload["data"] = model_dump(
            response.data, exclude={"files"}, exclude_none=True
        )
        if response.data.files:
            multipart: dict[str, Any] = {}
            attachments: list[dict] = payload["data"].pop("attachments", [])
            for index, file in enumerate(response.data.files):
                for attachment in attachments:
                    if attachment["filename"] == file.filename:
                        attachment["id"] = index
                        break
                multipart[f"files[{index}]"] = (file.filename, file.content)
            if attachments:
                payload["data"]["attachments"] = attachments
            multipart["payload_json"] = (
                None,
                json.dumps(payload),
                "application/json",
            )
            return {"files": multipart}
    return {"json": payload}
