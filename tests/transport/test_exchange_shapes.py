from typing import Any

from nonebot.adapters.discord.config import BotInfo
from nonebot.adapters.discord.exception import NetworkError
from nonebot.adapters.discord.transport.exchange import (
    REST_EXCHANGE,
    BearerAuth,
    BotAuth,
    BytesResponse,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    JsonValueBody,
    MultipartBody,
    NoAuth,
    RestCall,
    _bool_query,
)
from tests.fake.doubles import DummyAdapter

from nonebot.drivers import Request, Response
from pydantic import BaseModel
import pytest
from yarl import URL


class NullableBody(BaseModel):
    value: int | None = None


async def _capture(
    adapter: DummyAdapter,
    call: RestCall[Any],
    *,
    content: bytes = b"{}",
    status_code: int = 200,
) -> Request:
    captured: list[Request] = []

    async def request(setup: Request) -> Response:
        captured.append(setup)
        return Response(status_code, content=content)

    adapter.request = request  # type: ignore[method-assign]
    await REST_EXCHANGE.execute(adapter, call)
    assert len(captured) == 1
    return captured[0]


@pytest.mark.asyncio
async def test_exchange_serializes_explicit_null_filters_query_and_sets_auth() -> None:
    adapter = DummyAdapter()
    request = await _capture(
        adapter,
        RestCall(
            method="PATCH",
            url=adapter.base_url / "test",
            response=JsonResponse(Any),
            auth=BearerAuth("oauth-token"),
            query={"include": None, "verbose": "true"},
            body=JsonBody(NullableBody()),
            audit_reason="reason / unencoded",
        ),
    )

    assert request.headers["Authorization"] == "Bearer oauth-token"
    assert request.headers["X-Audit-Log-Reason"] == "reason / unencoded"
    assert request.url.query_string == "verbose=true"
    assert _bool_query(value=True) == "true"
    assert _bool_query(value=False) == "false"
    assert request.json == {"value": None}
    assert request.files is None


@pytest.mark.asyncio
async def test_exchange_keeps_unset_body_empty_and_rejects_authorization_override() -> (
    None
):
    adapter = DummyAdapter()
    request = await _capture(
        adapter,
        RestCall(
            method="DELETE",
            url=adapter.base_url / "test",
            response=EmptyResponse(),
            auth=NoAuth(),
        ),
        content=b"",
        status_code=204,
    )

    assert request.json is None
    assert request.files is None
    with pytest.raises(ValueError, match="Authorization must be provided"):
        await REST_EXCHANGE.execute(
            adapter,
            RestCall(
                method="GET",
                url=adapter.base_url / "test",
                response=JsonResponse(Any),
                auth=NoAuth(),
                headers={"Authorization": "wrong"},
            ),
        )


@pytest.mark.asyncio
async def test_exchange_serializes_top_level_list_and_custom_multipart() -> None:
    adapter = DummyAdapter()
    list_request = await _capture(
        adapter,
        RestCall(
            method="PUT",
            url=adapter.base_url / "bulk",
            response=JsonResponse(Any),
            auth=NoAuth(),
            body=JsonValueBody([NullableBody(value=1), NullableBody(value=2)]),
        ),
    )
    assert list_request.json == [{"value": 1}, {"value": 2}]
    assert list_request.files is None

    multipart_request = await _capture(
        adapter,
        RestCall(
            method="POST",
            url=adapter.base_url / "upload",
            response=JsonResponse(Any),
            auth=NoAuth(),
            body=MultipartBody(
                {"target_users_file": ("users.txt", b"1\n2")},
            ),
        ),
    )
    assert multipart_request.json is None
    assert multipart_request.files is not None


@pytest.mark.asyncio
async def test_exchange_preserves_encoded_url_and_response_modes() -> None:
    adapter = DummyAdapter()
    encoded = URL(f"{adapter.base_url}/reactions/%F0%9F%98%80%3A1", encoded=True)
    request = await _capture(
        adapter,
        RestCall(
            method="GET",
            url=encoded,
            response=BytesResponse(),
            auth=NoAuth(),
        ),
        content=b"raw",
    )
    assert str(request.url).endswith("%F0%9F%98%80%3A1")

    assert (
        await REST_EXCHANGE.execute(
            adapter,
            RestCall(
                method="DELETE",
                url=adapter.base_url / "empty",
                response=EmptyResponse(parse_nonempty_json=False),
                auth=NoAuth(),
            ),
        )
        is None
    )


@pytest.mark.asyncio
async def test_startup_calls_use_exchange_urls_auth_and_errors() -> None:
    adapter = DummyAdapter()
    token = adapter.__class__.__name__
    bot_info = BotInfo(token=token)
    requests: list[Request] = []
    responses = [
        Response(
            200,
            content=(
                b'{"url":"wss://gateway.discord.gg","shards":1,'
                b'"session_start_limit":{"total":1,"remaining":1,'
                b'"reset_after":1,"max_concurrency":1}}'
            ),
        ),
        Response(
            200,
            content=b'{"id":"1","username":"bot","discriminator":"0","avatar":null}',
        ),
    ]

    async def request(setup: Request) -> Response:
        requests.append(setup)
        return responses.pop(0)

    adapter.request = request  # type: ignore[method-assign]
    assert (await adapter._get_gateway_bot(bot_info)).url == "wss://gateway.discord.gg"  # noqa: SLF001
    assert (await adapter._get_bot_user(bot_info)).username == "bot"  # noqa: SLF001
    assert [str(request.url) for request in requests] == [
        "https://discord.com/api/v10/gateway/bot",
        "https://discord.com/api/v10/users/@me",
    ]
    assert all(
        request.headers["Authorization"] == "Bot test-token" for request in requests
    )

    async def empty_request(setup: Request) -> Response:
        del setup
        return Response(204, content=b"")

    adapter.request = empty_request  # type: ignore[method-assign]
    with pytest.raises(ValueError, match="Failed to get gateway info"):
        await adapter._get_gateway_bot(bot_info)  # noqa: SLF001
    with pytest.raises(ValueError, match="Failed to get bot user info"):
        await adapter._get_bot_user(bot_info)  # noqa: SLF001

    async def blank_gateway_request(setup: Request) -> Response:
        del setup
        return Response(
            200,
            content=(
                b'{"url":"  ","shards":1,"session_start_limit":'
                b'{"total":1,"remaining":1,"reset_after":1,"max_concurrency":1}}'
            ),
        )

    adapter.request = blank_gateway_request  # type: ignore[method-assign]
    with pytest.raises(ValueError, match="Failed to get gateway url"):
        await adapter._get_gateway_bot(bot_info)  # noqa: SLF001


@pytest.mark.asyncio
async def test_empty_response_still_maps_transport_failures() -> None:
    adapter = DummyAdapter()

    failure_message = "offline"

    async def fail_request(setup: Request) -> Response:
        del setup
        raise OSError(failure_message)

    adapter.request = fail_request  # type: ignore[method-assign]
    with pytest.raises(NetworkError, match="API request failed"):
        await REST_EXCHANGE.execute(
            adapter,
            RestCall(
                method="DELETE",
                url=adapter.base_url / "test",
                response=EmptyResponse(),
                auth=BotAuth(BotInfo(token=adapter.__class__.__name__)),
            ),
        )
