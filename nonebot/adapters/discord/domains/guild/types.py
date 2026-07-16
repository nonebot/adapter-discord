from enum import IntEnum, IntFlag

from .._enum import StrEnum


class DefaultMessageNotificationLevel(IntEnum):
    """Default message notification level.

    see https://discord.com/developers/docs/resources/guild#guild-object-default-message-notification-level
    """

    ALL_MESSAGES = 0
    """members will receive notifications for all messages by default"""
    ONLY_MENTIONS = 1
    """members will receive notifications only for messages
    that @mention them by default"""


class ExplicitContentFilterLevel(IntEnum):
    """Explicit content filter level.

    see https://discord.com/developers/docs/resources/guild#guild-object-explicit-content-filter-level
    """

    DISABLED = 0
    """media content will not be scanned"""
    MEMBERS_WITHOUT_ROLES = 1
    """media content sent by members without roles will be scanned"""
    ALL_MEMBERS = 2
    """media content sent by all members will be scanned"""


class GuildFeature(StrEnum):
    """Guild feature.

    see https://discord.com/developers/docs/resources/guild#guild-object-guild-features
    """

    ACTIVITIES_ALPHA = "ACTIVITIES_ALPHA"
    ACTIVITIES_EMPLOYEE = "ACTIVITIES_EMPLOYEE"
    ACTIVITIES_INTERNAL_DEV = "ACTIVITIES_INTERNAL_DEV"
    ANIMATED_BANNER = "ANIMATED_BANNER"
    """guild has access to set an animated guild banner image"""
    ANIMATED_ICON = "ANIMATED_ICON"
    """guild has access to set an animated guild icon"""
    APPLICATION_COMMAND_PERMISSIONS_V2 = "APPLICATION_COMMAND_PERMISSIONS_V2"
    """guild is using the old permissions configuration behavior"""
    AUTO_MODERATION = "AUTO_MODERATION"
    """guild has set up auto moderation rules"""
    AUTOMOD_TRIGGER_KEYWORD_FILTER = "AUTOMOD_TRIGGER_KEYWORD_FILTER"
    AUTOMOD_TRIGGER_ML_SPAM_FILTER = "AUTOMOD_TRIGGER_ML_SPAM_FILTER"
    """Given to guilds previously in the 2022-03_automod_trigger_ml_spam_filter experiment overrides"""
    AUTOMOD_TRIGGER_SPAM_LINK_FILTER = "AUTOMOD_TRIGGER_SPAM_LINK_FILTER"
    AUTOMOD_TRIGGER_USER_PROFILE = "AUTOMOD_TRIGGER_USER_PROFILE"
    """Server has enabled AutoMod for user profiles"""
    BANNER = "BANNER"
    """guild has access to set a guild banner image"""
    BFG = "BFG"
    """Internally documented as big funky guild"""
    BOOSTING_TIERS_EXPERIMENT_MEDIUM_GUILD = "BOOSTING_TIERS_EXPERIMENT_MEDIUM_GUILD"
    BOOSTING_TIERS_EXPERIMENT_SMALL_GUILD = "BOOSTING_TIERS_EXPERIMENT_SMALL_GUILD"
    BOT_DEVELOPER_EARLY_ACCESS = "BOT_DEVELOPER_EARLY_ACCESS"
    """Enables early access features for bot and library developers"""
    BURST_REACTIONS = "BURST_REACTIONS"
    """Enables burst reactions for the guild"""
    CHANNEL_EMOJIS_GENERATED = "CHANNEL_EMOJIS_GENERATED"
    CHANNEL_HIGHLIGHTS = "CHANNEL_HIGHLIGHTS"
    CHANNEL_HIGHLIGHTS_DISABLED = "CHANNEL_HIGHLIGHTS_DISABLED"
    CHANNEL_ICON_EMOJIS_GENERATED = "CHANNEL_ICON_EMOJIS_GENERATED"
    CLAN = "CLAN"
    """The server is a clan server"""
    CLYDE_DISABLED = "CLYDE_DISABLED"
    """Given when a server administrator disables ClydeAI for the guild"""
    CLYDE_ENABLED = "CLYDE_ENABLED"
    """Server has enabled Clyde AI"""
    CLYDE_EXPERIMENT_ENABLED = "CLYDE_EXPERIMENT_ENABLED"
    """Enables ClydeAI for the guild"""
    COMMUNITY = "COMMUNITY"
    """guild can enable welcome screen, Membership Screening,
    stage channels and discovery, and receives community updates"""
    COMMUNITY_CANARY = "COMMUNITY_CANARY"
    COMMUNITY_EXP_LARGE_GATED = "COMMUNITY_EXP_LARGE_GATED"
    COMMUNITY_EXP_LARGE_UNGATED = "COMMUNITY_EXP_LARGE_UNGATED"
    COMMUNITY_EXP_MEDIUM = "COMMUNITY_EXP_MEDIUM"
    CREATOR_ACCEPTED_NEW_TERMS = "CREATOR_ACCEPTED_NEW_TERMS"
    """The server owner accepted the new monetization terms"""
    CREATOR_MONETIZABLE = "CREATOR_MONETIZABLE"
    """Given to guilds that enabled role subscriptions through the manual approval system"""
    CREATOR_MONETIZABLE_DISABLED = "CREATOR_MONETIZABLE_DISABLED"
    CREATOR_MONETIZABLE_PENDING_NEW_OWNER_ONBOARDING = (
        "CREATOR_MONETIZABLE_PENDING_NEW_OWNER_ONBOARDING"
    )
    CREATOR_MONETIZABLE_RESTRICTED = "CREATOR_MONETIZABLE_RESTRICTED"
    CREATOR_MONETIZABLE_WHITEGLOVE = "CREATOR_MONETIZABLE_WHITEGLOVE"
    CREATOR_MONETIZABLE_PROVISIONAL = "CREATOR_MONETIZABLE_PROVISIONAL"
    """guild has enabled monetization"""
    CREATOR_MONETIZATION_APPLICATION_ALLOWLIST = (
        "CREATOR_MONETIZATION_APPLICATION_ALLOWLIST"
    )
    CREATOR_STORE_PAGE = "CREATOR_STORE_PAGE"
    """guild has enabled the role subscription promo page"""
    DEVELOPER_SUPPORT_SERVER = "DEVELOPER_SUPPORT_SERVER"
    """guild has been set as a support server on the App Directory"""
    DISCOVERABLE = "DISCOVERABLE"
    """guild is able to be discovered in the directory"""
    DISCOVERABLE_DISABLED = "DISCOVERABLE_DISABLED"
    """Guild is permanently removed from Discovery by Discord"""
    ENABLED_DISCOVERABLE_BEFORE = "ENABLED_DISCOVERABLE_BEFORE"
    """Given to servers that have enabled Discovery at any point"""
    ENABLED_MODERATION_EXPERIENCE_FOR_NON_COMMUNITY = (
        "ENABLED_MODERATION_EXPERIENCE_FOR_NON_COMMUNITY"
    )
    """Moves the member list from the guild settings to the member tab for non-community guilds"""
    EXPOSED_TO_ACTIVITIES_WTP_EXPERIMENT = "EXPOSED_TO_ACTIVITIES_WTP_EXPERIMENT"
    """Given to guilds previously in the 2021-11_activities_baseline_engagement_bundle experiment overrides"""
    FEATURABLE = "FEATURABLE"
    """guild is able to be featured in the directory"""
    GUESTS_ENABLED = "GUESTS_ENABLED"
    """Guild has used guest invites"""
    GUILD_AUTOMOD_DEFAULT_LIST = "GUILD_AUTOMOD_DEFAULT_LIST"
    """Given to guilds in the 2022-03_guild_automod_default_list experiment overrides"""
    GUILD_COMMUNICATION_DISABLED_GUILDS = "GUILD_COMMUNICATION_DISABLED_GUILDS"
    """Given to guilds previously in the 2021-11_guild_communication_disabled_guilds experiment overrides"""
    GUILD_HOME_DEPRECATION_OVERRIDE = "GUILD_HOME_DEPRECATION_OVERRIDE"
    GUILD_HOME_OVERRIDE = "GUILD_HOME_OVERRIDE"
    """Gives the guild access to the Home feature, enables Treatment 2 of the 2022-01_home_tab_guild experiment overrides"""
    GUILD_HOME_TEST = "GUILD_HOME_TEST"
    """Gives the guild access to the Home feature, enables Treatment 1 of the 2022-01_home_tab_guild experiment"""
    GUILD_MEMBER_VERIFICATION_EXPERIMENT = "GUILD_MEMBER_VERIFICATION_EXPERIMENT"
    """Given to guilds previously in the 2021-11_member_verification_manual_approval experiment"""
    GUILD_ONBOARDING = "GUILD_ONBOARDING"
    """Guild has enabled onboarding"""
    GUILD_ONBOARDING_ADMIN_ONLY = "GUILD_ONBOARDING_ADMIN_ONLY"
    GUILD_ONBOARDING_EVER_ENABLED = "GUILD_ONBOARDING_EVER_ENABLED"
    """Guild has ever enabled onboarding"""
    GUILD_ONBOARDING_HAS_PROMPTS = "GUILD_ONBOARDING_HAS_PROMPTS"
    GUILD_PRODUCTS = "GUILD_PRODUCTS"
    """Given to guilds previously in the 2023-04_server_products experiment overrides"""
    GUILD_PRODUCTS_ALLOW_ARCHIVED_FILE = "GUILD_PRODUCTS_ALLOW_ARCHIVED_FILE"
    GUILD_ROLE_SUBSCRIPTIONS = "GUILD_ROLE_SUBSCRIPTIONS"
    """Given to guilds previously in the 2021-06_guild_role_subscriptions experiment overrides"""
    GUILD_ROLE_SUBSCRIPTION_PURCHASE_FEEDBACK_LOOP = (
        "GUILD_ROLE_SUBSCRIPTION_PURCHASE_FEEDBACK_LOOP"
    )
    """Given to guilds previously in the 2022-05_mobile_web_role_subscription_purchase_page experiment overrides"""
    GUILD_ROLE_SUBSCRIPTION_TIER_TEMPLATE = "GUILD_ROLE_SUBSCRIPTION_TIER_TEMPLATE"
    GUILD_ROLE_SUBSCRIPTION_TRIALS = "GUILD_ROLE_SUBSCRIPTION_TRIALS"
    """Given to guilds previously in the 2022-01_guild_role_subscription_trials experiment overrides"""
    GUILD_SERVER_GUIDE = "GUILD_SERVER_GUIDE"
    """Guild has enabled server guide"""
    GUILD_WEB_PAGE_VANITY_URL = "GUILD_WEB_PAGE_VANITY_URL"
    HAD_EARLY_ACTIVITIES_ACCESS = "HAD_EARLY_ACTIVITIES_ACCESS"
    """Server previously had access to voice channel activities and can bypass the boost level requirement"""
    HAS_DIRECTORY_ENTRY = "HAS_DIRECTORY_ENTRY"
    """Guild is in a directory channel"""
    HIDE_FROM_EXPERIMENT_UI = "HIDE_FROM_EXPERIMENT_UI"
    HUB = "HUB"
    """Student Hubs contain a directory channel that let you find school-related, student-run servers for your school or university"""
    INCREASED_THREAD_LIMIT = "INCREASED_THREAD_LIMIT"
    """Allows the server to have 1,000+ active threads"""
    INTERNAL_EMPLOYEE_ONLY = "INTERNAL_EMPLOYEE_ONLY"
    """Restricts the guild so that only users with the staff flag can join"""
    INVITES_DISABLED = "INVITES_DISABLED"
    """guild has paused invites, preventing new users from joining"""
    INVITE_SPLASH = "INVITE_SPLASH"
    """guild has access to set an invite splash background"""
    LINKED_TO_HUB = "LINKED_TO_HUB"
    MARKETPLACES_CONNECTION_ROLES = "MARKETPLACES_CONNECTION_ROLES"
    MEMBER_PROFILES = "MEMBER_PROFILES"
    """Allows members to customize their avatar, banner and bio for that server"""
    MEMBER_SAFETY_PAGE_ROLLOUT = "MEMBER_SAFETY_PAGE_ROLLOUT"
    """Assigns the experiment of the Member Safety panel and lockdowns to the guild"""
    MEMBER_VERIFICATION_GATE_ENABLED = "MEMBER_VERIFICATION_GATE_ENABLED"
    """guild has enabled Membership Screening"""
    MEMBER_VERIFICATION_MANUAL_APPROVAL = "MEMBER_VERIFICATION_MANUAL_APPROVAL"
    MOBILE_WEB_ROLE_SUBSCRIPTION_PURCHASE_PAGE = (
        "MOBILE_WEB_ROLE_SUBSCRIPTION_PURCHASE_PAGE"
    )
    """Given to guilds previously in the 2022-05_mobile_web_role_subscription_purchase_page experiment overrides"""
    MONETIZATION_ENABLED = "MONETIZATION_ENABLED"
    """Allows the server to set a team in dev portal to receive role subscription payouts"""
    MORE_EMOJI = "MORE_EMOJI"
    """Adds 150 extra emoji slots to each category (normal and animated emoji). Not used in server boosting"""
    MORE_STICKERS = "MORE_STICKERS"
    """guild has increased custom sticker slots"""
    NEWS = "NEWS"
    """guild has access to create announcement channels"""
    NEW_THREAD_PERMISSIONS = "NEW_THREAD_PERMISSIONS"
    """Guild has new thread permissions"""
    NON_COMMUNITY_RAID_ALERTS = "NON_COMMUNITY_RAID_ALERTS"
    """Non-community guild is opt-in to raid alerts"""
    PARTNERED = "PARTNERED"
    """guild is partnered"""
    PREMIUM_TIER_3_OVERRIDE = "PREMIUM_TIER_3_OVERRIDE"
    """Forces the server to server boosting level 3"""
    PREVIEW_ENABLED = "PREVIEW_ENABLED"
    """guild can be previewed before joining via
    Membership Screening or the directory"""
    PRODUCTS_AVAILABLE_FOR_PURCHASE = "PRODUCTS_AVAILABLE_FOR_PURCHASE"
    """Guild has server products available for purchase"""
    RAID_ALERTS_DISABLED = "RAID_ALERTS_DISABLED"
    """Guild is opt-out from raid alerts"""
    RELAY_ENABLED = "RELAY_ENABLED"
    """Shards connections to the guild to different nodes that relay information between each other"""
    RESTRICT_SPAM_RISK_GUILDS = "RESTRICT_SPAM_RISK_GUILDS"
    ROLE_ICONS = "ROLE_ICONS"
    """guild is able to set role icons"""
    ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE = (
        "ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE"
    )
    """guild has role subscriptions that can be purchased"""
    ROLE_SUBSCRIPTIONS_ENABLED = "ROLE_SUBSCRIPTIONS_ENABLED"
    """guild has enabled role subscriptions"""
    ROLE_SUBSCRIPTIONS_ENABLED_FOR_PURCHASE = "ROLE_SUBSCRIPTIONS_ENABLED_FOR_PURCHASE"
    SHARD = "SHARD"
    SHARED_CANVAS_FRIENDS_AND_FAMILY_TEST = "SHARED_CANVAS_FRIENDS_AND_FAMILY_TEST"
    """Given to guilds previously in the 2023-01_shared_canvas experiment overrides"""
    SOUNDBOARD = "SOUNDBOARD"
    SUMMARIES_DISABLED_BY_USER = "SUMMARIES_DISABLED_BY_USER"
    SUMMARIES_ENABLED = "SUMMARIES_ENABLED"
    """Given to guilds in the 2023-02_p13n_summarization experiment overrides"""
    SUMMARIES_ENABLED_BY_USER = "SUMMARIES_ENABLED_BY_USER"
    SUMMARIES_ENABLED_GA = "SUMMARIES_ENABLED_GA"
    """Given to guilds in the 2023-02_p13n_summarization experiment overrides"""
    SUMMARIES_LONG_LOOKBACK = "SUMMARIES_LONG_LOOKBACK"
    SUMMARIES_OPT_OUT_EXPERIENCE = "SUMMARIES_OPT_OUT_EXPERIENCE"
    SUMMARIES_PAUSED = "SUMMARIES_PAUSED"
    STAFF_LEVEL_COLLABORATOR_REQUIRED = "STAFF_LEVEL_COLLABORATOR_REQUIRED"
    STAFF_LEVEL_RESTRICTED_COLLABORATOR_REQUIRED = (
        "STAFF_LEVEL_RESTRICTED_COLLABORATOR_REQUIRED"
    )
    TEXT_IN_STAGE_ENABLED = "TEXT_IN_STAGE_ENABLED"
    TEXT_IN_VOICE_ENABLED = "TEXT_IN_VOICE_ENABLED"
    """Show a chat button inside voice channels that opens a dedicated text channel in a sidebar similar to thread view"""
    THREADS_ENABLED_TESTING = "THREADS_ENABLED_TESTING"
    """Used by bot developers to test their bots with threads in guilds with 5 or less members and a bot. Also gives the premium thread features"""
    THREADS_ENABLED = "THREADS_ENABLED"
    """Enabled threads early access"""
    THREAD_DEFAULT_AUTO_ARCHIVE_DURATION = "THREAD_DEFAULT_AUTO_ARCHIVE_DURATION"
    """Unknown, presumably used for testing changes to the thread default auto archive duration"""
    THREADS_ONLY_CHANNEL = "THREADS_ONLY_CHANNEL"
    """Given to guilds previously in the 2021-07_threads_only_channel experiment overrides"""
    TICKETED_EVENTS_ENABLED = "TICKETED_EVENTS_ENABLED"
    """guild has enabled ticketed events"""
    TICKETING_ENABLED = "TICKETING_ENABLED"
    TIERLESS_BOOSTING_SYSTEM_MESSAGE = "TIERLESS_BOOSTING_SYSTEM_MESSAGE"
    """Server uses tierless boosting system messages (gradually rolling out to servers).

    This feature is part of Discord's tierless boosting experiment where servers can use
    Boosts to unlock perks without needing to reach specific levels. Currently in
    limited rollout - not documented in official API docs yet.

    see https://discord.com/blog/get-more-from-your-boosts-with-new-server-perks
    """
    VANITY_URL = "VANITY_URL"
    """guild has access to set a vanity URL"""
    VERIFIED = "VERIFIED"
    """guild is verified"""
    VIP_REGIONS = "VIP_REGIONS"
    """guild has access to set 384kbps bitrate in voice
    (previously VIP voice servers)"""
    VOICE_CHANNEL_EFFECTS = "VOICE_CHANNEL_EFFECTS"
    """Given to guilds previously in the 2022-06_voice_channel_effects experiment overrides"""
    VOICE_IN_THREADS = "VOICE_IN_THREADS"
    WELCOME_SCREEN_ENABLED = "WELCOME_SCREEN_ENABLED"
    """guild has enabled the welcome screen"""
    VIDEO_QUALITY_720_60FPS = "VIDEO_QUALITY_720_60FPS"
    TIERLESS_BOOSTING = "TIERLESS_BOOSTING"
    VIDEO_BITRATE_ENHANCED = "VIDEO_BITRATE_ENHANCED"
    STAGE_CHANNEL_VIEWERS_50 = "STAGE_CHANNEL_VIEWERS_50"
    BYPASS_SLOWMODE_PERMISSION_MIGRATION_COMPLETE = (
        "BYPASS_SLOWMODE_PERMISSION_MIGRATION_COMPLETE"
    )
    AUDIO_BITRATE_128_KBPS = "AUDIO_BITRATE_128_KBPS"
    PIN_PERMISSION_MIGRATION_COMPLETE = "PIN_PERMISSION_MIGRATION_COMPLETE"
    VIDEO_QUALITY_1080_60FPS = "VIDEO_QUALITY_1080_60FPS"
    AUDIO_BITRATE_256_KBPS = "AUDIO_BITRATE_256_KBPS"
    STAGE_CHANNEL_VIEWERS_150 = "STAGE_CHANNEL_VIEWERS_150"
    MAX_FILE_SIZE_50_MB = "MAX_FILE_SIZE_50_MB"


class GuildMemberFlags(IntFlag):
    """Guild member flags.

    see https://discord.com/developers/docs/resources/guild#guild-member-object-guild-member-flags
    """

    DID_REJOIN = 1 << 0
    """Member has left and rejoined the guild"""
    COMPLETED_ONBOARDING = 1 << 1
    """Member has completed onboarding"""
    BYPASSES_VERIFICATION = 1 << 2
    """Member is exempt from guild verification requirements"""
    STARTED_ONBOARDING = 1 << 3
    """Member has started onboarding"""


class GuildNSFWLevel(IntEnum):
    """Guild NSFW level.

    see https://discord.com/developers/docs/resources/guild#guild-object-guild-nsfw-level
    """

    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class GuildScheduledEventEntityType(IntEnum):
    """Guild Scheduled Event Entity Type

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-types
    """

    STAGE_INSTANCE = 1
    VOICE = 2
    EXTERNAL = 3


class GuildScheduledEventPrivacyLevel(IntEnum):
    """Guild Scheduled Event Privacy Level

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-privacy-level
    """

    GUILD_ONLY = 2


class GuildScheduledEventRecurrenceRuleFrequency(IntEnum):
    """Guild Scheduled Event Recurrence Rule - Frequency

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object-guild-scheduled-event-recurrence-rule-frequency
    """

    YEARLY = 0
    MONTHLY = 1
    WEEKLY = 2
    DAILY = 3


class GuildScheduledEventRecurrenceRuleMonth(IntEnum):
    """Guild Scheduled Event Recurrence Rule - Month

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object-guild-scheduled-event-recurrence-rule-month
    """

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class GuildScheduledEventRecurrenceRuleWeekday(IntEnum):
    """Guild Scheduled Event Recurrence Rule - Weekday

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-recurrence-rule-object-guild-scheduled-event-recurrence-rule-weekday
    """

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class GuildScheduledEventStatus(IntEnum):
    """Guild Scheduled Event Status

    Once status is set to COMPLETED or CANCELED, the status can no longer be updated.

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-status
    """

    SCHEDULED = 1
    ACTIVE = 2
    COMPLETED = 3
    CANCELED = 4


class IntegrationExpireBehaviors(IntEnum):
    """Integration Expire Behaviors

    see https://discord.com/developers/docs/resources/guild#integration-object-integration-expire-behaviors
    """

    RemoveRole = 0
    Kick = 1


class MFALevel(IntEnum):
    """MFA level.

    see https://discord.com/developers/docs/resources/guild#guild-object-mfa-level"""

    NONE = 0
    """guild has no MFA/2FA requirement for moderation actions"""
    ELEVATED = 1
    """guild has a 2FA requirement for moderation actions"""


class MutableGuildFeature(StrEnum):
    """Mutable guild feature.

    see https://discord.com/developers/docs/resources/guild#guild-object-mutable-guild-features
    """

    COMMUNITY = "COMMUNITY"
    """Enables Community Features in the guild"""
    DISCOVERABLE = "DISCOVERABLE"
    """Enables discovery in the guild, making it publicly listed"""
    INVITES_DISABLED = "INVITES_DISABLED"
    """Pauses all invites/access to the server"""
    RAID_ALERTS_DISABLED = "RAID_ALERTS_DISABLED"
    """Disables alerts for join raids"""


class OnboardingMode(IntEnum):
    """Defines the criteria used to satisfy Onboarding constraints that are required for enabling.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-mode
    """

    ONBOARDING_DEFAULT = 0
    """Counts only Default Channels towards constraints"""
    ONBOARDING_ADVANCED = 1
    """Counts Default Channels and Questions towards constraints"""


class OnboardingPromptType(IntEnum):
    """Onboarding prompt type.

    see https://discord.com/developers/docs/resources/guild#guild-onboarding-object-prompt-types
    """

    MULTIPLE_CHOICE = 0
    DROPDOWN = 1


class PremiumTier(IntEnum):
    """Premium tier.

    see https://discord.com/developers/docs/resources/guild#guild-object-premium-tier"""

    NONE = 0
    """guild has not unlocked any Server Boost perks"""
    TIER_1 = 1
    """guild has unlocked Server Boost level 1 perks"""
    TIER_2 = 2
    """guild has unlocked Server Boost level 2 perks"""
    TIER_3 = 3
    """guild has unlocked Server Boost level 3 perks"""


class RoleFlag(IntFlag):
    """Role Flags

    see https://discord.com/developers/docs/topics/permissions#role-object-role-flags
    """

    IN_PROMPT = 1 << 0
    """role can be selected by members in an onboarding prompt"""


class SystemChannelFlags(IntFlag):
    """System channel flags.

    see https://discord.com/developers/docs/resources/guild#guild-object-system-channel-flags
    """

    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    """Suppress member join notifications"""
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    """Suppress server boost notifications"""
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    """Suppress server setup tips"""
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3
    """Hide member join sticker reply buttons"""
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATIONS = 1 << 4
    """Suppress role subscription purchase and renewal notifications"""
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATION_REPLIES = 1 << 5
    """Hide role subscription sticker reply buttons"""


class VerificationLevel(IntEnum):
    """Verification level.

    see https://discord.com/developers/docs/resources/guild#guild-object-verification-level
    """

    NONE = 0
    """unrestricted"""
    LOW = 1
    """must have verified email on account"""
    MEDIUM = 2
    """must be registered on Discord for longer than 5 minutes"""
    HIGH = 3
    """must be a member of the server for longer than 10 minutes"""
    VERY_HIGH = 4
    """must have a verified phone number"""


__all__ = [
    "DefaultMessageNotificationLevel",
    "ExplicitContentFilterLevel",
    "GuildFeature",
    "GuildMemberFlags",
    "GuildNSFWLevel",
    "GuildScheduledEventEntityType",
    "GuildScheduledEventPrivacyLevel",
    "GuildScheduledEventRecurrenceRuleFrequency",
    "GuildScheduledEventRecurrenceRuleMonth",
    "GuildScheduledEventRecurrenceRuleWeekday",
    "GuildScheduledEventStatus",
    "IntegrationExpireBehaviors",
    "MFALevel",
    "MutableGuildFeature",
    "OnboardingMode",
    "OnboardingPromptType",
    "PremiumTier",
    "RoleFlag",
    "SystemChannelFlags",
    "VerificationLevel",
]
