from http import HTTPStatus
import json
from typing import TYPE_CHECKING, Any

from nonebot.drivers import Request
from nonebot.utils import escape_tag

from ..exception import (
    ActionFailed,
    DiscordAdapterException,
    NetworkError,
    RateLimitException,
    UnauthorizedException,
)
from ..utils import decompress_data, log

if TYPE_CHECKING:
    from ..adapter import Adapter
    from ..bot import Bot


async def _request(adapter: "Adapter", bot: "Bot", request: Request) -> Any:  # noqa: ANN401, ARG001 # TODO)): 验证bot参数是否需要, 重构为泛型函数, 接管type_validate部分
    try:
        request.timeout = adapter.discord_config.discord_api_timeout
        request.proxy = adapter.discord_config.discord_proxy
        data = await adapter.request(request)
        log(
            "TRACE",
            f"API code: {data.status_code} response: {escape_tag(str(data.content))}",
        )
        if data.status_code in (200, 201, 204):
            return data.content and json.loads(
                decompress_data(
                    data.content, compress=adapter.discord_config.discord_compress
                )
            )
        if data.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
            raise UnauthorizedException(data)  # noqa: TRY301
        if data.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitException(data)  # noqa: TRY301
        raise ActionFailed(data)  # noqa: TRY301
    except DiscordAdapterException:
        raise
    except Exception as e:
        msg = "API request failed"
        raise NetworkError(msg) from e
