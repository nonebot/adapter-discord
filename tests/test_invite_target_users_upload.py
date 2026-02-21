from types import SimpleNamespace
from typing import Any

import nonebot.adapters.discord.api.handle as handle_module
from nonebot.adapters.discord.api.model import File

from nonebot.drivers import Request
import pytest
from yarl import URL


class DummyAdapter(handle_module.HandleMixin):
    base_url = URL("https://discord.com/api/v10")
    discord_config = SimpleNamespace(discord_api_timeout=10.0, discord_proxy=None)

    @staticmethod
    def get_authorization(bot_info: object) -> str:
        del bot_info
        return "Bot test-token"


@pytest.fixture
def adapter() -> DummyAdapter:
    return DummyAdapter()


@pytest.fixture
def bot() -> SimpleNamespace:
    return SimpleNamespace(bot_info=SimpleNamespace())


@pytest.mark.asyncio
async def test_update_invite_target_users_uses_expected_multipart_field(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    async def fake_request(
        _adapter: object,
        request_obj: Request,
        *,
        parse_json: bool = True,
    ) -> None:
        del _adapter
        captured["request"] = request_obj
        captured["parse_json"] = parse_json

    monkeypatch.setattr(handle_module, "_request", fake_request)

    target_users_file = File(content=b"123\n456\n", filename="users.csv")
    await adapter._api_update_invite_target_users(  # noqa: SLF001
        bot=bot,
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
    assert captured["parse_json"] is False
