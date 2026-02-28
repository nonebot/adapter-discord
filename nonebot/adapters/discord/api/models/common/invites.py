from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Literal
import warnings

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ...types import (
    UNSET,
    GuildFeature,
    GuildNSFWLevel,
    InviteTargetType,
    InviteType,
    Missing,
    MissingOrNullable,
    VerificationLevel,
)

if TYPE_CHECKING:
    from .application import Application
    from .channels import Channel
    from .guild_members import GuildMember
    from .guild_scheduled_events import GuildScheduledEvent
    from .user import User


class Invite(BaseModel):
    type: InviteType
    code: str
    guild: Missing[InviteGuild] = UNSET
    channel: Channel | None = Field(...)
    inviter: Missing[User] = UNSET
    target_type: Missing[InviteTargetType] = UNSET
    target_user: Missing[User] = UNSET
    target_application: Missing[Application] = UNSET
    approximate_presence_count: Missing[int] = UNSET
    approximate_member_count: Missing[int] = UNSET
    expires_at: MissingOrNullable[datetime.datetime] = UNSET
    stage_instance: Missing[InviteStageInstance] = UNSET
    guild_scheduled_event: Missing[GuildScheduledEvent] = UNSET
    uses: Missing[int] = UNSET
    max_uses: Missing[int] = UNSET
    max_age: Missing[int] = UNSET
    temporary: Missing[bool] = UNSET
    created_at: Missing[datetime.datetime] = UNSET

    def __init__(self, **data) -> None:  # noqa: ANN003
        super().__init__(**data)
        if data.get("stage_instance", UNSET) is not UNSET:
            warnings.warn(
                "Invite.stage_instance is deprecated by Discord",
                DeprecationWarning,
                stacklevel=2,
            )


class InviteGuild(BaseModel):
    id: Snowflake
    name: str
    splash: str | None = None
    banner: str | None = None
    description: str | None = None
    icon: str | None = None
    features: list[GuildFeature]
    verification_level: VerificationLevel
    vanity_url_code: str | None = None
    nsfw_level: GuildNSFWLevel
    premium_subscription_count: int | None = None


class InviteMetadata(BaseModel):
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: datetime.datetime


class InviteTargetUsersJobStatus(BaseModel):
    status: Literal[0, 1, 2, 3]
    total_users: int
    processed_users: int
    created_at: datetime.datetime
    completed_at: datetime.datetime | None = Field(...)
    error_message: MissingOrNullable[str] = UNSET


class InviteStageInstance(BaseModel):
    members: list[GuildMember]
    participant_count: int
    speaker_count: int
    topic: str


__all__ = [
    "Invite",
    "InviteGuild",
    "InviteMetadata",
    "InviteStageInstance",
    "InviteTargetUsersJobStatus",
]
