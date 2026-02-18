from enum import Enum, IntEnum, IntFlag
from typing import Literal, TypeAlias, TypeVar, final
from typing_extensions import TypeIs, override

T = TypeVar("T")


class _UNSET(type):
    @override
    def __str__(cls) -> Literal["<UNSET>"]:
        return "<UNSET>"

    @override
    def __repr__(cls) -> Literal["<UNSET>"]:
        return "<UNSET>"

    def __bool__(cls) -> Literal[False]:
        return False


@final
class UNSET(metaclass=_UNSET):
    """UNSET means that the field maybe not given in the data.

    see https://discord.com/developers/docs/reference#nullable-and-optional-resource-fields"""


UnsetType: TypeAlias = type[UNSET]

Missing: TypeAlias = UnsetType | T
"""Missing means that the field maybe not given in the data.

Missing[T] equal to UnsetType | T.

example: Missing[int] == UnsetType | int

see https://discord.com/developers/docs/reference#nullable-and-optional-resource-fields"""

MissingOrNullable: TypeAlias = UnsetType | T | None
"""MissingOrNullable means that the field maybe not given in the data or value is None.

MissingOrNullable[T] equal to UnsetType | T | None.

example: MissingOrNullable[int] == UnsetType | int | None

see https://discord.com/developers/docs/reference#nullable-and-optional-resource-fields"""


def is_unset(value: object) -> TypeIs[UnsetType]:
    """Check if the value is UNSET."""
    return value is UNSET


def is_not_unset(value: T | UnsetType) -> TypeIs[T]:
    """Check if the value is not UNSET."""
    return value is not UNSET


class StrEnum(str, Enum):
    """String enum.

    see https://discord.com/developers/docs/reference#nullable-and-optional-resource-fields
    """


class ActivityAssetImage(StrEnum):
    """Activity Asset Image

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-asset-image
    """

    ApplicationAsset = "Application Asset"
    """{application_asset_id} see https://discord.com/developers/docs/reference#image-formatting"""
    MediaProxyImage = "Media Proxy Image"
    """mp:{image_id}"""


class ActivityFlags(IntFlag):
    """Activity Flags

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-flags
    """

    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5
    PARTY_PRIVACY_FRIENDS = 1 << 6
    PARTY_PRIVACY_VOICE_CHANNEL = 1 << 7
    EMBEDDED = 1 << 8


class ActivityType(IntEnum):
    """Activity Type

    see https://discord.com/developers/docs/topics/gateway-events#activity-object-activity-types
    """

    Game = 0
    """Playing {name}"""
    Streaming = 1
    """Streaming {details}"""
    Listening = 2
    """Listening to {name}"""
    Watching = 3
    """Watching {name}"""
    Custom = 4
    """{emoji} {name}"""
    Competing = 5
    """	Competing in {name}"""


class AnimationType(IntEnum):
    """Animation Type

    see https://discord.com/developers/docs/topics/gateway-events#voice-channel-effect-send-animation-types
    """

    PREMIUM = 0
    """A fun animation, sent by a Nitro subscriber"""
    BASIC = 1
    """The standard animation"""


class ApplicationCommandOptionType(IntEnum):
    """Application Command Option Type

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type
    """

    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    """Any integer between -2^53 and 2^53"""
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    """Includes all channel types + categories"""
    ROLE = 8
    MENTIONABLE = 9
    """Includes users and roles"""
    NUMBER = 10
    """Any double between -2^53 and 2^53"""
    ATTACHMENT = 11
    """attachment object"""


class ApplicationCommandPermissionsType(IntEnum):
    """Application command permissions type.

    see https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-application-command-permission-type
    """

    ROLE = 1
    USER = 2
    CHANNEL = 3


class ApplicationCommandType(IntEnum):
    """Application Command Type

    see https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-types
    """

    CHAT_INPUT = 1
    """Slash commands; a text-based command that shows up when a user types /"""
    USER = 2
    """A UI-based command that shows up when you right click or tap on a user"""
    MESSAGE = 3
    """A UI-based command that shows up when you right click or tap on a message"""


class ApplicationFlag(IntFlag):
    """Application flags.

    see https://discord.com/developers/docs/resources/application#application-object-application-flags
    """

    APPLICATION_AUTO_MODERATION_RULE_CREATE_BADGE = 1 << 6
    """Indicates if an app uses the Auto Moderation API"""
    GATEWAY_PRESENCE = 1 << 12
    """Intent required for bots in 100 or more servers
    to receive presence_update events"""
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    """Intent required for bots in under 100 servers to receive presence_update events,
    found on the Bot page in your app's settings"""
    GATEWAY_GUILD_MEMBERS = 1 << 14
    """Intent required for bots in 100 or more servers to
    receive member-related events like guild_member_add.
    See the list of member-related events under GUILD_MEMBERS"""
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    """Intent required for bots in under 100 servers to receive member-related events
    like guild_member_add, found on the Bot page in your app's settings.
    See the list of member-related events under GUILD_MEMBERS"""
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    """Indicates unusual growth of an app that prevents verification"""
    EMBEDDED = 1 << 17
    """Indicates if an app is embedded within the
    Discord client (currently unavailable publicly)"""
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    """Intent required for bots in 100 or more servers to receive message content"""
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    """Intent required for bots in under 100 servers to receive message content,
    found on the Bot page in your app's settings"""
    APPLICATION_COMMAND_BADGE = 1 << 23
    """Indicates if an app has registered global application commands"""


class ApplicationIntegrationType(IntEnum):
    """Application Integration Type

    see https://discord.com/developers/docs/resources/application#application-object-application-integration-types
    """

    GUILD_INSTALL = 0
    """App is installable to servers"""
    USER_INSTALL = 1
    """App is installable to users"""


class ApplicationRoleConnectionMetadataType(IntEnum):
    """Application role connection metadata type.

    see https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object-application-role-connection-metadata-type
    """

    INTEGER_LESS_THAN_OR_EQUAL = 1
    """the metadata value (integer) is less than or equal
    to the guild's configured value (integer)"""
    INTEGER_GREATER_THAN_OR_EQUAL = 2
    """the metadata value (integer) is greater than or equal
    to the guild's configured value (integer)"""
    INTEGER_EQUAL = 3
    """the metadata value (integer) is equal to the
    guild's configured value (integer)"""
    INTEGER_NOT_EQUAL = 4
    """	the metadata value (integer) is not equal to the
    guild's configured value (integer)"""
    DATETIME_LESS_THAN_OR_EQUAL = 5
    """	the metadata value (ISO8601 string) is less than or equal
    to the guild's configured value (integer; days before current date)"""
    DATETIME_GREATER_THAN_OR_EQUAL = 6
    """the metadata value (ISO8601 string) is greater than or equal
    to the guild's configured value (integer; days before current date)"""
    BOOLEAN_EQUAL = 7
    """the metadata value (integer) is equal to the
    guild's configured value (integer; 1)"""
    BOOLEAN_NOT_EQUAL = 8
    """the metadata value (integer) is not equal to the
    guild's configured value (integer; 1)"""


class AllowedMentionType(StrEnum):
    """Allowed mentions types.

    see https://discord.com/developers/docs/resources/message#allowed-mentions-object-allowed-mention-types
    """

    RoleMentions = "roles"
    """Controls role mentions"""
    UserMentions = "users"
    """Controls user mentions"""
    EveryoneMentions = "everyone"
    """Controls @everyone and @here mentions"""


class AttachmentFlag(IntFlag):
    """Attachment Flags

    see https://discord.com/developers/docs/resources/message#attachment-object-attachment-flags
    """

    IS_REMIX = 1 << 2
    """this attachment has been edited using the remix feature on mobile"""


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


class ButtonStyle(IntEnum):
    """Button styles.

    see https://discord.com/developers/docs/interactions/message-components#button-object-button-styles
    """

    Primary = 1
    """color: blurple, required field: custom_id"""
    Secondary = 2
    """color: grey, required field: custom_id"""
    Success = 3
    """color: green, required field: custom_id"""
    Danger = 4
    """color: red, required field: custom_id"""
    Link = 5
    """color: grey, navigates to a URL, required field: url"""
    Premium = 6
    """color: blurple, required field: sku_id"""


class ChannelFlags(IntFlag):
    """Channel flags.

    see https://discord.com/developers/docs/resources/channel#channel-object-channel-flags
    """

    PINNED = 1 << 1
    """this thread is pinned to the top of its parent GUILD_FORUM channel"""
    REQUIRE_TAG = 1 << 4
    """whether a tag is required to be specified
    when creating a thread in a GUILD_FORUM channel.
    Tags are specified in the applied_tags field."""
    HIDE_MEDIA_DOWNLOAD_OPTIONS = 1 << 15
    """when set hides the embedded media download options. Available only for
    media channels"""


class ChannelType(IntEnum):
    """Channel type.

    Type ANNOUNCEMENT_THREAD(10), PUBLIC_THREAD(11) and PRIVATE_THREAD(12) are only
    available in API v9 and above.

    The GUILD_MEDIA(16) channel type is still in active development.
    Avoid implementing any features that are not documented here, since they are
    subject to change without notice!

    see https://discord.com/developers/docs/resources/channel#channel-object-channel-types
    """

    GUILD_TEXT = 0
    """a text channel within a server"""
    DM = 1
    """a direct message between users"""
    GUILD_VOICE = 2
    """a voice channel within a server"""
    GROUP_DM = 3
    """a direct message between multiple users"""
    GUILD_CATEGORY = 4
    """an organizational category that contains up to 50 channels"""
    GUILD_ANNOUNCEMENT = 5
    """a channel that users can follow and crosspost
    into their own server (formerly news channels)"""
    ANNOUNCEMENT_THREAD = 10
    """a temporary sub-channel within a GUILD_ANNOUNCEMENT channel"""
    PUBLIC_THREAD = 11
    """a temporary sub-channel within a GUILD_TEXT or GUILD_FORUM channel"""
    PRIVATE_THREAD = 12
    """a temporary sub-channel within a GUILD_TEXT channel that is only viewable by
    those invited and those with the MANAGE_THREADS permission"""
    GUILD_STAGE_VOICE = 13
    """a voice channel for hosting events with an audience"""
    GUILD_DIRECTORY = 14
    """the channel in a hub containing the listed servers"""
    GUILD_FORUM = 15
    """Channel that can only contain threads"""
    GUILD_MEDIA = 16
    """Channel that can only contain threads, similar to GUILD_FORUM channels"""


class ComponentType(IntEnum):
    """Component types.

    see https://discord.com/developers/docs/interactions/message-components#component-object-component-types
    """

    ActionRow = 1
    """Container for other components"""
    Button = 2
    """Button object"""
    StringSelect = 3
    """Select menu for picking from defined text options"""
    TextInput = 4
    """TextSegment input object"""
    UserInput = 5
    """Select menu for users"""
    RoleSelect = 6
    """Select menu for roles"""
    MentionableSelect = 7
    """Select menu for mentionables (users and roles)"""
    ChannelSelect = 8
    """Select menu for channels"""


class ConnectionServiceType(StrEnum):
    """Connection service type.

    see https://discord.com/developers/docs/resources/user#connection-object-services"""

    Battle_net = "battlenet"
    Bungie_net = "bungie"
    Domain = "domain"
    eBay = "ebay"  # noqa: N815
    Epic_Games = "epicgames"
    Facebook = "facebook"
    GitHub = "github"
    Instagram = "instagram"
    League_of_Legends = "leagueoflegends"
    PayPal = "paypal"
    PlayStation_Network = "playstation"
    Reddit = "reddit"
    Riot_Games = "riotgames"
    Roblox = "roblox"
    Spotify = "spotify"
    Skype = "skype"
    Steam = "steam"
    TikTok = "tiktok"
    Twitch = "twitch"
    Twitter = "twitter"
    Xbox_Live = "xbox"
    YouTube = "youtube"


class DefaultMessageNotificationLevel(IntEnum):
    """Default message notification level.

    see https://discord.com/developers/docs/resources/guild#guild-object-default-message-notification-level
    """

    ALL_MESSAGES = 0
    """members will receive notifications for all messages by default"""
    ONLY_MENTIONS = 1
    """members will receive notifications only for messages
    that @mention them by default"""


class EmbedTypes(StrEnum):
    """
    Embed types.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-types
    """

    rich = "rich"
    """generic embed rendered from embed attributes"""
    image = "image"
    """image embed"""
    video = "video"
    """video embed"""
    gifv = "gifv"
    """animated gif image embed rendered as a video embed"""
    article = "article"
    """article embed"""
    link = "link"
    """link embed"""
    poll_result = "poll_result"
    """poll result embed"""


class EntitlementType(IntEnum):
    """Entitlement Types

    see https://discord.com/developers/docs/monetization/entitlements#entitlement-object-entitlement-types
    """

    PURCHASE = 1
    """Entitlement was purchased by user"""
    PREMIUM_SUBSCRIPTION = 2
    """Entitlement for Discord Nitro subscription"""
    DEVELOPER_GIFT = 3
    """Entitlement was gifted by developer"""
    TEST_MODE_PURCHASE = 4
    """Entitlement was purchased by a dev in application test mode"""
    FREE_PURCHASE = 5
    """Entitlement was granted when the SKU was free"""
    USER_GIFT = 6
    """Entitlement was gifted by another user"""
    PREMIUM_PURCHASE = 7
    """Entitlement was claimed by user for free as a Nitro Subscriber"""
    APPLICATION_SUBSCRIPTION = 8
    """Entitlement was purchased as an app subscription"""


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


class ForumLayoutTypes(IntEnum):
    """Forum layout types.

    see https://discord.com/developers/docs/resources/channel#channel-object-forum-layout-types
    """

    NOT_SET = 0
    """No default has been set for forum channel"""
    LIST_VIEW = 1
    """Display posts as a list"""
    GALLERY_VIEW = 2
    """Display posts as a collection of tiles"""


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


class GuildScheduledEventStatus(IntEnum):
    """Guild Scheduled Event Status

    Once status is set to COMPLETED or CANCELED, the status can no longer be updated.

    see https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-status
    """

    SCHEDULED = 1
    ACTIVE = 2
    COMPLETED = 3
    CANCELED = 4


class InteractionContextType(IntEnum):
    """Interaction Context Type

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-context-types
    """

    GUILD = 0
    """Interaction can be used within servers"""
    BOT_DM = 1
    """Interaction can be used within DMs with the app's bot user"""
    PRIVATE_CHANNEL = 2
    """Interaction can be used within Group DMs and DMs other than the app's bot user"""


class IntegrationExpireBehaviors(IntEnum):
    """Integration Expire Behaviors

    see https://discord.com/developers/docs/resources/guild#integration-object-integration-expire-behaviors
    """

    RemoveRole = 0
    Kick = 1


class InteractionType(IntEnum):
    """Interaction type.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
    """

    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class InteractionCallbackType(IntEnum):
    """Interaction callback type.

    see https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-type
    """

    PONG = 1
    """ACK a Ping"""
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    """respond to an interaction with a message"""
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    """ACK an interaction and edit a response later, the user sees a loading state"""
    DEFERRED_UPDATE_MESSAGE = 6
    """for components, ACK an interaction and edit the original message later;
    the user does not see a loading state"""
    UPDATE_MESSAGE = 7
    """for components, edit the message the component was attached to.
    Only valid for component-based interactions"""
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    """respond to an autocomplete interaction with suggested choices"""
    MODAL = 9
    """respond to an interaction with a popup modal.
    Not available for MODAL_SUBMIT and PING interactions."""


class InviteTargetType(IntEnum):
    """Invite target type.

    see https://discord.com/developers/docs/resources/invite#invite-object-invite-target-types
    """

    STREAM = 1
    EMBEDDED_APPLICATION = 2


class InviteType(IntEnum):
    """Invite Types

    see https://discord.com/developers/docs/resources/invite#invite-object-invite-types
    """

    GUILD = 0
    GROUP_DM = 1
    FRIEND = 2


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


class MessageActivityType(IntEnum):
    """Message activity type.

    see https://discord.com/developers/docs/resources/message#message-object-message-activity-types
    """

    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageFlag(IntFlag):
    """Message flags.

    see https://discord.com/developers/docs/resources/message#message-object-message-flags
    """

    CROSSPOSTED = 1 << 0
    """this message has been published to subscribed channels (via Channel Following)"""
    IS_CROSSPOST = 1 << 1
    """this message originated from a message in
    another channel (via Channel Following)"""
    SUPPRESS_EMBEDS = 1 << 2
    """do not include any embeds when serializing this message"""
    SOURCE_MESSAGE_DELETED = 1 << 3
    """the source message for this crosspost has been deleted (via Channel Following)"""
    URGENT = 1 << 4
    """this message came from the urgent message system"""
    HAS_THREAD = 1 << 5
    """this message has an associated thread, with the same id as the message"""
    EPHEMERAL = 1 << 6
    """this message is only visible to the user who invoked the Interaction"""
    LOADING = 1 << 7
    """this message is an Interaction Response and the bot is "thinking" """
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    """this message failed to mention some roles and add their members to the thread"""
    SUPPRESS_NOTIFICATIONS = 1 << 12
    """this message will not trigger push and desktop notifications"""
    IS_VOICE_MESSAGE = 1 << 13
    """this message is a voice message"""


class MessageReferenceType(IntEnum):
    """Message Reference Types

    Determines how associated data is populated.

    see https://discord.com/developers/docs/resources/message#message-reference-types
    """

    DEFAULT = 0
    """A standard reference used by replies.
    Coupled Message Field: `referenced_message`"""
    FORWARD = 1
    """Reference used to point to a message at a point in time.
    Coupled Message Field: `message_snapshot`"""


class MessageType(IntEnum):
    """Type REPLY(19) and CHAT_INPUT_COMMAND(20) are only available in API v8 and above.
    In v6, they are represented as type DEFAULT(0).
    Additionally, type THREAD_STARTER_MESSAGE(21) is only available in API v9 and above.

    see https://discord.com/developers/docs/resources/message#message-object-message-types
    """

    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    USER_JOIN = 7
    GUILD_BOOST = 8
    GUILD_BOOST_TIER_1 = 9
    GUILD_BOOST_TIER_2 = 10
    GUILD_BOOST_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
    AUTO_MODERATION_ACTION = 24
    ROLE_SUBSCRIPTION_PURCHASE = 25
    INTERACTION_PREMIUM_UPSELL = 26
    STAGE_START = 27
    STAGE_END = 28
    STAGE_SPEAKER = 29
    STAGE_TOPIC = 31
    GUILD_APPLICATION_PREMIUM_SUBSCRIPTION = 32
    GUILD_INCIDENT_ALERT_MODE_ENABLED = 36
    GUILD_INCIDENT_ALERT_MODE_DISABLED = 37
    GUILD_INCIDENT_REPORT_RAID = 38
    GUILD_INCIDENT_REPORT_FALSE_ALARM = 39
    PURCHASE_NOTIFICATION = 44
    POLL_RESULT = 46


class MembershipState(IntEnum):
    """Membership state.

    see https://discord.com/developers/docs/topics/teams#data-models-membership-state-enum
    """

    INVITED = 1
    ACCEPTED = 2


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


class OverwriteType(IntEnum):
    """Overwrite type.

    see https://discord.com/developers/docs/resources/channel#overwrite-object"""

    ROLE = 0
    MEMBER = 1


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


class PremiumType(IntEnum):
    """Premium types denote the level of premium a user has.
    Visit the Nitro page to learn more about the premium plans we currently offer.

    see https://discord.com/developers/docs/resources/user#user-object-premium-types"""

    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
    NITRO_BASIC = 3


class PresenceStatus(StrEnum):
    """Presence Status

    see https://discord.com/developers/docs/topics/gateway-events#presence-update-presence-update-event-fields
    """

    ONLINE = "online"
    DND = "dnd"
    IDLE = "idle"
    OFFLINE = "offline"


class ReactionType(IntEnum):
    """Reaction Types

    see https://discord.com/developers/docs/resources/message#get-reactions-reaction-types
    """

    NORMAL = 0
    BURST = 1


class RoleFlag(IntFlag):
    """Role Flags

    see https://discord.com/developers/docs/topics/permissions#role-object-role-flags
    """

    IN_PROMPT = 1 << 0
    """role can be selected by members in an onboarding prompt"""


class SKUFlag(IntFlag):
    """SKUFlag

    see https://discord.com/developers/docs/resources/sku#sku-object-sku-flags
    """

    AVAILABLE = 1 << 2
    """SKU is available for purchase"""
    GUILD_SUBSCRIPTION = 1 << 7
    """Recurring SKU that can be purchased by a user and applied
    to a single server. Grants access to every user in that server."""
    USER_SUBSCRIPTION = 1 << 8
    """Recurring SKU purchased by a user for themselves.
    Grants access to the purchasing user in every server."""


class SKUType(IntEnum):
    """SKU Type

    see https://discord.com/developers/docs/resources/sku#sku-object-sku-types
    """

    DURABLE = 2
    """Durable one-time purchase"""
    CONSUMABLE = 3
    """Consumable one-time purchase"""
    SUBSCRIPTION = 5
    """Represents a recurring subscription"""
    SUBSCRIPTION_GROUP = 6
    """System-generated group for each SUBSCRIPTION SKU created"""


class SortOrderTypes(IntEnum):
    """Sort order types.

    see https://discord.com/developers/docs/resources/channel#channel-object-sort-order-types
    """

    LATEST_ACTIVITY = 0
    """Sort forum posts by activity"""
    CREATION_DATE = 1
    """Sort forum posts by creation time (from most recent to oldest)"""


class StagePrivacyLevel(IntEnum):
    """Stage Privacy Level

    see https://discord.com/developers/docs/resources/stage-instance#stage-instance-object-privacy-level
    """

    PUBLIC = 1
    """The Stage instance is visible publicly. (deprecated)"""
    GUILD_ONLY = 2
    """The Stage instance is visible to only guild members."""


class StickerFormatType(IntEnum):
    """Sticker format type.

    see https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-format-types
    """

    PNG = 1
    APNG = 2
    LOTTIE = 3
    GIF = 4


class StickerType(IntEnum):
    """Sticker type.

    see https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-types
    """

    STANDARD = 1
    """an official sticker in a pack, part of Nitro or in a removed purchasable pack"""
    GUILD = 2
    """a sticker uploaded to a guild for the guild's members"""


class SubscriptionStatus(IntEnum):
    """Subscription Statuses

    see https://discord.com/developers/docs/resources/subscription#subscription-statuses
    """

    ACTIVE = 0
    """Subscription is active and scheduled to renew."""
    ENDING = 1
    """Subscription is active but will not renew."""
    INACTIVE = 2
    """Subscription is inactive and not being charged."""


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


class TeamMemberRoleType(StrEnum):
    """Team Member Role Types

    see https://discord.com/developers/docs/topics/teams#team-member-roles"""

    Admin = "admin"
    """Admins have similar access as owners, except they cannot take
    destructive actions on the team or team-owned apps."""
    Developer = "developer"
    """Developers can access information about team-owned apps,
    like the client secret or public key. They can also take limited
    actions on team-owned apps, like configuring interaction endpoints or
    resetting the bot token. Members with the Developer role cannot manage
    the team or its members, or take destructive actions on team-owned apps."""
    Read_only = "read_only"
    """Read-only members can access information about a team and
    any team-owned apps. Some examples include getting the IDs of
    applications and exporting payout records. Members can also
    invite bots associated with team-owned apps that are marked private."""


class TextInputStyle(IntEnum):
    """TextSegment input style.

    see https://discord.com/developers/docs/interactions/message-components#text-input-object-text-input-styles
    """

    Short = 1
    """Single-line input"""
    Paragraph = 2
    """Multi-line input"""


class TimeStampStyle(Enum):
    """Timestamp style.

    see https://discord.com/developers/docs/reference#message-formatting-timestamp-styles
    """

    ShortTime = "t"
    """16:20"""
    LongTime = "T"
    """16:20:30"""
    ShortDate = "d"
    """20/04/2021"""
    LongDate = "D"
    """20 April 2021"""
    ShortDateTime = "f"
    """20 April 2021 16:20"""
    LongDateTime = "F"
    """Tuesday, 20 April 2021 16:20"""
    RelativeTime = "R"
    """2 months ago"""


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


class UpdatePresenceStatusType(StrEnum):
    """Update Presence Status type.

    see https://discord.com/developers/docs/topics/gateway-events#update-presence-status-types
    """

    online = "online"
    """Online"""
    dnd = "dnd"
    """Do Not Disturb"""
    idle = "idle"
    """AFK"""
    invisible = "invisible"
    """Invisible and shown as offline"""
    offline = "offline"
    """	Offline"""


class UserFlags(IntFlag):
    """User flags denote certain attributes about a user.
    These flags are only available to bots.

    see https://discord.com/developers/docs/resources/user#user-object-user-flags"""

    STAFF = 1 << 0
    """Discord Employee"""
    PARTNER = 1 << 1
    """Partnered Server Owner"""
    HYPESQUAD = 1 << 2
    """HypeSquad Events Member"""
    BUG_HUNTER_LEVEL_1 = 1 << 3
    """Bug Hunter Level 1"""
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    """House Bravery Member"""
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    """House Brilliance Member"""
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    """House Balance Member"""
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    """Early Nitro Supporter"""
    TEAM_PSEUDO_USER = 1 << 10
    """User is a team"""
    BUG_HUNTER_LEVEL_2 = 1 << 14
    """Bug Hunter Level 2"""
    VERIFIED_BOT = 1 << 16
    """Verified Bot"""
    VERIFIED_DEVELOPER = 1 << 17
    """Early Verified Bot Developer"""
    CERTIFIED_MODERATOR = 1 << 18
    """Moderator Programs Alumni"""
    BOT_HTTP_INTERACTIONS = 1 << 19
    """Bot uses only HTTP interactions and is shown in the online member list"""
    ACTIVE_DEVELOPER = 1 << 22
    """User is an Active Developer"""


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


class VideoQualityMode(IntEnum):
    """Video quality mode.

    see https://discord.com/developers/docs/resources/channel#channel-object-video-quality-modes
    """

    AUTO = 1
    """Discord chooses the quality for optimal performance"""
    FULL = 2
    """720p"""


class VisibilityType(IntEnum):
    """Visibility type.

    see https://discord.com/developers/docs/resources/user#connection-object-visibility-types
    """

    NONE = 0
    """invisible to everyone except the user themselves"""
    EVERYONE = 1
    """visible to everyone"""


class WebhookType(IntEnum):
    """Webhook type.

    see https://discord.com/developers/docs/resources/webhook#webhook-object-webhook-types
    """

    Incoming = 1
    """	Incoming Webhooks can post messages to channels with a generated token"""
    Channel_Follower = 2
    """	Channel Follower Webhooks are internal webhooks used with Channel
    Following to post new messages into channels"""
    Application = 3
    """Application webhooks are webhooks used with Interactions"""


__all__ = [
    "UNSET",
    "ActivityAssetImage",
    "ActivityFlags",
    "ActivityType",
    "AllowedMentionType",
    "AnimationType",
    "ApplicationCommandOptionType",
    "ApplicationCommandPermissionsType",
    "ApplicationCommandType",
    "ApplicationFlag",
    "ApplicationIntegrationType",
    "ApplicationRoleConnectionMetadataType",
    "AttachmentFlag",
    "AuditLogEventType",
    "AutoModerationActionType",
    "AutoModerationRuleEventType",
    "ButtonStyle",
    "ChannelFlags",
    "ChannelType",
    "ComponentType",
    "ConnectionServiceType",
    "DefaultMessageNotificationLevel",
    "EmbedTypes",
    "EntitlementType",
    "ExplicitContentFilterLevel",
    "ForumLayoutTypes",
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
    "InteractionCallbackType",
    "InteractionContextType",
    "InteractionType",
    "InviteTargetType",
    "InviteType",
    "KeywordPresetType",
    "MFALevel",
    "MembershipState",
    "MessageActivityType",
    "MessageFlag",
    "MessageReferenceType",
    "MessageType",
    "Missing",
    "MissingOrNullable",
    "MutableGuildFeature",
    "OnboardingMode",
    "OnboardingPromptType",
    "OverwriteType",
    "PremiumTier",
    "PremiumType",
    "PresenceStatus",
    "ReactionType",
    "RoleFlag",
    "SKUFlag",
    "SKUType",
    "SortOrderTypes",
    "StagePrivacyLevel",
    "StickerFormatType",
    "StickerType",
    "SubscriptionStatus",
    "SystemChannelFlags",
    "TeamMemberRoleType",
    "TextInputStyle",
    "TimeStampStyle",
    "TriggerType",
    "UpdatePresenceStatusType",
    "UserFlags",
    "VerificationLevel",
    "VideoQualityMode",
    "VisibilityType",
    "WebhookType",
]
