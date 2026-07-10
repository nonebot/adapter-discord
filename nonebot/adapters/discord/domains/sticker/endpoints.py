from typing import TYPE_CHECKING

from nonebot.compat import type_validate_python

from .read import Sticker, StickerPack, StickerPacksResponse
from .write import ModifyGuildStickerParams
from ..message.read import File
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    MultipartBody,
    RestCall,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class StickerEndpointMixin:
    async def _api_get_sticker(
        self: "AdapterProtocol", bot: "Bot", *, sticker_id: SnowflakeType
    ) -> Sticker:
        """Get sticker.

        see https://discord.com/developers/docs/resources/sticker#get-sticker
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"stickers/{sticker_id}",
            response=JsonResponse(Sticker),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_nitro_sticker_packs(
        self: "AdapterProtocol", bot: "Bot"
    ) -> StickerPacksResponse:
        """List sticker packs.

        see https://discord.com/developers/docs/resources/sticker#list-sticker-packs
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "sticker-packs",
            response=JsonResponse(StickerPacksResponse),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_sticker_packs(
        self: "AdapterProtocol", bot: "Bot", *, pack_id: SnowflakeType
    ) -> StickerPack:
        """Get sticker pack.

        see https://discord.com/developers/docs/resources/sticker#get-sticker-pack
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"sticker-packs/{pack_id}",
            response=JsonResponse(StickerPack),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_guild_stickers(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Sticker]:
        """List guild stickers.

        see https://discord.com/developers/docs/resources/sticker#list-guild-stickers
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/stickers",
            response=JsonResponse(list[Sticker]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_sticker(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
    ) -> Sticker:
        """Get guild sticker.

        see https://discord.com/developers/docs/resources/sticker#get-guild-sticker
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
            response=JsonResponse(Sticker),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_guild_sticker(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        description: str,
        tags: str,
        file: File,
        reason: str | None = None,
    ) -> Sticker:
        """Create guild sticker.

        see https://discord.com/developers/docs/resources/sticker#create-guild-sticker
        """

        form = {
            "name": (None, name),
            "description": (None, description),
            "tags": (None, tags),
            "file": (file.filename, file.content),
        }

        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/stickers",
            response=JsonResponse(Sticker),
            auth=BotAuth(bot.bot_info),
            body=MultipartBody(form),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_sticker(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
        name: Missing[str] = UNSET,
        description: MissingOrNullable[str] = UNSET,
        tags: Missing[str] = UNSET,
        reason: str | None = None,
    ) -> Sticker:
        """Modify guild sticker.

        see https://discord.com/developers/docs/resources/sticker#modify-guild-sticker
        """

        data = type_validate_python(
            ModifyGuildStickerParams,
            {"name": name, "description": description, "tags": tags},
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
            response=JsonResponse(Sticker),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_guild_sticker(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sticker_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete guild sticker.

        see https://discord.com/developers/docs/resources/sticker#delete-guild-sticker
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/stickers/{sticker_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)


__all__ = ["StickerEndpointMixin"]
