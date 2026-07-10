from __future__ import annotations

from enum import Enum, IntEnum, IntFlag

from .._enum import StrEnum


class AllowedMentionType(StrEnum):
    """Allowed mentions types.

    see https://discord.com/developers/docs/resources/message#allowed-mentions-object-allowed-mention-types
    """

    RoleMentions = "roles"
    """Controls role mentions"""
    UserMentions = "users"
    """Controls user mentions"""
    EveryoneMentions = "everyone"
    """Controls @everyone and @here mentions"""


class AttachmentFlag(IntFlag):
    """Attachment Flags

    see https://discord.com/developers/docs/resources/message#attachment-object-attachment-flags
    """

    IS_REMIX = 1 << 2
    """this attachment has been edited using the remix feature on mobile"""


class EmbedTypes(StrEnum):
    """
    Embed types.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-types
    """

    rich = "rich"
    """generic embed rendered from embed attributes"""
    image = "image"
    """image embed"""
    video = "video"
    """video embed"""
    gifv = "gifv"
    """animated gif image embed rendered as a video embed"""
    article = "article"
    """article embed"""
    link = "link"
    """link embed"""
    poll_result = "poll_result"
    """poll result embed"""


class MessageActivityType(IntEnum):
    """Message activity type.

    see https://discord.com/developers/docs/resources/message#message-object-message-activity-types
    """

    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageFlag(IntFlag):
    """Message flags.

    see https://discord.com/developers/docs/resources/message#message-object-message-flags
    """

    CROSSPOSTED = 1 << 0
    """this message has been published to subscribed channels (via Channel Following)"""
    IS_CROSSPOST = 1 << 1
    """this message originated from a message in
    another channel (via Channel Following)"""
    SUPPRESS_EMBEDS = 1 << 2
    """do not include any embeds when serializing this message"""
    SOURCE_MESSAGE_DELETED = 1 << 3
    """the source message for this crosspost has been deleted (via Channel Following)"""
    URGENT = 1 << 4
    """this message came from the urgent message system"""
    HAS_THREAD = 1 << 5
    """this message has an associated thread, with the same id as the message"""
    EPHEMERAL = 1 << 6
    """this message is only visible to the user who invoked the Interaction"""
    LOADING = 1 << 7
    """this message is an Interaction Response and the bot is "thinking" """
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    """this message failed to mention some roles and add their members to the thread"""
    SUPPRESS_NOTIFICATIONS = 1 << 12
    """this message will not trigger push and desktop notifications"""
    IS_VOICE_MESSAGE = 1 << 13
    """this message is a voice message"""


class MessageReferenceType(IntEnum):
    """Message Reference Types

    Determines how associated data is populated.

    see https://discord.com/developers/docs/resources/message#message-reference-types
    """

    DEFAULT = 0
    """A standard reference used by replies.
    Coupled Message Field: `referenced_message`"""
    FORWARD = 1
    """Reference used to point to a message at a point in time.
    Coupled Message Field: `message_snapshot`"""


class MessageType(IntEnum):
    """Type REPLY(19) and CHAT_INPUT_COMMAND(20) are only available in API v8 and above.
    In v6, they are represented as type DEFAULT(0).
    Additionally, type THREAD_STARTER_MESSAGE(21) is only available in API v9 and above.

    see https://discord.com/developers/docs/resources/message#message-object-message-types
    """

    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    USER_JOIN = 7
    GUILD_BOOST = 8
    GUILD_BOOST_TIER_1 = 9
    GUILD_BOOST_TIER_2 = 10
    GUILD_BOOST_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
    AUTO_MODERATION_ACTION = 24
    ROLE_SUBSCRIPTION_PURCHASE = 25
    INTERACTION_PREMIUM_UPSELL = 26
    STAGE_START = 27
    STAGE_END = 28
    STAGE_SPEAKER = 29
    STAGE_TOPIC = 31
    GUILD_APPLICATION_PREMIUM_SUBSCRIPTION = 32
    GUILD_INCIDENT_ALERT_MODE_ENABLED = 36
    GUILD_INCIDENT_ALERT_MODE_DISABLED = 37
    GUILD_INCIDENT_REPORT_RAID = 38
    GUILD_INCIDENT_REPORT_FALSE_ALARM = 39
    PURCHASE_NOTIFICATION = 44
    POLL_RESULT = 46


class ReactionType(IntEnum):
    """Reaction Types

    see https://discord.com/developers/docs/resources/message#get-reactions-reaction-types
    """

    NORMAL = 0
    BURST = 1


class TimeStampStyle(Enum):
    """Timestamp style.

    see https://discord.com/developers/docs/reference#message-formatting-timestamp-styles
    """

    ShortTime = "t"
    """16:20"""
    LongTime = "T"
    """16:20:30"""
    ShortDate = "d"
    """20/04/2021"""
    LongDate = "D"
    """20 April 2021"""
    ShortDateTime = "f"
    """20 April 2021 16:20"""
    LongDateTime = "F"
    """Tuesday, 20 April 2021 16:20"""
    RelativeTime = "R"
    """2 months ago"""


__all__ = [
    "AllowedMentionType",
    "AttachmentFlag",
    "EmbedTypes",
    "MessageActivityType",
    "MessageFlag",
    "MessageReferenceType",
    "MessageType",
    "ReactionType",
    "TimeStampStyle",
]
