from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from http import HTTPStatus
import json
from typing import Any, Generic, NoReturn, Protocol, TypeAlias, TypeVar, cast

from nonebot.compat import type_validate_python
from nonebot.drivers import Request, Response
from nonebot.internal.driver import FileTypes, QueryVariable
from nonebot.utils import escape_tag
from yarl import URL

from .serialization import (
    build_multipart_payload,
    normalize_rest_json,
)
from ..config import BotInfo, Config
from ..domains.models import File
from ..exception import (
    ActionFailed,
    DiscordAdapterException,
    NetworkError,
    RateLimitException,
    UnauthorizedException,
)
from ..utils import decompress_data, log, reject_unset_values

ResponseT = TypeVar("ResponseT")


@dataclass(frozen=True, slots=True)
class BotAuth:
    bot_info: BotInfo


@dataclass(frozen=True, slots=True)
class BearerAuth:
    token: str


@dataclass(frozen=True, slots=True)
class NoAuth:
    pass


RestAuth: TypeAlias = BotAuth | BearerAuth | NoAuth


@dataclass(frozen=True, slots=True)
class JsonBody:
    value: object


@dataclass(frozen=True, slots=True)
class PreparedBody:
    payload: Mapping[str, object]
    files: Sequence[File] | None = None
    attachment_owner_path: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class MultipartBody:
    files: Mapping[str, FileTypes]


RestBody: TypeAlias = JsonBody | PreparedBody | MultipartBody


@dataclass(frozen=True, slots=True)
class JsonResponse(Generic[ResponseT]):
    annotation: Any
    allow_empty: bool = False


@dataclass(frozen=True, slots=True)
class BytesResponse:
    pass


@dataclass(frozen=True, slots=True)
class EmptyResponse:
    parse_nonempty_json: bool = True


ResponseSpec: TypeAlias = JsonResponse[ResponseT] | BytesResponse | EmptyResponse


@dataclass(frozen=True, slots=True)
class RestCall(Generic[ResponseT]):
    method: str
    url: URL
    response: ResponseSpec[ResponseT]
    auth: RestAuth
    query: Mapping[str, QueryVariable | None] = field(default_factory=dict)
    body: RestBody | None = None
    audit_reason: str | None = None
    headers: Mapping[str, str] = field(default_factory=dict)


class RestTransport(Protocol):
    discord_config: Config

    @staticmethod
    def get_authorization(bot_info: BotInfo) -> str: ...

    async def request(self, setup: Request) -> Response: ...


def _bool_query(*, value: bool | None) -> str | None:
    if value is None:
        return None
    return "true" if value else "false"


def _request_headers(
    transport: RestTransport, call: RestCall[ResponseT]
) -> dict[str, str]:
    if any(name.lower() == "authorization" for name in call.headers):
        msg = "Authorization must be provided through RestCall.auth"
        raise ValueError(msg)

    headers = dict(call.headers)
    if isinstance(call.auth, BotAuth):
        headers["Authorization"] = transport.get_authorization(call.auth.bot_info)
    elif isinstance(call.auth, BearerAuth):
        headers["Authorization"] = f"Bearer {call.auth.token}"
    if call.audit_reason is not None:
        headers["X-Audit-Log-Reason"] = call.audit_reason
    return headers


def _encode_body(
    call: RestCall[ResponseT],
) -> tuple[object | None, dict[str, FileTypes] | None]:
    request_json: object | None = None
    request_files: dict[str, FileTypes] | None = None
    if isinstance(call.body, JsonBody):
        if call.body.value is None:
            msg = "JsonBody(None) is ambiguous; use body=None for no body"
            raise TypeError(msg)
        request_json = normalize_rest_json(call.body.value)
    elif isinstance(call.body, PreparedBody):
        normalized = normalize_rest_json(call.body.payload)
        if not isinstance(normalized, dict):
            msg = "PreparedBody payload must normalize to a mapping"
            raise TypeError(msg)
        if call.body.files:
            request_files = build_multipart_payload(
                normalized,
                call.body.files,
                attachment_owner_path=call.body.attachment_owner_path,
            )
        else:
            request_json = normalized
    elif isinstance(call.body, MultipartBody):
        reject_unset_values(call.body.files)
        request_files = dict(call.body.files)
    return request_json, request_files


def _build_request(transport: RestTransport, call: RestCall[ResponseT]) -> Request:
    request_json, request_files = _encode_body(call)
    return Request(
        headers=_request_headers(transport, call),
        method=call.method,
        url=call.url,
        params={key: value for key, value in call.query.items() if value is not None},
        json=None if request_files is not None else request_json,
        files=request_files,
        timeout=transport.discord_config.discord_api_timeout,
        proxy=transport.discord_config.discord_proxy,
    )


def _raise_for_status(data: Response) -> NoReturn:
    if data.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
        raise UnauthorizedException(data)
    if data.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise RateLimitException(data)
    raise ActionFailed(data)


def _parse_response(
    transport: RestTransport,
    response: ResponseSpec[ResponseT],
    data: Response,
) -> object | None:
    if data.status_code not in (200, 201, 204):
        _raise_for_status(data)
    if isinstance(response, BytesResponse):
        return data.content
    if not data.content or (
        isinstance(response, EmptyResponse) and not response.parse_nonempty_json
    ):
        return None
    return json.loads(
        decompress_data(
            data.content,
            compress=transport.discord_config.discord_compress,
        )
    )


class RestExchange:
    async def execute(
        self,
        transport: RestTransport,
        call: RestCall[ResponseT],
    ) -> ResponseT:
        request = _build_request(transport, call)
        try:
            data = await transport.request(request)
            log(
                "TRACE",
                f"API code: {data.status_code} response: {escape_tag(str(data.content))}",
            )
            parsed = _parse_response(transport, call.response, data)
        except DiscordAdapterException:
            raise
        except Exception as e:
            msg = "API request failed"
            raise NetworkError(msg) from e

        if isinstance(call.response, BytesResponse):
            return cast("ResponseT", parsed)
        if isinstance(call.response, EmptyResponse):
            return cast("ResponseT", None)
        if parsed is None and call.response.allow_empty:
            return cast("ResponseT", None)
        return type_validate_python(call.response.annotation, parsed)


REST_EXCHANGE = RestExchange()
