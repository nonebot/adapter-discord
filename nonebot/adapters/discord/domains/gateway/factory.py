"""Gateway dispatch conversion from wire payloads to public events."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import ModuleType, UnionType
from typing import TYPE_CHECKING, TypeAlias, cast

from nonebot.compat import type_validate_python
from pydantic import ValidationError

from ..interaction.types import InteractionType
from ...payload import Dispatch
from ...protocol import UNSET, is_unset

if TYPE_CHECKING:
    from ...event import Event


EventParser: TypeAlias = Callable[[dict[str, object]], "Event"]
UnknownEventParser: TypeAlias = Callable[[Dispatch], "Event"]


@dataclass(frozen=True, slots=True)
class EventBinding:
    event_type: type["Event"] | UnionType
    parser: EventParser


class EventFactory:
    def __init__(self, bindings: Mapping[str, EventBinding]) -> None:
        self.bindings = bindings
        self._unknown_event_parser: UnknownEventParser | None = None

    def configure_unknown_event_parser(self, parser: UnknownEventParser) -> None:
        """Configure parsing for the intentionally unbound gateway event."""
        self._unknown_event_parser = parser

    def from_dispatch(self, dispatch: Dispatch) -> "Event":
        binding = self.bindings.get(dispatch.type)
        if binding is not None:
            return binding.parser(dispatch.data)

        if self._unknown_event_parser is None:
            msg = "Gateway event registry has not been initialized"
            raise RuntimeError(msg)
        return self._unknown_event_parser(dispatch)


def model_parser(event_type: type["Event"] | UnionType) -> EventParser:
    """Return the standard Pydantic parser for one event model or union."""

    def parse(data: dict[str, object]) -> "Event":
        return cast(
            "Event", type_validate_python(cast("type[Event]", event_type), data)
        )

    return parse


def initialize_event_registry(event: ModuleType) -> None:
    """Build the registry after ``event`` has declared every event class."""
    if EVENT_BINDINGS:
        return

    event_model = event.Event
    event_type_enum = event.EventType

    def unknown_event_parser(dispatch: Dispatch) -> "Event":
        # Preserve the 1.x policy for the only unbound enum member while
        # explicitly rejecting real unknown gateway event strings.
        event_type = event_type_enum(dispatch.type)
        event_value = type_validate_python(event_model, dispatch.data)
        event_value.__type__ = event_type
        return event_value

    def message_create_parser(data: dict[str, object]) -> "Event":
        event_type = (
            event.GuildMessageCreateEvent
            if not is_unset(data.get("guild_id", UNSET))
            else event.DirectMessageCreateEvent
        )
        return model_parser(event_type)(data)

    interaction_event_types: Mapping[InteractionType, type[Event]] = {
        InteractionType.PING: event.PingInteractionEvent,
        InteractionType.APPLICATION_COMMAND: event.ApplicationCommandInteractionEvent,
        InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE: (
            event.ApplicationCommandAutoCompleteInteractionEvent
        ),
        InteractionType.MESSAGE_COMPONENT: event.MessageComponentInteractionEvent,
        InteractionType.MODAL_SUBMIT: event.ModalSubmitInteractionEvent,
    }

    def interaction_create_parser(data: dict[str, object]) -> "Event":
        interaction_type = InteractionType(data["type"])
        return model_parser(interaction_event_types[interaction_type])(data)

    def guild_create_parser(data: dict[str, object]) -> "Event":
        try:
            return model_parser(event.GuildCreateEvent)(data)
        except ValidationError:
            return model_parser(event.GuildCreateCompatEvent)(data)

    def binding(event_type: type["Event"] | UnionType) -> EventBinding:
        return EventBinding(event_type, model_parser(event_type))

    event_bindings = {
        event_type_enum.HELLO.value: binding(event.HelloEvent),
        event_type_enum.READY.value: binding(event.ReadyEvent),
        event_type_enum.RESUMED.value: binding(event.ResumedEvent),
        event_type_enum.RECONNECT.value: binding(event.ReconnectEvent),
        event_type_enum.INVALID_SESSION.value: binding(event.InvalidSessionEvent),
        event_type_enum.APPLICATION_COMMAND_PERMISSIONS_UPDATE.value: binding(
            event.ApplicationCommandPermissionsUpdateEvent
        ),
        event_type_enum.AUTO_MODERATION_RULE_CREATE.value: binding(
            event.AutoModerationRuleCreateEvent
        ),
        event_type_enum.AUTO_MODERATION_RULE_UPDATE.value: binding(
            event.AutoModerationRuleUpdateEvent
        ),
        event_type_enum.AUTO_MODERATION_RULE_DELETE.value: binding(
            event.AutoModerationRuleDeleteEvent
        ),
        event_type_enum.AUTO_MODERATION_ACTION_EXECUTION.value: binding(
            event.AutoModerationActionExecutionEvent
        ),
        event_type_enum.CHANNEL_CREATE.value: binding(event.ChannelCreateEvent),
        event_type_enum.CHANNEL_UPDATE.value: binding(event.ChannelUpdateEvent),
        event_type_enum.CHANNEL_DELETE.value: binding(event.ChannelDeleteEvent),
        event_type_enum.CHANNEL_PINS_UPDATE.value: binding(
            event.ChannelPinsUpdateEvent
        ),
        event_type_enum.THREAD_CREATE.value: binding(event.ThreadCreateEvent),
        event_type_enum.THREAD_UPDATE.value: binding(event.ThreadUpdateEvent),
        event_type_enum.THREAD_DELETE.value: binding(event.ThreadDeleteEvent),
        event_type_enum.THREAD_LIST_SYNC.value: binding(event.ThreadListSyncEvent),
        event_type_enum.THREAD_MEMBER_UPDATE.value: binding(
            event.ThreadMemberUpdateEvent
        ),
        event_type_enum.THREAD_MEMBERS_UPDATE.value: binding(
            event.ThreadMembersUpdateEvent
        ),
        event_type_enum.ENTITLEMENT_CREATE.value: binding(event.EntitlementCreateEvent),
        event_type_enum.ENTITLEMENT_UPDATE.value: binding(event.EntitlementUpdateEvent),
        event_type_enum.ENTITLEMENT_DELETE.value: binding(event.EntitlementDeleteEvent),
        event_type_enum.GUILD_CREATE.value: EventBinding(
            event.GuildCreateEvent | event.GuildCreateCompatEvent,
            guild_create_parser,
        ),
        event_type_enum.GUILD_UPDATE.value: binding(event.GuildUpdateEvent),
        event_type_enum.GUILD_DELETE.value: binding(event.GuildDeleteEvent),
        event_type_enum.GUILD_AUDIT_LOG_ENTRY_CREATE.value: binding(
            event.GuildAuditLogEntryCreateEvent
        ),
        event_type_enum.GUILD_BAN_ADD.value: binding(event.GuildBanAddEvent),
        event_type_enum.GUILD_BAN_REMOVE.value: binding(event.GuildBanRemoveEvent),
        event_type_enum.GUILD_EMOJIS_UPDATE.value: binding(
            event.GuildEmojisUpdateEvent
        ),
        event_type_enum.GUILD_STICKERS_UPDATE.value: binding(
            event.GuildStickersUpdateEvent
        ),
        event_type_enum.GUILD_INTEGRATIONS_UPDATE.value: binding(
            event.GuildIntegrationsUpdateEvent
        ),
        event_type_enum.GUILD_MEMBER_ADD.value: binding(event.GuildMemberAddEvent),
        event_type_enum.GUILD_MEMBER_REMOVE.value: binding(
            event.GuildMemberRemoveEvent
        ),
        event_type_enum.GUILD_MEMBER_UPDATE.value: binding(
            event.GuildMemberUpdateEvent
        ),
        event_type_enum.GUILD_MEMBERS_CHUNK.value: binding(
            event.GuildMembersChunkEvent
        ),
        event_type_enum.GUILD_ROLE_CREATE.value: binding(event.GuildRoleCreateEvent),
        event_type_enum.GUILD_ROLE_UPDATE.value: binding(event.GuildRoleUpdateEvent),
        event_type_enum.GUILD_ROLE_DELETE.value: binding(event.GuildRoleDeleteEvent),
        event_type_enum.GUILD_SCHEDULED_EVENT_CREATE.value: binding(
            event.GuildScheduledEventCreateEvent
        ),
        event_type_enum.GUILD_SCHEDULED_EVENT_UPDATE.value: binding(
            event.GuildScheduledEventUpdateEvent
        ),
        event_type_enum.GUILD_SCHEDULED_EVENT_DELETE.value: binding(
            event.GuildScheduledEventDeleteEvent
        ),
        event_type_enum.GUILD_SCHEDULED_EVENT_USER_ADD.value: binding(
            event.GuildScheduledEventUserAddEvent
        ),
        event_type_enum.GUILD_SCHEDULED_EVENT_USER_REMOVE.value: binding(
            event.GuildScheduledEventUserRemoveEvent
        ),
        event_type_enum.INTEGRATION_CREATE.value: binding(event.IntegrationCreateEvent),
        event_type_enum.INTEGRATION_UPDATE.value: binding(event.IntegrationUpdateEvent),
        event_type_enum.INTEGRATION_DELETE.value: binding(event.IntegrationDeleteEvent),
        event_type_enum.INTERACTION_CREATE.value: EventBinding(
            event.PingInteractionEvent
            | event.ApplicationCommandInteractionEvent
            | event.ApplicationCommandAutoCompleteInteractionEvent
            | event.MessageComponentInteractionEvent
            | event.ModalSubmitInteractionEvent,
            interaction_create_parser,
        ),
        event_type_enum.INVITE_CREATE.value: binding(event.InviteCreateEvent),
        event_type_enum.INVITE_DELETE.value: binding(event.InviteDeleteEvent),
        event_type_enum.MESSAGE_CREATE.value: EventBinding(
            event.GuildMessageCreateEvent | event.DirectMessageCreateEvent,
            message_create_parser,
        ),
        event_type_enum.MESSAGE_UPDATE.value: binding(
            event.GuildMessageUpdateEvent | event.DirectMessageUpdateEvent
        ),
        event_type_enum.MESSAGE_DELETE.value: binding(
            event.GuildMessageDeleteEvent | event.DirectMessageDeleteEvent
        ),
        event_type_enum.MESSAGE_DELETE_BULK.value: binding(
            event.GuildMessageDeleteBulkEvent | event.DirectMessageDeleteBulkEvent
        ),
        event_type_enum.MESSAGE_REACTION_ADD.value: binding(
            event.GuildMessageReactionAddEvent | event.DirectMessageReactionAddEvent
        ),
        event_type_enum.MESSAGE_REACTION_REMOVE.value: binding(
            event.GuildMessageReactionRemoveEvent
            | event.DirectMessageReactionRemoveEvent
        ),
        event_type_enum.MESSAGE_REACTION_REMOVE_ALL.value: binding(
            event.GuildMessageReactionRemoveAllEvent
            | event.DirectMessageReactionRemoveAllEvent
        ),
        event_type_enum.MESSAGE_REACTION_REMOVE_EMOJI.value: binding(
            event.GuildMessageReactionRemoveEmojiEvent
            | event.DirectMessageReactionRemoveEmojiEvent
        ),
        event_type_enum.PRESENCE_UPDATE.value: binding(event.PresenceUpdateEvent),
        event_type_enum.STAGE_INSTANCE_CREATE.value: binding(
            event.StageInstanceCreateEvent
        ),
        event_type_enum.STAGE_INSTANCE_UPDATE.value: binding(
            event.StageInstanceUpdateEvent
        ),
        event_type_enum.STAGE_INSTANCE_DELETE.value: binding(
            event.StageInstanceDeleteEvent
        ),
        event_type_enum.SUBSCRIPTION_CREATE.value: binding(
            event.SubscriptionCreateEvent
        ),
        event_type_enum.SUBSCRIPTION_UPDATE.value: binding(
            event.SubscriptionUpdateEvent
        ),
        event_type_enum.SUBSCRIPTION_DELETE.value: binding(
            event.SubscriptionDeleteEvent
        ),
        event_type_enum.TYPING_START.value: binding(
            event.GuildTypingStartEvent | event.DirectTypingStartEvent
        ),
        event_type_enum.USER_UPDATE.value: binding(event.UserUpdateEvent),
        event_type_enum.VOICE_CHANNEL_STATUS_UPDATE.value: binding(
            event.VoiceChannelStatusUpdateEvent
        ),
        event_type_enum.VOICE_CHANNEL_START_TIME_UPDATE.value: binding(
            event.VoiceChannelStartTimeUpdateEvent
        ),
        event_type_enum.VOICE_CHANNEL_EFFECT_SEND.value: binding(
            event.VoiceChannelEffectSendEvent
        ),
        event_type_enum.VOICE_STATE_UPDATE.value: binding(event.VoiceStateUpdateEvent),
        event_type_enum.VOICE_SERVER_UPDATE.value: binding(
            event.VoiceServerUpdateEvent
        ),
        event_type_enum.WEBHOOKS_UPDATE.value: binding(event.WebhooksUpdateEvent),
        event_type_enum.MESSAGE_POLL_VOTE_ADD.value: binding(
            event.GuildMessagePollVoteAddEvent | event.DirectMessagePollVoteAddEvent
        ),
        event_type_enum.MESSAGE_POLL_VOTE_REMOVE.value: binding(
            event.GuildMessagePollVoteRemoveEvent
            | event.DirectMessagePollVoteRemoveEvent
        ),
    }
    EVENT_BINDINGS.update(event_bindings)
    EVENT_FACTORY.configure_unknown_event_parser(unknown_event_parser)


# ``event`` initializes this module after declaring public event classes. Keeping
# the mapping and factory instances stable preserves imported object identities.
EVENT_BINDINGS: dict[str, EventBinding] = {}
EVENT_FACTORY = EventFactory(EVENT_BINDINGS)


__all__ = [
    "EVENT_BINDINGS",
    "EVENT_FACTORY",
    "EventBinding",
    "EventFactory",
    "EventParser",
    "model_parser",
]
