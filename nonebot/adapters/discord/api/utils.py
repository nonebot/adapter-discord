from typing import Any

from nonebot.compat import type_validate_python
from pydantic import BaseModel

from .model import (
    ExecuteWebhookParams,
    File,
    InteractionCallbackMessage,
    InteractionResponse,
    MessageEditParams,
    MessageSend,
    Snowflake,
    WebhookMessageEditParams,
)
from .types import UNSET, Missing, MissingOrNullable
from ..serialization import PreparedRequest, prepare_request


class ForumThreadMessageRequest(BaseModel):
    name: str
    auto_archive_duration: Missing[int] = UNSET
    rate_limit_per_user: MissingOrNullable[int] = UNSET
    applied_tags: Missing[list[Snowflake]] = UNSET
    message: MessageSend


def _extract_files(model: BaseModel) -> list[File] | None:
    files = getattr(model, "files", None)
    if files is None or files is UNSET or len(files) == 0:
        return None
    return files


def parse_data(
    data: dict[str, Any],
    model_class: type[
        ExecuteWebhookParams
        | MessageEditParams
        | MessageSend
        | WebhookMessageEditParams
    ],
) -> PreparedRequest:
    model = type_validate_python(model_class, data)
    return prepare_request(
        model,
        files=_extract_files(model),
        exclude={"files"},
        omit_unset_values=True,
    )


def parse_forum_thread_message(data: dict[str, Any]) -> PreparedRequest:
    message_data = {
        key: value
        for key, value in data.items()
        if key
        not in {"name", "auto_archive_duration", "rate_limit_per_user", "applied_tags"}
        and value is not None
    }
    payload: dict[str, Any] = {
        "name": data["name"],
        "message": message_data,
    }
    auto_archive_duration = data.get("auto_archive_duration", UNSET)
    if auto_archive_duration is not UNSET and auto_archive_duration is not None:
        payload["auto_archive_duration"] = auto_archive_duration
    rate_limit_per_user = data.get("rate_limit_per_user", UNSET)
    if rate_limit_per_user is not UNSET:
        payload["rate_limit_per_user"] = rate_limit_per_user
    applied_tags = data.get("applied_tags", UNSET)
    if applied_tags is not UNSET and applied_tags is not None:
        payload["applied_tags"] = applied_tags

    model = type_validate_python(ForumThreadMessageRequest, payload)
    return prepare_request(
        model,
        files=_extract_files(model.message),
        attachment_owner_path=("message",),
        exclude={"message": {"files"}},
        exclude_none=True,
        omit_unset_values=True,
    )


def parse_interaction_response(response: InteractionResponse) -> PreparedRequest:
    exclude = None
    files = None
    if response.data and isinstance(response.data, InteractionCallbackMessage):
        exclude = {"data": {"files"}}
        files = _extract_files(response.data)
    return prepare_request(
        response,
        files=files,
        attachment_owner_path=("data",),
        exclude=exclude,
        exclude_none=True,
        omit_unset_values=True,
    )
