from typing import TYPE_CHECKING
from typing_extensions import Unpack

from .read import ApplicationEmojis, Emoji
from .write import (
    CreateApplicationEmojiParams,
    CreateGuildEmojiParams,
    ModifyApplicationEmojiParams,
    ModifyGuildEmojiParams,
)
from ...api.validation import validate_outbound_value
from ...protocol import UNSET, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    RestCall,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class EmojiEndpointMixin:
    async def _api_list_guild_emojis(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Emoji]:
        """List guild emojis.

        see https://discord.com/developers/docs/resources/emoji#list-guild-emojis
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/emojis",
            response=JsonResponse(list[Emoji]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> Emoji:
        """Get guild emoji.

        see https://discord.com/developers/docs/resources/emoji#get-guild-emoji
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
            response=JsonResponse(Emoji),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_guild_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[CreateGuildEmojiParams],
    ) -> Emoji:
        """Create guild emoji.

        see https://discord.com/developers/docs/resources/emoji#create-guild-emoji
        """
        fields = validate_outbound_value(CreateGuildEmojiParams, fields)
        name = fields["name"]
        image = fields["image"]
        roles = fields.get("roles")

        if not name:
            msg = "name is required"
            raise ValueError(msg)
        if not image:
            msg = "image is required"
            raise ValueError(msg)
        data = {
            "name": name,
            "image": image,
            "roles": roles,
        }
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/emojis",
            response=JsonResponse(Emoji),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyGuildEmojiParams],
    ) -> Emoji:
        """Modify guild emoji.

        see https://discord.com/developers/docs/resources/emoji#modify-guild-emoji
        """
        fields = validate_outbound_value(ModifyGuildEmojiParams, fields)
        name = fields.get("name", UNSET)
        roles = fields.get("roles", UNSET)

        data = validate_outbound_value(
            ModifyGuildEmojiParams,
            {
                key: value
                for key, value in {"name": name, "roles": roles}.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
            response=JsonResponse(Emoji),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_guild_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        emoji_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete guild emoji.

        see https://discord.com/developers/docs/resources/emoji#delete-guild-emoji
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/emojis/{emoji_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_list_application_emojis(
        self: "AdapterProtocol", bot: "Bot", *, application_id: SnowflakeType
    ) -> ApplicationEmojis:
        """List application emojis.

        see https://discord.com/developers/docs/resources/emoji#list-application-emojis
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"applications/{application_id}/emojis",
            response=JsonResponse(ApplicationEmojis),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_application_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> Emoji:
        """Get application emoji.

        see https://discord.com/developers/docs/resources/emoji#get-application-emoji
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
            response=JsonResponse(Emoji),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_application_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        **fields: Unpack[CreateApplicationEmojiParams],
    ) -> Emoji:
        """Create application emoji.

        see https://discord.com/developers/docs/resources/emoji#create-application-emoji
        """
        fields = validate_outbound_value(CreateApplicationEmojiParams, fields)
        name = fields["name"]
        image = fields["image"]

        if not name:
            msg = "name is required"
            raise ValueError(msg)
        if not image:
            msg = "image is required"
            raise ValueError(msg)
        data = {"name": name, "image": image}
        call = RestCall(
            method="POST",
            url=self.base_url / f"applications/{application_id}/emojis",
            response=JsonResponse(Emoji),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_application_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
        **fields: Unpack[ModifyApplicationEmojiParams],
    ) -> Emoji:
        """Modify application emoji.

        see https://discord.com/developers/docs/resources/emoji#modify-application-emoji
        """
        fields = validate_outbound_value(ModifyApplicationEmojiParams, fields)
        name = fields["name"]

        call = RestCall(
            method="PATCH",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
            response=JsonResponse(Emoji),
            auth=BotAuth(bot.bot_info),
            body=JsonBody({"name": name}),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_application_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        emoji_id: SnowflakeType,
    ) -> None:
        """Delete application emoji.

        see https://discord.com/developers/docs/resources/emoji#delete-application-emoji
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"applications/{application_id}/emojis/{emoji_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)


__all__ = ["EmojiEndpointMixin"]
