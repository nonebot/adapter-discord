from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional, Type, Union
from typing_extensions import override

from nonebot.adapters import Event as BaseEvent
from nonebot.utils import escape_tag

from pydantic import Field

from .api.model import *
from .api.types import UNSET, InteractionType, Missing
from .message import Message


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

    # GUILDS
    GUILD_CREATE = "GUILD_CREATE"
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

    # TYPING
    TYPING_START = "TYPING_START"

    # USER
    USER_UPDATE = "USER_UPDATE"

    # VOICE
    VOICE_STATE_UPDATE = "VOICE_STATE_UPDATE"
    VOICE_SERVER_UPDATE = "VOICE_SERVER_UPDATE"

    # WEBHOOKS
    WEBHOOKS_UPDATE = "WEBHOOKS_UPDATE"


class Event(BaseEvent):
    """Event"""

    __type__: EventType
    timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def time(self) -> datetime:
        return self.timestamp

    @override
    def get_event_name(self) -> str:
        return self.__class__.__name__

    @override
    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    @override
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @override
    def get_user_id(self) -> str:
        raise ValueError("Event has no context!")

    @override
    def get_session_id(self) -> str:
        raise ValueError("Event has no context!")

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

    reply: Optional[MessageGet] = None

    @property
    def message(self) -> Message:
        return self.get_message()

    @property
    def original_message(self) -> Message:
        return getattr(self, "_original_message", self.get_message())  # type: ignore

    @override
    def get_type(self) -> str:
        return "message"

    @override
    def get_user_id(self) -> str:
        return str(self.author.id)

    @override
    def get_session_id(self) -> str:
        return str(self.author.id)

    @override
    def get_message(self) -> Message:
        if not hasattr(self, "_message"):
            setattr(self, "_message", Message.from_guild_message(self))
            setattr(self, "_original_message", Message.from_guild_message(self))
        return getattr(self, "_message")

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

    token: str
    session_id: str
    seq: int


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
    permissions: List[ApplicationCommandPermissions]


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


class GuildEvent(NoticeEvent):
    """Guild event

    see https://discord.com/developers/docs/topics/gateway-events#guilds"""


class GuildCreateEvent(GuildEvent, GuildCreate):
    """Guild create event

    see https://discord.com/developers/docs/topics/gateway-events#guild-create"""

    __type__ = EventType.GUILD_CREATE


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


class InteractionCreateEvent(NoticeEvent, InteractionCreate):
    """Interaction create event

    see https://discord.com/developers/docs/topics/gateway-events#interaction-create"""

    __type__ = EventType.INTERACTION_CREATE


class PingInteractionEvent(InteractionCreateEvent):
    type: Literal[InteractionType.PING]
    data: Literal[UNSET] = UNSET


class ApplicationCommandInteractionEvent(InteractionCreateEvent):
    type: Literal[InteractionType.APPLICATION_COMMAND]
    data: ApplicationCommandData


class ApplicationCommandAutoCompleteInteractionEvent(InteractionCreateEvent):
    type: Literal[InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE]
    data: ApplicationCommandData


class MessageComponentInteractionEvent(InteractionCreateEvent):
    type: Literal[InteractionType.MESSAGE_COMPONENT]
    data: MessageComponentData
    message: MessageGet


class ModalSubmitInteractionEvent(InteractionCreateEvent):
    type: Literal[InteractionType.MODAL_SUBMIT]
    data: ModalSubmitData


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


class MessageCreateEvent(MessageEvent, MessageCreate):
    """Message Create Event

    see https://discord.com/developers/docs/topics/gateway-events#message-create
    """

    __type__ = EventType.MESSAGE_CREATE


class GuildMessageCreateEvent(MessageCreateEvent):
    guild_id: Snowflake


class DirectMessageCreateEvent(MessageCreateEvent):
    to_me: bool = True
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)


class MessageUpdateEvent(NoticeEvent, MessageUpdate):
    """Message Update Event

    see https://discord.com/developers/docs/topics/gateway-events#message-update
    """

    __type__ = EventType.MESSAGE_UPDATE


class GuildMessageUpdateEvent(MessageUpdateEvent):
    guild_id: Snowflake


class DirectMessageUpdateEvent(MessageUpdateEvent):
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)


class MessageDeleteEvent(NoticeEvent, MessageDelete):
    """Message Delete Event

    see https://discord.com/developers/docs/topics/gateway-events#message-delete
    """

    __type__ = EventType.MESSAGE_DELETE


class GuildMessageDeleteEvent(MessageDeleteEvent):
    guild_id: Snowflake


class DirectMessageDeleteEvent(MessageDeleteEvent):
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)


class MessageDeleteBulkEvent(NoticeEvent, MessageDeleteBulk):
    """Message Delete Bulk Event

    see https://discord.com/developers/docs/topics/gateway-events#message-delete-bulk
    """

    __type__ = EventType.MESSAGE_DELETE


class GuildMessageDeleteBulkEvent(MessageDeleteBulkEvent):
    guild_id: Snowflake


class DirectMessageDeleteBulkEvent(MessageDeleteBulkEvent):
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)


class MessageReactionAddEvent(NoticeEvent, MessageReactionAdd):
    """
    Message Reaction Add Event

    see https://discord.com/developers/docs/topics/gateway#message-reaction-add
    """

    __type__ = EventType.MESSAGE_REACTION_ADD


class GuildMessageReactionAddEvent(MessageReactionAddEvent):
    guild_id: Snowflake


class DirectMessageReactionAddEvent(MessageReactionAddEvent):
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)


class MessageReactionRemoveEvent(NoticeEvent, MessageReactionRemove):
    """Message Reaction Remove Event

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove
    """

    __type__ = EventType.MESSAGE_REACTION_REMOVE


class GuildMessageReactionRemoveEvent(MessageReactionRemoveEvent):
    guild_id: Snowflake


class DirectMessageReactionRemoveEvent(MessageReactionRemoveEvent):
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)


class MessageReactionRemoveAllEvent(NoticeEvent, MessageReactionRemoveAll):
    """Message Reaction Remove All Event

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-all
    """

    __type__ = EventType.MESSAGE_REACTION_REMOVE_ALL


class GuildMessageReactionRemoveAllEvent(MessageReactionRemoveAllEvent):
    guild_id: Snowflake


class DirectMessageReactionRemoveAllEvent(MessageReactionRemoveAllEvent):
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)


class MessageReactionRemoveEmojiEvent(NoticeEvent, MessageReactionRemoveEmoji):
    """Message Reaction Remove Emoji Event

    see https://discord.com/developers/docs/topics/gateway-events#message-reaction-remove-emoji
    """

    __type__ = EventType.MESSAGE_REACTION_REMOVE_EMOJI


class GuildMessageReactionRemoveEmojiEvent(MessageReactionRemoveEmojiEvent):
    guild_id: Snowflake


class DirectMessageReactionRemoveEmojiEvent(MessageReactionRemoveEmojiEvent):
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)


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


class TypingStartEvent(NoticeEvent, TypingStart):
    """Typing Start Event

    see https://discord.com/developers/docs/topics/gateway-events#typing-start
    """

    __type__ = EventType.TYPING_START


class GuildTypingStartEvent(TypingStartEvent):
    guild_id: Snowflake
    member: GuildMember


class DirectTypingStartEvent(TypingStartEvent):
    guild_id: Literal[UNSET] = Field(UNSET, exclude=True)
    member: Literal[UNSET] = Field(UNSET, exclude=True)


class UserUpdateEvent(NoticeEvent, UserUpdate):
    """User Update Event

    see https://discord.com/developers/docs/topics/gateway-events#user-update
    """

    __type__ = EventType.USER_UPDATE


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


event_classes: Dict[str, Type[Event]] = {
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
    EventType.GUILD_CREATE.value: GuildCreateEvent,
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
    EventType.INTERACTION_CREATE.value: Union[
        PingInteractionEvent,
        ApplicationCommandInteractionEvent,
        ApplicationCommandAutoCompleteInteractionEvent,
        MessageComponentInteractionEvent,
        ModalSubmitInteractionEvent,
        InteractionCreateEvent,
    ],
    EventType.INVITE_CREATE.value: InviteCreateEvent,
    EventType.INVITE_DELETE.value: InviteDeleteEvent,
    EventType.MESSAGE_CREATE.value: Union[
        GuildMessageCreateEvent, DirectMessageCreateEvent, MessageCreateEvent
    ],
    EventType.MESSAGE_UPDATE.value: Union[
        GuildMessageUpdateEvent, DirectMessageUpdateEvent, MessageUpdateEvent
    ],
    EventType.MESSAGE_DELETE.value: Union[
        GuildMessageDeleteEvent, DirectMessageDeleteEvent, MessageDeleteEvent
    ],
    EventType.MESSAGE_DELETE_BULK.value: Union[
        GuildMessageDeleteBulkEvent,
        DirectMessageDeleteBulkEvent,
        MessageDeleteBulkEvent,
    ],
    EventType.MESSAGE_REACTION_ADD.value: Union[
        GuildMessageReactionAddEvent,
        DirectMessageReactionAddEvent,
        MessageReactionAddEvent,
    ],
    EventType.MESSAGE_REACTION_REMOVE: Union[
        GuildMessageReactionRemoveEvent,
        DirectMessageReactionRemoveEvent,
        MessageReactionRemoveEvent,
    ],
    EventType.MESSAGE_REACTION_REMOVE_ALL: Union[
        GuildMessageReactionRemoveAllEvent,
        DirectMessageReactionRemoveAllEvent,
        MessageReactionRemoveAllEvent,
    ],
    EventType.MESSAGE_REACTION_REMOVE_EMOJI: Union[
        GuildMessageReactionRemoveEmojiEvent,
        DirectMessageReactionRemoveEmojiEvent,
        MessageReactionRemoveEmojiEvent,
    ],
    EventType.PRESENCE_UPDATE.value: PresenceUpdateEvent,
    EventType.STAGE_INSTANCE_CREATE.value: StageInstanceCreateEvent,
    EventType.STAGE_INSTANCE_UPDATE.value: StageInstanceUpdateEvent,
    EventType.STAGE_INSTANCE_DELETE.value: StageInstanceDeleteEvent,
    EventType.TYPING_START.value: Union[
        GuildTypingStartEvent, DirectTypingStartEvent, TypingStartEvent
    ],
    EventType.USER_UPDATE.value: UserUpdateEvent,
    EventType.VOICE_STATE_UPDATE.value: VoiceStateUpdateEvent,
    EventType.VOICE_SERVER_UPDATE.value: VoiceServerUpdateEvent,
    EventType.WEBHOOKS_UPDATE.value: WebhooksUpdateEvent,
}

__all__ = [
    "EventType",
    "Event",
    "MetaEvent",
    "NoticeEvent",
    "RequestEvent",
    "MessageEvent",
    "HelloEvent",
    "ReadyEvent",
    "ResumedEvent",
    "ReconnectEvent",
    "InvalidSessionEvent",
    "ApplicationCommandPermissionsUpdateEvent",
    "AutoModerationEvent",
    "AutoModerationRuleCreateEvent",
    "AutoModerationRuleUpdateEvent",
    "AutoModerationRuleDeleteEvent",
    "AutoModerationActionExecutionEvent",
    "ChannelEvent",
    "ChannelCreateEvent",
    "ChannelUpdateEvent",
    "ChannelDeleteEvent",
    "ChannelPinsUpdateEvent",
    "ThreadEvent",
    "ThreadCreateEvent",
    "ThreadUpdateEvent",
    "ThreadDeleteEvent",
    "ThreadListSyncEvent",
    "ThreadMemberUpdateEvent",
    "ThreadMembersUpdateEvent",
    "GuildEvent",
    "GuildCreateEvent",
    "GuildUpdateEvent",
    "GuildDeleteEvent",
    "GuildAuditLogEntryCreateEvent",
    "GuildBanAddEvent",
    "GuildBanRemoveEvent",
    "GuildEmojisUpdateEvent",
    "GuildStickersUpdateEvent",
    "GuildIntegrationsUpdateEvent",
    "GuildMemberAddEvent",
    "GuildMemberRemoveEvent",
    "GuildMemberUpdateEvent",
    "GuildMembersChunkEvent",
    "GuildRoleCreateEvent",
    "GuildRoleUpdateEvent",
    "GuildRoleDeleteEvent",
    "GuildScheduledEventCreateEvent",
    "GuildScheduledEventUpdateEvent",
    "GuildScheduledEventDeleteEvent",
    "GuildScheduledEventUserAddEvent",
    "GuildScheduledEventUserRemoveEvent",
    "IntegrationEvent",
    "IntegrationCreateEvent",
    "IntegrationUpdateEvent",
    "IntegrationDeleteEvent",
    "InteractionCreateEvent",
    "PingInteractionEvent",
    "ApplicationCommandInteractionEvent",
    "ApplicationCommandAutoCompleteInteractionEvent",
    "MessageComponentInteractionEvent",
    "ModalSubmitInteractionEvent",
    "InviteCreateEvent",
    "InviteDeleteEvent",
    "MessageCreateEvent",
    "GuildMessageCreateEvent",
    "DirectMessageCreateEvent",
    "MessageUpdateEvent",
    "GuildMessageUpdateEvent",
    "DirectMessageUpdateEvent",
    "MessageDeleteEvent",
    "GuildMessageDeleteEvent",
    "DirectMessageDeleteEvent",
    "MessageDeleteBulkEvent",
    "GuildMessageDeleteBulkEvent",
    "DirectMessageDeleteBulkEvent",
    "MessageReactionAddEvent",
    "GuildMessageReactionAddEvent",
    "DirectMessageReactionAddEvent",
    "MessageReactionRemoveEvent",
    "GuildMessageReactionRemoveEvent",
    "DirectMessageReactionRemoveEvent",
    "MessageReactionRemoveAllEvent",
    "GuildMessageReactionRemoveAllEvent",
    "DirectMessageReactionRemoveAllEvent",
    "MessageReactionRemoveEmojiEvent",
    "GuildMessageReactionRemoveEmojiEvent",
    "DirectMessageReactionRemoveEmojiEvent",
    "PresenceUpdateEvent",
    "StageInstanceCreateEvent",
    "StageInstanceUpdateEvent",
    "StageInstanceDeleteEvent",
    "TypingStartEvent",
    "GuildTypingStartEvent",
    "DirectTypingStartEvent",
    "UserUpdateEvent",
    "VoiceStateUpdateEvent",
    "VoiceServerUpdateEvent",
    "WebhooksUpdateEvent",
    "event_classes",
]
