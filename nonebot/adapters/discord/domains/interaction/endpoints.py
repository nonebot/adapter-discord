from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from .read import InteractionResponse
from ..component.read import Component, DirectComponent
from ..message.read import AllowedMention, Embed, File, MessageGet
from ..message.types import MessageFlag
from ..message.write import AttachmentSend, PollRequest
from ..webhook.write import ExecuteWebhookParams, WebhookMessageEditParams
from ...api.validation import validate_outbound_value
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonResponse,
    PreparedBody,
    RestCall,
    _bool_query,
)
from ...utils import model_dump

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class InteractionEndpointMixin:
    async def _api_create_interaction_response(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        interaction_id: SnowflakeType,
        interaction_token: str,
        response: InteractionResponse,
        with_response: bool | None = None,
    ) -> InteractionResponse | None:
        """Create an interaction response.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#create-interaction-response
        """
        request_files: list[File] | None = None
        if isinstance(response.data, Mapping):
            raw_files = response.data.get("files")
            if isinstance(raw_files, list) and raw_files:
                request_files = [
                    file if isinstance(file, File) else File(**file)
                    for file in raw_files
                ]
        payload: dict[str, object] = model_dump(
            response,
            exclude_none=True,
            omit_unset_values=True,
        )
        data = payload.get("data")
        if isinstance(data, Mapping):
            data_payload = dict(data)
            data_payload.pop("files", None)
            payload["data"] = data_payload
        params = PreparedBody(
            payload,
            files=request_files,
            attachment_owner_path=("data",),
        )

        query = {"with_response": _bool_query(value=with_response)}
        call = RestCall(
            method="POST",
            url=self.base_url
            / f"interactions/{interaction_id}/{interaction_token}/callback",
            response=JsonResponse(InteractionResponse, allow_empty=True),
            auth=BotAuth(bot.bot_info),
            query=query,
            body=params,
        )
        resp = await REST_EXCHANGE.execute(self, call)
        if resp is None:
            return None
        return resp

    async def _api_get_origin_interaction_response(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = None,
    ) -> MessageGet:
        """Get the original interaction response.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#get-original-interaction-response
        """

        params = {"thread_id": thread_id}
        call = RestCall(
            method="GET",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/@original",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_edit_origin_interaction_response(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        content: MissingOrNullable[str] = UNSET,
        embeds: MissingOrNullable[list[Embed]] = UNSET,
        flags: MissingOrNullable[MessageFlag] = UNSET,
        allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
        components: MissingOrNullable[list[Component]] = UNSET,
        files: Missing[list[File]] = UNSET,
        attachments: MissingOrNullable[list[AttachmentSend]] = UNSET,
        poll: MissingOrNullable[PollRequest] = UNSET,
    ) -> MessageGet:
        """Edit the original interaction response.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#edit-original-interaction-response
        """
        params: dict[str, Any] = {"thread_id": thread_id}
        if with_components is not None:
            params["with_components"] = str(with_components).lower()

        data = {
            "content": content,
            "embeds": embeds,
            "flags": flags,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "poll": poll,
        }
        request_kwargs_payload = dict(
            validate_outbound_value(
                WebhookMessageEditParams,
                {key: value for key, value in data.items() if value is not UNSET},
            )
        )
        request_kwargs_files = request_kwargs_payload.pop("files", None)
        request_kwargs = PreparedBody(
            request_kwargs_payload, files=request_kwargs_files or None
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/@original",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            query=params,
            body=request_kwargs,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_origin_interaction_response(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        thread_id: SnowflakeType | None = None,
    ) -> None:
        """Delete the original interaction response.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#delete-original-interaction-response
        """

        params = {"thread_id": thread_id}
        call = RestCall(
            method="DELETE",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/@original",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_create_followup_message(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        content: str | None = None,
        tts: bool | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: AllowedMention | None = None,
        components: list[DirectComponent] | None = None,
        files: list[File] | None = None,
        attachments: list[AttachmentSend] | None = None,
        flags: MessageFlag | None = None,
        poll: PollRequest | None = None,
    ) -> MessageGet:
        """Create a followup message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message
        """
        has_payload = any(
            [
                bool(content),
                bool(embeds),
                bool(components),
                bool(files),
            ]
        )
        if not has_payload:
            msg = "content/embeds/components/files is required"
            raise ValueError(msg)
        data = {
            "content": content,
            "tts": tts,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "flags": flags,
            "poll": poll,
        }
        request_kwargs_payload = dict(
            validate_outbound_value(
                ExecuteWebhookParams,
                {
                    key: value
                    for key, value in {
                        key: value for (key, value) in data.items() if value is not None
                    }.items()
                    if value is not UNSET
                },
            )
        )
        request_kwargs_files = request_kwargs_payload.pop("files", None)
        request_kwargs = PreparedBody(
            request_kwargs_payload, files=request_kwargs_files or None
        )

        call = RestCall(
            method="POST",
            url=self.base_url / f"webhooks/{application_id}/{interaction_token}",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            body=request_kwargs,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_followup_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
    ) -> MessageGet:
        """Get a followup message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#get-followup-message
        """

        params = {"thread_id": thread_id}
        call = RestCall(
            method="GET",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_edit_followup_message(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
        with_components: bool | None = None,
        content: MissingOrNullable[str] = UNSET,
        embeds: MissingOrNullable[list[Embed]] = UNSET,
        flags: MissingOrNullable[MessageFlag] = UNSET,
        allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
        components: MissingOrNullable[list[Component]] = UNSET,
        files: Missing[list[File]] = UNSET,
        attachments: MissingOrNullable[list[AttachmentSend]] = UNSET,
        poll: MissingOrNullable[PollRequest] = UNSET,
    ) -> MessageGet:
        """Edit a followup message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#edit-followup-message
        """

        params: dict[str, Any] = {"thread_id": thread_id}
        if with_components is not None:
            params["with_components"] = str(with_components).lower()
        data = {
            "content": content,
            "embeds": embeds,
            "flags": flags,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "poll": poll,
        }
        request_kwargs_payload = dict(
            validate_outbound_value(
                WebhookMessageEditParams,
                {key: value for key, value in data.items() if value is not UNSET},
            )
        )
        request_kwargs_files = request_kwargs_payload.pop("files", None)
        request_kwargs = PreparedBody(
            request_kwargs_payload, files=request_kwargs_files or None
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            query=params,
            body=request_kwargs,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_followup_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        interaction_token: str,
        message_id: SnowflakeType,
        thread_id: SnowflakeType | None = None,
    ) -> None:
        """Delete a followup message.

        see https://discord.com/developers/docs/interactions/receiving-and-responding#delete-followup-message
        """

        params = {"thread_id": thread_id}
        call = RestCall(
            method="DELETE",
            url=self.base_url
            / f"webhooks/{application_id}/{interaction_token}/messages/{message_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        await REST_EXCHANGE.execute(self, call)


__all__ = ["InteractionEndpointMixin"]
