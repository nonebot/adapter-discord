from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Literal
import warnings

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ..types import (
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
    from ..model import Application, Channel, GuildMember, GuildScheduledEvent, User


class Invite(BaseModel):
    """Invite

    Warning:
        stage_instance is deprecated by Discord and may be omitted.

    see https://discord.com/developers/docs/resources/invite#invite-object
    """

    type: InviteType
    code: str
    guild: Missing[InviteGuild] = UNSET
    channel: Channel | None = Field(...)  # partial channel object
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
    """partial guild object for Invite.guild

    see https://discord.com/developers/docs/resources/invite#invite-object-example-invite-object
    """

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
    """Invite Metadata

    see https://discord.com/developers/docs/resources/invite#invite-metadata-object
    """

    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: datetime.datetime


class InviteTargetUsersJobStatus(BaseModel):
    """Invite target users job status.

    see https://discord.com/developers/docs/resources/invite#get-target-users-job-status
    """

    status: Literal[0, 1, 2, 3]
    total_users: int
    processed_users: int
    created_at: datetime.datetime
    completed_at: datetime.datetime | None = Field(...)
    error_message: MissingOrNullable[str] = UNSET


class InviteStageInstance(BaseModel):
    """Invite Stage Instance

    This is deprecated.

    see https://discord.com/developers/docs/resources/invite#invite-stage-instance-object
    """

    members: list[GuildMember]  # partial guild member objects
    participant_count: int
    speaker_count: int
    topic: str


class InviteCreate(BaseModel):
    channel_id: Snowflake
    code: str
    created_at: datetime.datetime
    guild_id: Missing[Snowflake] = UNSET
    inviter: Missing[User] = UNSET
    max_age: int
    max_uses: int
    target_type: Missing[InviteTargetType] = UNSET
    target_user: Missing[User] = UNSET
    target_application: Missing[Application] = UNSET
    temporary: bool
    uses: int


class InviteDelete(BaseModel):
    channel_id: Snowflake
    guild_id: Missing[Snowflake] = UNSET
    code: str

    def __init__(self, **data) -> None:  # noqa: ANN003
        super().__init__(**data)
        warnings.warn(
            "InviteStageInstance is deprecated by Discord",
            DeprecationWarning,
            stacklevel=2,
        )
