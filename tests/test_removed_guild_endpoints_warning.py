from collections.abc import Awaitable, Callable

import nonebot.adapters.discord.transport.exchange as exchange_module
from tests.fake.doubles import DummyAdapter, DummyBot

from nonebot.drivers import Request, Response
import pytest


@pytest.fixture
def patch_api_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_request(_adapter: object, _request: Request) -> Response:
        return Response(200, content=b"{}")

    def fake_type_validate_python(_type: object, value: object) -> object:
        return value

    monkeypatch.setattr(DummyAdapter, "request", fake_request)
    monkeypatch.setattr(
        exchange_module, "type_validate_python", fake_type_validate_python
    )


async def _call_create_guild(adapter: DummyAdapter, bot: DummyBot) -> None:
    await adapter._api_create_guild(bot=bot, name="test-guild")  # noqa: SLF001


async def _call_delete_guild(adapter: DummyAdapter, bot: DummyBot) -> None:
    await adapter._api_delete_guild(bot=bot, guild_id=1)  # noqa: SLF001


async def _call_modify_guild_mfa(adapter: DummyAdapter, bot: DummyBot) -> None:
    await adapter._api_modify_guild_MFA_level(  # noqa: SLF001
        bot=bot,
        guild_id=1,
        level=1,
    )


async def _call_create_guild_from_template(
    adapter: DummyAdapter, bot: DummyBot
) -> None:
    await adapter._api_create_guild_from_guild_template(  # noqa: SLF001
        bot=bot,
        template_code="template-code",
        name="template-guild",
    )


EndpointCall = Callable[[DummyAdapter, DummyBot], Awaitable[None]]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("caller", "match_text"),
    [
        (_call_create_guild, "_api_create_guild"),
        (_call_delete_guild, "_api_delete_guild"),
        (_call_modify_guild_mfa, "_api_modify_guild_MFA_level"),
        (
            _call_create_guild_from_template,
            "_api_create_guild_from_guild_template",
        ),
    ],
)
async def test_removed_guild_endpoints_emit_deprecation_warning(
    dummy_adapter: DummyAdapter,
    dummy_bot: DummyBot,
    patch_api_runtime: None,
    caller: EndpointCall,
    match_text: str,
) -> None:
    del patch_api_runtime
    with pytest.warns(DeprecationWarning, match=match_text):
        await caller(dummy_adapter, dummy_bot)
