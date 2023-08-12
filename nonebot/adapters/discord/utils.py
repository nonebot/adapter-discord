from typing import Union
import zlib

from nonebot.utils import logger_wrapper

log = logger_wrapper("Discord")


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unescape(s: str) -> str:
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def decompress_data(data: Union[str, bytes], compress: bool) -> Union[str, bytes]:
    return zlib.decompress(data) if compress else data  # type: ignore
