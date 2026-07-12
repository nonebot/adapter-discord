from typing import TYPE_CHECKING
from typing_extensions import Unpack

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
from ...api.validation import validate_outbound_value
from ...protocol import SnowflakeType
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
        **fields: Unpack[SendSoundboardSoundParams],
    ) -> None:
        """Send soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#send-soundboard-sound
        """
        fields = validate_outbound_value(SendSoundboardSoundParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/send-soundboard-sound",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
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

    async def _api_create_guild_soundboard_sound(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        **fields: Unpack[CreateGuildSoundboardSoundParams],
    ) -> SoundboardSound:
        """Create guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#create-guild-soundboard-sound
        """
        fields = validate_outbound_value(CreateGuildSoundboardSoundParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds",
            response=JsonResponse(SoundboardSound),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_guild_soundboard_sound(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        sound_id: SnowflakeType,
        **fields: Unpack[ModifyGuildSoundboardSoundParams],
    ) -> SoundboardSound:
        """Modify guild soundboard sound.

        see https://discord.com/developers/docs/resources/soundboard#modify-guild-soundboard-sound
        """
        fields = validate_outbound_value(ModifyGuildSoundboardSoundParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds/{sound_id}",
            response=JsonResponse(SoundboardSound),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
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
