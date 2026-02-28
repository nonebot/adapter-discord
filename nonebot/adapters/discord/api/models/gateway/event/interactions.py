from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from ...common.channels import Channel
from ...common.guild_members import GuildMember
from ...common.messages import MessageGet
from ...common.monetization import Entitlement
from ...common.snowflake import Snowflake
from ...common.user import User
from ...interactions.interactions import (
    ApplicationCommandData,
    InteractionData,
    InteractionGuild,
    MessageComponentData,
    ModalSubmitData,
)
from ....types import (
    UNSET,
    ApplicationIntegrationType,
    InteractionContextType,
    InteractionType,
    Missing,
)


class InteractionCreateBasePayload(BaseModel):
    id: Snowflake
    application_id: Snowflake
    attachment_size_limit: int
    guild: Missing[InteractionGuild] = UNSET
    guild_id: Missing[Snowflake] = UNSET
    channel: Missing[Channel] = UNSET
    channel_id: Missing[Snowflake] = UNSET
    member: Missing[GuildMember] = UNSET
    user: Missing[User] = UNSET
    token: str
    version: int
    app_permissions: Missing[str] = UNSET
    locale: Missing[str] = UNSET
    guild_locale: Missing[str] = UNSET
    entitlements: Missing[list[Entitlement]] = UNSET
    authorizing_integration_owners: dict[
        ApplicationIntegrationType, Snowflake | Literal["0"]
    ]
    context: Missing[InteractionContextType] = UNSET


class PingInteractionCreatePayload(InteractionCreateBasePayload):
    type: Literal[InteractionType.PING]
    data: Missing[InteractionData] = UNSET
    message: Missing[MessageGet] = UNSET


class ApplicationCommandInteractionCreatePayload(InteractionCreateBasePayload):
    type: Literal[InteractionType.APPLICATION_COMMAND]
    data: ApplicationCommandData
    message: Missing[MessageGet] = UNSET


class ApplicationCommandAutoCompleteInteractionCreatePayload(
    InteractionCreateBasePayload
):
    type: Literal[InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE]
    data: ApplicationCommandData
    message: Missing[MessageGet] = UNSET


class MessageComponentInteractionCreatePayload(InteractionCreateBasePayload):
    type: Literal[InteractionType.MESSAGE_COMPONENT]
    data: MessageComponentData
    message: MessageGet


class ModalSubmitInteractionCreatePayload(InteractionCreateBasePayload):
    type: Literal[InteractionType.MODAL_SUBMIT]
    data: ModalSubmitData
    message: Missing[MessageGet] = UNSET


__all__ = [
    "ApplicationCommandAutoCompleteInteractionCreatePayload",
    "ApplicationCommandInteractionCreatePayload",
    "InteractionCreateBasePayload",
    "MessageComponentInteractionCreatePayload",
    "ModalSubmitInteractionCreatePayload",
    "PingInteractionCreatePayload",
]
