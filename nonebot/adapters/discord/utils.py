from typing import Any, Optional, Union
import zlib

from nonebot.compat import model_dump as model_dump_
from nonebot.utils import logger_wrapper

from pydantic import BaseModel

from .api.types import UNSET

log = logger_wrapper("Discord")


def exclude_unset_data(data: Any) -> Any:
    if isinstance(data, dict):
        return data.__class__(
            (k, exclude_unset_data(v)) for k, v in data.items() if v is not UNSET
        )
    elif isinstance(data, list):
        return data.__class__(exclude_unset_data(i) for i in data)
    elif data is UNSET:
        return None
    return data


def model_dump(
    model: BaseModel,
    include: Optional[set[str]] = None,
    exclude: Optional[set[str]] = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
) -> dict[str, Any]:
    data = model_dump_(
        model,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
    )
    if exclude_none or exclude_unset:
        return exclude_unset_data(data)
    else:
        return data


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unescape(s: str) -> str:
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def decompress_data(data: Union[str, bytes], compress: bool) -> Union[str, bytes]:
    return zlib.decompress(data) if compress else data  # type: ignore
