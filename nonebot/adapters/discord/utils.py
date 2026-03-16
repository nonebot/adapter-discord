from typing import Any, TypeAlias
import zlib

from nonebot.compat import PYDANTIC_V2
from nonebot.utils import logger_wrapper
from pydantic import BaseModel

from .api.types import UNSET

if PYDANTIC_V2:
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


def omit_unset(data: Any) -> Any:  # noqa: ANN401
    """Recursively omit fields whose value is exactly ``UNSET``."""

    if isinstance(data, dict):
        return data.__class__(
            (k, omit_unset(v)) for k, v in data.items() if v is not UNSET
        )
    if isinstance(data, (list, tuple, set)):
        return data.__class__(omit_unset(i) for i in data if i is not UNSET)
    return data


# TODO)): Switch back to nonebot.compat.model_dump. Wait for the next release.
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

    if PYDANTIC_V2:
        data = model.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
    else:
        data = model.dict(
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
