"""Internal canonical model namespace; never a public compatibility facade."""

from importlib import import_module
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel

from . import _types as _types_module
from .. import protocol as _protocol

if TYPE_CHECKING:
    import pydantic as _static_pydantic

    from .application import (
        gateway as _static_application_gateway,
        read as _static_application_read,
        types as _static_application_types,
        write as _static_application_write,
    )
    from .channel import (
        gateway as _static_channel_gateway,
        read as _static_channel_read,
        types as _static_channel_types,
        write as _static_channel_write,
    )
    from .command import (
        read as _static_command_read,
        types as _static_command_types,
        write as _static_command_write,
    )
    from .component import (
        read as _static_component_read,
        types as _static_component_types,
    )
    from .emoji import read as _static_emoji_read, write as _static_emoji_write
    from .gateway import (
        read as _static_gateway_read,
        types as _static_gateway_types,
        write as _static_gateway_write,
    )
    from .guild import (
        gateway as _static_guild_gateway,
        read as _static_guild_read,
        types as _static_guild_types,
        write as _static_guild_write,
    )
    from .interaction import (
        read as _static_interaction_read,
        types as _static_interaction_types,
        write as _static_interaction_write,
    )
    from .invite import (
        gateway as _static_invite_gateway,
        read as _static_invite_read,
        types as _static_invite_types,
    )
    from .lobby import (
        read as _static_lobby_read,
        types as _static_lobby_types,
        write as _static_lobby_write,
    )
    from .lobby.write import (
        _LobbyMemberWriteParamsBase as _static_lobby_member_write_params_base,
    )
    from .message import (
        read as _static_message_read,
        types as _static_message_types,
        write as _static_message_write,
    )
    from .moderation import (
        gateway as _static_moderation_gateway,
        read as _static_moderation_read,
        types as _static_moderation_types,
        write as _static_moderation_write,
    )
    from .soundboard import (
        read as _static_soundboard_read,
        write as _static_soundboard_write,
    )
    from .soundboard.read import (
        _SoundboardSoundsListResponse as _static_soundboard_sounds_list_response,
    )
    from .sticker import (
        read as _static_sticker_read,
        types as _static_sticker_types,
        write as _static_sticker_write,
    )
    from .user import (
        gateway as _static_user_gateway,
        read as _static_user_read,
        types as _static_user_types,
        write as _static_user_write,
    )
    from .voice import (
        gateway as _static_voice_gateway,
        read as _static_voice_read,
        types as _static_voice_types,
        write as _static_voice_write,
    )
    from .webhook import (
        gateway as _static_webhook_gateway,
        read as _static_webhook_read,
        types as _static_webhook_types,
        write as _static_webhook_write,
    )
    from .. import protocol as _static_protocol

    SKU = _static_application_read.SKU
    ActionRow = _static_component_read.ActionRow
    Activity = _static_message_read.Activity
    ActivityAssets = _static_gateway_read.ActivityAssets
    ActivityButtons = _static_gateway_read.ActivityButtons
    ActivityEmoji = _static_gateway_read.ActivityEmoji
    ActivityInstance = _static_gateway_read.ActivityInstance
    ActivityLocation = _static_gateway_read.ActivityLocation
    ActivityParty = _static_gateway_read.ActivityParty
    ActivitySecrets = _static_gateway_read.ActivitySecrets
    ActivityTimestamps = _static_gateway_read.ActivityTimestamps
    AddLobbyMemberParams = _static_lobby_write.AddLobbyMemberParams
    AllowedMention = _static_message_read.AllowedMention
    AnswerVoters = _static_message_read.AnswerVoters
    AnyCommandOption = _static_command_read.AnyCommandOption
    Application = _static_application_read.Application
    ApplicationCommand = _static_command_read.ApplicationCommand
    ApplicationCommandBulkOverwriteParams = (
        _static_command_write.ApplicationCommandBulkOverwriteParams
    )
    ApplicationCommandCreate = _static_command_write.ApplicationCommandCreate
    ApplicationCommandData = _static_interaction_read.ApplicationCommandData
    ApplicationCommandEditParams = _static_command_write.ApplicationCommandEditParams
    ApplicationCommandInteractionDataOption = (
        _static_interaction_read.ApplicationCommandInteractionDataOption
    )
    ApplicationCommandOption = _static_command_read.ApplicationCommandOption
    ApplicationCommandOptionChoice = _static_command_read.ApplicationCommandOptionChoice
    ApplicationCommandPermissions = _static_command_read.ApplicationCommandPermissions
    ApplicationEmojis = _static_emoji_read.ApplicationEmojis
    ApplicationIntegrationTypeConfiguration = (
        _static_application_read.ApplicationIntegrationTypeConfiguration
    )
    ApplicationReady = _static_application_read.ApplicationReady
    ApplicationRoleConnection = _static_application_read.ApplicationRoleConnection
    ApplicationRoleConnectionMetadata = (
        _static_application_read.ApplicationRoleConnectionMetadata
    )
    ArchivedThreadsResponse = _static_channel_read.ArchivedThreadsResponse
    Attachment = _static_message_read.Attachment
    AttachmentOption = _static_command_read.AttachmentOption
    AttachmentSend = _static_message_write.AttachmentSend
    AuditLog = _static_moderation_read.AuditLog
    AuditLogChange = _static_moderation_read.AuditLogChange
    AuditLogChangeException = _static_moderation_read.AuditLogChangeException
    AuditLogEntry = _static_moderation_read.AuditLogEntry
    AuthorizationResponse = _static_application_read.AuthorizationResponse
    AutoModerationAction = _static_moderation_read.AutoModerationAction
    AutoModerationActionExecution = (
        _static_moderation_gateway.AutoModerationActionExecution
    )
    AutoModerationActionMetadata = _static_moderation_read.AutoModerationActionMetadata
    AutoModerationRule = _static_moderation_read.AutoModerationRule
    AutoModerationRuleCreate = _static_moderation_gateway.AutoModerationRuleCreate
    AutoModerationRuleDelete = _static_moderation_gateway.AutoModerationRuleDelete
    AutoModerationRuleUpdate = _static_moderation_gateway.AutoModerationRuleUpdate
    AvatarDecorationData = _static_user_read.AvatarDecorationData
    Ban = _static_guild_read.Ban
    BaseModel = _static_pydantic.BaseModel
    BooleanOption = _static_command_read.BooleanOption
    BulkBan = _static_moderation_read.BulkBan
    Button = _static_component_read.Button
    Channel = _static_channel_read.Channel
    ChannelCreate = _static_channel_gateway.ChannelCreate
    ChannelDelete = _static_channel_gateway.ChannelDelete
    ChannelMention = _static_channel_read.ChannelMention
    ChannelOption = _static_command_read.ChannelOption
    ChannelPinsUpdate = _static_channel_gateway.ChannelPinsUpdate
    ChannelUpdate = _static_channel_gateway.ChannelUpdate
    ClientStatus = _static_gateway_read.ClientStatus
    CommandOptionBase = _static_command_read.CommandOptionBase
    Component = _static_component_read.Component
    ComponentEmoji = _static_component_read.ComponentEmoji
    Connection = _static_user_read.Connection
    CountDetails = _static_channel_read.CountDetails
    CreateAndModifyAutoModerationRuleParams = (
        _static_moderation_write.CreateAndModifyAutoModerationRuleParams
    )
    CreateGuildChannelParams = _static_guild_write.CreateGuildChannelParams
    CreateGuildParams = _static_guild_write.CreateGuildParams
    CreateGuildRoleParams = _static_guild_write.CreateGuildRoleParams
    CreateGuildScheduledEventParams = (
        _static_guild_write.CreateGuildScheduledEventParams
    )
    CreateGuildSoundboardSoundParams = (
        _static_soundboard_write.CreateGuildSoundboardSoundParams
    )
    CreateGuildTemplateParams = _static_guild_write.CreateGuildTemplateParams
    CreateLobbyMemberParams = _static_lobby_write.CreateLobbyMemberParams
    CreateLobbyParams = _static_lobby_write.CreateLobbyParams
    CreateWebhookParams = _static_webhook_write.CreateWebhookParams
    CurrentUserGuild = _static_guild_read.CurrentUserGuild
    DefaultReaction = _static_channel_read.DefaultReaction
    DirectComponent = _static_component_read.DirectComponent
    EditCurrentApplicationParams = (
        _static_application_write.EditCurrentApplicationParams
    )
    Embed = _static_message_read.Embed
    EmbedAuthor = _static_message_read.EmbedAuthor
    EmbedField = _static_message_read.EmbedField
    EmbedFooter = _static_message_read.EmbedFooter
    EmbedImage = _static_message_read.EmbedImage
    EmbedProvider = _static_message_read.EmbedProvider
    EmbedThumbnail = _static_message_read.EmbedThumbnail
    EmbedVideo = _static_message_read.EmbedVideo
    Emoji = _static_emoji_read.Emoji
    Entitlement = _static_application_read.Entitlement
    EntitlementCreate = _static_application_gateway.EntitlementCreate
    EntitlementDelete = _static_application_gateway.EntitlementDelete
    EntitlementUpdate = _static_application_gateway.EntitlementUpdate
    ExecuteWebhookParams = _static_webhook_write.ExecuteWebhookParams
    File = _static_message_read.File
    FollowedChannel = _static_channel_read.FollowedChannel
    ForumTag = _static_channel_read.ForumTag
    ForumTagRequest = _static_channel_read.ForumTagRequest
    Gateway = _static_gateway_read.Gateway
    GatewayBot = _static_gateway_read.GatewayBot
    Guild = _static_guild_read.Guild
    GuildApplicationCommandPermissions = (
        _static_command_read.GuildApplicationCommandPermissions
    )
    GuildAuditLogEntryCreate = _static_moderation_gateway.GuildAuditLogEntryCreate
    GuildBanAdd = _static_guild_gateway.GuildBanAdd
    GuildBanRemove = _static_guild_gateway.GuildBanRemove
    GuildCreate = _static_guild_gateway.GuildCreate
    GuildCreateCompat = _static_guild_gateway.GuildCreateCompat
    GuildCreateCompatChannel = _static_guild_gateway.GuildCreateCompatChannel
    GuildCreateCompatOverwrite = _static_guild_gateway.GuildCreateCompatOverwrite
    GuildCreateCompatRole = _static_guild_gateway.GuildCreateCompatRole
    GuildDelete = _static_guild_gateway.GuildDelete
    GuildEmojisUpdate = _static_guild_gateway.GuildEmojisUpdate
    GuildIncidentsData = _static_guild_read.GuildIncidentsData
    GuildIntegrationsUpdate = _static_guild_gateway.GuildIntegrationsUpdate
    GuildMember = _static_guild_read.GuildMember
    GuildMemberAdd = _static_guild_gateway.GuildMemberAdd
    GuildMemberRemove = _static_guild_gateway.GuildMemberRemove
    GuildMemberUpdate = _static_guild_gateway.GuildMemberUpdate
    GuildMembersChunk = _static_guild_gateway.GuildMembersChunk
    GuildOnboarding = _static_guild_read.GuildOnboarding
    GuildPreview = _static_guild_read.GuildPreview
    GuildRoleCreate = _static_guild_gateway.GuildRoleCreate
    GuildRoleDelete = _static_guild_gateway.GuildRoleDelete
    GuildRoleUpdate = _static_guild_gateway.GuildRoleUpdate
    GuildScheduledEvent = _static_guild_read.GuildScheduledEvent
    GuildScheduledEventCreate = _static_guild_gateway.GuildScheduledEventCreate
    GuildScheduledEventDelete = _static_guild_gateway.GuildScheduledEventDelete
    GuildScheduledEventEntityMetadata = (
        _static_guild_read.GuildScheduledEventEntityMetadata
    )
    GuildScheduledEventRecurrenceRuleN_WeekdayStructure = (
        _static_guild_read.GuildScheduledEventRecurrenceRuleN_WeekdayStructure
    )
    GuildScheduledEventUpdate = _static_guild_gateway.GuildScheduledEventUpdate
    GuildScheduledEventUser = _static_guild_read.GuildScheduledEventUser
    GuildScheduledEventUserAdd = _static_guild_gateway.GuildScheduledEventUserAdd
    GuildScheduledEventUserRemove = _static_guild_gateway.GuildScheduledEventUserRemove
    GuildStickersUpdate = _static_guild_gateway.GuildStickersUpdate
    GuildTemplate = _static_guild_read.GuildTemplate
    GuildTemplateGuild = _static_guild_read.GuildTemplateGuild
    GuildTemplateGuildChannel = _static_guild_read.GuildTemplateGuildChannel
    GuildTemplateGuildRole = _static_guild_read.GuildTemplateGuildRole
    GuildUpdate = _static_guild_gateway.GuildUpdate
    GuildVanityURL = _static_guild_read.GuildVanityURL
    GuildWidget = _static_guild_read.GuildWidget
    GuildWidgetChannel = _static_guild_read.GuildWidgetChannel
    GuildWidgetSettings = _static_guild_read.GuildWidgetSettings
    GuildWidgetUser = _static_guild_read.GuildWidgetUser
    Hello = _static_gateway_read.Hello
    Identify = _static_gateway_write.Identify
    IdentifyConnectionProperties = _static_gateway_write.IdentifyConnectionProperties
    InstallParams = _static_application_read.InstallParams
    IntegerOption = _static_command_read.IntegerOption
    Integration = _static_guild_read.Integration
    IntegrationAccount = _static_guild_read.IntegrationAccount
    IntegrationApplication = _static_guild_read.IntegrationApplication
    IntegrationCreate = _static_guild_gateway.IntegrationCreate
    IntegrationDelete = _static_guild_gateway.IntegrationDelete
    IntegrationUpdate = _static_guild_gateway.IntegrationUpdate
    InteractionCallbackAutocomplete = (
        _static_interaction_write.InteractionCallbackAutocomplete
    )
    InteractionCallbackData = _static_interaction_write.InteractionCallbackData
    InteractionCallbackMessage = _static_interaction_write.InteractionCallbackMessage
    InteractionCallbackModal = _static_interaction_write.InteractionCallbackModal
    InteractionData = _static_interaction_read.InteractionData
    InteractionGuild = _static_interaction_read.InteractionGuild
    InteractionResponse = _static_interaction_read.InteractionResponse
    Invite = _static_invite_read.Invite
    InviteCreate = _static_invite_gateway.InviteCreate
    InviteDelete = _static_invite_gateway.InviteDelete
    InviteGuild = _static_invite_read.InviteGuild
    InviteMetadata = _static_invite_read.InviteMetadata
    InviteStageInstance = _static_invite_read.InviteStageInstance
    InviteTargetUsersJobStatus = _static_invite_read.InviteTargetUsersJobStatus
    LinkChannelToLobbyParams = _static_lobby_write.LinkChannelToLobbyParams
    ListActiveGuildThreadsResponse = _static_guild_read.ListActiveGuildThreadsResponse
    ListDefaultSoundboardSoundsResponse = (
        _static_soundboard_read.ListDefaultSoundboardSoundsResponse
    )
    ListGuildSoundboardSoundsResponse = (
        _static_soundboard_read.ListGuildSoundboardSoundsResponse
    )
    Lobby = _static_lobby_read.Lobby
    LobbyMember = _static_lobby_read.LobbyMember
    MembershipScreening = _static_guild_read.MembershipScreening
    MentionableOption = _static_command_read.MentionableOption
    MessageActivity = _static_message_read.MessageActivity
    MessageCall = _static_message_read.MessageCall
    MessageComponentData = _static_interaction_read.MessageComponentData
    MessageEditParams = _static_message_write.MessageEditParams
    MessageGet = _static_message_read.MessageGet
    MessageInteraction = _static_message_read.MessageInteraction
    MessageInteractionMetadata = _static_message_read.MessageInteractionMetadata
    MessageReference = _static_message_read.MessageReference
    MessageSend = _static_message_write.MessageSend
    MessageSnapshot = _static_message_read.MessageSnapshot
    MessageSnapshotMessage = _static_message_read.MessageSnapshotMessage
    ModalSubmitData = _static_interaction_read.ModalSubmitData
    ModifyChannelParams = _static_channel_write.ModifyChannelParams
    ModifyCurrentMemberParams = _static_guild_write.ModifyCurrentMemberParams
    ModifyCurrentUserParams = _static_user_write.ModifyCurrentUserParams
    ModifyCurrentUserVoiceStateParams = (
        _static_voice_write.ModifyCurrentUserVoiceStateParams
    )
    ModifyGuildChannelPositionParams = (
        _static_channel_write.ModifyGuildChannelPositionParams
    )
    ModifyGuildEmojiParams = _static_emoji_write.ModifyGuildEmojiParams
    ModifyGuildIncidentActionsParams = (
        _static_guild_write.ModifyGuildIncidentActionsParams
    )
    ModifyGuildMemberParams = _static_guild_write.ModifyGuildMemberParams
    ModifyGuildOnboardingParams = _static_guild_write.ModifyGuildOnboardingParams
    ModifyGuildParams = _static_guild_write.ModifyGuildParams
    ModifyGuildRoleParams = _static_guild_write.ModifyGuildRoleParams
    ModifyGuildRolePositionParams = _static_guild_write.ModifyGuildRolePositionParams
    ModifyGuildScheduledEventParams = (
        _static_guild_write.ModifyGuildScheduledEventParams
    )
    ModifyGuildSoundboardSoundParams = (
        _static_soundboard_write.ModifyGuildSoundboardSoundParams
    )
    ModifyGuildStickerParams = _static_sticker_write.ModifyGuildStickerParams
    ModifyGuildTemplateParams = _static_guild_write.ModifyGuildTemplateParams
    ModifyGuildWelcomeScreenParams = _static_guild_write.ModifyGuildWelcomeScreenParams
    ModifyGuildWidgetParams = _static_guild_write.ModifyGuildWidgetParams
    ModifyLobbyParams = _static_lobby_write.ModifyLobbyParams
    ModifyThreadParams = _static_channel_write.ModifyThreadParams
    NumberOption = _static_command_read.NumberOption
    OnboardingPrompt = _static_guild_read.OnboardingPrompt
    OnboardingPromptOption = _static_guild_read.OnboardingPromptOption
    OptionChoice = _static_command_read.OptionChoice
    OptionalAuditEntryInfo = _static_moderation_read.OptionalAuditEntryInfo
    Overwrite = _static_channel_read.Overwrite
    PartialOverwrite = _static_channel_read.PartialOverwrite
    Poll = _static_message_read.Poll
    PollAnswer = _static_message_read.PollAnswer
    PollAnswerCount = _static_message_read.PollAnswerCount
    PollAnswerRequest = _static_message_write.PollAnswerRequest
    PollMedia = _static_message_read.PollMedia
    PollRequest = _static_message_write.PollRequest
    PollResults = _static_message_read.PollResults
    PresenceUpdate = _static_user_gateway.PresenceUpdate
    PresenceUpdateUser = _static_user_gateway.PresenceUpdateUser
    Reaction = _static_message_read.Reaction
    Ready = _static_gateway_read.Ready
    RecurrenceRule = _static_guild_read.RecurrenceRule
    RequestGuildMembers = _static_gateway_write.RequestGuildMembers
    ResolvedData = _static_message_read.ResolvedData
    Resume = _static_gateway_write.Resume
    Role = _static_guild_read.Role
    RoleColors = _static_guild_read.RoleColors
    RoleOption = _static_command_read.RoleOption
    RoleSubscriptionData = _static_message_read.RoleSubscriptionData
    RoleTags = _static_guild_read.RoleTags
    SelectDefaultValue = _static_component_read.SelectDefaultValue
    SelectMenu = _static_component_read.SelectMenu
    SelectMenuResolved = _static_component_read.SelectMenuResolved
    SelectOption = _static_component_read.SelectOption
    SendSoundboardSoundParams = _static_soundboard_write.SendSoundboardSoundParams
    SessionStartLimit = _static_gateway_read.SessionStartLimit
    Snowflake = _static_protocol.Snowflake
    SnowflakeType = _static_protocol.SnowflakeType
    SoundboardSound = _static_soundboard_read.SoundboardSound
    SourceChannel = _static_webhook_read.SourceChannel
    SourceGuild = _static_webhook_read.SourceGuild
    StageInstance = _static_voice_read.StageInstance
    StageInstanceCreate = _static_voice_gateway.StageInstanceCreate
    StageInstanceDelete = _static_voice_gateway.StageInstanceDelete
    StageInstanceUpdate = _static_voice_gateway.StageInstanceUpdate
    StartThreadFromMessageParams = _static_channel_write.StartThreadFromMessageParams
    StartThreadWithoutMessageParams = (
        _static_channel_write.StartThreadWithoutMessageParams
    )
    Sticker = _static_sticker_read.Sticker
    StickerItem = _static_sticker_read.StickerItem
    StickerPack = _static_sticker_read.StickerPack
    StickerPacksResponse = _static_sticker_read.StickerPacksResponse
    StringOption = _static_command_read.StringOption
    SubCommandGroupOption = _static_command_read.SubCommandGroupOption
    SubCommandOption = _static_command_read.SubCommandOption
    Subscription = _static_application_read.Subscription
    SubscriptionCreate = _static_application_gateway.SubscriptionCreate
    SubscriptionDelete = _static_application_gateway.SubscriptionDelete
    SubscriptionUpdate = _static_application_gateway.SubscriptionUpdate
    Team = _static_application_read.Team
    TeamMember = _static_application_read.TeamMember
    TeamMemberUser = _static_application_read.TeamMemberUser
    TextInput = _static_component_read.TextInput
    ThreadCreate = _static_channel_gateway.ThreadCreate
    ThreadDelete = _static_channel_gateway.ThreadDelete
    ThreadListSync = _static_channel_gateway.ThreadListSync
    ThreadMember = _static_channel_read.ThreadMember
    ThreadMemberUpdate = _static_channel_gateway.ThreadMemberUpdate
    ThreadMembersUpdate = _static_channel_gateway.ThreadMembersUpdate
    ThreadMetadata = _static_channel_read.ThreadMetadata
    ThreadUpdate = _static_channel_gateway.ThreadUpdate
    TriggerMetadata = _static_moderation_read.TriggerMetadata
    UnavailableGuild = _static_guild_read.UnavailableGuild
    UpdatePresence = _static_gateway_write.UpdatePresence
    UpdateVoiceState = _static_gateway_write.UpdateVoiceState
    User = _static_user_read.User
    UserOption = _static_command_read.UserOption
    UserUpdate = _static_user_gateway.UserUpdate
    VoiceChannelEffectSend = _static_voice_gateway.VoiceChannelEffectSend
    VoiceChannelStartTimeUpdate = _static_voice_gateway.VoiceChannelStartTimeUpdate
    VoiceChannelStatusUpdate = _static_voice_gateway.VoiceChannelStatusUpdate
    VoiceRegion = _static_voice_read.VoiceRegion
    VoiceServerUpdate = _static_voice_gateway.VoiceServerUpdate
    VoiceState = _static_voice_read.VoiceState
    VoiceStateUpdate = _static_voice_gateway.VoiceStateUpdate
    Webhook = _static_webhook_read.Webhook
    WebhookMessageEditParams = _static_webhook_write.WebhookMessageEditParams
    WebhooksUpdate = _static_webhook_gateway.WebhooksUpdate
    WelcomeScreen = _static_guild_read.WelcomeScreen
    WelcomeScreenChannel = _static_guild_read.WelcomeScreenChannel
    _LobbyMemberWriteParamsBase = _static_lobby_member_write_params_base
    _SoundboardSoundsListResponse = _static_soundboard_sounds_list_response
    UNSET = _static_protocol.UNSET
    UnsetType = _static_protocol.UnsetType
    Missing = _static_protocol.Missing
    MissingOrNullable = _static_protocol.MissingOrNullable
    is_unset = _static_protocol.is_unset
    is_not_unset = _static_protocol.is_not_unset
    ActivityAssetImage = _static_gateway_types.ActivityAssetImage
    ActivityFlags = _static_gateway_types.ActivityFlags
    ActivityType = _static_gateway_types.ActivityType
    AllowedMentionType = _static_message_types.AllowedMentionType
    AnimationType = _static_voice_types.AnimationType
    ApplicationCommandOptionType = _static_command_types.ApplicationCommandOptionType
    ApplicationCommandPermissionsType = (
        _static_command_types.ApplicationCommandPermissionsType
    )
    ApplicationCommandType = _static_command_types.ApplicationCommandType
    ApplicationFlag = _static_application_types.ApplicationFlag
    ApplicationIntegrationType = _static_application_types.ApplicationIntegrationType
    ApplicationRoleConnectionMetadataType = (
        _static_application_types.ApplicationRoleConnectionMetadataType
    )
    AttachmentFlag = _static_message_types.AttachmentFlag
    AuditLogEventType = _static_moderation_types.AuditLogEventType
    AutoModerationActionType = _static_moderation_types.AutoModerationActionType
    AutoModerationRuleEventType = _static_moderation_types.AutoModerationRuleEventType
    ButtonStyle = _static_component_types.ButtonStyle
    ChannelFlags = _static_channel_types.ChannelFlags
    ChannelType = _static_channel_types.ChannelType
    ComponentType = _static_component_types.ComponentType
    ConnectionServiceType = _static_user_types.ConnectionServiceType
    DefaultMessageNotificationLevel = (
        _static_guild_types.DefaultMessageNotificationLevel
    )
    EmbedTypes = _static_message_types.EmbedTypes
    EntitlementType = _static_application_types.EntitlementType
    ExplicitContentFilterLevel = _static_guild_types.ExplicitContentFilterLevel
    ForumLayoutTypes = _static_channel_types.ForumLayoutTypes
    GuildFeature = _static_guild_types.GuildFeature
    GuildMemberFlags = _static_guild_types.GuildMemberFlags
    GuildNSFWLevel = _static_guild_types.GuildNSFWLevel
    GuildScheduledEventEntityType = _static_guild_types.GuildScheduledEventEntityType
    GuildScheduledEventPrivacyLevel = (
        _static_guild_types.GuildScheduledEventPrivacyLevel
    )
    GuildScheduledEventRecurrenceRuleFrequency = (
        _static_guild_types.GuildScheduledEventRecurrenceRuleFrequency
    )
    GuildScheduledEventRecurrenceRuleMonth = (
        _static_guild_types.GuildScheduledEventRecurrenceRuleMonth
    )
    GuildScheduledEventRecurrenceRuleWeekday = (
        _static_guild_types.GuildScheduledEventRecurrenceRuleWeekday
    )
    GuildScheduledEventStatus = _static_guild_types.GuildScheduledEventStatus
    IntegrationExpireBehaviors = _static_guild_types.IntegrationExpireBehaviors
    InteractionCallbackType = _static_interaction_types.InteractionCallbackType
    InteractionContextType = _static_interaction_types.InteractionContextType
    InteractionType = _static_interaction_types.InteractionType
    InviteTargetType = _static_invite_types.InviteTargetType
    InviteType = _static_invite_types.InviteType
    KeywordPresetType = _static_moderation_types.KeywordPresetType
    LobbyMemberFlags = _static_lobby_types.LobbyMemberFlags
    MFALevel = _static_guild_types.MFALevel
    MembershipState = _static_application_types.MembershipState
    MessageActivityType = _static_message_types.MessageActivityType
    MessageFlag = _static_message_types.MessageFlag
    MessageReferenceType = _static_message_types.MessageReferenceType
    MessageType = _static_message_types.MessageType
    MutableGuildFeature = _static_guild_types.MutableGuildFeature
    OnboardingMode = _static_guild_types.OnboardingMode
    OnboardingPromptType = _static_guild_types.OnboardingPromptType
    OverwriteType = _static_channel_types.OverwriteType
    PremiumTier = _static_guild_types.PremiumTier
    PremiumType = _static_user_types.PremiumType
    PresenceStatus = _static_gateway_types.PresenceStatus
    ReactionType = _static_message_types.ReactionType
    RoleFlag = _static_guild_types.RoleFlag
    SKUFlag = _static_application_types.SKUFlag
    SKUType = _static_application_types.SKUType
    SortOrderTypes = _static_channel_types.SortOrderTypes
    StagePrivacyLevel = _static_voice_types.StagePrivacyLevel
    StickerFormatType = _static_sticker_types.StickerFormatType
    StickerType = _static_sticker_types.StickerType
    SubscriptionStatus = _static_application_types.SubscriptionStatus
    SystemChannelFlags = _static_guild_types.SystemChannelFlags
    TeamMemberRoleType = _static_application_types.TeamMemberRoleType
    TextInputStyle = _static_component_types.TextInputStyle
    TimeStampStyle = _static_message_types.TimeStampStyle
    TriggerType = _static_moderation_types.TriggerType
    UpdatePresenceStatusType = _static_gateway_types.UpdatePresenceStatusType
    UserFlags = _static_user_types.UserFlags
    VerificationLevel = _static_guild_types.VerificationLevel
    VideoQualityMode = _static_channel_types.VideoQualityMode
    VisibilityType = _static_user_types.VisibilityType
    WebhookType = _static_webhook_types.WebhookType

_MODEL_MODULES = tuple(
    import_module(module_name)
    for module_name in (
        "nonebot.adapters.discord.domains.application.gateway",
        "nonebot.adapters.discord.domains.application.read",
        "nonebot.adapters.discord.domains.application.write",
        "nonebot.adapters.discord.domains.channel.gateway",
        "nonebot.adapters.discord.domains.channel.read",
        "nonebot.adapters.discord.domains.channel.write",
        "nonebot.adapters.discord.domains.command.read",
        "nonebot.adapters.discord.domains.command.write",
        "nonebot.adapters.discord.domains.component.read",
        "nonebot.adapters.discord.domains.component.write",
        "nonebot.adapters.discord.domains.emoji.read",
        "nonebot.adapters.discord.domains.emoji.write",
        "nonebot.adapters.discord.domains.gateway.read",
        "nonebot.adapters.discord.domains.gateway.write",
        "nonebot.adapters.discord.domains.guild.gateway",
        "nonebot.adapters.discord.domains.guild.read",
        "nonebot.adapters.discord.domains.guild.write",
        "nonebot.adapters.discord.domains.interaction.gateway",
        "nonebot.adapters.discord.domains.interaction.read",
        "nonebot.adapters.discord.domains.interaction.write",
        "nonebot.adapters.discord.domains.invite.gateway",
        "nonebot.adapters.discord.domains.invite.read",
        "nonebot.adapters.discord.domains.lobby.read",
        "nonebot.adapters.discord.domains.lobby.write",
        "nonebot.adapters.discord.domains.message.gateway",
        "nonebot.adapters.discord.domains.message.read",
        "nonebot.adapters.discord.domains.message.write",
        "nonebot.adapters.discord.domains.moderation.gateway",
        "nonebot.adapters.discord.domains.moderation.read",
        "nonebot.adapters.discord.domains.moderation.write",
        "nonebot.adapters.discord.domains.soundboard.gateway",
        "nonebot.adapters.discord.domains.soundboard.read",
        "nonebot.adapters.discord.domains.soundboard.write",
        "nonebot.adapters.discord.domains.sticker.read",
        "nonebot.adapters.discord.domains.sticker.write",
        "nonebot.adapters.discord.domains.user.gateway",
        "nonebot.adapters.discord.domains.user.read",
        "nonebot.adapters.discord.domains.user.write",
        "nonebot.adapters.discord.domains.voice.gateway",
        "nonebot.adapters.discord.domains.voice.read",
        "nonebot.adapters.discord.domains.voice.write",
        "nonebot.adapters.discord.domains.webhook.gateway",
        "nonebot.adapters.discord.domains.webhook.read",
        "nonebot.adapters.discord.domains.webhook.write",
    )
)

_PROTOCOL_EXPORTS = (
    "UNSET",
    "Missing",
    "MissingOrNullable",
    "Snowflake",
    "SnowflakeType",
    "UnsetType",
    "is_not_unset",
    "is_unset",
)

__all__ = [
    "SKU",
    "UNSET",
    "ActionRow",
    "Activity",
    "ActivityAssetImage",
    "ActivityAssets",
    "ActivityButtons",
    "ActivityEmoji",
    "ActivityFlags",
    "ActivityInstance",
    "ActivityLocation",
    "ActivityParty",
    "ActivitySecrets",
    "ActivityTimestamps",
    "ActivityType",
    "AddLobbyMemberParams",
    "AllowedMention",
    "AllowedMentionType",
    "AnimationType",
    "AnswerVoters",
    "AnyCommandOption",
    "Application",
    "ApplicationCommand",
    "ApplicationCommandBulkOverwriteParams",
    "ApplicationCommandCreate",
    "ApplicationCommandData",
    "ApplicationCommandEditParams",
    "ApplicationCommandInteractionDataOption",
    "ApplicationCommandOption",
    "ApplicationCommandOptionChoice",
    "ApplicationCommandOptionType",
    "ApplicationCommandPermissions",
    "ApplicationCommandPermissionsType",
    "ApplicationCommandType",
    "ApplicationEmojis",
    "ApplicationFlag",
    "ApplicationIntegrationType",
    "ApplicationIntegrationTypeConfiguration",
    "ApplicationReady",
    "ApplicationRoleConnection",
    "ApplicationRoleConnectionMetadata",
    "ApplicationRoleConnectionMetadataType",
    "ArchivedThreadsResponse",
    "Attachment",
    "AttachmentFlag",
    "AttachmentOption",
    "AttachmentSend",
    "AuditLog",
    "AuditLogChange",
    "AuditLogChangeException",
    "AuditLogEntry",
    "AuditLogEventType",
    "AuthorizationResponse",
    "AutoModerationAction",
    "AutoModerationActionExecution",
    "AutoModerationActionMetadata",
    "AutoModerationActionType",
    "AutoModerationRule",
    "AutoModerationRuleCreate",
    "AutoModerationRuleDelete",
    "AutoModerationRuleEventType",
    "AutoModerationRuleUpdate",
    "AvatarDecorationData",
    "Ban",
    "BaseModel",
    "BooleanOption",
    "BulkBan",
    "Button",
    "ButtonStyle",
    "Channel",
    "ChannelCreate",
    "ChannelDelete",
    "ChannelFlags",
    "ChannelMention",
    "ChannelOption",
    "ChannelPinsUpdate",
    "ChannelType",
    "ChannelUpdate",
    "ClientStatus",
    "CommandOptionBase",
    "Component",
    "ComponentEmoji",
    "ComponentType",
    "Connection",
    "ConnectionServiceType",
    "CountDetails",
    "CreateAndModifyAutoModerationRuleParams",
    "CreateGuildChannelParams",
    "CreateGuildParams",
    "CreateGuildRoleParams",
    "CreateGuildScheduledEventParams",
    "CreateGuildSoundboardSoundParams",
    "CreateGuildTemplateParams",
    "CreateLobbyMemberParams",
    "CreateLobbyParams",
    "CreateWebhookParams",
    "CurrentUserGuild",
    "DefaultMessageNotificationLevel",
    "DefaultReaction",
    "DirectComponent",
    "EditCurrentApplicationParams",
    "Embed",
    "EmbedAuthor",
    "EmbedField",
    "EmbedFooter",
    "EmbedImage",
    "EmbedProvider",
    "EmbedThumbnail",
    "EmbedTypes",
    "EmbedVideo",
    "Emoji",
    "Entitlement",
    "EntitlementCreate",
    "EntitlementDelete",
    "EntitlementType",
    "EntitlementUpdate",
    "ExecuteWebhookParams",
    "ExplicitContentFilterLevel",
    "File",
    "FollowedChannel",
    "ForumLayoutTypes",
    "ForumTag",
    "ForumTagRequest",
    "Gateway",
    "GatewayBot",
    "Guild",
    "GuildApplicationCommandPermissions",
    "GuildAuditLogEntryCreate",
    "GuildBanAdd",
    "GuildBanRemove",
    "GuildCreate",
    "GuildCreateCompat",
    "GuildCreateCompatChannel",
    "GuildCreateCompatOverwrite",
    "GuildCreateCompatRole",
    "GuildDelete",
    "GuildEmojisUpdate",
    "GuildFeature",
    "GuildIncidentsData",
    "GuildIntegrationsUpdate",
    "GuildMember",
    "GuildMemberAdd",
    "GuildMemberFlags",
    "GuildMemberRemove",
    "GuildMemberUpdate",
    "GuildMembersChunk",
    "GuildNSFWLevel",
    "GuildOnboarding",
    "GuildPreview",
    "GuildRoleCreate",
    "GuildRoleDelete",
    "GuildRoleUpdate",
    "GuildScheduledEvent",
    "GuildScheduledEventCreate",
    "GuildScheduledEventDelete",
    "GuildScheduledEventEntityMetadata",
    "GuildScheduledEventEntityType",
    "GuildScheduledEventPrivacyLevel",
    "GuildScheduledEventRecurrenceRuleFrequency",
    "GuildScheduledEventRecurrenceRuleMonth",
    "GuildScheduledEventRecurrenceRuleN_WeekdayStructure",
    "GuildScheduledEventRecurrenceRuleWeekday",
    "GuildScheduledEventStatus",
    "GuildScheduledEventUpdate",
    "GuildScheduledEventUser",
    "GuildScheduledEventUserAdd",
    "GuildScheduledEventUserRemove",
    "GuildStickersUpdate",
    "GuildTemplate",
    "GuildTemplateGuild",
    "GuildTemplateGuildChannel",
    "GuildTemplateGuildRole",
    "GuildUpdate",
    "GuildVanityURL",
    "GuildWidget",
    "GuildWidgetChannel",
    "GuildWidgetSettings",
    "GuildWidgetUser",
    "Hello",
    "Identify",
    "IdentifyConnectionProperties",
    "InstallParams",
    "IntegerOption",
    "Integration",
    "IntegrationAccount",
    "IntegrationApplication",
    "IntegrationCreate",
    "IntegrationDelete",
    "IntegrationExpireBehaviors",
    "IntegrationUpdate",
    "InteractionCallbackAutocomplete",
    "InteractionCallbackData",
    "InteractionCallbackMessage",
    "InteractionCallbackModal",
    "InteractionCallbackType",
    "InteractionContextType",
    "InteractionData",
    "InteractionGuild",
    "InteractionResponse",
    "InteractionType",
    "Invite",
    "InviteCreate",
    "InviteDelete",
    "InviteGuild",
    "InviteMetadata",
    "InviteStageInstance",
    "InviteTargetType",
    "InviteTargetUsersJobStatus",
    "InviteType",
    "KeywordPresetType",
    "LinkChannelToLobbyParams",
    "ListActiveGuildThreadsResponse",
    "ListDefaultSoundboardSoundsResponse",
    "ListGuildSoundboardSoundsResponse",
    "Lobby",
    "LobbyMember",
    "LobbyMemberFlags",
    "MFALevel",
    "MembershipScreening",
    "MembershipState",
    "MentionableOption",
    "MessageActivity",
    "MessageActivityType",
    "MessageCall",
    "MessageComponentData",
    "MessageEditParams",
    "MessageFlag",
    "MessageGet",
    "MessageInteraction",
    "MessageInteractionMetadata",
    "MessageReference",
    "MessageReferenceType",
    "MessageSend",
    "MessageSnapshot",
    "MessageSnapshotMessage",
    "MessageType",
    "Missing",
    "MissingOrNullable",
    "ModalSubmitData",
    "ModifyChannelParams",
    "ModifyCurrentMemberParams",
    "ModifyCurrentUserParams",
    "ModifyCurrentUserVoiceStateParams",
    "ModifyGuildChannelPositionParams",
    "ModifyGuildEmojiParams",
    "ModifyGuildIncidentActionsParams",
    "ModifyGuildMemberParams",
    "ModifyGuildOnboardingParams",
    "ModifyGuildParams",
    "ModifyGuildRoleParams",
    "ModifyGuildRolePositionParams",
    "ModifyGuildScheduledEventParams",
    "ModifyGuildSoundboardSoundParams",
    "ModifyGuildStickerParams",
    "ModifyGuildTemplateParams",
    "ModifyGuildWelcomeScreenParams",
    "ModifyGuildWidgetParams",
    "ModifyLobbyParams",
    "ModifyThreadParams",
    "MutableGuildFeature",
    "NumberOption",
    "OnboardingMode",
    "OnboardingPrompt",
    "OnboardingPromptOption",
    "OnboardingPromptType",
    "OptionChoice",
    "OptionalAuditEntryInfo",
    "Overwrite",
    "OverwriteType",
    "PartialOverwrite",
    "Poll",
    "PollAnswer",
    "PollAnswerCount",
    "PollAnswerRequest",
    "PollMedia",
    "PollRequest",
    "PollResults",
    "PremiumTier",
    "PremiumType",
    "PresenceStatus",
    "PresenceUpdate",
    "PresenceUpdateUser",
    "Reaction",
    "ReactionType",
    "Ready",
    "RecurrenceRule",
    "RequestGuildMembers",
    "ResolvedData",
    "Resume",
    "Role",
    "RoleColors",
    "RoleFlag",
    "RoleOption",
    "RoleSubscriptionData",
    "RoleTags",
    "SKUFlag",
    "SKUType",
    "SelectDefaultValue",
    "SelectMenu",
    "SelectMenuResolved",
    "SelectOption",
    "SendSoundboardSoundParams",
    "SessionStartLimit",
    "Snowflake",
    "SnowflakeType",
    "SortOrderTypes",
    "SoundboardSound",
    "SourceChannel",
    "SourceGuild",
    "StageInstance",
    "StageInstanceCreate",
    "StageInstanceDelete",
    "StageInstanceUpdate",
    "StagePrivacyLevel",
    "StartThreadFromMessageParams",
    "StartThreadWithoutMessageParams",
    "Sticker",
    "StickerFormatType",
    "StickerItem",
    "StickerPack",
    "StickerPacksResponse",
    "StickerType",
    "StringOption",
    "SubCommandGroupOption",
    "SubCommandOption",
    "Subscription",
    "SubscriptionCreate",
    "SubscriptionDelete",
    "SubscriptionStatus",
    "SubscriptionUpdate",
    "SystemChannelFlags",
    "Team",
    "TeamMember",
    "TeamMemberRoleType",
    "TeamMemberUser",
    "TextInput",
    "TextInputStyle",
    "ThreadCreate",
    "ThreadDelete",
    "ThreadListSync",
    "ThreadMember",
    "ThreadMemberUpdate",
    "ThreadMembersUpdate",
    "ThreadMetadata",
    "ThreadUpdate",
    "TimeStampStyle",
    "TriggerMetadata",
    "TriggerType",
    "UnavailableGuild",
    "UnsetType",
    "UpdatePresence",
    "UpdatePresenceStatusType",
    "UpdateVoiceState",
    "User",
    "UserFlags",
    "UserOption",
    "UserUpdate",
    "VerificationLevel",
    "VideoQualityMode",
    "VisibilityType",
    "VoiceChannelEffectSend",
    "VoiceChannelStartTimeUpdate",
    "VoiceChannelStatusUpdate",
    "VoiceRegion",
    "VoiceServerUpdate",
    "VoiceState",
    "VoiceStateUpdate",
    "Webhook",
    "WebhookMessageEditParams",
    "WebhookType",
    "WebhooksUpdate",
    "WelcomeScreen",
    "WelcomeScreenChannel",
    "_LobbyMemberWriteParamsBase",
    "_SoundboardSoundsListResponse",
    "is_not_unset",
    "is_unset",
]


globals()["BaseModel"] = _BaseModel
for _model_module in (_types_module, *_MODEL_MODULES):
    for _model_name in _model_module.__all__:
        globals()[_model_name] = getattr(_model_module, _model_name)

for _protocol_name in _PROTOCOL_EXPORTS:
    globals()[_protocol_name] = getattr(_protocol, _protocol_name)
