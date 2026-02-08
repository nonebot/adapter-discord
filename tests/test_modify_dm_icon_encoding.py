import base64
import importlib
from types import SimpleNamespace
from typing import Any, cast

from nonebot.drivers import Request
import pytest
from yarl import URL

handle_module = cast(
    "Any", importlib.import_module("nonebot.adapters.discord.api.handle")
)


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
async def test_modify_dm_icon_bytes_are_encoded_to_data_uri(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    async def fake_request(
        _adapter: object,
        request_obj: Request,
        *,
        parse_json: bool = True,
    ) -> dict[str, object]:
        del _adapter, parse_json
        captured["json"] = request_obj.json
        return {}

    def fake_type_validate_python(_type: object, value: object) -> object:
        return value

    monkeypatch.setattr(handle_module, "_request", fake_request)
    monkeypatch.setattr(
        handle_module, "type_validate_python", fake_type_validate_python
    )

    icon = b"\x89PNG\r\n\x1a\n\x00test"
    expected_icon = f"data:image/png;base64,{base64.b64encode(icon).decode('ascii')}"

    await adapter._api_modify_DM(  # noqa: SLF001
        bot=bot,
        channel_id=1,
        name="group-dm",
        icon=icon,
    )

    payload = captured["json"]
    assert isinstance(payload, dict)
    assert payload["icon"] == expected_icon


@pytest.mark.asyncio
async def test_modify_dm_invalid_icon_bytes_raise_value_error(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
) -> None:
    with pytest.raises(ValueError, match="unsupported image format"):
        await adapter._api_modify_DM(  # noqa: SLF001
            bot=bot,
            channel_id=1,
            icon=b"not-an-image",
        )
