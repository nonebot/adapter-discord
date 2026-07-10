from __future__ import annotations

from enum import IntEnum


class AuditLogEventType(IntEnum):
    """Audit Log Event Type

    see https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-audit-log-events
    """

    GUILD_UPDATE = 1
    CHANNEL_CREATE = 10
    CHANNEL_UPDATE = 11
    CHANNEL_DELETE = 12
    CHANNEL_OVERWRITE_CREATE = 13
    CHANNEL_OVERWRITE_UPDATE = 14
    CHANNEL_OVERWRITE_DELETE = 15
    MEMBER_KICK = 20
    MEMBER_PRUNE = 21
    MEMBER_BAN_ADD = 22
    MEMBER_BAN_REMOVE = 23
    MEMBER_UPDATE = 24
    MEMBER_ROLE_UPDATE = 25
    MEMBER_MOVE = 26
    MEMBER_DISCONNECT = 27
    BOT_ADD = 28
    ROLE_CREATE = 30
    ROLE_UPDATE = 31
    ROLE_DELETE = 32
    INVITE_CREATE = 40
    INVITE_UPDATE = 41
    INVITE_DELETE = 42
    WEBHOOK_CREATE = 50
    WEBHOOK_UPDATE = 51
    WEBHOOK_DELETE = 52
    EMOJI_CREATE = 60
    EMOJI_UPDATE = 61
    EMOJI_DELETE = 62
    MESSAGE_DELETE = 72
    MESSAGE_BULK_DELETE = 73
    MESSAGE_PIN = 74
    MESSAGE_UNPIN = 75
    INTEGRATION_CREATE = 80
    INTEGRATION_UPDATE = 81
    INTEGRATION_DELETE = 82
    STAGE_INSTANCE_CREATE = 83
    STAGE_INSTANCE_UPDATE = 84
    STAGE_INSTANCE_DELETE = 85
    STICKER_CREATE = 90
    STICKER_UPDATE = 91
    STICKER_DELETE = 92
    GUILD_SCHEDULED_EVENT_CREATE = 100
    GUILD_SCHEDULED_EVENT_UPDATE = 101
    GUILD_SCHEDULED_EVENT_DELETE = 102
    THREAD_CREATE = 110
    THREAD_UPDATE = 111
    THREAD_DELETE = 112
    APPLICATION_COMMAND_PERMISSION_UPDATE = 121
    AUTO_MODERATION_RULE_CREATE = 140
    AUTO_MODERATION_RULE_UPDATE = 141
    AUTO_MODERATION_RULE_DELETE = 142
    AUTO_MODERATION_BLOCK_MESSAGE = 143
    AUTO_MODERATION_FLAG_TO_CHANNEL = 144
    AUTO_MODERATION_USER_COMMUNICATION_DISABLED = 145
    CREATOR_MONETIZATION_REQUEST_CREATED = 150
    CREATOR_MONETIZATION_TERMS_ACCEPTED = 151
    ONBOARDING_PROMPT_CREATE = 163
    ONBOARDING_PROMPT_UPDATE = 164
    ONBOARDING_PROMPT_DELETE = 165
    ONBOARDING_CREATE = 166
    ONBOARDING_UPDATE = 167
    HOME_SETTINGS_CREATE = 190
    HOME_SETTINGS_UPDATE = 191


class AutoModerationActionType(IntEnum):
    """Auto moderation action type.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-action-object-action-types
    """

    BLOCK_MESSAGE = 1
    """blocks a member's message and prevents it from being posted.
    A custom explanation can be specified and shown to
    members whenever their message is blocked."""
    SEND_ALERT_MESSAGE = 2
    """logs user content to a specified channel"""
    TIMEOUT = 3
    """timeout user for a specified duration

    A TIMEOUT action can only be set up for KEYWORD and MENTION_SPAM rules.
    The MODERATE_MEMBERS permission is required to use the TIMEOUT action type."""
    BLOCK_MEMBER_INTERACTION = 4
    """prevents a member from using text, voice, or other interactions"""


class AutoModerationRuleEventType(IntEnum):
    """Auto moderation rule event type.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-event-types
    """

    MESSAGE_SEND = 1
    """when a member sends or edits a message in the guild"""
    MEMBER_UPDATE = 2
    """when a member edits their profile"""


class KeywordPresetType(IntEnum):
    """Keyword preset type.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-keyword-preset-types
    """

    PROFANITY = 1
    """words that may be considered forms of swearing or cursing"""
    SEXUAL_CONTENT = 2
    """"words that refer to sexually explicit behavior or activity"""
    SLURS = 3
    """personal insults or words that may be considered hate speech"""


class TriggerType(IntEnum):
    """Trigger type.

    see https://discord.com/developers/docs/resources/auto-moderation#auto-moderation-rule-object-trigger-types
    """

    KEYWORD = 1
    """check if content contains words from a user defined list of keywords"""
    SPAM = 3
    """check if content represents generic spam"""
    KEYWORD_PRESET = 4
    """check if content contains words from internal pre-defined wordsets"""
    MENTION_SPAM = 5
    """check if content contains more unique mentions than allowed"""
    MEMBER_PROFILE = 6
    """check if member profile contains words from a user defined list of keywords"""


__all__ = [
    "AuditLogEventType",
    "AutoModerationActionType",
    "AutoModerationRuleEventType",
    "KeywordPresetType",
    "TriggerType",
]
