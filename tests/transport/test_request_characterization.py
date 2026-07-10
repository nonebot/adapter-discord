from typing import Any

from nonebot.adapters.discord.api.model import MessageGet
from nonebot.adapters.discord.exception import (
    ActionFailed,
    NetworkError,
    RateLimitException,
    UnauthorizedException,
)
from nonebot.adapters.discord.transport.exchange import (
    REST_EXCHANGE,
    BytesResponse,
    JsonResponse,
    NoAuth,
    ResponseSpec,
    RestCall,
)
from tests.fake.doubles import DummyAdapter

from nonebot.drivers import Request
from pydantic import ValidationError
import pytest


def _call(response: ResponseSpec[Any] | None = None) -> RestCall[Any]:
    if response is None:
        response = JsonResponse(Any)
    return RestCall(
        method="GET",
        url=DummyAdapter.base_url / "test",
        response=response,
        auth=NoAuth(),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [200, 201])
async def test_request_decodes_success_json(status_code: int) -> None:
    adapter = DummyAdapter(status_code=status_code, content=b'{"ok": true}')

    result = await REST_EXCHANGE.execute(adapter, _call())

    assert result == {"ok": True}
    assert adapter.request_calls == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status_code", "content"),
    [(200, b""), (201, b""), (204, b"")],
)
async def test_request_returns_none_for_empty_or_no_content_response(
    status_code: int, content: bytes
) -> None:
    adapter = DummyAdapter(status_code=status_code, content=content)

    assert await REST_EXCHANGE.execute(adapter, _call()) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [401, 403])
async def test_request_maps_auth_failures_to_unauthorized(status_code: int) -> None:
    adapter = DummyAdapter(status_code=status_code, content=b'{"code": 0}')

    with pytest.raises(UnauthorizedException) as exc_info:
        await REST_EXCHANGE.execute(adapter, _call())

    assert exc_info.value.status_code == status_code


@pytest.mark.asyncio
async def test_request_maps_rate_limit_failure() -> None:
    adapter = DummyAdapter(status_code=429, content=b'{"code": 0}')

    with pytest.raises(RateLimitException) as exc_info:
        await REST_EXCHANGE.execute(adapter, _call())

    assert exc_info.value.status_code == 429


@pytest.mark.asyncio
async def test_request_maps_other_http_failure_to_action_failed() -> None:
    adapter = DummyAdapter(status_code=500, content=b'{"code": 0}')

    with pytest.raises(ActionFailed) as exc_info:
        await REST_EXCHANGE.execute(adapter, _call())

    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_request_wraps_transport_failure_as_network_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = DummyAdapter()

    failure_message = "connection reset"

    async def raise_transport_error(_request: Request) -> object:
        raise OSError(failure_message)

    monkeypatch.setattr(adapter, "request", raise_transport_error)

    with pytest.raises(NetworkError, match="API request failed"):
        await REST_EXCHANGE.execute(adapter, _call())


@pytest.mark.asyncio
async def test_request_wraps_decompression_failure_as_network_error() -> None:
    adapter = DummyAdapter(content=b"not-zlib")
    adapter.discord_config.discord_compress = True

    with pytest.raises(NetworkError, match="API request failed"):
        await REST_EXCHANGE.execute(adapter, _call())


@pytest.mark.asyncio
async def test_request_wraps_success_json_decode_failure_as_network_error() -> None:
    adapter = DummyAdapter(content=b"not-json")

    with pytest.raises(NetworkError, match="API request failed"):
        await REST_EXCHANGE.execute(adapter, _call())


@pytest.mark.asyncio
async def test_response_validation_error_after_request_is_not_network_error() -> None:
    adapter = DummyAdapter(content=b"{}")

    with pytest.raises(ValidationError):
        await REST_EXCHANGE.execute(adapter, _call(JsonResponse(MessageGet)))


@pytest.mark.asyncio
async def test_bytes_response_returns_raw_content() -> None:
    adapter = DummyAdapter(content=b"raw-bytes")

    assert await REST_EXCHANGE.execute(adapter, _call(BytesResponse())) == b"raw-bytes"
