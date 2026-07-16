from datetime import datetime
from typing import TYPE_CHECKING

from nonebot.compat import type_validate_python

from .read import StageInstance, VoiceRegion, VoiceState
from .types import StagePrivacyLevel
from .write import ModifyCurrentUserVoiceStateParams
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    JsonValueBody,
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
        channel_id: Missing[SnowflakeType] = UNSET,
        suppress: Missing[bool] = UNSET,
        request_to_speak_timestamp: MissingOrNullable[datetime] = UNSET,
    ) -> None:
        """Modify current user voice state.

        see https://discord.com/developers/docs/resources/voice#modify-current-user-voice-state
        """

        data = type_validate_python(
            ModifyCurrentUserVoiceStateParams,
            {
                "channel_id": channel_id,
                "suppress": suppress,
                "request_to_speak_timestamp": request_to_speak_timestamp,
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/voice-states/@me",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_modify_user_voice_state(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType,
        channel_id: SnowflakeType | None = None,
        suppress: bool | None = None,
    ) -> None:
        """Modify user voice state.

        see https://discord.com/developers/docs/resources/voice#modify-user-voice-state
        """

        data = {"channel_id": channel_id, "suppress": suppress}
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/voice-states/{user_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(
                {key: value for (key, value) in data.items() if value is not None}
            ),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_create_stage_instance(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        topic: str,
        privacy_level: StagePrivacyLevel | None = None,
        send_start_notification: bool | None = None,
        guild_scheduled_event_id: SnowflakeType | None = None,
        reason: str | None = None,
    ) -> StageInstance:
        """Create stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#create-stage-instance
        """

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
            body=JsonValueBody(
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
        topic: str | None = None,
        privacy_level: StagePrivacyLevel | None = None,
        reason: str | None = None,
    ) -> StageInstance:
        """Modify stage instance.

        see https://discord.com/developers/docs/resources/stage-instance#modify-stage-instance
        """

        data = {"topic": topic, "privacy_level": privacy_level}
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"stage-instances/{channel_id}",
            response=JsonResponse(StageInstance),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(
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
