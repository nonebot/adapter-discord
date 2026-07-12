from typing import TYPE_CHECKING, Any, Literal, overload
from typing_extensions import Unpack

from .read import Webhook
from .write import (
    CreateWebhookParams,
    ExecuteWebhookParams,
    ModifyWebhookParams,
    ModifyWebhookWithTokenParams,
    WebhookMessageEditParams,
)
from ..message.read import MessageGet
from ...api.validation import validate_outbound_value
from ...protocol import SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    NoAuth,
    PreparedBody,
    RestCall,
    _bool_query,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class WebhookEndpointMixin:
    async def _api_create_webhook(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[CreateWebhookParams],
    ) -> Webhook:
        """Create webhook.

        see https://discord.com/developers/docs/resources/webhook#create-webhook
        """
        fields = validate_outbound_value(CreateWebhookParams, fields)
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/webhooks",
            response=JsonResponse(Webhook),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_channel_webhooks(
        self: "AdapterProtocol", bot: "Bot", *, channel_id: SnowflakeType
    ) -> list[Webhook]:
        """Get channel webhooks.

        see https://discord.com/developers/docs/resources/webhook#get-channel-webhooks
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/webhooks",
            response=JsonResponse(list[Webhook]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_guild_webhooks(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[Webhook]:
        """Get guild webhooks.

        see https://discord.com/developers/docs/resources/webhook#get-guild-webhooks
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/webhooks",
            response=JsonResponse(list[Webhook]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_webhook(
        self: "AdapterProtocol", bot: "Bot", *, webhook_id: SnowflakeType
    ) -> Webhook:
        """Get webhook.

        see https://discord.com/developers/docs/resources/webhook#get-webhook
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}",
            response=JsonResponse(Webhook),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_webhook_with_token(
        self: "AdapterProtocol",
        *,
        webhook_id: SnowflakeType,
        token: str,
    ) -> Webhook:
        """Get webhook with token.

        see https://discord.com/developers/docs/resources/webhook#get-webhook-with-token
        """
        call = RestCall(
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
            response=JsonResponse(Webhook),
            auth=NoAuth(),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_webhook(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyWebhookParams],
    ) -> Webhook:
        """Modify webhook.

        see https://discord.com/developers/docs/resources/webhook#modify-webhook
        """
        fields = validate_outbound_value(ModifyWebhookParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"webhooks/{webhook_id}",
            response=JsonResponse(Webhook),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(fields),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_webhook_with_token(
        self: "AdapterProtocol",
        *,
        webhook_id: SnowflakeType,
        token: str,
        **fields: Unpack[ModifyWebhookWithTokenParams],
    ) -> Webhook:
        """Modify webhook with token.

        see https://discord.com/developers/docs/resources/webhook#modify-webhook-with-token
        """
        fields = validate_outbound_value(ModifyWebhookWithTokenParams, fields)
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
            response=JsonResponse(Webhook),
            auth=NoAuth(),
            body=JsonBody(fields),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_webhook(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete webhook.

        see https://discord.com/developers/docs/resources/webhook#delete-webhook
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_delete_webhook_with_token(
        self: "AdapterProtocol",
        *,
        webhook_id: SnowflakeType,
        token: str,
    ) -> None:
        """Delete webhook with token.

        see https://discord.com/developers/docs/resources/webhook#delete-webhook-with-token
        """
        call = RestCall(
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
            response=EmptyResponse(),
            auth=NoAuth(),
        )
        await REST_EXCHANGE.execute(self, call)

    @overload
    async def _api_execute_webhook(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: Literal[True],
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        **fields: Unpack[ExecuteWebhookParams],
    ) -> MessageGet: ...

    @overload
    async def _api_execute_webhook(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: Literal[False] | None = None,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        **fields: Unpack[ExecuteWebhookParams],
    ) -> None: ...

    async def _api_execute_webhook(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        wait: bool | None = None,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        **fields: Unpack[ExecuteWebhookParams],
    ) -> MessageGet | None:
        """Execute webhook.

        see https://discord.com/developers/docs/resources/webhook#execute-webhook
        """
        fields = validate_outbound_value(ExecuteWebhookParams, fields)
        has_payload = any(
            bool(fields.get(key))
            for key in ("content", "embeds", "components", "files", "poll")
        )
        if not has_payload:
            msg = "content/embeds/components/files/poll is required"
            raise ValueError(msg)
        params = {}
        if wait is not None:
            params["wait"] = str(wait).lower()
        if thread_id is not None:
            params["thread_id"] = thread_id
        if with_components is not None:
            params["with_components"] = str(with_components).lower()
        request_kwargs_files = fields.pop("files", None)
        payload = {key: value for key, value in fields.items() if value is not None}
        request_kwargs = PreparedBody(payload, files=request_kwargs_files or None)

        call = RestCall(
            method="POST",
            url=self.base_url / f"webhooks/{webhook_id}/{token}",
            response=JsonResponse(MessageGet, allow_empty=True),
            auth=BotAuth(bot.bot_info),
            query=params,
            body=request_kwargs,
        )
        resp = await REST_EXCHANGE.execute(self, call)
        if resp is None:
            return None
        return resp

    async def _api_execute_slack_compatible_webhook(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        payload: dict[str, Any],
        thread_id: SnowflakeType | None = None,
        wait: bool | None = None,
    ) -> MessageGet | None:
        """Execute Slack-compatible webhook.

        see https://discord.com/developers/docs/resources/webhook#execute-slack-compatible-webhook
        """

        params = {"thread_id": thread_id, "wait": _bool_query(value=wait)}
        call = RestCall(
            method="POST",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/slack",
            response=JsonResponse(MessageGet, allow_empty=True),
            auth=BotAuth(bot.bot_info),
            query=params,
            body=JsonBody(payload),
        )
        resp = await REST_EXCHANGE.execute(self, call)
        if resp is None:
            return None
        return resp

    async def _api_execute_github_compatible_webhook(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        payload: dict[str, Any],
        thread_id: SnowflakeType | None = None,
        wait: bool | None = None,
    ) -> MessageGet | None:
        """Execute GitHub-compatible webhook.

        see https://discord.com/developers/docs/resources/webhook#execute-github-compatible-webhook
        """

        params = {"thread_id": thread_id, "wait": _bool_query(value=wait)}
        call = RestCall(
            method="POST",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/github",
            response=JsonResponse(MessageGet, allow_empty=True),
            auth=BotAuth(bot.bot_info),
            query=params,
            body=JsonBody(payload),
        )
        resp = await REST_EXCHANGE.execute(self, call)
        if resp is None:
            return None
        return resp

    async def _api_get_webhook_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
    ) -> MessageGet:
        """Get webhook message.

        see https://discord.com/developers/docs/resources/webhook#get-webhook-message
        """

        params = {"thread_id": thread_id}
        call = RestCall(
            method="GET",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/messages/{message_id}",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_edit_webhook_message(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        webhook_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        **fields: Unpack[WebhookMessageEditParams],
    ) -> MessageGet:
        """Edit webhook message.

        see https://discord.com/developers/docs/resources/webhook#edit-webhook-message
        """
        params: dict[str, Any] = {"thread_id": thread_id}
        if with_components is not None:
            params["with_components"] = str(with_components).lower()

        fields = validate_outbound_value(WebhookMessageEditParams, fields)
        request_kwargs_files = fields.pop("files", None)
        request_kwargs = PreparedBody(fields, files=request_kwargs_files or None)
        call = RestCall(
            method="PATCH",
            url=self.base_url
            / f"webhooks/{webhook_id}/{webhook_token}/messages/{message_id}",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            query=params,
            body=request_kwargs,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_webhook_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        webhook_id: SnowflakeType,
        token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
    ) -> None:
        """Delete webhook message.

        see https://discord.com/developers/docs/resources/webhook#delete-webhook-message
        """

        params = {"thread_id": thread_id}
        call = RestCall(
            method="DELETE",
            url=self.base_url / f"webhooks/{webhook_id}/{token}/messages/{message_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        await REST_EXCHANGE.execute(self, call)


__all__ = ["WebhookEndpointMixin"]
