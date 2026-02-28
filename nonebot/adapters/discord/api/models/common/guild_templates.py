from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .snowflake import Snowflake
from ...types import (
    UNSET,
    ChannelType,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    ForumLayoutTypes,
    Missing,
    MissingOrNullable,
    SortOrderTypes,
    SystemChannelFlags,
    VerificationLevel,
)

if TYPE_CHECKING:
    from .channels import DefaultReaction, ForumTag, Overwrite
    from .emoji import Emoji
    from .user import User


class GuildTemplate(BaseModel):
    code: str
    name: str
    description: str | None = None
    usage_count: int
    creator_id: Snowflake
    creator: User
    created_at: datetime.datetime
    updated_at: datetime.datetime
    source_guild_id: Snowflake
    serialized_source_guild: GuildTemplateGuild
    is_dirty: bool | None = None


class GuildTemplateGuild(BaseModel):
    name: str
    description: str | None = None
    region: MissingOrNullable[str] = UNSET
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    preferred_locale: str
    afk_channel_id: Snowflake | None = None
    afk_timeout: int
    system_channel_id: Snowflake | None = None
    system_channel_flags: SystemChannelFlags
    icon_hash: MissingOrNullable[str] = UNSET
    roles: list[GuildTemplateGuildRole]
    channels: list[GuildTemplateGuildChannel]


class GuildTemplateGuildRole(BaseModel):
    id: Snowflake
    name: str
    permissions: str
    color: int
    hoist: bool
    mentionable: bool
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET


class GuildTemplateGuildChannel(BaseModel):
    id: Snowflake
    type: ChannelType
    name: MissingOrNullable[str] = UNSET
    position: Missing[int] = UNSET
    topic: MissingOrNullable[str] = UNSET
    bitrate: Missing[int] = UNSET
    user_limit: Missing[int] = UNSET
    nsfw: Missing[bool] = UNSET
    rate_limit_per_user: Missing[int] = UNSET
    parent_id: MissingOrNullable[Snowflake] = UNSET
    default_auto_archive_duration: MissingOrNullable[int] = UNSET
    permission_overwrites: Missing[list[Overwrite]] = UNSET
    available_tags: MissingOrNullable[list[ForumTag]] = UNSET
    template: Missing[str] = UNSET
    default_reaction_emoji: MissingOrNullable[DefaultReaction] = UNSET
    default_thread_rate_limit_per_user: MissingOrNullable[int] = UNSET
    default_sort_order: MissingOrNullable[SortOrderTypes] = UNSET
    default_forum_layout: MissingOrNullable[ForumLayoutTypes] = UNSET
    icon_emoji: MissingOrNullable[Emoji] = UNSET
    theme_color: MissingOrNullable[int] = UNSET


__all__ = [
    "GuildTemplate",
    "GuildTemplateGuild",
    "GuildTemplateGuildChannel",
    "GuildTemplateGuildRole",
]
