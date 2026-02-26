import base64

import nonebot.adapters.discord.api.handle as handle_module
from tests.fake.doubles import DummyAdapter, DummyBot

from nonebot.drivers import Request
import pytest


@pytest.mark.asyncio
async def test_modify_dm_icon_bytes_are_encoded_to_data_uri(
    dummy_adapter: DummyAdapter,
    dummy_bot: DummyBot,
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

    await dummy_adapter._api_modify_DM(  # noqa: SLF001
        bot=dummy_bot,
        channel_id=1,
        name="group-dm",
        icon=icon,
    )

    payload = captured["json"]
    assert isinstance(payload, dict)
    assert payload["icon"] == expected_icon


@pytest.mark.asyncio
async def test_modify_dm_invalid_icon_bytes_raise_value_error(
    dummy_adapter: DummyAdapter,
    dummy_bot: DummyBot,
) -> None:
    with pytest.raises(ValueError, match="unsupported image format"):
        await dummy_adapter._api_modify_DM(  # noqa: SLF001
            bot=dummy_bot,
            channel_id=1,
            icon=b"not-an-image",
        )
