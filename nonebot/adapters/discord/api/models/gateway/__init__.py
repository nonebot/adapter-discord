from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .frame import (
        Dispatch,
        Heartbeat,
        HeartbeatAck,
        Hello,
        Identify,
        InvalidSession,
        Opcode,
        Payload,
        PayloadType,
        Reconnect,
        Resume,
    )
    from .gateway_event_fields import (
        Activity,
        ActivityAssets,
        ActivityButtons,
        ActivityEmoji,
        ActivityParty,
        ActivitySecrets,
        ActivityTimestamps,
        ClientStatus,
        PresenceUpdate,
        PresenceUpdateUser,
        StageInstanceCreate,
        StageInstanceDelete,
        StageInstanceUpdate,
        UserUpdate,
        VoiceChannelEffectSend,
        VoiceChannelStartTimeUpdate,
        VoiceChannelStatusUpdate,
        VoiceServerUpdate,
        VoiceStateUpdate,
        WebhooksUpdate,
    )
    from .gateway_payloads import (
        ApplicationReady,
        Hello as HelloData,
        Identify as IdentifyData,
        IdentifyConnectionProperties,
        Ready,
        RequestGuildMembers,
        Resume as ResumeData,
        UpdatePresence,
        UpdateVoiceState,
    )


__all__ = [
    "Activity",
    "ActivityAssets",
    "ActivityButtons",
    "ActivityEmoji",
    "ActivityParty",
    "ActivitySecrets",
    "ActivityTimestamps",
    "ApplicationReady",
    "ClientStatus",
    "Dispatch",
    "Heartbeat",
    "HeartbeatAck",
    "Hello",
    "HelloData",
    "Identify",
    "IdentifyConnectionProperties",
    "IdentifyData",
    "InvalidSession",
    "Opcode",
    "Payload",
    "PayloadType",
    "PresenceUpdate",
    "PresenceUpdateUser",
    "Ready",
    "Reconnect",
    "RequestGuildMembers",
    "Resume",
    "ResumeData",
    "StageInstanceCreate",
    "StageInstanceDelete",
    "StageInstanceUpdate",
    "UpdatePresence",
    "UpdateVoiceState",
    "UserUpdate",
    "VoiceChannelEffectSend",
    "VoiceChannelStartTimeUpdate",
    "VoiceChannelStatusUpdate",
    "VoiceServerUpdate",
    "VoiceStateUpdate",
    "WebhooksUpdate",
]


_EXPORTS: dict[str, tuple[str, str]] = {
    "Activity": (".gateway_event_fields", "Activity"),
    "ActivityAssets": (".gateway_event_fields", "ActivityAssets"),
    "ActivityButtons": (".gateway_event_fields", "ActivityButtons"),
    "ActivityEmoji": (".gateway_event_fields", "ActivityEmoji"),
    "ActivityParty": (".gateway_event_fields", "ActivityParty"),
    "ActivitySecrets": (".gateway_event_fields", "ActivitySecrets"),
    "ActivityTimestamps": (".gateway_event_fields", "ActivityTimestamps"),
    "ApplicationReady": (".gateway_payloads", "ApplicationReady"),
    "ClientStatus": (".gateway_event_fields", "ClientStatus"),
    "Dispatch": (".frame", "Dispatch"),
    "Heartbeat": (".frame", "Heartbeat"),
    "HeartbeatAck": (".frame", "HeartbeatAck"),
    "Hello": (".frame", "Hello"),
    "HelloData": (".gateway_payloads", "Hello"),
    "Identify": (".frame", "Identify"),
    "IdentifyConnectionProperties": (
        ".gateway_payloads",
        "IdentifyConnectionProperties",
    ),
    "IdentifyData": (".gateway_payloads", "Identify"),
    "InvalidSession": (".frame", "InvalidSession"),
    "Opcode": (".frame", "Opcode"),
    "Payload": (".frame", "Payload"),
    "PayloadType": (".frame", "PayloadType"),
    "PresenceUpdate": (".gateway_event_fields", "PresenceUpdate"),
    "PresenceUpdateUser": (".gateway_event_fields", "PresenceUpdateUser"),
    "Ready": (".gateway_payloads", "Ready"),
    "Reconnect": (".frame", "Reconnect"),
    "RequestGuildMembers": (".gateway_payloads", "RequestGuildMembers"),
    "Resume": (".frame", "Resume"),
    "ResumeData": (".gateway_payloads", "Resume"),
    "StageInstanceCreate": (".gateway_event_fields", "StageInstanceCreate"),
    "StageInstanceDelete": (".gateway_event_fields", "StageInstanceDelete"),
    "StageInstanceUpdate": (".gateway_event_fields", "StageInstanceUpdate"),
    "UpdatePresence": (".gateway_payloads", "UpdatePresence"),
    "UpdateVoiceState": (".gateway_payloads", "UpdateVoiceState"),
    "UserUpdate": (".gateway_event_fields", "UserUpdate"),
    "VoiceChannelEffectSend": (".gateway_event_fields", "VoiceChannelEffectSend"),
    "VoiceChannelStartTimeUpdate": (
        ".gateway_event_fields",
        "VoiceChannelStartTimeUpdate",
    ),
    "VoiceChannelStatusUpdate": (".gateway_event_fields", "VoiceChannelStatusUpdate"),
    "VoiceServerUpdate": (".gateway_event_fields", "VoiceServerUpdate"),
    "VoiceStateUpdate": (".gateway_event_fields", "VoiceStateUpdate"),
    "WebhooksUpdate": (".gateway_event_fields", "WebhooksUpdate"),
}


def __getattr__(name: str) -> object:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError:
        raise AttributeError(name) from None

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
