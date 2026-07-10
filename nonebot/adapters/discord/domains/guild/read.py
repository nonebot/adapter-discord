"""Canonical guild.read models."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import (
        AvatarDecorationData,
        Channel,
        DefaultReaction,
        Emoji,
        ForumTag,
        Overwrite,
        Sticker,
        ThreadMember,
        User,
    )

from .._model_support import (
    UNSET,
    BaseModel,
    ChannelType,
    DefaultMessageNotificationLevel,
    ExplicitContentFilterLevel,
    Field,
    ForumLayoutTypes,
    GuildFeature,
    GuildMemberFlags,
    GuildNSFWLevel,
    GuildScheduledEventEntityType,
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventRecurrenceRuleFrequency,
    GuildScheduledEventRecurrenceRuleMonth,
    GuildScheduledEventRecurrenceRuleWeekday,
    GuildScheduledEventStatus,
    IntegrationExpireBehaviors,
    Literal,
    MFALevel,
    Missing,
    MissingOrNullable,
    OnboardingMode,
    OnboardingPromptType,
    PremiumTier,
    RoleFlag,
    Snowflake,
    SortOrderTypes,
    SystemChannelFlags,
    VerificationLevel,
    datetime,
)


class Guild(BaseModel):
    """Guild

    see https://discord.com/developers/docs/resources/guild#guild-object"""

    id: Snowflake
    name: str
    icon: str | None = Field(...)
    icon_hash: MissingOrNullable[str] = UNSET
    splash: str | None = Field(...)
    discovery_splash: str | None = None
    owner: Missing[bool] = UNSET
    owner_id: Snowflake
    permissions: Missing[str] = UNSET
    region: MissingOrNullable[str] = UNSET
    afk_channel_id: Snowflake | None = Field(...)
    afk_timeout: int
    widget_enabled: Missing[bool] = UNSET
    widget_channel_id: MissingOrNullable[Snowflake] = UNSET
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    roles: list[Role]
    emojis: list[Emoji]
    features: list[GuildFeature]
    mfa_level: MFALevel
    application_id: Snowflake | None = Field(...)
    system_channel_id: Snowflake | None = Field(...)
    system_channel_flags: SystemChannelFlags
    rules_channel_id: Snowflake | None = Field(...)
    max_presences: int | None = Field(...)
    max_members: int | None = Field(...)
    vanity_url_code: str | None = Field(...)
    description: str | None = Field(...)
    banner: str | None = Field(...)
    premium_tier: PremiumTier
    premium_subscription_count: int | None = Field(...)
    preferred_locale: str
    public_updates_channel_id: Snowflake | None = Field(...)
    max_video_channel_users: Missing[int] = UNSET
    max_stage_video_channel_users: Missing[int] = UNSET
    approximate_member_count: Missing[int] = UNSET
    approximate_presence_count: Missing[int] = UNSET
    welcome_screen: Missing[WelcomeScreen] = UNSET
    nsfw_level: GuildNSFWLevel
    stickers: Missing[list[Sticker]] = UNSET
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: MissingOrNullable[Snowflake] = UNSET
    incidents_data: MissingOrNullable[GuildIncidentsData] = UNSET


class GuildIncidentsData(BaseModel):
    """Incidents Data.

    see https://discord.com/developers/docs/resources/guild#incidents-data-object
    """

    invites_disabled_until: datetime.datetime | None = Field(...)
    dms_disabled_until: datetime.datetime | None = Field(...)
    dm_spam_detected_at: MissingOrNullable[datetime.datetime] = UNSET
    raid_detected_at: MissingOrNullable[datetime.datetime] = UNSET


class CurrentUserGuild(BaseModel):
    """partial guild object for Get Current User Guilds API

    see https://discord.com/developers/docs/resources/user#get-current-user-guilds"""

    id: Snowflake
    name: str
    icon: str | None = Field(...)
    owner: Missing[bool] = UNSET
    permissions: Missing[str] = UNSET
    features: list[GuildFeature]
    approximate_member_count: Missing[int] = UNSET
    approximate_presence_count: Missing[int] = UNSET


class UnavailableGuild(BaseModel):
    """Unavailable Guild

    see https://discord.com/developers/docs/resources/guild#unavailable-guild-object"""

    id: Snowflake
    unavailable: Literal[True]


class GuildPreview(BaseModel):
    """Guild Preview

    see https://discord.com/developers/docs/resources/guild#guild-preview-object"""

    id: Snowflake
    name: str
    icon: str | None = None
    splash: str | None = None
    discovery_splash: str | None = None
    emojis: list[Emoji]
    features: list[GuildFeature]
    approximate_member_count: int
    approximate_presence_count: int
    description: str | None = None
    stickers: list[Sticker]


class GuildWidgetSettings(BaseModel):
    """Guild Widget Settings

    see https://discord.com/developers/docs/resources/guild#guild-widget-settings-object
    """

    enabled: bool
    channel_id: Snowflake | None = None


class GuildWidget(BaseModel):
    """Guild Widget

    see https://discord.com/developers/docs/resources/guild#guild-widget-object"""

    id: Snowflake
    name: str
    instant_invite: str | None = None
    channels: list[GuildWidgetChannel]
    members: list[GuildWidgetUser]
    presence_count: int


class GuildVanityURL(BaseModel):
    """Guild Vanity URL.

    see https://discord.com/developers/docs/resources/guild#get-guild-vanity-url
    """

    code: str | None = None
    uses: int


class GuildWidgetChannel(BaseModel):
    """partial channel objects for GuildWidget.channels

    see https://discord.com/developers/docs/resources/guild#guild-widget-object-example-guild-widget
    """

    id: Snowflake
    name: str
    position: Missing[int] = UNSET


class GuildWidgetUser(BaseModel):
    """partial user objects for GuildWidget.members

    The fields id, discriminator and avatar are anonymized to prevent abuse.

    see https://discord.com/developers/docs/resources/guild#guild-widget-object-example-guild-widget
    """

    id: str
    username: str
    discriminator: str
    avatar: str | None = None
    status: str
    avatar_url: str


class GuildMember(BaseModel):
    """Guild Member

    see https://discord.com/developers/docs/resources/guild#guild-member-object"""

    user: Missing[User] = UNSET
    nick: MissingOrNullable[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    roles: list[Snowflake]
    joined_at: datetime.datetime
    premium_since: MissingOrNullable[datetime.datetime] = UNSET
    deaf: Missing[bool] = UNSET
    mute: Missing[bool] = UNSET
    flags: GuildMemberFlags
    pending: Missing[bool] = UNSET
    permissions: Missing[str] = UNSET
    communication_disabled_until: MissingOrNullable[datetime.datetime] = UNSET
    avatar_decoration_data: MissingOrNullable[AvatarDecorationData] = UNSET


class Integration(BaseModel):
    """Integration

    see https://discord.com/developers/docs/resources/guild#integration-object"""

    id: Snowflake
    name: str
    type: str
    enabled: bool
    syncing: Missing[bool] = UNSET
    role_id: Missing[Snowflake] = UNSET
    enable_emoticons: Missing[bool] = UNSET
    expire_behavior: Missing[IntegrationExpireBehaviors] = UNSET
    expire_grace_period: Missing[int] = UNSET
    user: Missing[User] = UNSET
    account: IntegrationAccount
    synced_at: Missing[datetime.datetime] = UNSET
    subscriber_count: Missing[int] = UNSET
    revoked: Missing[bool] = UNSET
    application: Missing[IntegrationApplication] = UNSET
    scopes: Missing[list[str]] = UNSET  # TODO: OAuth2 scopes


class IntegrationAccount(BaseModel):
    """Integration Account

    see https://discord.com/developers/docs/resources/guild#integration-account-object
    """

    id: str
    name: str


class IntegrationApplication(BaseModel):
    """Integration Application

    see https://discord.com/developers/docs/resources/guild#integration-application-object
    """

    id: Snowflake
    name: str
    icon: str | None = None
    description: str
    bot: Missing[User] = UNSET


class Ban(BaseModel):
    """Ban

    see https://discord.com/developers/docs/resources/guild#ban-object"""

    reason: str | None = None
    user: User


class WelcomeScreen(BaseModel):
    """Welcome screen.

    see https://discord.com/developers/docs/resources/guild#welcome-screen-object"""

    description: str | None = None
    welcome_channels: list[WelcomeScreenChannel]


class WelcomeScreenChannel(BaseModel):
    """Welcome screen channel.

    see https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-channel-structure
    """

    channel_id: Snowflake
    description: str
    emoji_id: Snowflake | None = None
    emoji_name: str | None = None


class GuildOnboarding(BaseModel):
    """Guild onboarding.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object"""

    guild_id: Snowflake
    prompts: list[OnboardingPrompt]
    default_channel_ids: list[Snowflake]
    enabled: bool
    mode: OnboardingMode


class OnboardingPrompt(BaseModel):
    """Onboarding prompt.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-prompt-structure
    """

    id: Snowflake
    type: OnboardingPromptType
    options: list[OnboardingPromptOption]
    title: str
    single_select: bool
    required: bool
    in_onboarding: bool


class OnboardingPromptOption(BaseModel):
    """Onboarding prompt option.

    When creating or updating a prompt option, the `emoji_id`, `emoji_name`, and
    `emoji_animated` fields must be used instead of the emoji object.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-prompt-option-structure
    """

    id: Snowflake
    channel_ids: list[Snowflake]
    role_ids: list[Snowflake]
    emoji: Missing[Emoji] = UNSET
    emoji_id: Missing[Snowflake] = UNSET
    emoji_name: Missing[str] = UNSET
    emoji_animated: Missing[bool] = UNSET
    title: str
    description: str | None = None


class MembershipScreening(BaseModel):
    """Membership screening.

    see https://discord.com/developers/docs/resources/guild#membership-screening-object
    """


class ListActiveGuildThreadsResponse(BaseModel):
    """List Active Guild Threads Response

    see https://discord.com/developers/docs/resources/guild#list-active-guild-threads"""

    threads: list[Channel]
    members: list[ThreadMember]


class GuildScheduledEvent(BaseModel):
    """Guild Scheduled Event

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object
    """

    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake | None = None
    creator_id: MissingOrNullable[Snowflake] = UNSET
    name: str
    description: MissingOrNullable[str] = UNSET
    scheduled_start_time: datetime.datetime
    scheduled_end_time: datetime.datetime | None = None
    privacy_level: GuildScheduledEventPrivacyLevel
    status: GuildScheduledEventStatus
    entity_type: GuildScheduledEventEntityType
    entity_id: Snowflake | None = None
    entity_metadata: GuildScheduledEventEntityMetadata | None = None
    creator: Missing[User] = UNSET
    user_count: Missing[int] = UNSET
    image: MissingOrNullable[str] = UNSET
    recurrence_rule: RecurrenceRule | None = None


class GuildScheduledEventEntityMetadata(BaseModel):
    """Guild Scheduled Event Entity Metadata

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: Missing[str] = UNSET


class GuildScheduledEventUser(BaseModel):
    """Guild Scheduled Event User

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-user-object
    """

    guild_scheduled_event_id: Snowflake
    user: User
    member: Missing[GuildMember] = UNSET


class GuildTemplate(BaseModel):
    """Guild Template

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object
    """

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
    """partial guild object for GuildTemplate

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
    """

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
    """partial role object for GuildTemplateGuild

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
    """

    id: Snowflake
    name: str
    permissions: str
    color: int
    hoist: bool
    mentionable: bool
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET


class GuildTemplateGuildChannel(BaseModel):
    """partial role object for GuildTemplateGuild

    see https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
    """

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


class RoleColors(BaseModel):
    """Role colors.

    see https://discord.com/developers/docs/topics/permissions#role-object-role-colors-object
    """

    primary_color: int
    secondary_color: int | None = None
    tertiary_color: int | None = None


class Role(BaseModel):
    """Role

    see https://discord.com/developers/docs/topics/permissions#role-object"""

    id: Snowflake
    name: str
    color: int
    colors: Missing[RoleColors] = UNSET
    hoist: bool
    icon: MissingOrNullable[str] = UNSET
    unicode_emoji: MissingOrNullable[str] = UNSET
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: Missing[RoleTags] = UNSET
    flags: Missing[RoleFlag] = UNSET


class RoleTags(BaseModel):
    """Role tags.

    see https://discord.com/developers/docs/topics/permissions#role-object-role-tags-structure
    """

    bot_id: Missing[Snowflake] = UNSET
    integration_id: Missing[Snowflake] = UNSET
    premium_subscriber: Missing[None] = UNSET
    subscription_listing_id: Missing[Snowflake] = UNSET
    available_for_purchase: Missing[None] = UNSET
    guild_connections: Missing[None] = UNSET


class RecurrenceRule(BaseModel):
    """Discord's recurrence rule is a subset of the behaviors defined
    in the iCalendar RFC and implemented by python's dateutil rrule

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object
    """

    start: datetime.datetime
    """Starting time of the recurrence interval"""
    end: datetime.datetime | None = None
    """Ending time of the recurrence interval"""
    frequency: GuildScheduledEventRecurrenceRuleFrequency
    """How often the event occurs"""
    interval: int
    """The spacing between the events, defined by frequency. For example,
    frecency of WEEKLY and an interval of 2 would be "every-other week"""
    by_weekday: list[GuildScheduledEventRecurrenceRuleWeekday] | None = None
    """Set of specific days within a week for the event to recur on"""
    by_n_weekday: list[GuildScheduledEventRecurrenceRuleN_WeekdayStructure] | None = (
        None
    )
    """List of specific days within a specific week (1-5) to recur on"""
    by_month: list[GuildScheduledEventRecurrenceRuleMonth] | None = None
    """Set of specific months to recur on"""
    by_month_day: int | None = None
    """Set of specific dates within a month to recur on"""
    by_year_day: int | None = None
    """Set of days within a year to recur on (1-364)"""
    count: int | None = None
    """The total amount of times that the event is allowed to recur before stopping"""


class GuildScheduledEventRecurrenceRuleN_WeekdayStructure(BaseModel):  # noqa: N801
    """Guild Scheduled Event Recurrence Rule - N_Weekday Structure

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object-guild-scheduled-event-recurrence-rule-nweekday-structure
    """

    n: int
    """The week to reoccur on. 1 - 5"""
    day: GuildScheduledEventRecurrenceRuleWeekday
    """The day within the week to reoccur on"""


__all__ = [
    "Ban",
    "CurrentUserGuild",
    "Guild",
    "GuildIncidentsData",
    "GuildMember",
    "GuildOnboarding",
    "GuildPreview",
    "GuildScheduledEvent",
    "GuildScheduledEventEntityMetadata",
    "GuildScheduledEventRecurrenceRuleN_WeekdayStructure",
    "GuildScheduledEventUser",
    "GuildTemplate",
    "GuildTemplateGuild",
    "GuildTemplateGuildChannel",
    "GuildTemplateGuildRole",
    "GuildVanityURL",
    "GuildWidget",
    "GuildWidgetChannel",
    "GuildWidgetSettings",
    "GuildWidgetUser",
    "Integration",
    "IntegrationAccount",
    "IntegrationApplication",
    "ListActiveGuildThreadsResponse",
    "MembershipScreening",
    "OnboardingPrompt",
    "OnboardingPromptOption",
    "RecurrenceRule",
    "Role",
    "RoleColors",
    "RoleTags",
    "UnavailableGuild",
    "WelcomeScreen",
    "WelcomeScreenChannel",
]
