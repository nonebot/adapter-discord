import zlib
from typing import AnyStr

try:
    import ujson as json
except ImportError:
    import json

from nonebot.utils import logger_wrapper

log = logger_wrapper("Discord")


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unescape(s: str) -> str:
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


json_loads = json.loads
json_dumps = json.dumps


def decompress_data(data: AnyStr, compress: bool) -> AnyStr:
    return zlib.decompress(data) if compress else data
