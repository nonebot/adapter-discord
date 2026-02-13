from collections.abc import Awaitable, Callable
from types import SimpleNamespace
from typing import Any, Optional

import nonebot.adapters.discord.api.handle as handle_module

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


MethodCaller = Callable[
    [DummyAdapter, SimpleNamespace, str, Optional[int]], Awaitable[None]
]


async def _call_create_reaction(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
    emoji: str,
    emoji_id: Optional[int],
) -> None:
    await adapter._api_create_reaction(  # noqa: SLF001
        bot=bot,
        channel_id=1,
        message_id=2,
        emoji=emoji,
        emoji_id=emoji_id,
    )


async def _call_delete_own_reaction(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
    emoji: str,
    emoji_id: Optional[int],
) -> None:
    await adapter._api_delete_own_reaction(  # noqa: SLF001
        bot=bot,
        channel_id=1,
        message_id=2,
        emoji=emoji,
        emoji_id=emoji_id,
    )


async def _call_delete_user_reaction(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
    emoji: str,
    emoji_id: Optional[int],
) -> None:
    await adapter._api_delete_user_reaction(  # noqa: SLF001
        bot=bot,
        channel_id=1,
        message_id=2,
        user_id=3,
        emoji=emoji,
        emoji_id=emoji_id,
    )


async def _call_get_reactions(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
    emoji: str,
    emoji_id: Optional[int],
) -> None:
    await adapter._api_get_reactions(  # noqa: SLF001
        bot=bot,
        channel_id=1,
        message_id=2,
        emoji=emoji,
        emoji_id=emoji_id,
    )


async def _call_delete_all_reactions_for_emoji(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
    emoji: str,
    emoji_id: Optional[int],
) -> None:
    await adapter._api_delete_all_reactions_for_emoji(  # noqa: SLF001
        bot=bot,
        channel_id=1,
        message_id=2,
        emoji=emoji,
        emoji_id=emoji_id,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case",
    [
        (_call_create_reaction, "/@me", "😀", None, "%F0%9F%98%80"),
        (_call_delete_own_reaction, "/@me", "😀", None, "%F0%9F%98%80"),
        (_call_delete_user_reaction, "/3", "😀", None, "%F0%9F%98%80"),
        (_call_get_reactions, "", "😀", None, "%F0%9F%98%80"),
        (_call_delete_all_reactions_for_emoji, "", "😀", None, "%F0%9F%98%80"),
        (_call_create_reaction, "/@me", "name", 123, "name%3A123"),
        (_call_delete_own_reaction, "/@me", "name", 123, "name%3A123"),
        (_call_delete_user_reaction, "/3", "name", 123, "name%3A123"),
        (_call_get_reactions, "", "name", 123, "name%3A123"),
        (_call_delete_all_reactions_for_emoji, "", "name", 123, "name%3A123"),
    ],
)
async def test_reaction_endpoints_encode_emoji_once(
    adapter: DummyAdapter,
    bot: SimpleNamespace,
    monkeypatch: pytest.MonkeyPatch,
    case: tuple[MethodCaller, str, str, Optional[int], str],
) -> None:
    caller, suffix, emoji, emoji_id, encoded_emoji = case
    captured: list[str] = []

    async def fake_request(
        _adapter: object,
        request_obj: Request,
        *,
        parse_json: bool = True,
    ) -> list[Any]:
        del _adapter, parse_json
        captured.append(str(request_obj.url))
        return []

    monkeypatch.setattr(handle_module, "_request", fake_request)

    await caller(adapter, bot, emoji, emoji_id)

    assert captured
    assert captured[-1].endswith(
        f"/channels/1/messages/2/reactions/{encoded_emoji}{suffix}"
    )
    assert "%25" not in captured[-1]
