from dataclasses import dataclass
import json
from typing import Any, Literal

from nonebot.compat import PYDANTIC_V2
from pydantic import BaseModel

if PYDANTIC_V2:
    from pydantic import TypeAdapter
else:
    from pydantic.json import pydantic_encoder

from .api.model import File
from .utils import IncEx, model_dump

if PYDANTIC_V2:
    _JSON_ADAPTER = TypeAdapter(Any)


@dataclass(frozen=True, slots=True)
class PreparedRequest:
    body: BaseModel
    files: list[File] | None = None
    attachment_owner_path: tuple[str, ...] = ()
    include: IncEx | None = None
    exclude: IncEx | None = None
    by_alias: bool = False
    exclude_unset: bool = False
    exclude_defaults: bool = False
    exclude_none: bool = False
    omit_unset_values: bool = False


def prepare_request(  # noqa: PLR0913
    body: BaseModel,
    *,
    files: list[File] | None = None,
    attachment_owner_path: tuple[str, ...] = (),
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    omit_unset_values: bool = False,
) -> PreparedRequest:
    return PreparedRequest(
        body=body,
        files=files,
        attachment_owner_path=attachment_owner_path,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        omit_unset_values=omit_unset_values,
    )


def encode_json_text(value: object) -> str:
    if PYDANTIC_V2:
        return _JSON_ADAPTER.dump_json(value).decode()
    return json.dumps(value, default=pydantic_encoder)


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


def encode_model_json_data(  # noqa: PLR0913
    model: BaseModel,
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    *,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    omit_unset_values: bool = False,
) -> dict[str, Any]:
    # Keep JSON-data and JSON-text transport encoding on one path so HTTP bodies,
    # multipart payload_json, and gateway frames cannot drift apart.
    return json.loads(
        encode_model_json_text(
            model,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            omit_unset_values=omit_unset_values,
        )
    )


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


def _build_multipart_payload(
    payload: dict[str, Any],
    files: list[File],
    *,
    attachment_owner_path: tuple[str, ...] = (),
) -> dict[str, Any]:
    multipart: dict[str, Any] = {}
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
    multipart["payload_json"] = (None, encode_json_text(payload), "application/json")
    return multipart


def encode_prepared_request(
    prepared: PreparedRequest,
) -> dict[Literal["files", "json"], Any]:
    payload = encode_model_json_data(
        prepared.body,
        include=prepared.include,
        exclude=prepared.exclude,
        by_alias=prepared.by_alias,
        exclude_unset=prepared.exclude_unset,
        exclude_defaults=prepared.exclude_defaults,
        exclude_none=prepared.exclude_none,
        omit_unset_values=prepared.omit_unset_values,
    )
    if prepared.files:
        return {
            "files": _build_multipart_payload(
                payload,
                prepared.files,
                attachment_owner_path=prepared.attachment_owner_path,
            )
        }
    return {"json": payload}
