from typing import TYPE_CHECKING

from nonebot.compat import type_validate_python

from .read import (
    ListDefaultSoundboardSoundsResponse,
    ListGuildSoundboardSoundsResponse,
    SoundboardSound,
)
from .write import (
    CreateGuildSoundboardSoundParams,
    ModifyGuildSoundboardSoundParams,
    SendSoundboardSoundParams,
)
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
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


class SoundboardEndpointMixin:
    async def _api_send_soundboard_sound(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        sound_id: SnowflakeType,
        source_guild_id: Missing[SnowflakeType] = UNSET,
    ) -> None:
        """Send soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#send-soundboard-sound
        """

        data = type_validate_python(
            SendSoundboardSoundParams,
            {"sound_id": sound_id, "source_guild_id": source_guild_id},
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/send-soundboard-sound",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_list_default_soundboard_sounds(
        self: "AdapterProtocol", bot: "Bot"
    ) -> ListDefaultSoundboardSoundsResponse:
        """List default soundboard sounds.

        see https://discord.com/developers/docs/resources/soundboard#list-default-soundboard-sounds
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "soundboard-default-sounds",
            response=JsonResponse(ListDefaultSoundboardSoundsResponse),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_guild_soundboard_sounds(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
    ) -> ListGuildSoundboardSoundsResponse:
        """List guild soundboard sounds.

        see https://discord.com/developers/docs/resources/soundboard#list-guild-soundboard-sounds
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds",
            response=JsonResponse(ListGuildSoundboardSoundsResponse),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_soundboard_sound(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sound_id: SnowflakeType,
    ) -> SoundboardSound:
        """Get guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#get-guild-soundboard-sound
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds/{sound_id}",
            response=JsonResponse(SoundboardSound),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_guild_soundboard_sound(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        sound: str,
        volume: Missing[float] = UNSET,
        emoji_id: Missing[SnowflakeType] = UNSET,
        emoji_name: Missing[str] = UNSET,
    ) -> SoundboardSound:
        """Create guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#create-guild-soundboard-sound
        """

        data = type_validate_python(
            CreateGuildSoundboardSoundParams,
            {
                "name": name,
                "sound": sound,
                "volume": volume,
                "emoji_id": emoji_id,
                "emoji_name": emoji_name,
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds",
            response=JsonResponse(SoundboardSound),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_soundboard_sound(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sound_id: SnowflakeType,
        name: Missing[str] = UNSET,
        volume: Missing[float] = UNSET,
        emoji_id: MissingOrNullable[SnowflakeType] = UNSET,
        emoji_name: MissingOrNullable[str] = UNSET,
    ) -> SoundboardSound:
        """Modify guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#modify-guild-soundboard-sound
        """

        data = type_validate_python(
            ModifyGuildSoundboardSoundParams,
            {
                "name": name,
                "volume": volume,
                "emoji_id": emoji_id,
                "emoji_name": emoji_name,
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds/{sound_id}",
            response=JsonResponse(SoundboardSound),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_guild_soundboard_sound(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sound_id: SnowflakeType,
    ) -> None:
        """Delete guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#delete-guild-soundboard-sound
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds/{sound_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)


__all__ = ["SoundboardEndpointMixin"]
