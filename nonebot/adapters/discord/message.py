from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
import datetime
import re
from typing import (
    Any,
    overload,
)
from typing_extensions import Self, override

from nonebot.adapters import (
    Message as BaseMessage,
    MessageSegment as BaseMessageSegment,
)

from nonebot.compat import type_validate_python

from .api import (
    UNSET,
    ActionRow,
    AttachmentSend,
    Button,
    Component,
    ComponentType,
    Embed,
    File,
    MessageGet,
    MessageReference,
    Poll,
    PollAnswerRequest,
    PollRequest,
    SelectMenu,
    Snowflake,
    SnowflakeType,
    TextInput,
    TimeStampStyle,
)
from .api.types import is_not_unset
from .utils import unescape


class MessageSegment(BaseMessageSegment["Message"]):
    """Message segment for Discord messages.

    see https://discord.com/developers/docs/reference#message-formatting
    """

    @classmethod
    @override
    def get_message_class(cls) -> type["Message"]:
        return Message

    @staticmethod
    def attachment(
        file: str | File | AttachmentSend,
        description: str | None = None,
        content: bytes | None = None,
        *,
        url: str | None = None,
        proxy_url: str | None = None,
    ) -> "AttachmentSegment":
        if isinstance(file, str):
            _filename = file
            _description = description
            _content = content
        elif isinstance(file, File):
            _filename = file.filename
            _description = description
            _content = file.content
        elif isinstance(file, AttachmentSend):
            _filename = file.filename
            _description = file.description
            _content = content
        else:
            msg = "file must be str, File or AttachmentSend"
            raise TypeError(msg)
        if _content is None:
            return AttachmentSegment(
                "attachment",
                {
                    "attachment": AttachmentSend(
                        filename=_filename, description=_description
                    ),
                    "file": None,
                    "url": url,
                    "proxy_url": proxy_url,
                },
            )
        return AttachmentSegment(
            "attachment",
            {
                "attachment": AttachmentSend(
                    filename=_filename, description=_description
                ),
                "file": (
                    File(filename=_filename, content=_content)
                    if isinstance(_filename, str)
                    else None
                ),
                "url": url,
                "proxy_url": proxy_url,
            },
        )

    @staticmethod
    def sticker(sticker_id: SnowflakeType) -> "StickerSegment":
        return StickerSegment("sticker", {"id": Snowflake(sticker_id)})

    @staticmethod
    def embed(embed: Embed) -> "EmbedSegment":
        return EmbedSegment("embed", {"embed": embed})

    @staticmethod
    def component(component: Component) -> "ComponentSegment":
        if isinstance(component, (Button, SelectMenu)):
            component_ = ActionRow(components=[component])
        else:
            component_ = component
        return ComponentSegment("component", {"component": component_})

    @staticmethod
    def custom_emoji(
        name: str,
        emoji_id: str,
        animated: bool | None = None,  # noqa: FBT001
    ) -> "CustomEmojiSegment":
        return CustomEmojiSegment(
            "custom_emoji", {"name": name, "id": emoji_id, "animated": animated}
        )

    @staticmethod
    def mention_user(user_id: SnowflakeType) -> "MentionUserSegment":
        return MentionUserSegment("mention_user", {"user_id": Snowflake(user_id)})

    @staticmethod
    def mention_role(role_id: SnowflakeType) -> "MentionRoleSegment":
        return MentionRoleSegment("mention_role", {"role_id": Snowflake(role_id)})

    @staticmethod
    def mention_channel(channel_id: SnowflakeType) -> "MentionChannelSegment":
        return MentionChannelSegment(
            "mention_channel", {"channel_id": Snowflake(channel_id)}
        )

    @staticmethod
    def mention_everyone() -> "MentionEveryoneSegment":
        return MentionEveryoneSegment("mention_everyone")

    @staticmethod
    def text(content: str) -> "TextSegment":
        return TextSegment("text", {"text": content})

    @staticmethod
    def timestamp(
        timestamp: int | datetime.datetime, style: TimeStampStyle | None = None
    ) -> "TimestampSegment":
        if isinstance(timestamp, datetime.datetime):
            timestamp = int(timestamp.timestamp())
        return TimestampSegment("timestamp", {"timestamp": timestamp, "style": style})

    @staticmethod
    @overload
    def reference(reference: MessageReference) -> "ReferenceSegment": ...

    @staticmethod
    @overload
    def reference(
        reference: SnowflakeType,
        channel_id: SnowflakeType | None = None,
        guild_id: SnowflakeType | None = None,
        fail_if_not_exists: bool | None = None,  # noqa: FBT001
    ) -> "ReferenceSegment": ...

    @staticmethod
    def reference(
        reference: SnowflakeType | MessageReference,
        channel_id: SnowflakeType | None = None,
        guild_id: SnowflakeType | None = None,
        fail_if_not_exists: bool | None = None,  # noqa: FBT001
    ):
        if isinstance(reference, MessageReference):
            _reference = reference
        else:
            _reference = MessageReference(
                message_id=Snowflake(reference) if reference else UNSET,
                channel_id=Snowflake(channel_id) if channel_id else UNSET,
                guild_id=Snowflake(guild_id) if guild_id else UNSET,
                fail_if_not_exists=fail_if_not_exists or UNSET,
            )

        return ReferenceSegment("reference", {"reference": _reference})

    @staticmethod
    def poll(poll: Poll | PollRequest) -> "PollSegment":
        return PollSegment("poll", {"poll": poll})

    @override
    def is_text(self) -> bool:
        return self.type == "text"

    @classmethod
    @override
    def _validate(cls, value) -> Self:  # noqa: ANN001
        if isinstance(value, cls):
            return value
        if isinstance(value, MessageSegment):
            msg = f"Type {type(value)} can not be converted to {cls}"
            raise TypeError(msg)
        if not isinstance(value, dict):
            msg = f"Expected dict for MessageSegment, got {type(value)}"
            raise TypeError(msg)
        if "type" not in value:
            msg = f"Expected dict with 'type' for MessageSegment, got {value}"
            raise ValueError(msg)
        _type = value["type"]
        if _type not in SEGMENT_TYPE_MAP:
            msg = f"Invalid MessageSegment type: {_type}"
            raise ValueError(msg)
        segment_type = SEGMENT_TYPE_MAP[_type]

        # casting value to subclass of MessageSegment
        if cls is MessageSegment:
            return type_validate_python(segment_type, value)
        # init segment instance directly if type matched
        if cls is segment_type:
            return segment_type(type=_type, data=value.get("data", {}))
        msg = f"Segment type {_type!r} can not be converted to {cls}"
        raise ValueError(msg)


@dataclass
class StickerSegment(MessageSegment):
    """Sticker segment.

    see https://discord.com/developers/docs/resources/channel#create-message
    """

    @override
    def __str__(self) -> str:
        return f"<Sticker:{self.data['id']}>"


@dataclass
class ComponentSegment(MessageSegment):
    """Component segment.

    see https://discord.com/developers/docs/interactions/message-components
    """

    @override
    def __str__(self) -> str:
        return f"<Component:{self.data['component'].type}>"

    @classmethod
    @override
    def _validate(cls, value) -> Self:  # noqa: ANN001
        instance = super()._validate(value)
        if "component" not in instance.data:
            msg = f"Expected dict with 'component' in 'data' for ComponentSegment, got {value}"
            raise ValueError(msg)
        if not isinstance(
            component := instance.data["component"], (ActionRow, TextInput)
        ):
            if not isinstance(component, dict):
                msg = f"Expected dict for ComponentData, got {type(component)}"
                raise TypeError(msg)
            if "type" not in component:
                msg = f"Expected dict with 'type' for ComponentData, got {component}"
                raise ValueError(msg)
            if component["type"] == ComponentType.ActionRow:
                instance.data["component"] = type_validate_python(ActionRow, component)
            elif component["type"] == ComponentType.TextInput:
                instance.data["component"] = type_validate_python(TextInput, component)
            else:
                msg = f"Invalid ComponentType: {component['type']}"
                raise ValueError(msg)
        return instance


@dataclass
class CustomEmojiSegment(MessageSegment):
    """Custom emoji segment.

    see https://discord.com/developers/docs/reference#message-formatting
    """

    @override
    def __str__(self) -> str:
        if self.data.get("animated"):
            return f"<a:{self.data['name']}:{self.data['id']}>"
        return f"<:{self.data['name']}:{self.data['id']}>"


@dataclass
class MentionUserSegment(MessageSegment):
    """Mention user segment.

    see https://discord.com/developers/docs/reference#message-formatting
    """

    @override
    def __str__(self) -> str:
        return f"<@{self.data['user_id']}>"


@dataclass
class MentionChannelSegment(MessageSegment):
    """Mention channel segment.

    see https://discord.com/developers/docs/reference#message-formatting
    """

    @override
    def __str__(self) -> str:
        return f"<#{self.data['channel_id']}>"


@dataclass
class MentionRoleSegment(MessageSegment):
    """Mention role segment.

    see https://discord.com/developers/docs/reference#message-formatting
    """

    @override
    def __str__(self) -> str:
        return f"<@&{self.data['role_id']}>"


@dataclass
class MentionEveryoneSegment(MessageSegment):
    """Mention everyone segment.

    see https://discord.com/developers/docs/reference#message-formatting
    """

    @override
    def __str__(self) -> str:
        return "@everyone"


@dataclass
class TimestampSegment(MessageSegment):
    """Timestamp segment.

    see https://discord.com/developers/docs/reference#message-formatting-timestamp-styles
    """

    @override
    def __str__(self) -> str:
        style = self.data.get("style")
        return (
            f"<t:{self.data['timestamp']}"
            + (
                f":{style.value if isinstance(style, TimeStampStyle) else style}"
                if style
                else ""
            )
            + ">"
        )


@dataclass
class TextSegment(MessageSegment):
    """Text segment.

    see https://discord.com/developers/docs/resources/channel#create-message
    """

    @override
    def __str__(self) -> str:
        return self.data["text"]


@dataclass
class EmbedSegment(MessageSegment):
    """Embed segment.

    see https://discord.com/developers/docs/resources/message#embed-object
    """

    @override
    def __str__(self) -> str:
        return f"<Embed:{self.data['embed'].type}>"

    @classmethod
    @override
    def _validate(cls, value) -> Self:  # noqa: ANN001
        instance = super()._validate(value)
        if "embed" not in instance.data:
            msg = f"Expected dict with 'embed' in 'data' for EmbedSegment, got {value}"
            raise ValueError(msg)
        if not isinstance(embed := instance.data["embed"], Embed):
            instance.data["embed"] = type_validate_python(Embed, embed)
        return instance


@dataclass
class AttachmentSegment(MessageSegment):
    """Attachment segment.

    see https://discord.com/developers/docs/reference#uploading-files
    """

    @override
    def __str__(self) -> str:
        return f"<Attachment:{self.data['attachment'].filename}>"

    @classmethod
    @override
    def _validate(cls, value) -> Self:  # noqa: ANN001
        instance = super()._validate(value)
        if "attachment" not in instance.data:
            msg = f"Expected dict with 'attachment' in 'data' for AttachmentSegment, got {value}"
            raise ValueError(msg)
        if not isinstance(attachment := instance.data["attachment"], AttachmentSend):
            instance.data["attachment"] = type_validate_python(
                AttachmentSend, attachment
            )
        if (file := instance.data.get("file")) is not None and not isinstance(
            file, File
        ):
            instance.data["file"] = type_validate_python(File, file)
        url = instance.data.get("url")
        if url is not None and not isinstance(url, str):
            msg = f"Expected str for AttachmentSegment.data['url'], got {type(url)}"
            raise TypeError(msg)
        proxy_url = instance.data.get("proxy_url")
        if proxy_url is not None and not isinstance(proxy_url, str):
            msg = (
                "Expected str for AttachmentSegment.data['proxy_url'], "
                f"got {type(proxy_url)}"
            )
            raise TypeError(msg)
        return instance


@dataclass
class ReferenceSegment(MessageSegment):
    """Reference segment.

    see https://discord.com/developers/docs/resources/message#message-reference-object
    """

    @override
    def __str__(self) -> str:
        return f"<Reference:{self.data['reference'].message_id}>"

    @classmethod
    @override
    def _validate(cls, value) -> Self:  # noqa: ANN001
        instance = super()._validate(value)
        if "reference" not in instance.data:
            msg = f"Expected dict with 'reference' in 'data' for ReferenceSegment, got {value}"
            raise ValueError(msg)
        if not isinstance(reference := instance.data["reference"], MessageReference):
            instance.data["reference"] = type_validate_python(
                MessageReference, reference
            )
        return instance


@dataclass
class PollSegment(MessageSegment):
    """Poll segment.

    see https://discord.com/developers/docs/resources/poll#poll-object
    """

    @override
    def __str__(self) -> str:
        return f"<Poll:{self.data['poll'].question.text}>"

    @classmethod
    @override
    def _validate(cls, value) -> Self:  # noqa: ANN001
        instance = super()._validate(value)
        if "poll" not in instance.data:
            msg = f"Expected dict with 'poll' in 'data' for PollSegment, got {value}"
            raise ValueError(msg)
        if not isinstance(poll := instance.data["poll"], (Poll, PollRequest)):
            if not isinstance(poll, dict):
                msg = f"Expected dict for PollData, got {type(poll)}"
                raise TypeError(msg)
            if (
                "expiry" in poll
                or "results" in poll
                or any("answer_id" in answer for answer in poll.get("answers", []))
            ):
                instance.data["poll"] = type_validate_python(Poll, poll)
            else:
                instance.data["poll"] = type_validate_python(PollRequest, poll)
        return instance


SEGMENT_TYPE_MAP = {
    "attachment": AttachmentSegment,
    "sticker": StickerSegment,
    "embed": EmbedSegment,
    "component": ComponentSegment,
    "custom_emoji": CustomEmojiSegment,
    "mention_user": MentionUserSegment,
    "mention_role": MentionRoleSegment,
    "mention_channel": MentionChannelSegment,
    "mention_everyone": MentionEveryoneSegment,
    "text": TextSegment,
    "timestamp": TimestampSegment,
    "reference": ReferenceSegment,
    "poll": PollSegment,
}


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @override
    def get_segment_class(cls) -> type[MessageSegment]:
        return MessageSegment

    @override
    def __add__(
        self, other: str | MessageSegment | Iterable[MessageSegment]
    ) -> "Message":
        return super().__add__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @override
    def __radd__(
        self, other: str | MessageSegment | Iterable[MessageSegment]
    ) -> "Message":
        return super().__radd__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:  # noqa: C901, PLR0912
        text_begin = 0
        for embed in re.finditer(
            r"<(?P<type>(@!|@&|@|#|/|:|a:|t:))(?P<param>[^<]+?)>",
            msg,
        ):
            if content := msg[text_begin : embed.pos + embed.start()]:
                yield MessageSegment.text(unescape(content))
            text_begin = embed.pos + embed.end()
            if embed.group("type") in ("@!", "@"):
                yield MessageSegment.mention_user(Snowflake(embed.group("param")))
            elif embed.group("type") == "@&":
                yield MessageSegment.mention_role(Snowflake(embed.group("param")))
            elif embed.group("type") == "#":
                yield MessageSegment.mention_channel(Snowflake(embed.group("param")))
            elif embed.group("type") == "/":
                # TODO: slash command
                pass
            elif embed.group("type") in (":", "a:"):
                if len(cut := embed.group("param").split(":")) == 2:  # noqa: PLR2004
                    yield MessageSegment.custom_emoji(
                        cut[0], cut[1], embed.group("type") == "a:"
                    )
                else:
                    yield MessageSegment.text(unescape(embed.group()))
            elif len(cut := embed.group("param").split(":")) == 2 and cut[0].isdigit():  # noqa: PLR2004
                yield MessageSegment.timestamp(int(cut[0]), TimeStampStyle(cut[1]))
            elif embed.group().isdigit():
                yield MessageSegment.timestamp(int(embed.group()))
            else:
                yield MessageSegment.text(unescape(embed.group()))
        if content := msg[text_begin:]:
            yield MessageSegment.text(unescape(content))

    @classmethod
    def from_guild_message(cls, message: MessageGet) -> "Message":
        msg = Message()
        if message.mention_everyone:
            msg.append(MessageSegment.mention_everyone())
        if message.content:
            msg.extend(Message(message.content))
        if message.attachments:
            msg.extend(
                MessageSegment.attachment(
                    AttachmentSend(
                        filename=attachment.filename,
                        description=(
                            attachment.description
                            if isinstance(attachment.description, str)
                            else None
                        ),
                    ),
                    url=attachment.url,
                    proxy_url=attachment.proxy_url,
                )
                for attachment in message.attachments
            )
        if message.embeds:
            msg.extend(MessageSegment.embed(embed) for embed in message.embeds)
        if is_not_unset(message.components):
            msg.extend(
                MessageSegment.component(component) for component in message.components
            )
        if is_not_unset(message.poll):
            msg.append(MessageSegment.poll(message.poll))
        return msg

    def extract_content(self) -> str:
        return "".join(
            str(seg)
            for seg in self
            if seg.type
            in (
                "text",
                "custom_emoji",
                "mention_user",
                "mention_role",
                "mention_everyone",
                "mention_channel",
                "timestamp",
            )
        )

    def clone(self) -> "Message":
        new = self.__class__()
        for segment in self:
            new.append(
                type_validate_python(
                    MessageSegment,
                    {
                        "type": segment.type,
                        "data": deepcopy(segment.data),
                    },
                )
            )
        return new

    def sendable(self) -> "Message":
        new = self.clone()
        attachments_segment = new["attachment"] or None
        if attachments_segment is not None:
            for index, attachment in enumerate(attachments_segment):
                if attachment.data["file"] is None:
                    raise ValueError(_get_unsendable_attachment_msg(index, attachment))
        return new


def parse_message(message: Message | MessageSegment | str) -> dict[str, Any]:
    message = MessageSegment.text(message) if isinstance(message, str) else message
    message = message if isinstance(message, Message) else Message(message)

    content = message.extract_content() or None
    if embeds := (message["embed"] or None):
        embeds = [embed.data["embed"] for embed in embeds]
    if reference := (message["reference"] or None):
        reference = reference[-1].data["reference"]
    if components := (message["component"] or None):
        components = [component.data["component"] for component in components]
    if sticker_ids := (message["sticker"] or None):
        sticker_ids = [sticker.data["id"] for sticker in sticker_ids]
    if poll := (message["poll"] or None):
        poll = poll[-1].data["poll"]
        if isinstance(poll, Poll):
            poll = PollRequest(
                question=poll.question,
                answers=[
                    PollAnswerRequest(poll_media=answer.poll_media)
                    for answer in poll.answers
                ],
                allow_multiselect=poll.allow_multiselect,
                layout_type=poll.layout_type,
            )

    attachments, files = extract_attachments(message)

    return {
        k: v
        for k, v in {
            "content": content,
            "embeds": embeds,
            "message_reference": reference,
            "components": components,
            "sticker_ids": sticker_ids,
            "poll": poll,
            "files": files,
            "attachments": attachments,
        }.items()
        if v is not None
    }


def extract_attachments(
    message: Message,
) -> tuple[list[AttachmentSend] | None, list[File] | None]:
    attachments_segment = message["attachment"] or None
    if not attachments_segment:
        return None, None

    attachments_list: list[AttachmentSend] = []
    files_list: list[File] = []
    for index, attachment in enumerate(attachments_segment):
        file = attachment.data["file"]
        if file is None:
            raise ValueError(_get_unsendable_attachment_msg(index, attachment))
        attachments_list.append(attachment.data["attachment"])
        files_list.append(file)

    attachments = attachments_list or None
    files = files_list or None
    return attachments, files


def _get_unsendable_attachment_msg(index: int, attachment: MessageSegment) -> str:
    if attachment.data.get("url") or attachment.data.get("proxy_url"):
        return (
            f"Attachment segment at index {index} is not sendable because file "
            "content is missing; call "
            "`await bot.fetch_attachments(message)` first"
        )
    return (
        f"Attachment segment at index {index} is not sendable because file "
        "content is missing; provide `content=` in "
        "MessageSegment.attachment(...)"
    )
