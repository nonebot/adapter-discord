from typing import TYPE_CHECKING
from typing_extensions import Unpack

from .read import StageInstance, VoiceRegion, VoiceState
from .write import (
    CreateStageInstanceParams,
    ModifyCurrentUserVoiceStateParams,
    ModifyStageInstanceParams,
    ModifyUserVoiceStateParams,
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


class VoiceEndpointMixin:
    async def _api_list_voice_regions(
        self: "AdapterProtocol", bot: "Bot"
    ) -> list[VoiceRegion]:
        """List voice regions.

        see https://discord.com/developers/docs/resources/voice#list-voice-regions
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "voice/regions",
            response=JsonResponse(list[VoiceRegion]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_current_user_voice_state(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> VoiceState:
        """Get current user voice state.

        see https://discord.com/developers/docs/resources/voice#get-current-user-voice-state
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/voice-states/@me",
            response=JsonResponse(VoiceState),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_user_voice_state(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
    ) -> VoiceState:
        """Get user voice state.

        see https://discord.com/developers/docs/resources/voice#get-user-voice-state
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
            response=JsonResponse(VoiceState),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_current_user_voice_state(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        **fields: Unpack[ModifyCurrentUserVoiceStateParams],
    ) -> None:
        """Modify current user voice state.

        see https://discord.com/developers/docs/resources/voice#modify-current-user-voice-state
        """
        fields = validate_outbound_value(ModifyCurrentUserVoiceStateParams, fields)
        channel_id = fields.get("channel_id", UNSET)
        suppress = fields.get("suppress", UNSET)
        request_to_speak_timestamp = fields.get("request_to_speak_timestamp", UNSET)

        data = validate_outbound_value(
            ModifyCurrentUserVoiceStateParams,
            {
                key: value
                for key, value in {
                    "channel_id": channel_id,
                    "suppress": suppress,
                    "request_to_speak_timestamp": request_to_speak_timestamp,
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/voice-states/@me",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_modify_user_voice_state(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        **fields: Unpack[ModifyUserVoiceStateParams],
    ) -> None:
        """Modify user voice state.

        see https://discord.com/developers/docs/resources/voice#modify-user-voice-state
        """
        fields = validate_outbound_value(ModifyUserVoiceStateParams, fields)
        channel_id = fields.get("channel_id")
        suppress = fields.get("suppress")

        data = {"channel_id": channel_id, "suppress": suppress}
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_create_stage_instance(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        reason: str | None = None,
        **fields: Unpack[CreateStageInstanceParams],
    ) -> StageInstance:
        """Create stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#create-stage-instance
        """
        fields = validate_outbound_value(CreateStageInstanceParams, fields)
        channel_id = fields["channel_id"]
        topic = fields["topic"]
        privacy_level = fields.get("privacy_level")
        send_start_notification = fields.get("send_start_notification")
        guild_scheduled_event_id = fields.get("guild_scheduled_event_id")

        data = {
            "channel_id": channel_id,
            "topic": topic,
            "privacy_level": privacy_level,
            "send_start_notification": send_start_notification,
            "guild_scheduled_event_id": guild_scheduled_event_id,
        }
        call = RestCall(
            method="POST",
            url=self.base_url / "stage-instances",
            response=JsonResponse(StageInstance),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_stage_instance(
        self: "AdapterProtocol", bot: "Bot", *, channel_id: SnowflakeType
    ) -> StageInstance:
        """Get stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#get-stage-instance
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"stage-instances/{channel_id}",
            response=JsonResponse(StageInstance),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_stage_instance(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyStageInstanceParams],
    ) -> StageInstance:
        """Modify stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#modify-stage-instance
        """
        fields = validate_outbound_value(ModifyStageInstanceParams, fields)
        topic = fields.get("topic")
        privacy_level = fields.get("privacy_level")

        data = {"topic": topic, "privacy_level": privacy_level}
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"stage-instances/{channel_id}",
            response=JsonResponse(StageInstance),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_stage_instance(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#delete-stage-instance
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"stage-instances/{channel_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)


__all__ = ["VoiceEndpointMixin"]
