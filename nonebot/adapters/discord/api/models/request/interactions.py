from __future__ import annotations

from typing import TypeAlias

from pydantic import BaseModel

from .messages import AllowedMention, AttachmentSend, File
from .polls import PollRequest
from ..common.embeds import Embed
from ..common.interactions import (
    AnyCommandOption,
    ApplicationCommandOptionChoice,
    Component,
)
from ..common.snowflake import Snowflake
from ...types import (
    UNSET,
    ApplicationCommandType,
    ApplicationIntegrationType,
    InteractionCallbackType,
    InteractionContextType,
    MessageFlag,
    Missing,
    MissingOrNullable,
)


class ApplicationCommandCreate(BaseModel):
    name: str
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    description: Missing[str] = UNSET
    description_localizations: MissingOrNullable[dict[str, str]] = UNSET
    options: Missing[list[AnyCommandOption]] = UNSET
    default_member_permissions: MissingOrNullable[str] = UNSET
    dm_permission: MissingOrNullable[bool] = UNSET
    default_permission: Missing[bool] = UNSET
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    contexts: Missing[list[InteractionContextType]] = UNSET
    type: Missing[ApplicationCommandType] = UNSET
    nsfw: Missing[bool] = UNSET


class ApplicationCommandBulkOverwriteParams(BaseModel):
    id: Missing[Snowflake] = UNSET
    type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT
    name: str
    name_localizations: dict[str, str] | None = None
    description: str | None = None
    description_localizations: dict[str, str] | None = None
    options: list[AnyCommandOption] | None = None
    default_member_permissions: str | None = None
    dm_permission: bool | None = None
    default_permission: bool | None = None
    nsfw: bool | None = None
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    contexts: MissingOrNullable[list[InteractionContextType]] = UNSET


class ApplicationCommandEditParams(BaseModel):
    name: Missing[str] = UNSET
    name_localizations: MissingOrNullable[dict[str, str]] = UNSET
    description: Missing[str] = UNSET
    description_localizations: MissingOrNullable[dict[str, str]] = UNSET
    options: Missing[list[AnyCommandOption]] = UNSET
    default_member_permissions: MissingOrNullable[str] = UNSET
    dm_permission: MissingOrNullable[bool] = UNSET
    default_permission: Missing[bool] = UNSET
    nsfw: Missing[bool] = UNSET
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    contexts: Missing[list[InteractionContextType]] = UNSET


class InteractionResponse(BaseModel):
    type: InteractionCallbackType
    data: Missing[InteractionCallbackData] = UNSET


class InteractionCallbackMessage(BaseModel):
    tts: bool | None = None
    content: str | None = None
    embeds: list[Embed] | None = None
    allowed_mentions: AllowedMention | None = None
    flags: MessageFlag | None = None
    components: list[Component] | None = None
    attachments: list[AttachmentSend] | None = None
    poll: PollRequest | None = None
    files: list[File] | None = None


class InteractionCallbackAutocomplete(BaseModel):
    choices: list[ApplicationCommandOptionChoice]


class InteractionCallbackModal(BaseModel):
    custom_id: str
    title: str
    components: list[Component]


InteractionCallbackData: TypeAlias = (
    InteractionCallbackMessage
    | InteractionCallbackAutocomplete
    | InteractionCallbackModal
)


__all__ = [
    "ApplicationCommandBulkOverwriteParams",
    "ApplicationCommandCreate",
    "ApplicationCommandEditParams",
    "InteractionCallbackAutocomplete",
    "InteractionCallbackData",
    "InteractionCallbackMessage",
    "InteractionCallbackModal",
    "InteractionResponse",
]
