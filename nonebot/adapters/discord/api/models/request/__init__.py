"""Request models.

See https://discord.com/developers/docs/reference
"""

from __future__ import annotations

from .emoji import ModifyGuildEmojiParams
from .interactions import (
    ApplicationCommandBulkOverwriteParams,
    ApplicationCommandCreate,
    ApplicationCommandEditParams,
    InteractionCallbackAutocomplete,
    InteractionCallbackData,
    InteractionCallbackMessage,
    InteractionCallbackModal,
    InteractionResponse,
)
from .polls import PollAnswerRequest, PollRequest
from .soundboard import (
    CreateGuildSoundboardSoundParams,
    ModifyGuildSoundboardSoundParams,
    SendSoundboardSoundParams,
)
from .stickers import ModifyGuildStickerParams
from .voice import ModifyCurrentUserVoiceStateParams

__all__ = [
    "ApplicationCommandBulkOverwriteParams",
    "ApplicationCommandCreate",
    "ApplicationCommandEditParams",
    "CreateGuildSoundboardSoundParams",
    "InteractionCallbackAutocomplete",
    "InteractionCallbackData",
    "InteractionCallbackMessage",
    "InteractionCallbackModal",
    "InteractionResponse",
    "ModifyCurrentUserVoiceStateParams",
    "ModifyGuildEmojiParams",
    "ModifyGuildSoundboardSoundParams",
    "ModifyGuildStickerParams",
    "PollAnswerRequest",
    "PollRequest",
    "SendSoundboardSoundParams",
]
