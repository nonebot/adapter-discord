from typing import TYPE_CHECKING

from .read import Invite, InviteTargetUsersJobStatus
from ..message.read import File
from ...protocol import SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    BytesResponse,
    JsonResponse,
    MultipartBody,
    RestCall,
    _bool_query,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class InviteEndpointMixin:
    async def _api_get_invite(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        invite_code: str,
        with_counts: bool | None = None,
        with_expiration: bool | None = None,
        guild_scheduled_event_id: SnowflakeType | None = None,
    ) -> Invite:
        """Get invite.

        see https://discord.com/developers/docs/resources/invite#get-invite
        """

        params = {
            "with_counts": _bool_query(value=with_counts),
            "with_expiration": _bool_query(value=with_expiration),
            "guild_scheduled_event_id": guild_scheduled_event_id,
        }
        call = RestCall(
            method="GET",
            url=self.base_url / f"invites/{invite_code}",
            response=JsonResponse(Invite),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_invite(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        invite_code: str,
        reason: str | None = None,
    ) -> Invite:
        """Delete invite.

        see https://discord.com/developers/docs/resources/invite#delete-invite
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"invites/{invite_code}",
            response=JsonResponse(Invite),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_invite_target_users(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        invite_code: str,
    ) -> bytes:
        """Get invite target users.

        see https://discord.com/developers/docs/resources/invite#get-target-users
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"invites/{invite_code}/target-users",
            response=BytesResponse(),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_update_invite_target_users(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        invite_code: str,
        target_users_file: File,
    ) -> None:
        """Update invite target users.

        see https://discord.com/developers/docs/resources/invite#update-target-users
        """

        call = RestCall(
            method="PUT",
            url=self.base_url / f"invites/{invite_code}/target-users",
            response=BytesResponse(),
            auth=BotAuth(bot.bot_info),
            body=MultipartBody(
                {
                    "target_users_file": (
                        target_users_file.filename,
                        target_users_file.content,
                    )
                }
            ),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_get_invite_target_users_job_status(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        invite_code: str,
    ) -> InviteTargetUsersJobStatus:
        """Get invite target users job status.

        see https://discord.com/developers/docs/resources/invite#get-target-users-job-status
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"invites/{invite_code}/target-users/job-status",
            response=JsonResponse(InviteTargetUsersJobStatus),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["InviteEndpointMixin"]
