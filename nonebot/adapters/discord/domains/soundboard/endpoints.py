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
        sound_id = fields["sound_id"]
        source_guild_id = fields.get("source_guild_id", UNSET)

        data = validate_outbound_value(
            SendSoundboardSoundParams,
            {
                key: value
                for key, value in {
                    "sound_id": sound_id,
                    "source_guild_id": source_guild_id,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/send-soundboard-sound",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields["name"]
        sound = fields["sound"]
        volume = fields.get("volume", UNSET)
        emoji_id = fields.get("emoji_id", UNSET)
        emoji_name = fields.get("emoji_name", UNSET)

        data = validate_outbound_value(
            CreateGuildSoundboardSoundParams,
            {
                key: value
                for key, value in {
                    "name": name,
                    "sound": sound,
                    "volume": volume,
                    "emoji_id": emoji_id,
                    "emoji_name": emoji_name,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds",
            response=JsonResponse(SoundboardSound),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
        name = fields.get("name", UNSET)
        volume = fields.get("volume", UNSET)
        emoji_id = fields.get("emoji_id", UNSET)
        emoji_name = fields.get("emoji_name", UNSET)

        data = validate_outbound_value(
            ModifyGuildSoundboardSoundParams,
            {
                key: value
                for key, value in {
                    "name": name,
                    "volume": volume,
                    "emoji_id": emoji_id,
                    "emoji_name": emoji_name,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/soundboard-sounds/{sound_id}",
            response=JsonResponse(SoundboardSound),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
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
