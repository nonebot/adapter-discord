from typing_extensions import override

from nonebot.adapters.discord.adapter import Adapter
from nonebot.adapters.discord.api.handle import HandleMixin
from nonebot.adapters.discord.bot import Bot
from nonebot.adapters.discord.config import BotInfo, Config

from nonebot.drivers import Request, Response
from yarl import URL


class DummyAdapter(Adapter, HandleMixin):
    base_url = URL("https://discord.com/api/v10")

    def __init__(self, *, status_code: int = 200, content: bytes = b"{}") -> None:
        self.discord_config = Config()
        self.status_code = status_code
        self.content = content
        self.request_calls = 0

    @override
    @staticmethod
    def get_authorization(bot_info: object) -> str:
        del bot_info
        return "Bot test-token"

    @override
    async def request(self, setup: Request) -> Response:
        del setup
        self.request_calls += 1
        return Response(self.status_code, content=self.content)


class DummyBot(Bot):
    def __init__(
        self,
        adapter: DummyAdapter | None = None,
        *,
        token: str = "x" * 10,
    ) -> None:
        if adapter is not None:
            self.adapter = self._adapter = adapter
        self._bot_info = BotInfo(token=token)
