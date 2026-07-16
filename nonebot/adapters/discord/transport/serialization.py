from collections.abc import Mapping, Sequence, Set as AbstractSet
from datetime import date, datetime
from typing import Any, TypeAlias

from nonebot.internal.driver import FileTypes
from pydantic import BaseModel, TypeAdapter

from ..domains.models import File
from ..utils import IncEx, model_dump, reject_unset_values

_JSON_ADAPTER = TypeAdapter(Any)

MultipartFormData: TypeAlias = dict[str, FileTypes]


def _stable_sort_key(value: object) -> tuple[str, str, str]:
    value_type = type(value)
    return (value_type.__module__, value_type.__qualname__, repr(value))


def encode_json_text(value: object) -> str:
    return _JSON_ADAPTER.dump_json(value).decode()


def encode_model_json_text(  # noqa: PLR0913
    model: BaseModel,
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    *,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    omit_unset_values: bool = False,
) -> str:
    payload = model_dump(
        model,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        omit_unset_values=omit_unset_values,
    )
    return encode_json_text(payload)


def _normalize_tree(value: object) -> object:  # noqa: PLR0911
    if isinstance(value, datetime):
        encoded = value.isoformat()
        return encoded[:-6] + "Z" if encoded.endswith("+00:00") else encoded
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, BaseModel):
        dumped = model_dump(value, omit_unset_values=True)
        reject_unset_values(dumped)
        return _normalize_tree(dumped)
    if isinstance(value, Mapping):
        return {key: _normalize_tree(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalize_tree(item) for item in value]
    if isinstance(value, AbstractSet):
        return [_normalize_tree(item) for item in sorted(value, key=_stable_sort_key)]
    return value


def normalize_rest_json(value: object) -> object:
    """Create a JSON-compatible tree without mutating the caller's value."""
    reject_unset_values(value)
    normalized = _normalize_tree(value)
    reject_unset_values(normalized)
    return _JSON_ADAPTER.dump_python(normalized, mode="json")


def _resolve_attachment_owner(
    payload: dict[str, Any], attachment_owner_path: tuple[str, ...]
) -> dict[str, Any]:
    container = payload
    for key in attachment_owner_path:
        value = container.get(key)
        if not isinstance(value, dict):
            msg = f"attachment owner path {attachment_owner_path!r} is not a mapping"
            raise TypeError(msg)
        container = value
    return container


def build_multipart_payload(
    payload: dict[str, Any],
    files: Sequence[File],
    *,
    attachment_owner_path: tuple[str, ...] = (),
) -> MultipartFormData:
    multipart: MultipartFormData = {}
    container = _resolve_attachment_owner(payload, attachment_owner_path)
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
    multipart["payload_json"] = (
        None,
        encode_json_text(payload).encode(),
        "application/json",
    )
    return multipart


__all__ = [
    "MultipartFormData",
    "build_multipart_payload",
    "encode_json_text",
    "encode_model_json_text",
    "normalize_rest_json",
]
