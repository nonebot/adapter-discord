from __future__ import annotations

from pydantic import BaseModel, Field

from .snowflake import Snowflake
from ..types import MembershipState, TeamMemberRoleType


# Teams
# see https://discord.com/developers/docs/topics/teams
class Team(BaseModel):
    """Team.

    see https://discord.com/developers/docs/topics/teams#data-models-team-object
    """

    icon: str | None = Field(...)
    id: str
    members: list[TeamMember]
    name: str
    owner_user_id: Snowflake


class TeamMember(BaseModel):
    """Team member.

    see https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    membership_state: MembershipState
    team_id: Snowflake
    user: TeamMemberUser
    role: TeamMemberRoleType


class TeamMemberUser(BaseModel):
    """partial user object for TeamMember

    see https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    avatar: str | None = None
    discriminator: str
    id: Snowflake
    username: str
