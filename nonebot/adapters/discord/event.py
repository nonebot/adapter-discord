from datetime import datetime
from enum import Enum
import inspect
import sys
from types import UnionType
from typing_extensions import override
import warnings

from nonebot.adapters import Event as BaseEvent

from nonebot.compat import PYDANTIC_V2
from nonebot.utils import escape_tag
from pydantic import BaseModel, Field

from .api import model as _model_module
from .api.model import (
    ApplicationCommandPermissions,
    AutoModerationActionExecution,
    AutoModerationRuleCreate,
    AutoModerationRuleDelete,
    AutoModerationRuleUpdate,
    ChannelCreate,
    ChannelDelete,
    ChannelPinsUpdate,
    ChannelUpdate,
    EntitlementCreate,
    EntitlementDelete,
    EntitlementUpdate,
    GuildAuditLogEntryCreate,
    GuildBanAdd,
    GuildBanRemove,
    GuildCreate,
    GuildCreateCompat,
    GuildDelete,
    GuildEmojisUpdate,
    GuildIntegrationsUpdate,
    GuildMemberAdd,
    GuildMemberRemove,
    GuildMembersChunk,
    GuildMemberUpdate,
    GuildRoleCreate,
    GuildRoleDelete,
    GuildRoleUpdate,
    GuildScheduledEventCreate,
    GuildScheduledEventDelete,
    GuildScheduledEventUpdate,
    GuildScheduledEventUserAdd,
    GuildScheduledEventUserRemove,
    GuildStickersUpdate,
    GuildUpdate,
    IntegrationCreate,
    IntegrationDelete,
    IntegrationUpdate,
    InviteCreate,
    MessageGet,
    PresenceUpdate,
    Ready,
    Snowflake,
    StageInstanceCreate,
    StageInstanceDelete,
    StageInstanceUpdate,
    SubscriptionCreate,
    SubscriptionDelete,
    SubscriptionUpdate,
    ThreadCreate,
    ThreadDelete,
    ThreadListSync,
    ThreadMembersUpdate,
    ThreadMemberUpdate,
    ThreadUpdate,
    UserUpdate,
    VoiceChannelEffectSend,
    VoiceChannelStartTimeUpdate,
    VoiceChannelStatusUpdate,
    VoiceServerUpdate,
    VoiceStateUpdate,
    WebhooksUpdate,
)
from .api.models.gateway_events import (
    ApplicationCommandAutoCompleteInteractionCreatePayload,
    ApplicationCommandInteractionCreatePayload,
    DirectMessageCreatePayload,
    DirectMessageDeleteBulkPayload,
    DirectMessageDeletePayload,
    DirectMessagePollVoteAddPayload,
    DirectMessagePollVoteRemovePayload,
    DirectMessageReactionAddPayload,
    DirectMessageReactionRemoveAllPayload,
    DirectMessageReactionRemoveEmojiPayload,
    DirectMessageReactionRemovePayload,
    DirectMessageUpdatePayload,
    DirectTypingStartPayload,
    GuildMessageCreatePayload,
    GuildMessageDeleteBulkPayload,
    GuildMessageDeletePayload,
    GuildMessagePollVoteAddPayload,
    GuildMessagePollVoteRemovePayload,
    GuildMessageReactionAddPayload,
    GuildMessageReactionRemoveAllPayload,
    GuildMessageReactionRemoveEmojiPayload,
    GuildMessageReactionRemovePayload,
    GuildMessageUpdatePayload,
    GuildTypingStartPayload,
    InteractionCreateBasePayload,
    MessageComponentInteractionCreatePayload,
    ModalSubmitInteractionCreatePayload,
    PingInteractionCreatePayload,
)
from .api.types import UNSET, Missing, is_unset
from .message import Message
from .utils import log, model_dump


class EventType(str, Enum):
    """Event Type

    see https://discord.com/developers/docs/topics/gateway-events#receive-events"""

    # Init Event
    HELLO = "HELLO"
    READY = "READY"
    RESUMED = "RESUMED"
    RECONNECT = "RECONNECT"
    INVALID_SESSION = "INVALID_SESSION"

    # APPLICATION
    APPLICATION_COMMAND_PERMISSIONS_UPDATE = "APPLICATION_COMMAND_PERMISSIONS_UPDATE"

    # AUTO MODERATION
    AUTO_MODERATION_RULE_CREATE = "AUTO_MODERATION_RULE_CREATE"
    AUTO_MODERATION_RULE_UPDATE = "AUTO_MODERATION_RULE_UPDATE"
    AUTO_MODERATION_RULE_DELETE = "AUTO_MODERATION_RULE_DELETE"
    AUTO_MODERATION_ACTION_EXECUTION = "AUTO_MODERATION_ACTION_EXECUTION"

    # CHANNELS
    CHANNEL_CREATE = "CHANNEL_CREATE"
    CHANNEL_UPDATE = "CHANNEL_UPDATE"
    CHANNEL_DELETE = "CHANNEL_DELETE"
    CHANNEL_PINS_UPDATE = "CHANNEL_PINS_UPDATE"

    # THREADS
    THREAD_CREATE = "THREAD_CREATE"
    THREAD_UPDATE = "THREAD_UPDATE"
    THREAD_DELETE = "THREAD_DELETE"
    THREAD_LIST_SYNC = "THREAD_LIST_SYNC"
    THREAD_MEMBER_UPDATE = "THREAD_MEMBER_UPDATE"
    THREAD_MEMBERS_UPDATE = "THREAD_MEMBERS_UPDATE"

    # ENTITLEMENTS
    ENTITLEMENT_CREATE = "ENTITLEMENT_CREATE"
    ENTITLEMENT_UPDATE = "ENTITLEMENT_UPDATE"
    ENTITLEMENT_DELETE = "ENTITLEMENT_DELETE"

    # GUILDS
    GUILD_CREATE = "GUILD_CREATE"
    GUILD_CREATE_COMPAT = "GUILD_CREATE_COMPAT"
    GUILD_UPDATE = "GUILD_UPDATE"
    GUILD_DELETE = "GUILD_DELETE"
    GUILD_AUDIT_LOG_ENTRY_CREATE = "GUILD_AUDIT_LOG_ENTRY_CREATE"
    GUILD_BAN_ADD = "GUILD_BAN_ADD"
    GUILD_BAN_REMOVE = "GUILD_BAN_REMOVE"
    GUILD_EMOJIS_UPDATE = "GUILD_EMOJIS_UPDATE"
    GUILD_STICKERS_UPDATE = "GUILD_STICKERS_UPDATE"
    GUILD_INTEGRATIONS_UPDATE = "GUILD_INTEGRATIONS_UPDATE"

    # GUILD_MEMBERS
    GUILD_MEMBER_ADD = "GUILD_MEMBER_ADD"
    GUILD_MEMBER_UPDATE = "GUILD_MEMBER_UPDATE"
    GUILD_MEMBER_REMOVE = "GUILD_MEMBER_REMOVE"
    GUILD_MEMBERS_CHUNK = "GUILD_MEMBERS_CHUNK"

    # GUILD_ROLE
    GUILD_ROLE_CREATE = "GUILD_ROLE_CREATE"
    GUILD_ROLE_UPDATE = "GUILD_ROLE_UPDATE"
    GUILD_ROLE_DELETE = "GUILD_ROLE_DELETE"

    # GUILD_SCHEDULED_EVENT
    GUILD_SCHEDULED_EVENT_CREATE = "GUILD_SCHEDULED_EVENT_CREATE"
    GUILD_SCHEDULED_EVENT_UPDATE = "GUILD_SCHEDULED_EVENT_UPDATE"
    GUILD_SCHEDULED_EVENT_DELETE = "GUILD_SCHEDULED_EVENT_DELETE"
    GUILD_SCHEDULED_EVENT_USER_ADD = "GUILD_SCHEDULED_EVENT_USER_ADD"
    GUILD_SCHEDULED_EVENT_USER_REMOVE = "GUILD_SCHEDULED_EVENT_USER_REMOVE"

    # INTEGRATION
    INTEGRATION_CREATE = "INTEGRATION_CREATE"
    INTEGRATION_UPDATE = "INTEGRATION_UPDATE"
    INTEGRATION_DELETE = "INTEGRATION_DELETE"
    INTERACTION_CREATE = "INTERACTION_CREATE"

    # INVITE
    INVITE_CREATE = "INVITE_CREATE"
    INVITE_DELETE = "INVITE_DELETE"

    # MESSAGE
    MESSAGE_CREATE = "MESSAGE_CREATE"
    MESSAGE_UPDATE = "MESSAGE_UPDATE"
    MESSAGE_DELETE = "MESSAGE_DELETE"
    MESSAGE_DELETE_BULK = "MESSAGE_DELETE_BULK"

    # MESSAGE_REACTION
    MESSAGE_REACTION_ADD = "MESSAGE_REACTION_ADD"
    MESSAGE_REACTION_REMOVE = "MESSAGE_REACTION_REMOVE"
    MESSAGE_REACTION_REMOVE_ALL = "MESSAGE_REACTION_REMOVE_ALL"
    MESSAGE_REACTION_REMOVE_EMOJI = "MESSAGE_REACTION_REMOVE_EMOJI"

    # PRESENCE
    PRESENCE_UPDATE = "PRESENCE_UPDATE"

    # STAGE_INSTANCE
    STAGE_INSTANCE_CREATE = "STAGE_INSTANCE_CREATE"
    STAGE_INSTANCE_UPDATE = "STAGE_INSTANCE_UPDATE"
    STAGE_INSTANCE_DELETE = "STAGE_INSTANCE_DELETE"

    # SUBSCRIPTION
    SUBSCRIPTION_CREATE = "SUBSCRIPTION_CREATE"
    SUBSCRIPTION_UPDATE = "SUBSCRIPTION_UPDATE"
    SUBSCRIPTION_DELETE = "SUBSCRIPTION_DELETE"

    # TYPING
    TYPING_START = "TYPING_START"

    # USER
    USER_UPDATE = "USER_UPDATE"

    # VOICE
    VOICE_CHANNEL_STATUS_UPDATE = "VOICE_CHANNEL_STATUS_UPDATE"
    VOICE_CHANNEL_START_TIME_UPDATE = "VOICE_CHANNEL_START_TIME_UPDATE"
    VOICE_CHANNEL_EFFECT_SEND = "VOICE_CHANNEL_EFFECT_SEND"
    VOICE_STATE_UPDATE = "VOICE_STATE_UPDATE"
    VOICE_SERVER_UPDATE = "VOICE_SERVER_UPDATE"

    # WEBHOOKS
    WEBHOOKS_UPDATE = "WEBHOOKS_UPDATE"

    # POLL
    MESSAGE_POLL_VOTE_ADD = "MESSAGE_POLL_VOTE_ADD"
    MESSAGE_POLL_VOTE_REMOVE = "MESSAGE_POLL_VOTE_REMOVE"


class Event(BaseEvent):
    """Event"""

    __type__: EventType
    timestamp__: datetime = Field(default_factory=datetime.now)

    @property
    def time(self) -> datetime:
        return self.timestamp__

    def __getattr__(self, name: str) -> datetime:
        if name == "timestamp":
            warnings.warn(
                "Event.timestamp is deprecated, use Event.time",
                DeprecationWarning,
                stacklevel=2,
            )
            return self.timestamp__
        return super().__getattribute__(name)

    @override
    def get_event_name(self) -> str:
        return self.__class__.__name__

    @override
    def get_event_description(self) -> str:
        return escape_tag(str(model_dump(self, omit_unset_values=True)))

    @override
    def get_message(self) -> Message:
        msg = "Event has no message!"
        raise ValueError(msg)

    @override
    def get_user_id(self) -> str:
        msg = "Event has no context!"
        raise ValueError(msg)

    @override
    def get_session_id(self) -> str:
        msg = "Event has no context!"
        raise ValueError(msg)

    @override
    def is_tome(self) -> bool:
        return False


class MetaEvent(Event):
    """Meta event"""

    @override
    def get_type(self) -> str:
        return "meta_event"


class NoticeEvent(Event):
    """Notice event"""

    @override
    def get_type(self) -> str:
        return "notice"


class RequestEvent(Event):
    """Request event"""

    @override
    def get_type(self) -> str:
        return "request"


class MessageEvent(Event, MessageGet):
    """Message event"""

    to_me: bool = False

    reply: MessageGet | None = None

    @property
    def message(self) -> Message:
        return self.get_message()

    @property
    def original_message(self) -> Message:
        return (
            original_message
            if isinstance(
                (original_message := getattr(self, "_original_message", None)), Message
            )
            else self.get_message()
        )

    @override
    def get_type(self) -> str:
        return "message"

    @staticmethod
    def _format_preview(content: str, max_length: int = 120) -> str:
        normalized = content.replace("\r\n", "\n").replace("\r", "\n")
        normalized = normalized.replace("\n", "\\n").strip()
        if not normalized:
            return "<empty>"
        if len(normalized) > max_length:
            return normalized[: max_length - 3] + "..."
        return normalized

    @override
    def get_event_description(self) -> str:
        guild_id = getattr(self, "guild_id", UNSET)
        location = (
            f"Guild {guild_id}, Channel {self.channel_id}"
            if not is_unset(guild_id)
            else f"Channel {self.channel_id}"
        )
        preview = self._format_preview(
            self.get_message().extract_content() or self.content
        )
        return escape_tag(
            f"Message {self.id} from {self.author.id}({self.author.username})"
            f"@[{location}] {preview}"
        )

    @override
    def get_user_id(self) -> str:
        return str(self.author.id)

    @override
    def get_session_id(self) -> str:
        return str(self.author.id)

    @override
    def get_message(self) -> Message:
        if not hasattr(self, "_message"):
            self._message = Message.from_guild_message(self)
            self._original_message = Message.from_guild_message(self)
        return self._message

    @override
    def is_tome(self) -> bool:
        return self.to_me

    @property
    def user_id(self) -> Snowflake:
        return self.author.id

    @property
    def message_id(self) -> Snowflake:
        return self.id


class HelloEvent(MetaEvent):
    """Hello event

    see https://discord.com/developers/docs/topics/gateway#hello"""

    __type__ = EventType.HELLO

    heartbeat_interval: int


class ReadyEvent(MetaEvent, Ready):
    """Ready event

    see https://discord.com/developers/docs/topics/gateway-events#ready"""

    __type__ = EventType.READY


class ResumedEvent(MetaEvent):
    """Resumed event

    see https://discord.com/developers/docs/topics/gateway-events#resumed"""

    __type__ = EventType.RESUMED


class ReconnectEvent(MetaEvent):
    """Reconnect event

    see https://discord.com/developers/docs/topics/gateway-events#reconnect"""

    __type__ = EventType.RECONNECT


class InvalidSessionEvent(MetaEvent):
    """Invalid session event

    see https://discord.com/developers/docs/topics/gateway-events#invalid-session"""

    __type__ = EventType.INVALID_SESSION


class ApplicationCommandPermissionsUpdateEvent(NoticeEvent):
    """Application command create event

    see https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object
    """

    __type__ = EventType.APPLICATION_COMMAND_PERMISSIONS_UPDATE
    id: Snowflake
    application_id: Snowflake
    guild_id: Snowflake
    permissions: list[ApplicationCommandPermissions]


class AutoModerationEvent(NoticeEvent):
    """Auto Moderation event"""


class AutoModerationRuleCreateEvent(AutoModerationEvent, AutoModerationRuleCreate):
    """Automation update event

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-create
    """

    __type__ = EventType.AUTO_MODERATION_RULE_CREATE


class AutoModerationRuleUpdateEvent(AutoModerationEvent, AutoModerationRuleUpdate):
    """Automation update event

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-update
    """

    __type__ = EventType.AUTO_MODERATION_RULE_UPDATE


class AutoModerationRuleDeleteEvent(AutoModerationEvent, AutoModerationRuleDelete):
    """Automation update event

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-rule-delete
    """

    __type__ = EventType.AUTO_MODERATION_RULE_DELETE


class AutoModerationActionExecutionEvent(
    AutoModerationEvent, AutoModerationActionExecution
):
    """Automation update event

    see https://discord.com/developers/docs/topics/gateway-events#auto-moderation-action-execution
    """

    __type__ = EventType.AUTO_MODERATION_ACTION_EXECUTION


class ChannelEvent(NoticeEvent):
    """Channel event

    see https://discord.com/developers/docs/topics/gateway-events#channels"""


class ChannelCreateEvent(ChannelEvent, ChannelCreate):
    """Channel create event

    see https://discord.com/developers/docs/topics/gateway-events#channel-create"""

    __type__ = EventType.CHANNEL_CREATE


class ChannelUpdateEvent(ChannelEvent, ChannelUpdate):
    """Channel update event

    see https://discord.com/developers/docs/topics/gateway-events#channel-update"""

    __type__ = EventType.CHANNEL_UPDATE


class ChannelDeleteEvent(ChannelEvent, ChannelDelete):
    """Channel delete event

    see https://discord.com/developers/docs/topics/gateway-events#channel-delete"""

    __type__ = EventType.CHANNEL_DELETE


class ChannelPinsUpdateEvent(ChannelEvent, ChannelPinsUpdate):
    """Channel pins update event

    see https://discord.com/developers/docs/topics/gateway-events#channel-pins-update"""

    __type__ = EventType.CHANNEL_PINS_UPDATE


class ThreadEvent(NoticeEvent):
    """Thread event"""


class ThreadCreateEvent(ThreadEvent, ThreadCreate):
    """Thread create event

    see https://discord.com/developers/docs/topics/gateway-events#thread-create"""

    __type__ = EventType.THREAD_CREATE


class ThreadUpdateEvent(ThreadEvent, ThreadUpdate):
    """Thread update event

    see https://discord.com/developers/docs/topics/gateway-events#thread-update"""

    __type__ = EventType.THREAD_UPDATE


class ThreadDeleteEvent(ThreadEvent, ThreadDelete):
    """Thread delete event

    see https://discord.com/developers/docs/topics/gateway-events#thread-delete"""

    __type__ = EventType.THREAD_DELETE


class ThreadListSyncEvent(ThreadEvent, ThreadListSync):
    """Thread list sync event

    see https://discord.com/developers/docs/topics/gateway-events#thread-list-sync"""

    __type__ = EventType.THREAD_LIST_SYNC


class ThreadMemberUpdateEvent(ThreadEvent, ThreadMemberUpdate):
    __type__ = EventType.THREAD_MEMBER_UPDATE


class ThreadMembersUpdateEvent(ThreadEvent, ThreadMembersUpdate):
    __type__ = EventType.THREAD_MEMBERS_UPDATE


class EntitlementEvent(NoticeEvent):
    """Entitlement event

    see https://discord.com/developers/docs/topics/gateway-events#entitlements"""


class EntitlementCreateEvent(EntitlementEvent, EntitlementCreate):
    """Entitlement create event

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-create"""

    __type__ = EventType.ENTITLEMENT_CREATE


class EntitlementUpdateEvent(EntitlementEvent, EntitlementUpdate):
    """Entitlement update event

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-update"""

    __type__ = EventType.ENTITLEMENT_UPDATE


class EntitlementDeleteEvent(EntitlementEvent, EntitlementDelete):
    """Entitlement delete event

    see https://discord.com/developers/docs/topics/gateway-events#entitlement-delete"""

    __type__ = EventType.ENTITLEMENT_DELETE


class GuildEvent(NoticeEvent):
    """Guild event

    see https://discord.com/developers/docs/topics/gateway-events#guilds"""


class GuildCreateEvent(GuildEvent, GuildCreate):
    """Guild create event

    see https://discord.com/developers/docs/topics/gateway-events#guild-create"""

    __type__ = EventType.GUILD_CREATE


class GuildCreateCompatEvent(GuildEvent, GuildCreateCompat):
    __type__ = EventType.GUILD_CREATE_COMPAT

    def __init__(self, **data) -> None:  # noqa: ANN003
        super().__init__(**data)
        log(
            "WARNING",
            "Detected mixed-format GUILD_CREATE payload; "
            "parsing as GuildCreateCompatEvent",
        )


class GuildUpdateEvent(GuildEvent, GuildUpdate):
    """Guild update event

    see https://discord.com/developers/docs/topics/gateway-events#guild-update"""

    __type__ = EventType.GUILD_UPDATE


class GuildDeleteEvent(GuildEvent, GuildDelete):
    """Guild delete event

    see https://discord.com/developers/docs/topics/gateway-events#guild-delete"""

    __type__ = EventType.GUILD_DELETE


class GuildAuditLogEntryCreateEvent(GuildEvent, GuildAuditLogEntryCreate):
    """Guild audit log entry create event

    see https://discord.com/developers/docs/topics/gateway-events#guild-audit-log-entry-create
    """

    __type__ = EventType.GUILD_AUDIT_LOG_ENTRY_CREATE


class GuildBanAddEvent(GuildEvent, GuildBanAdd):
    """Guild ban add event

    see https://discord.com/developers/docs/topics/gateway-events#guild-ban-add"""

    __type__ = EventType.GUILD_BAN_ADD


class GuildBanRemoveEvent(GuildEvent, GuildBanRemove):
    """Guild ban remove event

    see https://discord.com/developers/docs/topics/gateway-events#guild-ban-remove"""

    __type__ = EventType.GUILD_BAN_REMOVE


class GuildEmojisUpdateEvent(GuildEvent, GuildEmojisUpdate):
    """Guild emojis update event

    see https://discord.com/developers/docs/topics/gateway-events#guild-emojis-update"""

    __type__ = EventType.GUILD_EMOJIS_UPDATE


class GuildStickersUpdateEvent(GuildEvent, GuildStickersUpdate):
    """Guild stickers update event

    see https://discord.com/developers/docs/topics/gateway-events#guild-stickers-update
    """

    __type__ = EventType.GUILD_STICKERS_UPDATE


class GuildIntegrationsUpdateEvent(GuildEvent, GuildIntegrationsUpdate):
    """Guild integrations update event

    see https://discord.com/developers/docs/topics/gateway-events#guild-integrations-update
    """

    __type__ = EventType.GUILD_INTEGRATIONS_UPDATE


class GuildMemberAddEvent(GuildEvent, GuildMemberAdd):
    """Guild member add event

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-add"""

    __type__ = EventType.GUILD_MEMBER_ADD


class GuildMemberRemoveEvent(GuildEvent, GuildMemberRemove):
    """Guild member remove event

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-remove"""

    __type__ = EventType.GUILD_MEMBER_REMOVE


class GuildMemberUpdateEvent(GuildEvent, GuildMemberUpdate):
    """Guild member update event

    see https://discord.com/developers/docs/topics/gateway-events#guild-member-update"""

    __type__ = EventType.GUILD_MEMBER_UPDATE


class GuildMembersChunkEvent(GuildEvent, GuildMembersChunk):
    """Guild members chunk event

    see https://discord.com/developers/docs/topics/gateway-events#guild-members-chunk"""

    __type__ = EventType.GUILD_MEMBERS_CHUNK


class GuildRoleCreateEvent(GuildEvent, GuildRoleCreate):
    """Guild role create event

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-create"""

    __type__ = EventType.GUILD_ROLE_CREATE


class GuildRoleUpdateEvent(GuildEvent, GuildRoleUpdate):
    """Guild role update event

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-update"""

    __type__ = EventType.GUILD_ROLE_UPDATE


class GuildRoleDeleteEvent(GuildEvent, GuildRoleDelete):
    """Guild role delete event

    see https://discord.com/developers/docs/topics/gateway-events#guild-role-delete"""

    __type__ = EventType.GUILD_ROLE_DELETE


class GuildScheduledEventCreateEvent(GuildEvent, GuildScheduledEventCreate):
    """Guild scheduled event create event

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-create
    """

    __type__ = EventType.GUILD_SCHEDULED_EVENT_CREATE


class GuildScheduledEventUpdateEvent(GuildEvent, GuildScheduledEventUpdate):
    """Guild scheduled event update event

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-update
    """

    __type__ = EventType.GUILD_SCHEDULED_EVENT_UPDATE


class GuildScheduledEventDeleteEvent(GuildEvent, GuildScheduledEventDelete):
    """Guild scheduled event delete event

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-delete
    """

    __type__ = EventType.GUILD_SCHEDULED_EVENT_DELETE


class GuildScheduledEventUserAddEvent(GuildEvent, GuildScheduledEventUserAdd):
    """Guild scheduled event user add event

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-add
    """

    __type__ = EventType.GUILD_SCHEDULED_EVENT_USER_ADD


class GuildScheduledEventUserRemoveEvent(GuildEvent, GuildScheduledEventUserRemove):
    """Guild scheduled event user remove event

    see https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-remove
    """

    __type__ = EventType.GUILD_SCHEDULED_EVENT_USER_REMOVE


class IntegrationEvent(NoticeEvent):
    """Integration event"""


class IntegrationCreateEvent(IntegrationEvent, IntegrationCreate):
    """Integration create event

    see https://discord.com/developers/docs/topics/gateway-events#integration-create"""

    __type__ = EventType.INTEGRATION_CREATE


class IntegrationUpdateEvent(IntegrationEvent, IntegrationUpdate):
    """Integration update event

    see https://discord.com/developers/docs/topics/gateway-events#integration-update"""

    __type__ = EventType.INTEGRATION_UPDATE


class IntegrationDeleteEvent(IntegrationEvent, IntegrationDelete):
    """Integration delete event

    see https://discord.com/developers/docs/topics/gateway-events#integration-delete"""

    __type__ = EventType.INTEGRATION_DELETE


class InteractionCreateEvent(NoticeEvent, InteractionCreateBasePayload):
    __type__ = EventType.INTERACTION_CREATE

    @override
    def get_user_id(self) -> str:
        if not is_unset(self.user):
            return str(self.user.id)
        if not is_unset(self.member) and not is_unset(self.member.user):
            return str(self.member.user.id)
        msg = "Event has no context!"
        raise ValueError(msg)


class PingInteractionEvent(InteractionCreateEvent, PingInteractionCreatePayload): ...


class ApplicationCommandInteractionEvent(
    InteractionCreateEvent, ApplicationCommandInteractionCreatePayload
): ...


class ApplicationCommandAutoCompleteInteractionEvent(
    InteractionCreateEvent, ApplicationCommandAutoCompleteInteractionCreatePayload
): ...


class MessageComponentInteractionEvent(
    InteractionCreateEvent, MessageComponentInteractionCreatePayload
): ...


class ModalSubmitInteractionEvent(
    InteractionCreateEvent, ModalSubmitInteractionCreatePayload
): ...


class InviteCreateEvent(NoticeEvent, InviteCreate):
    """Invite create event

    see https://discord.com/developers/docs/topics/gateway-events#invite-create"""

    __type__ = EventType.INVITE_CREATE


class InviteDeleteEvent(NoticeEvent):
    """Invite delete event

    see https://discord.com/developers/docs/topics/gateway-events#invite-delete"""

    __type__ = EventType.INVITE_DELETE
    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    code: str


class MessageCreateEvent(MessageEvent):
    """Message Create Event

    see https://discord.com/developers/docs/topics/gateway-events#message-create
    """

    __type__ = EventType.MESSAGE_CREATE


class GuildMessageCreateEvent(MessageCreateEvent, GuildMessageCreatePayload): ...


class DirectMessageCreateEvent(MessageCreateEvent, DirectMessageCreatePayload):
    to_me: bool = True


class MessageUpdateEvent(NoticeEvent):
    """Message Update Event

    see https://discord.com/developers/docs/topics/gateway-events#message-update
    """

    __type__ = EventType.MESSAGE_UPDATE


class GuildMessageUpdateEvent(MessageUpdateEvent, GuildMessageUpdatePayload): ...


class DirectMessageUpdateEvent(MessageUpdateEvent, DirectMessageUpdatePayload): ...


class MessageDeleteEvent(NoticeEvent):
    """Message Delete Event

    see https://discord.com/developers/docs/topics/gateway-events#message-delete
    """

    __type__ = EventType.MESSAGE_DELETE


class GuildMessageDeleteEvent(MessageDeleteEvent, GuildMessageDeletePayload): ...


class DirectMessageDeleteEvent(MessageDeleteEvent, DirectMessageDeletePayload): ...


class MessageDeleteBulkEvent(NoticeEvent):
    """Message Delete Bulk Event

    see https://discord.com/developers/docs/topics/gateway-events#message-delete-bulk
    """

    __type__ = EventType.MESSAGE_DELETE_BULK


class GuildMessageDeleteBulkEvent(
    MessageDeleteBulkEvent, GuildMessageDeleteBulkPayload
): ...


class DirectMessageDeleteBulkEvent(
    MessageDeleteBulkEvent, DirectMessageDeleteBulkPayload
): ...


class MessageReactionAddEvent(NoticeEvent):
    """
    Message Reaction Add Event

    see https://discord.com/developers/docs/topics/gateway#message-reaction-add
    """

    __type__ = EventType.MESSAGE_REACTION_ADD


class GuildMessageReactionAddEvent(
    MessageReactionAddEvent, GuildMessageReactionAddPayload
): ...


class DirectMessageReactionAddEvent(
    MessageReactionAddEvent, DirectMessageReactionAddPayload
): ...


class MessageReactionRemoveEvent(NoticeEvent):
    """Message Reaction Remove Event

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove
    """

    __type__ = EventType.MESSAGE_REACTION_REMOVE


class GuildMessageReactionRemoveEvent(
    MessageReactionRemoveEvent, GuildMessageReactionRemovePayload
): ...


class DirectMessageReactionRemoveEvent(
    MessageReactionRemoveEvent, DirectMessageReactionRemovePayload
): ...


class MessageReactionRemoveAllEvent(NoticeEvent):
    """Message Reaction Remove All Event

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-all
    """

    __type__ = EventType.MESSAGE_REACTION_REMOVE_ALL


class GuildMessageReactionRemoveAllEvent(
    MessageReactionRemoveAllEvent, GuildMessageReactionRemoveAllPayload
): ...


class DirectMessageReactionRemoveAllEvent(
    MessageReactionRemoveAllEvent, DirectMessageReactionRemoveAllPayload
): ...


class MessageReactionRemoveEmojiEvent(NoticeEvent):
    """Message Reaction Remove Emoji Event

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-emoji
    """

    __type__ = EventType.MESSAGE_REACTION_REMOVE_EMOJI


class GuildMessageReactionRemoveEmojiEvent(
    MessageReactionRemoveEmojiEvent, GuildMessageReactionRemoveEmojiPayload
): ...


class DirectMessageReactionRemoveEmojiEvent(
    MessageReactionRemoveEmojiEvent, DirectMessageReactionRemoveEmojiPayload
): ...


class PresenceUpdateEvent(NoticeEvent, PresenceUpdate):
    """Presence Update Event

    see https://discord.com/developers/docs/topics/gateway-events#presence-update
    """

    __type__ = EventType.PRESENCE_UPDATE


class StageInstanceCreateEvent(GuildEvent, StageInstanceCreate):
    """Stage instance create event

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-create
    """

    __type__ = EventType.STAGE_INSTANCE_CREATE


class StageInstanceUpdateEvent(GuildEvent, StageInstanceUpdate):
    """Stage instance update event

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-update
    """

    __type__ = EventType.STAGE_INSTANCE_UPDATE


class StageInstanceDeleteEvent(GuildEvent, StageInstanceDelete):
    """Stage instance delete event

    see https://discord.com/developers/docs/topics/gateway-events#stage-instance-delete
    """

    __type__ = EventType.STAGE_INSTANCE_DELETE


class SubscriptionEvent(NoticeEvent):
    """Subscription event

    see https://discord.com/developers/docs/topics/gateway-events#subscriptions"""


class SubscriptionCreateEvent(SubscriptionEvent, SubscriptionCreate):
    """Subscription create event

    see https://discord.com/developers/docs/topics/gateway-events#subscription-create"""

    __type__ = EventType.SUBSCRIPTION_CREATE


class SubscriptionUpdateEvent(SubscriptionEvent, SubscriptionUpdate):
    """Subscription Update event

    see https://discord.com/developers/docs/topics/gateway-events#subscription-update"""

    __type__ = EventType.SUBSCRIPTION_UPDATE


class SubscriptionDeleteEvent(SubscriptionEvent, SubscriptionDelete):
    """Subscription delete event

    see https://discord.com/developers/docs/topics/gateway-events#subscription-delete"""

    __type__ = EventType.SUBSCRIPTION_DELETE


class TypingStartEvent(NoticeEvent):
    """Typing Start Event

    see https://discord.com/developers/docs/topics/gateway-events#typing-start
    """

    __type__ = EventType.TYPING_START


class GuildTypingStartEvent(TypingStartEvent, GuildTypingStartPayload): ...


class DirectTypingStartEvent(TypingStartEvent, DirectTypingStartPayload): ...


class UserUpdateEvent(NoticeEvent, UserUpdate):
    """User Update Event

    see https://discord.com/developers/docs/topics/gateway-events#user-update
    """

    __type__ = EventType.USER_UPDATE


class VoiceChannelEffectSendEvent(NoticeEvent, VoiceChannelEffectSend):
    """Voice Channel Effect Send Event

    see https://discord.com/developers/docs/topics/gateway-events#voice-channel-effect-send
    """

    __type__ = EventType.VOICE_CHANNEL_EFFECT_SEND


class VoiceChannelStatusUpdateEvent(NoticeEvent, VoiceChannelStatusUpdate):
    """Voice Channel Status Update Event

    This dispatch exists in practice but is not fully documented in the
    official Discord Gateway Events page yet.
    """

    __type__ = EventType.VOICE_CHANNEL_STATUS_UPDATE


class VoiceChannelStartTimeUpdateEvent(NoticeEvent, VoiceChannelStartTimeUpdate):
    """Voice Channel Start Time Update Event

    This dispatch exists in practice but is not fully documented in the
    official Discord Gateway Events page yet.
    """

    __type__ = EventType.VOICE_CHANNEL_START_TIME_UPDATE


class VoiceStateUpdateEvent(NoticeEvent, VoiceStateUpdate):
    """Voice State Update Event

    see https://discord.com/developers/docs/topics/gateway-events#voice-state-update
    """

    __type__ = EventType.VOICE_STATE_UPDATE


class VoiceServerUpdateEvent(NoticeEvent, VoiceServerUpdate):
    """Voice Server Update Event

    see https://discord.com/developers/docs/topics/gateway-events#voice-server-update
    """

    __type__ = EventType.VOICE_SERVER_UPDATE


class WebhooksUpdateEvent(NoticeEvent, WebhooksUpdate):
    """Webhooks Update Event

    see https://discord.com/developers/docs/topics/gateway-events#webhooks-update
    """

    __type__ = EventType.WEBHOOKS_UPDATE


class MessagePollVoteAddEvent(NoticeEvent):
    """Message Poll Vote Add Event

    see https://discord.com/developers/docs/topics/gateway-events#message-poll-vote-add
    """

    __type__ = EventType.MESSAGE_POLL_VOTE_ADD


class GuildMessagePollVoteAddEvent(
    MessagePollVoteAddEvent, GuildMessagePollVoteAddPayload
): ...


class DirectMessagePollVoteAddEvent(
    MessagePollVoteAddEvent, DirectMessagePollVoteAddPayload
): ...


class MessagePollVoteRemoveEvent(NoticeEvent):
    """Message Poll Vote Remove Event

    see https://discord.com/developers/docs/topics/gateway-events#message-poll-vote-remove
    """

    __type__ = EventType.MESSAGE_POLL_VOTE_REMOVE


class GuildMessagePollVoteRemoveEvent(
    MessagePollVoteRemoveEvent, GuildMessagePollVoteRemovePayload
): ...


class DirectMessagePollVoteRemoveEvent(
    MessagePollVoteRemoveEvent, DirectMessagePollVoteRemovePayload
): ...


event_classes: dict[str, type[Event] | UnionType] = {
    EventType.HELLO.value: HelloEvent,
    EventType.READY.value: ReadyEvent,
    EventType.RESUMED.value: ResumedEvent,
    EventType.RECONNECT.value: ReconnectEvent,
    EventType.INVALID_SESSION.value: InvalidSessionEvent,
    EventType.APPLICATION_COMMAND_PERMISSIONS_UPDATE.value: (
        ApplicationCommandPermissionsUpdateEvent
    ),
    EventType.AUTO_MODERATION_RULE_CREATE.value: AutoModerationRuleCreateEvent,
    EventType.AUTO_MODERATION_RULE_UPDATE.value: AutoModerationRuleUpdateEvent,
    EventType.AUTO_MODERATION_RULE_DELETE.value: AutoModerationRuleDeleteEvent,
    EventType.AUTO_MODERATION_ACTION_EXECUTION.value: (
        AutoModerationActionExecutionEvent
    ),
    EventType.CHANNEL_CREATE.value: ChannelCreateEvent,
    EventType.CHANNEL_UPDATE.value: ChannelUpdateEvent,
    EventType.CHANNEL_DELETE.value: ChannelDeleteEvent,
    EventType.CHANNEL_PINS_UPDATE.value: ChannelPinsUpdateEvent,
    EventType.THREAD_CREATE.value: ThreadCreateEvent,
    EventType.THREAD_UPDATE.value: ThreadUpdateEvent,
    EventType.THREAD_DELETE.value: ThreadDeleteEvent,
    EventType.THREAD_LIST_SYNC.value: ThreadListSyncEvent,
    EventType.THREAD_MEMBER_UPDATE.value: ThreadMemberUpdateEvent,
    EventType.THREAD_MEMBERS_UPDATE.value: ThreadMembersUpdateEvent,
    EventType.ENTITLEMENT_CREATE.value: EntitlementCreateEvent,
    EventType.ENTITLEMENT_UPDATE.value: EntitlementUpdateEvent,
    EventType.ENTITLEMENT_DELETE.value: EntitlementDeleteEvent,
    EventType.GUILD_CREATE.value: GuildCreateEvent | GuildCreateCompatEvent,
    EventType.GUILD_UPDATE.value: GuildUpdateEvent,
    EventType.GUILD_DELETE.value: GuildDeleteEvent,
    EventType.GUILD_AUDIT_LOG_ENTRY_CREATE.value: GuildAuditLogEntryCreateEvent,
    EventType.GUILD_BAN_ADD.value: GuildBanAddEvent,
    EventType.GUILD_BAN_REMOVE.value: GuildBanRemoveEvent,
    EventType.GUILD_EMOJIS_UPDATE.value: GuildEmojisUpdateEvent,
    EventType.GUILD_STICKERS_UPDATE.value: GuildStickersUpdateEvent,
    EventType.GUILD_INTEGRATIONS_UPDATE.value: GuildIntegrationsUpdateEvent,
    EventType.GUILD_MEMBER_ADD.value: GuildMemberAddEvent,
    EventType.GUILD_MEMBER_REMOVE.value: GuildMemberRemoveEvent,
    EventType.GUILD_MEMBER_UPDATE.value: GuildMemberUpdateEvent,
    EventType.GUILD_MEMBERS_CHUNK.value: GuildMembersChunkEvent,
    EventType.GUILD_ROLE_CREATE.value: GuildRoleCreateEvent,
    EventType.GUILD_ROLE_UPDATE.value: GuildRoleUpdateEvent,
    EventType.GUILD_ROLE_DELETE.value: GuildRoleDeleteEvent,
    EventType.GUILD_SCHEDULED_EVENT_CREATE.value: GuildScheduledEventCreateEvent,
    EventType.GUILD_SCHEDULED_EVENT_UPDATE.value: GuildScheduledEventUpdateEvent,
    EventType.GUILD_SCHEDULED_EVENT_DELETE.value: GuildScheduledEventDeleteEvent,
    EventType.GUILD_SCHEDULED_EVENT_USER_ADD.value: GuildScheduledEventUserAddEvent,
    EventType.GUILD_SCHEDULED_EVENT_USER_REMOVE.value: (
        GuildScheduledEventUserRemoveEvent
    ),
    EventType.INTEGRATION_CREATE.value: IntegrationCreateEvent,
    EventType.INTEGRATION_UPDATE.value: IntegrationUpdateEvent,
    EventType.INTEGRATION_DELETE.value: IntegrationDeleteEvent,
    EventType.INTERACTION_CREATE.value: (
        PingInteractionEvent
        | ApplicationCommandInteractionEvent
        | ApplicationCommandAutoCompleteInteractionEvent
        | MessageComponentInteractionEvent
        | ModalSubmitInteractionEvent
    ),
    EventType.INVITE_CREATE.value: InviteCreateEvent,
    EventType.INVITE_DELETE.value: InviteDeleteEvent,
    EventType.MESSAGE_CREATE.value: (
        GuildMessageCreateEvent | DirectMessageCreateEvent
    ),
    EventType.MESSAGE_UPDATE.value: (
        GuildMessageUpdateEvent | DirectMessageUpdateEvent
    ),
    EventType.MESSAGE_DELETE.value: (
        GuildMessageDeleteEvent | DirectMessageDeleteEvent
    ),
    EventType.MESSAGE_DELETE_BULK.value: (
        GuildMessageDeleteBulkEvent | DirectMessageDeleteBulkEvent
    ),
    EventType.MESSAGE_REACTION_ADD.value: (
        GuildMessageReactionAddEvent | DirectMessageReactionAddEvent
    ),
    EventType.MESSAGE_REACTION_REMOVE.value: (
        GuildMessageReactionRemoveEvent | DirectMessageReactionRemoveEvent
    ),
    EventType.MESSAGE_REACTION_REMOVE_ALL.value: (
        GuildMessageReactionRemoveAllEvent | DirectMessageReactionRemoveAllEvent
    ),
    EventType.MESSAGE_REACTION_REMOVE_EMOJI.value: (
        GuildMessageReactionRemoveEmojiEvent | DirectMessageReactionRemoveEmojiEvent
    ),
    EventType.PRESENCE_UPDATE.value: PresenceUpdateEvent,
    EventType.STAGE_INSTANCE_CREATE.value: StageInstanceCreateEvent,
    EventType.STAGE_INSTANCE_UPDATE.value: StageInstanceUpdateEvent,
    EventType.STAGE_INSTANCE_DELETE.value: StageInstanceDeleteEvent,
    EventType.SUBSCRIPTION_CREATE.value: SubscriptionCreateEvent,
    EventType.SUBSCRIPTION_UPDATE.value: SubscriptionUpdateEvent,
    EventType.SUBSCRIPTION_DELETE.value: SubscriptionDeleteEvent,
    EventType.TYPING_START.value: GuildTypingStartEvent | DirectTypingStartEvent,
    EventType.USER_UPDATE.value: UserUpdateEvent,
    EventType.VOICE_CHANNEL_STATUS_UPDATE.value: VoiceChannelStatusUpdateEvent,
    EventType.VOICE_CHANNEL_START_TIME_UPDATE.value: VoiceChannelStartTimeUpdateEvent,
    EventType.VOICE_CHANNEL_EFFECT_SEND.value: VoiceChannelEffectSendEvent,
    EventType.VOICE_STATE_UPDATE.value: VoiceStateUpdateEvent,
    EventType.VOICE_SERVER_UPDATE.value: VoiceServerUpdateEvent,
    EventType.WEBHOOKS_UPDATE.value: WebhooksUpdateEvent,
    EventType.MESSAGE_POLL_VOTE_ADD.value: (
        GuildMessagePollVoteAddEvent | DirectMessagePollVoteAddEvent
    ),
    EventType.MESSAGE_POLL_VOTE_REMOVE.value: (
        GuildMessagePollVoteRemoveEvent | DirectMessagePollVoteRemoveEvent
    ),
}

_model_types_namespace = vars(_model_module)

for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
    if issubclass(obj, BaseModel) and obj.__module__ == __name__:
        if PYDANTIC_V2:
            obj.model_rebuild(_types_namespace=_model_types_namespace)
        else:
            obj.update_forward_refs(
                **{
                    k: v
                    for k, v in _model_types_namespace.items()
                    if isinstance(v, type)
                }
            )

__all__ = [
    "ApplicationCommandAutoCompleteInteractionEvent",
    "ApplicationCommandInteractionEvent",
    "ApplicationCommandPermissionsUpdateEvent",
    "AutoModerationActionExecutionEvent",
    "AutoModerationEvent",
    "AutoModerationRuleCreateEvent",
    "AutoModerationRuleDeleteEvent",
    "AutoModerationRuleUpdateEvent",
    "ChannelCreateEvent",
    "ChannelDeleteEvent",
    "ChannelEvent",
    "ChannelPinsUpdateEvent",
    "ChannelUpdateEvent",
    "DirectMessageCreateEvent",
    "DirectMessageDeleteBulkEvent",
    "DirectMessageDeleteEvent",
    "DirectMessagePollVoteAddEvent",
    "DirectMessagePollVoteRemoveEvent",
    "DirectMessageReactionAddEvent",
    "DirectMessageReactionRemoveAllEvent",
    "DirectMessageReactionRemoveEmojiEvent",
    "DirectMessageReactionRemoveEvent",
    "DirectMessageUpdateEvent",
    "DirectTypingStartEvent",
    "EntitlementCreateEvent",
    "EntitlementDeleteEvent",
    "EntitlementUpdateEvent",
    "Event",
    "EventType",
    "GuildAuditLogEntryCreateEvent",
    "GuildBanAddEvent",
    "GuildBanRemoveEvent",
    "GuildCreateCompatEvent",
    "GuildCreateEvent",
    "GuildDeleteEvent",
    "GuildEmojisUpdateEvent",
    "GuildEvent",
    "GuildIntegrationsUpdateEvent",
    "GuildMemberAddEvent",
    "GuildMemberRemoveEvent",
    "GuildMemberUpdateEvent",
    "GuildMembersChunkEvent",
    "GuildMessageCreateEvent",
    "GuildMessageDeleteBulkEvent",
    "GuildMessageDeleteEvent",
    "GuildMessagePollVoteAddEvent",
    "GuildMessagePollVoteRemoveEvent",
    "GuildMessageReactionAddEvent",
    "GuildMessageReactionRemoveAllEvent",
    "GuildMessageReactionRemoveEmojiEvent",
    "GuildMessageReactionRemoveEvent",
    "GuildMessageUpdateEvent",
    "GuildRoleCreateEvent",
    "GuildRoleDeleteEvent",
    "GuildRoleUpdateEvent",
    "GuildScheduledEventCreateEvent",
    "GuildScheduledEventDeleteEvent",
    "GuildScheduledEventUpdateEvent",
    "GuildScheduledEventUserAddEvent",
    "GuildScheduledEventUserRemoveEvent",
    "GuildStickersUpdateEvent",
    "GuildTypingStartEvent",
    "GuildUpdateEvent",
    "HelloEvent",
    "IntegrationCreateEvent",
    "IntegrationDeleteEvent",
    "IntegrationEvent",
    "IntegrationUpdateEvent",
    "InteractionCreateEvent",
    "InvalidSessionEvent",
    "InviteCreateEvent",
    "InviteDeleteEvent",
    "MessageComponentInteractionEvent",
    "MessageCreateEvent",
    "MessageDeleteBulkEvent",
    "MessageDeleteEvent",
    "MessageEvent",
    "MessagePollVoteAddEvent",
    "MessagePollVoteRemoveEvent",
    "MessageReactionAddEvent",
    "MessageReactionRemoveAllEvent",
    "MessageReactionRemoveEmojiEvent",
    "MessageReactionRemoveEvent",
    "MessageUpdateEvent",
    "MetaEvent",
    "ModalSubmitInteractionEvent",
    "NoticeEvent",
    "PingInteractionEvent",
    "PresenceUpdateEvent",
    "ReadyEvent",
    "ReconnectEvent",
    "RequestEvent",
    "ResumedEvent",
    "StageInstanceCreateEvent",
    "StageInstanceDeleteEvent",
    "StageInstanceUpdateEvent",
    "SubscriptionCreateEvent",
    "SubscriptionDeleteEvent",
    "SubscriptionUpdateEvent",
    "ThreadCreateEvent",
    "ThreadDeleteEvent",
    "ThreadEvent",
    "ThreadListSyncEvent",
    "ThreadMemberUpdateEvent",
    "ThreadMembersUpdateEvent",
    "ThreadUpdateEvent",
    "TypingStartEvent",
    "UserUpdateEvent",
    "VoiceChannelEffectSendEvent",
    "VoiceChannelStartTimeUpdateEvent",
    "VoiceChannelStatusUpdateEvent",
    "VoiceServerUpdateEvent",
    "VoiceStateUpdateEvent",
    "WebhooksUpdateEvent",
    "event_classes",
]
