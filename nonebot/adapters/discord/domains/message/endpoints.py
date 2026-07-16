from typing import TYPE_CHECKING, Annotated, overload
from urllib.parse import quote

from yarl import URL

from .read import (
    AllowedMention,
    AnswerVoters,
    Embed,
    File,
    MessageGet,
    MessageReference,
)
from .types import MessageFlag, MessageReferenceType, ReactionType
from .write import AttachmentSend, MessageEditParams, MessageSend, PollRequest
from ..component.read import Component, DirectComponent
from ..user.read import User
from ...api.utils import parse_data
from ...api.validation import AtMostOne, Range, validate
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonResponse,
    JsonValueBody,
    PreparedBody,
    RestCall,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


def _build_reaction_url(
    *,
    base_url: URL,
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
    emoji: str,
    suffix: str = "",
) -> URL:
    encoded_emoji = quote(emoji, safe="")
    suffix_path = f"/{suffix}" if suffix else ""
    return URL(
        (
            f"{base_url}/channels/{channel_id}/messages/"
            f"{message_id}/reactions/{encoded_emoji}{suffix_path}"
        ),
        encoded=True,
    )


class MessageEndpointMixin:
    @overload
    async def _api_get_channel_messages(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: SnowflakeType | None = None,
        before: None = None,
        after: None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[MessageGet]: ...

    @overload
    async def _api_get_channel_messages(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: None = None,
        before: SnowflakeType | None = None,
        after: None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[MessageGet]: ...

    @overload
    async def _api_get_channel_messages(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: None = None,
        before: None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[MessageGet]: ...

    @validate(
        cross_rules=(
            AtMostOne(
                fields=("around", "before", "after"),
                message="around, before and after are mutually exclusive",
            ),
        )
    )
    async def _api_get_channel_messages(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        around: SnowflakeType | None = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[MessageGet]:
        """Get channel messages.

        see https://discord.com/developers/docs/resources/message#get-channel-messages
        """

        params = {
            "around": around,
            "before": before,
            "after": after,
            "limit": limit,
        }
        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/messages",
            response=JsonResponse(list[MessageGet]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_channel_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """Get a channel message.

        see https://discord.com/developers/docs/resources/message#get-channel-message
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_message(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        content: str | None = None,
        nonce: int | str | None = None,
        enforce_nonce: bool | None = None,
        tts: bool | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: AllowedMention | None = None,
        message_reference: MessageReference | None = None,
        components: list[DirectComponent] | None = None,
        sticker_ids: list[SnowflakeType] | None = None,
        files: list[File] | None = None,
        attachments: list[AttachmentSend] | None = None,
        flags: MessageFlag | None = None,
        poll: PollRequest | None = None,
    ) -> MessageGet:
        """Create a message.

        see https://discord.com/developers/docs/resources/message#create-message
        """
        has_payload = any(
            [
                bool(content),
                bool(embeds),
                bool(sticker_ids),
                bool(components),
                bool(files),
                poll is not None,
            ]
        )
        if not has_payload and (
            message_reference is None
            or message_reference.type != MessageReferenceType.FORWARD
        ):
            msg = "content/embeds/sticker_ids/components/files/poll is required"
            raise ValueError(msg)
        data = {
            "content": content,
            "nonce": nonce,
            "enforce_nonce": enforce_nonce,
            "tts": tts,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "message_reference": message_reference,
            "components": components,
            "sticker_ids": sticker_ids,
            "files": files,
            "attachments": attachments,
            "flags": flags,
            "poll": poll,
        }
        params = parse_data(
            {key: value for (key, value) in data.items() if value is not None},
            MessageSend,
        )

        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/messages",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            body=PreparedBody(params),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_crosspost_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """Crosspost a message.

        see https://discord.com/developers/docs/resources/message#crosspost-message
        """

        call = RestCall(
            method="POST",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/crosspost",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_create_reaction(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """Create a reaction.

        see https://discord.com/developers/docs/resources/message#create-reaction
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"

        call = RestCall(
            method="PUT",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
                suffix="@me",
            ),
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_delete_own_reaction(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """Delete own reaction.

        see https://discord.com/developers/docs/resources/message#delete-own-reaction
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"

        call = RestCall(
            method="DELETE",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
                suffix="@me",
            ),
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_delete_user_reaction(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        user_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """Delete a user reaction.

        see https://discord.com/developers/docs/resources/message#delete-user-reaction
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"

        call = RestCall(
            method="DELETE",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
                suffix=str(user_id),
            ),
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_get_reactions(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
        type: ReactionType | None = None,  # noqa: A002
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> list[User]:
        """Get reactions.

        see https://discord.com/developers/docs/resources/message#get-reactions
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"

        params = {"after": after, "limit": limit, "type": type}
        call = RestCall(
            method="GET",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
            ),
            response=JsonResponse(list[User]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_all_reactions(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> None:
        """Delete all reactions.

        see https://discord.com/developers/docs/resources/message#delete-all-reactions
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url
            / f"channels/{channel_id}/messages/{message_id}/reactions",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_delete_all_reactions_for_emoji(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        emoji: str,
        emoji_id: SnowflakeType | None = None,
    ) -> None:
        """Delete all reactions for emoji.

        see https://discord.com/developers/docs/resources/message#delete-all-reactions-for-emoji
        """
        if emoji_id is not None:
            emoji = f"{emoji}:{emoji_id}"

        call = RestCall(
            method="DELETE",
            url=_build_reaction_url(
                base_url=self.base_url,
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
            ),
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_edit_message(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        content: MissingOrNullable[str] = UNSET,
        embeds: MissingOrNullable[list[Embed]] = UNSET,
        flags: MissingOrNullable[MessageFlag] = UNSET,
        allowed_mentions: MissingOrNullable[AllowedMention] = UNSET,
        components: MissingOrNullable[list[Component]] = UNSET,
        files: Missing[list[File]] = UNSET,
        attachments: MissingOrNullable[list[AttachmentSend]] = UNSET,
        sticker_ids: Missing[list[SnowflakeType]] = UNSET,
        poll: MissingOrNullable[PollRequest] = UNSET,
    ) -> MessageGet:
        """Edit a message.

        see https://discord.com/developers/docs/resources/message#edit-message
        """
        data = {
            "content": content,
            "embeds": embeds,
            "flags": flags,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "files": files,
            "attachments": attachments,
            "sticker_ids": sticker_ids,
            "poll": poll,
        }
        params = parse_data(data, MessageEditParams)

        call = RestCall(
            method="PATCH",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
            body=PreparedBody(params),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete a message.

        see https://discord.com/developers/docs/resources/message#delete-message
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"channels/{channel_id}/messages/{message_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_bulk_delete_message(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        messages: Annotated[
            list[SnowflakeType],
            Range(
                message="messages must contain 2-100 items",
                min_length=2,
                max_length=100,
            ),
        ],
        reason: str | None = None,
    ) -> None:
        """Bulk delete messages.

        see https://discord.com/developers/docs/resources/message#bulk-delete-messages
        """

        data = {"messages": messages}
        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/messages/bulk-delete",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(data),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_get_answer_voters(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
        answer_id: int,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AnswerVoters:
        """Get answer voters.

        see https://discord.com/developers/docs/resources/poll#get-answer-voters
        """

        params = {"after": after, "limit": limit}
        call = RestCall(
            method="GET",
            url=self.base_url
            / f"channels/{channel_id}/polls/{message_id}/answers/{answer_id}",
            response=JsonResponse(AnswerVoters),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_end_poll(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        channel_id: SnowflakeType,
        message_id: SnowflakeType,
    ) -> MessageGet:
        """End poll.

        see https://discord.com/developers/docs/resources/poll#end-poll
        """

        call = RestCall(
            method="POST",
            url=self.base_url / f"channels/{channel_id}/polls/{message_id}/expire",
            response=JsonResponse(MessageGet),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["MessageEndpointMixin"]
