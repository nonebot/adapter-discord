from typing import TYPE_CHECKING, Any, Optional, Union
from typing_extensions import override

from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event

from .api import (
    AllowedMention,
    ApiClient,
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


async def _check_reply(bot: "Bot", event: MessageEvent) -> None:
    if not event.message_reference or not event.message_reference.message_id:
        return
    try:
        msg = await bot.get_channel_message(
            channel_id=event.channel_id, message_id=event.message_reference.message_id
        )
        event.reply = msg
        if msg.author.id == bot.self_info.id:
            event.to_me = True
    except Exception as e:
        log("WARNING", f"Error when getting message reply info: {repr(e)}", e)


def _check_at_me(bot: "Bot", event: MessageEvent) -> None:
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
            and len(message) >= 2
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
    def __init__(self, adapter: "Adapter", self_id: str, bot_info: BotInfo):
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
            raise RuntimeError(f"Bot {self.self_id} is not connected!")
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str) -> None:
        self._session_id = session_id

    @property
    def self_info(self) -> User:
        if self._self_info is None:
            raise RuntimeError(f"Bot {self.bot_info} is not connected!")
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
            raise RuntimeError(f"Bot {self.self_id} is not connected!")
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

    async def send_to(
        self,
        channel_id: SnowflakeType,
        message: Union[str, Message, MessageSegment],
        tts: bool = False,
        nonce: Union[int, str, None] = None,
        allowed_mentions: Optional[AllowedMention] = None,
    ):
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
            raise RuntimeError("Event cannot be replied to!")
        message = message if isinstance(message, Message) else Message(message)
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
