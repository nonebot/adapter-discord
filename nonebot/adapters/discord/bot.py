from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Literal, Optional, Union
from typing_extensions import override
from urllib.parse import urlparse

from nonebot.adapters import Bot as BaseBot

from nonebot.drivers import Request
from nonebot.message import handle_event

from .api import (
    UNSET,
    AllowedMention,
    ApiClient,
    File,
    InteractionCallbackMessage,
    InteractionCallbackType,
    InteractionResponse,
    MessageGet,
    MessageReference,
    Snowflake,
    SnowflakeType,
    User,
)
from .config import BotInfo
from .event import Event, InteractionCreateEvent, MessageEvent
from .exception import ActionFailed
from .message import Message, MessageSegment, parse_message
from .utils import log

if TYPE_CHECKING:
    from .adapter import Adapter


DISCORD_ATTACHMENT_HOSTS = {"cdn.discordapp.com", "media.discordapp.net"}
AttachmentFetchOnError = Literal["raise", "skip"]


async def _check_reply(bot: "Bot", event: MessageEvent) -> None:
    message_reference = event.message_reference
    if message_reference is UNSET:
        return

    message_id = message_reference.message_id
    if message_id is UNSET:
        return

    try:
        msg = await bot.get_channel_message(
            channel_id=event.channel_id, message_id=message_id
        )
        event.reply = msg
        if msg.author.id == bot.self_info.id:
            event.to_me = True
    except Exception as e:
        log("WARNING", f"Error when getting message reply info: {e!r}", e)


def _check_at_me(bot: "Bot", event: MessageEvent) -> None:  # noqa: C901
    if event.mentions is not None and bot.self_info.id in [
        user.id for user in event.mentions
    ]:
        event.to_me = True

    def _is_at_me_seg(segment: MessageSegment) -> bool:
        return (
            segment.type == "mention_user"
            and segment.data.get("user_id") == bot.self_info.id
        )

    message = event.get_message()

    # ensure message is not empty
    if not message:
        message.append(MessageSegment.text(""))

    deleted = False
    if _is_at_me_seg(message[0]):
        message.pop(0)
        deleted = True
        if message and message[0].type == "text":
            message[0].data["text"] = message[0].data["text"].lstrip("\xa0").lstrip()
            if not message[0].data["text"]:
                del message[0]

    if not deleted:
        # check the last segment
        i = -1
        last_msg_seg = message[i]
        if (
            last_msg_seg.type == "text"
            and not last_msg_seg.data["text"].strip()
            and len(message) >= 2  # noqa: PLR2004
        ):
            i -= 1
            last_msg_seg = message[i]

        if _is_at_me_seg(last_msg_seg):
            deleted = True
            del message[i:]

    if not message:
        message.append(MessageSegment.text(""))


class Bot(BaseBot, ApiClient):
    """
    Discord 协议 Bot 适配。
    """

    adapter: "Adapter"

    @override
    def __init__(self, adapter: "Adapter", self_id: str, bot_info: BotInfo) -> None:
        super().__init__(adapter, self_id)
        self.adapter = adapter
        self._bot_info: BotInfo = bot_info
        self._application_id: Snowflake = Snowflake(self_id)
        self._session_id: Optional[str] = None
        self._self_info: Optional[User] = None
        self._sequence: Optional[int] = None

    @override
    def __repr__(self) -> str:
        return f"Bot(type={self.type!r}, self_id={self.self_id!r})"

    @property
    def ready(self) -> bool:
        return self._session_id is not None

    @property
    def bot_info(self) -> BotInfo:
        return self._bot_info

    @property
    def application_id(self) -> Snowflake:
        return self._application_id

    @property
    def session_id(self) -> str:
        if self._session_id is None:
            msg = f"Bot {self.self_id} is not connected!"
            raise RuntimeError(msg)
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str) -> None:
        self._session_id = session_id

    @property
    def self_info(self) -> User:
        if self._self_info is None:
            msg = f"Bot {self.bot_info} is not connected!"
            raise RuntimeError(msg)
        return self._self_info

    @self_info.setter
    def self_info(self, self_info: User) -> None:
        self._self_info = self_info

    @property
    def has_sequence(self) -> bool:
        return self._sequence is not None

    @property
    def sequence(self) -> int:
        if self._sequence is None:
            msg = f"Bot {self.self_id} is not connected!"
            raise RuntimeError(msg)
        return self._sequence

    @sequence.setter
    def sequence(self, sequence: int) -> None:
        self._sequence = sequence

    def clear(self) -> None:
        self._session_id = None
        self._sequence = None

    async def handle_event(self, event: Event) -> None:
        if isinstance(event, MessageEvent):
            await _check_reply(self, event)
            _check_at_me(self, event)
        await handle_event(self, event)

    async def fetch_attachments(  # noqa: PLR0913
        self,
        message: Union[str, Message, MessageSegment],
        *,
        allowed_hosts: Optional[set[str]] = None,
        require_https: bool = True,
        timeout: Optional[float] = None,
        max_bytes: Optional[int] = None,
        prefer_proxy_url: bool = True,
        on_error: AttachmentFetchOnError = "raise",
    ) -> Message:
        message = MessageSegment.text(message) if isinstance(message, str) else message
        message = message if isinstance(message, Message) else Message(message)
        new = message.clone()

        if allowed_hosts is None:
            allowed_hosts = DISCORD_ATTACHMENT_HOSTS

        attachment_segments = new["attachment"] or []
        for index, attachment in enumerate(attachment_segments):
            if attachment.data["file"] is not None:
                continue

            url = self._pick_attachment_url(
                attachment,
                allowed_hosts=allowed_hosts,
                require_https=require_https,
                prefer_proxy_url=prefer_proxy_url,
            )
            if url is None:
                if on_error == "raise":
                    msg = (
                        f"Attachment segment at index {index} has no fetchable "
                        "url/proxy_url"
                    )
                    raise ValueError(msg)
                continue

            content = await self._fetch_attachment_content(
                url,
                timeout=timeout,
                max_bytes=max_bytes,
            )
            if content is None:
                if on_error == "raise":
                    msg = (
                        f"Failed to fetch attachment content for segment "
                        f"at index {index} from URL {url}"
                    )
                    raise ValueError(msg)
                continue

            attachment.data["file"] = File(
                filename=attachment.data["attachment"].filename,
                content=content,
            )

        return new

    @staticmethod
    def _pick_attachment_url(
        attachment: MessageSegment,
        *,
        allowed_hosts: set[str],
        require_https: bool,
        prefer_proxy_url: bool,
    ) -> Optional[str]:
        urls = []
        if prefer_proxy_url:
            urls.extend(
                [
                    attachment.data.get("proxy_url"),
                    attachment.data.get("url"),
                ]
            )
        else:
            urls.extend(
                [
                    attachment.data.get("url"),
                    attachment.data.get("proxy_url"),
                ]
            )

        for candidate in urls:
            if isinstance(candidate, str) and Bot._is_supported_attachment_url(
                candidate,
                allowed_hosts=allowed_hosts,
                require_https=require_https,
            ):
                return candidate

        return None

    @staticmethod
    def _is_supported_attachment_url(
        url: str, *, allowed_hosts: set[str], require_https: bool
    ) -> bool:
        parsed = urlparse(url)
        scheme_ok = parsed.scheme == "https" if require_https else bool(parsed.scheme)
        return scheme_ok and parsed.netloc in allowed_hosts

    async def _fetch_attachment_content(
        self,
        url: str,
        *,
        timeout: Optional[float],
        max_bytes: Optional[int],
    ) -> Optional[bytes]:
        try:
            request = Request(
                method="GET",
                url=url,
                timeout=timeout or self.adapter.discord_config.discord_api_timeout,
                proxy=self.adapter.discord_config.discord_proxy,
            )
            response = await self.adapter.request(request)
            if response.status_code != HTTPStatus.OK or not response.content:
                return None
            content = (
                response.content.encode()
                if isinstance(response.content, str)
                else response.content
            )
            if max_bytes is not None and len(content) > max_bytes:
                return None
            return content  # noqa: TRY300
        except Exception as e:
            log("DEBUG", f"Failed to fetch attachment content from URL {url}: {e!r}", e)
            return None

    async def send_to(
        self,
        channel_id: SnowflakeType,
        message: Union[str, Message, MessageSegment],
        tts: bool = False,  # noqa: FBT001, FBT002
        nonce: Union[int, str, None] = None,
        allowed_mentions: Optional[AllowedMention] = None,
    ) -> MessageGet:
        message = MessageSegment.text(message) if isinstance(message, str) else message
        message = message if isinstance(message, Message) else Message(message)
        message = message.sendable()
        message_data = parse_message(message)

        return await self.create_message(
            channel_id=channel_id,
            nonce=nonce,
            tts=tts,
            allowed_mentions=allowed_mentions,
            **message_data,
        )

    @override
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        tts: bool = False,
        nonce: Union[int, str, None] = None,
        allowed_mentions: Optional[AllowedMention] = None,
        mention_sender: Optional[bool] = None,
        at_sender: Optional[bool] = None,
        reply_message: bool = False,
        **params: Any,
    ) -> MessageGet:
        """send message.

        Args:
            event: Event Object
            message: message to send
            mention_sender: whether @ event subject
            reply_message: whether reply event message
            tts: whether send as a TTS message
            nonce: can be used to verify a message was sent
            allowed_mentions: allowed mentions for the message
            **params: other params

        Returns:
            message model
        """
        message = MessageSegment.text(message) if isinstance(message, str) else message
        message = message if isinstance(message, Message) else Message(message)
        message = message.sendable()
        if isinstance(event, InteractionCreateEvent):
            message_data = parse_message(message)
            response = InteractionResponse(
                type=InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                data=InteractionCallbackMessage(
                    tts=tts, allowed_mentions=allowed_mentions, **message_data
                ),
            )
            try:
                await self.create_interaction_response(
                    interaction_id=event.id,
                    interaction_token=event.token,
                    response=response,
                )
            except ActionFailed:
                return await self.create_followup_message(
                    application_id=event.application_id,
                    interaction_token=event.token,
                    **message_data,
                )
            return await self.get_origin_interaction_response(
                application_id=event.application_id,
                interaction_token=event.token,
            )

        if not isinstance(event, MessageEvent) or not event.channel_id or not event.id:
            msg = "Event cannot be replied to!"
            raise RuntimeError(msg)
        if mention_sender or at_sender:
            message.insert(0, MessageSegment.mention_user(event.user_id))
        if reply_message:
            message += MessageSegment.reference(MessageReference(message_id=event.id))

        message_data = parse_message(message)

        return await self.create_message(
            channel_id=event.channel_id,
            nonce=nonce,
            tts=tts,
            allowed_mentions=allowed_mentions,
            **message_data,
        )
