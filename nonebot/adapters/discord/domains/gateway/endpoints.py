from typing import TYPE_CHECKING

from .read import Gateway, GatewayBot
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    JsonResponse,
    NoAuth,
    RestCall,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class GatewayEndpointMixin:
    async def _api_get_gateway(self: "AdapterProtocol") -> Gateway:
        """Get gateway.

        see https://discord.com/developers/docs/events/gateway#get-gateway
        """
        call = RestCall(
            method="GET",
            url=self.base_url / "gateway",
            response=JsonResponse(Gateway),
            auth=NoAuth(),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_gateway_bot(self: "AdapterProtocol", bot: "Bot") -> GatewayBot:
        """Get gateway bot.

        see https://discord.com/developers/docs/events/gateway#get-gateway-bot
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "gateway/bot",
            response=JsonResponse(GatewayBot),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["GatewayEndpointMixin"]
