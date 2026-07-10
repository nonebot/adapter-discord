from typing import Any

from nonebot.adapters.discord.api.model import File
from tests.fake.doubles import DummyAdapter, DummyBot

from nonebot.drivers import Request, Response
import pytest


@pytest.mark.asyncio
async def test_update_invite_target_users_uses_expected_multipart_field(
    dummy_adapter: DummyAdapter,
    dummy_bot: DummyBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    async def fake_request(request_obj: Request) -> Response:
        captured["request"] = request_obj
        return Response(200, content=b"uploaded")

    monkeypatch.setattr(dummy_adapter, "request", fake_request)

    target_users_file = File(content=b"123\n456\n", filename="users.csv")
    await dummy_adapter._api_update_invite_target_users(  # noqa: SLF001
        bot=dummy_bot,
        invite_code="abc123",
        target_users_file=target_users_file,
    )

    request_obj = captured["request"]
    assert isinstance(request_obj, Request)
    assert request_obj.method == "PUT"
    assert str(request_obj.url).endswith("/invites/abc123/target-users")

    files = request_obj.files
    assert isinstance(files, list)
    assert files == [("target_users_file", ("users.csv", b"123\n456\n", None))]
    assert request_obj.json is None
