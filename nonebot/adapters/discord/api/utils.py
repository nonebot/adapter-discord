import json
from typing import Any, Literal

from nonebot.compat import type_validate_python

from .models import (
    ExecuteWebhookParams,
    InteractionCallbackMessage,
    InteractionResponse,
    MessageEditParams,
    MessageSend,
    WebhookMessageEditParams,
)
from .types import UNSET
from ..utils import model_dump


def _build_multipart_payload(
    payload: dict[str, Any],
    files: list[Any],
    *,
    attachment_owner: dict[str, Any] | None = None,
) -> dict[Literal["files", "json"], Any]:
    multipart: dict[str, Any] = {}
    container = payload if attachment_owner is None else attachment_owner
    has_attachments = "attachments" in container
    attachments = container.get("attachments", [])
    if isinstance(attachments, list):
        attachments = container.pop("attachments", [])

    for index, file in enumerate(files):
        if isinstance(attachments, list):
            for attachment in attachments:
                if attachment.get("filename") == file.filename:
                    attachment["id"] = index
                    break
        multipart[f"files[{index}]"] = (file.filename, file.content)

    if isinstance(attachments, list) and has_attachments:
        container["attachments"] = attachments
    multipart["payload_json"] = (None, json.dumps(payload), "application/json")
    result: dict[Literal["files", "json"], Any] = {"files": multipart}
    return result


def parse_data(
    data: dict[str, Any],
    model_class: type[
        ExecuteWebhookParams
        | MessageEditParams
        | MessageSend
        | WebhookMessageEditParams
    ],
) -> dict[Literal["files", "json"], Any]:
    model = type_validate_python(model_class, data)
    payload: dict[str, Any] = model_dump(
        model,
        exclude={"files"},
        omit_unset_values=True,
    )
    files = getattr(model, "files", None)
    if files is not None and files is not UNSET and len(files) > 0:
        return _build_multipart_payload(payload, files)
    return {"json": payload}


def parse_forum_thread_message(
    data: dict[str, Any],
) -> dict[Literal["files", "json"], Any]:
    message_data = {
        key: value
        for key, value in data.items()
        if key
        not in {"name", "auto_archive_duration", "rate_limit_per_user", "applied_tags"}
        and value is not None
    }
    model = type_validate_python(MessageSend, message_data)
    payload: dict[str, Any] = {"name": data["name"]}
    content: dict[str, Any] = model_dump(
        model,
        exclude={"files"},
        exclude_none=True,
        omit_unset_values=True,
    )
    auto_archive_duration = data.get("auto_archive_duration", UNSET)
    if auto_archive_duration is not UNSET and auto_archive_duration is not None:
        payload["auto_archive_duration"] = auto_archive_duration
    rate_limit_per_user = data.get("rate_limit_per_user", UNSET)
    if rate_limit_per_user is not UNSET:
        payload["rate_limit_per_user"] = rate_limit_per_user
    applied_tags = data.get("applied_tags", UNSET)
    if applied_tags is not UNSET and applied_tags is not None:
        payload["applied_tags"] = applied_tags
    payload["message"] = content
    if model.files is not UNSET and model.files:
        return _build_multipart_payload(
            payload,
            model.files,
            attachment_owner=payload["message"],
        )
    return {"json": payload}


def parse_interaction_response(
    response: InteractionResponse,
) -> dict[Literal["files", "json"], Any]:
    payload: dict[str, Any] = model_dump(
        response,
        exclude_none=True,
        omit_unset_values=True,
    )
    if response.data and isinstance(response.data, InteractionCallbackMessage):
        payload["data"] = model_dump(
            response.data,
            exclude={"files"},
            exclude_none=True,
            omit_unset_values=True,
        )
        if response.data.files:
            return _build_multipart_payload(
                payload,
                response.data.files,
                attachment_owner=payload["data"],
            )
    return {"json": payload}
