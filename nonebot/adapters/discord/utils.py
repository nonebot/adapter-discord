from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeAlias
import zlib

from nonebot.utils import logger_wrapper
from pydantic import BaseModel

from .protocol import UNSET

if TYPE_CHECKING:
    from pydantic.main import IncEx
else:
    IncEx: TypeAlias = (
        set[int]
        | set[str]
        | dict[int, "IncEx | bool"]
        | dict[str, "IncEx | bool"]
        | None
    )

log = logger_wrapper("Discord")


def _stable_sort_key(value: object) -> tuple[str, str, str]:
    value_type = type(value)
    return (value_type.__module__, value_type.__qualname__, repr(value))


def reject_unset_values(value: object, path: str = "$") -> None:  # noqa: C901
    """Reject outbound values that encode wire absence as a value sentinel."""
    if value is UNSET:
        msg = (
            "REST request mappings must omit absent fields instead of using "
            f"UNSET at {path}"
        )
        raise TypeError(msg)
    if isinstance(value, BaseModel):
        field_names = type(value).model_fields
        for field_name in field_names:
            item = getattr(value, field_name)
            if item is not UNSET:
                reject_unset_values(item, f"{path}.{field_name}")
        return
    if isinstance(value, Mapping):
        for key, item in sorted(
            value.items(), key=lambda pair: _stable_sort_key(pair[0])
        ):
            reject_unset_values(key, f"{path}[key={key!r}]")
            item_path = (
                f"{path}.{key}"
                if isinstance(key, str) and key.isidentifier()
                else f"{path}[{key!r}]"
            )
            reject_unset_values(item, item_path)
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            reject_unset_values(item, f"{path}[{index}]")
        return
    if isinstance(value, (set, frozenset)):
        for index, item in enumerate(sorted(value, key=_stable_sort_key)):
            reject_unset_values(item, f"{path}[{index}]")


def omit_unset(data: Any) -> Any:  # noqa: ANN401
    """Recursively omit fields whose value is exactly ``UNSET``."""

    if isinstance(data, dict):
        return data.__class__(
            (k, omit_unset(v)) for k, v in data.items() if v is not UNSET
        )
    if isinstance(data, (list, tuple, set)):
        return data.__class__(omit_unset(i) for i in data if i is not UNSET)
    return data


def model_dump(  # noqa: PLR0913
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
    """Dump a model to Python data; transport JSON encoding lives elsewhere."""

    data = model.model_dump(
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
    )
    if omit_unset_values:
        data = omit_unset(data)
    return data


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unescape(s: str) -> str:
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def decompress_data(data: str | bytes, *, compress: bool) -> str | bytes:
    if not compress:
        return data
    if isinstance(data, str):
        msg = "compressed data must be bytes"
        raise TypeError(msg)
    return zlib.decompress(data)
