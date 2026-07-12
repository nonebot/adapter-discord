"""Stable public facade for canonical Discord Pydantic models."""

from importlib import import_module
from types import ModuleType
from typing import TYPE_CHECKING

from ._public_module import bind_public_module
from ..domains import _model_support
from ..domains._manifest import DOMAIN_MODEL_MODULES

if TYPE_CHECKING:
    from ..domains import models as _static_domains_models
    from ..domains.models import (
        _LobbyMemberWriteParamsBase as _static_lobby_member_write_params_base,
        _SoundboardSoundsListResponse as _static_soundboard_sounds_list_response,
    )

    SKU = _static_domains_models.SKU
    ActionRow = _static_domains_models.ActionRow
    Activity = _static_domains_models.Activity
    ActivityAssets = _static_domains_models.ActivityAssets
    ActivityButtons = _static_domains_models.ActivityButtons
    ActivityEmoji = _static_domains_models.ActivityEmoji
    ActivityInstance = _static_domains_models.ActivityInstance
    ActivityLocation = _static_domains_models.ActivityLocation
    ActivityParty = _static_domains_models.ActivityParty
    ActivitySecrets = _static_domains_models.ActivitySecrets
    ActivityTimestamps = _static_domains_models.ActivityTimestamps
    AddLobbyMemberParams = _static_domains_models.AddLobbyMemberParams
    AllowedMention = _static_domains_models.AllowedMention
    AnswerVoters = _static_domains_models.AnswerVoters
    AnyCommandOption = _static_domains_models.AnyCommandOption
    Application = _static_domains_models.Application
    ApplicationCommand = _static_domains_models.ApplicationCommand
    ApplicationCommandBulkOverwriteParams = (
        _static_domains_models.ApplicationCommandBulkOverwriteParams
    )
    ApplicationCommandCreate = _static_domains_models.ApplicationCommandCreate
    ApplicationCommandData = _static_domains_models.ApplicationCommandData
    ApplicationCommandEditParams = _static_domains_models.ApplicationCommandEditParams
    ApplicationCommandInteractionDataOption = (
        _static_domains_models.ApplicationCommandInteractionDataOption
    )
    ApplicationCommandOption = _static_domains_models.ApplicationCommandOption
    ApplicationCommandOptionChoice = (
        _static_domains_models.ApplicationCommandOptionChoice
    )
    ApplicationCommandPermissions = _static_domains_models.ApplicationCommandPermissions
    ApplicationEmojis = _static_domains_models.ApplicationEmojis
    ApplicationIntegrationTypeConfiguration = (
        _static_domains_models.ApplicationIntegrationTypeConfiguration
    )
    ApplicationReady = _static_domains_models.ApplicationReady
    ApplicationRoleConnection = _static_domains_models.ApplicationRoleConnection
    ApplicationRoleConnectionMetadata = (
        _static_domains_models.ApplicationRoleConnectionMetadata
    )
    ArchivedThreadsResponse = _static_domains_models.ArchivedThreadsResponse
    Attachment = _static_domains_models.Attachment
    AttachmentOption = _static_domains_models.AttachmentOption
    AttachmentSend = _static_domains_models.AttachmentSend
    AuditLog = _static_domains_models.AuditLog
    AuditLogChange = _static_domains_models.AuditLogChange
    AuditLogChangeException = _static_domains_models.AuditLogChangeException
    AuditLogEntry = _static_domains_models.AuditLogEntry
    AuthorizationResponse = _static_domains_models.AuthorizationResponse
    AutoModerationAction = _static_domains_models.AutoModerationAction
    AutoModerationActionExecution = _static_domains_models.AutoModerationActionExecution
    AutoModerationActionMetadata = _static_domains_models.AutoModerationActionMetadata
    AutoModerationRule = _static_domains_models.AutoModerationRule
    AutoModerationRuleCreate = _static_domains_models.AutoModerationRuleCreate
    AutoModerationRuleDelete = _static_domains_models.AutoModerationRuleDelete
    AutoModerationRuleUpdate = _static_domains_models.AutoModerationRuleUpdate
    AvatarDecorationData = _static_domains_models.AvatarDecorationData
    Ban = _static_domains_models.Ban
    BaseModel = _static_domains_models.BaseModel
    BooleanOption = _static_domains_models.BooleanOption
    BulkBan = _static_domains_models.BulkBan
    Button = _static_domains_models.Button
    Channel = _static_domains_models.Channel
    ChannelCreate = _static_domains_models.ChannelCreate
    ChannelDelete = _static_domains_models.ChannelDelete
    ChannelMention = _static_domains_models.ChannelMention
    ChannelOption = _static_domains_models.ChannelOption
    ChannelPinsUpdate = _static_domains_models.ChannelPinsUpdate
    ChannelUpdate = _static_domains_models.ChannelUpdate
    ClientStatus = _static_domains_models.ClientStatus
    CommandOptionBase = _static_domains_models.CommandOptionBase
    Component = _static_domains_models.Component
    ComponentEmoji = _static_domains_models.ComponentEmoji
    Connection = _static_domains_models.Connection
    CountDetails = _static_domains_models.CountDetails
    CreateAutoModerationRuleParams = (
        _static_domains_models.CreateAutoModerationRuleParams
    )
    ModifyAutoModerationRuleParams = (
        _static_domains_models.ModifyAutoModerationRuleParams
    )
    CreateFollowupMessageParams = _static_domains_models.CreateFollowupMessageParams
    CreateGuildChannelParams = _static_domains_models.CreateGuildChannelParams
    CreateGuildParams = _static_domains_models.CreateGuildParams
    CreateGuildRoleParams = _static_domains_models.CreateGuildRoleParams
    CreateGuildScheduledEventParams = (
        _static_domains_models.CreateGuildScheduledEventParams
    )
    CreateGuildSoundboardSoundParams = (
        _static_domains_models.CreateGuildSoundboardSoundParams
    )
    CreateGuildTemplateParams = _static_domains_models.CreateGuildTemplateParams
    CreateLobbyMemberParams = _static_domains_models.CreateLobbyMemberParams
    CreateLobbyParams = _static_domains_models.CreateLobbyParams
    CreateWebhookParams = _static_domains_models.CreateWebhookParams
    CurrentUserGuild = _static_domains_models.CurrentUserGuild
    DefaultReaction = _static_domains_models.DefaultReaction
    DirectComponent = _static_domains_models.DirectComponent
    EditCurrentApplicationParams = _static_domains_models.EditCurrentApplicationParams
    Embed = _static_domains_models.Embed
    EmbedAuthor = _static_domains_models.EmbedAuthor
    EmbedField = _static_domains_models.EmbedField
    EmbedFooter = _static_domains_models.EmbedFooter
    EmbedImage = _static_domains_models.EmbedImage
    EmbedProvider = _static_domains_models.EmbedProvider
    EmbedThumbnail = _static_domains_models.EmbedThumbnail
    EmbedVideo = _static_domains_models.EmbedVideo
    Emoji = _static_domains_models.Emoji
    Entitlement = _static_domains_models.Entitlement
    EntitlementCreate = _static_domains_models.EntitlementCreate
    EntitlementDelete = _static_domains_models.EntitlementDelete
    EntitlementUpdate = _static_domains_models.EntitlementUpdate
    ExecuteWebhookParams = _static_domains_models.ExecuteWebhookParams
    File = _static_domains_models.File
    FollowedChannel = _static_domains_models.FollowedChannel
    ForumTag = _static_domains_models.ForumTag
    ForumTagRequest = _static_domains_models.ForumTagRequest
    Gateway = _static_domains_models.Gateway
    GatewayBot = _static_domains_models.GatewayBot
    Guild = _static_domains_models.Guild
    GuildApplicationCommandCreateParams = (
        _static_domains_models.GuildApplicationCommandCreateParams
    )
    GuildApplicationCommandEditParams = (
        _static_domains_models.GuildApplicationCommandEditParams
    )
    GuildApplicationCommandPermissions = (
        _static_domains_models.GuildApplicationCommandPermissions
    )
    GuildAuditLogEntryCreate = _static_domains_models.GuildAuditLogEntryCreate
    GuildBanAdd = _static_domains_models.GuildBanAdd
    GuildBanRemove = _static_domains_models.GuildBanRemove
    GuildCreate = _static_domains_models.GuildCreate
    GuildCreateCompat = _static_domains_models.GuildCreateCompat
    GuildCreateCompatChannel = _static_domains_models.GuildCreateCompatChannel
    GuildCreateCompatOverwrite = _static_domains_models.GuildCreateCompatOverwrite
    GuildCreateCompatRole = _static_domains_models.GuildCreateCompatRole
    GuildDelete = _static_domains_models.GuildDelete
    GuildEmojisUpdate = _static_domains_models.GuildEmojisUpdate
    GuildIncidentsData = _static_domains_models.GuildIncidentsData
    GuildIntegrationsUpdate = _static_domains_models.GuildIntegrationsUpdate
    GuildMember = _static_domains_models.GuildMember
    GuildMemberAdd = _static_domains_models.GuildMemberAdd
    GuildMemberRemove = _static_domains_models.GuildMemberRemove
    GuildMemberUpdate = _static_domains_models.GuildMemberUpdate
    GuildMembersChunk = _static_domains_models.GuildMembersChunk
    GuildOnboarding = _static_domains_models.GuildOnboarding
    GuildPreview = _static_domains_models.GuildPreview
    GuildRoleCreate = _static_domains_models.GuildRoleCreate
    GuildRoleDelete = _static_domains_models.GuildRoleDelete
    GuildRoleUpdate = _static_domains_models.GuildRoleUpdate
    GuildScheduledEvent = _static_domains_models.GuildScheduledEvent
    GuildScheduledEventCreate = _static_domains_models.GuildScheduledEventCreate
    GuildScheduledEventDelete = _static_domains_models.GuildScheduledEventDelete
    GuildScheduledEventEntityMetadata = (
        _static_domains_models.GuildScheduledEventEntityMetadata
    )
    GuildScheduledEventRecurrenceRuleN_WeekdayStructure = (
        _static_domains_models.GuildScheduledEventRecurrenceRuleN_WeekdayStructure
    )
    GuildScheduledEventUpdate = _static_domains_models.GuildScheduledEventUpdate
    GuildScheduledEventUser = _static_domains_models.GuildScheduledEventUser
    GuildScheduledEventUserAdd = _static_domains_models.GuildScheduledEventUserAdd
    GuildScheduledEventUserRemove = _static_domains_models.GuildScheduledEventUserRemove
    GuildStickersUpdate = _static_domains_models.GuildStickersUpdate
    GuildTemplate = _static_domains_models.GuildTemplate
    GuildTemplateGuild = _static_domains_models.GuildTemplateGuild
    GuildTemplateGuildChannel = _static_domains_models.GuildTemplateGuildChannel
    GuildTemplateGuildRole = _static_domains_models.GuildTemplateGuildRole
    GuildUpdate = _static_domains_models.GuildUpdate
    GuildVanityURL = _static_domains_models.GuildVanityURL
    GuildWidget = _static_domains_models.GuildWidget
    GuildWidgetChannel = _static_domains_models.GuildWidgetChannel
    GuildWidgetSettings = _static_domains_models.GuildWidgetSettings
    GuildWidgetUser = _static_domains_models.GuildWidgetUser
    Hello = _static_domains_models.Hello
    Identify = _static_domains_models.Identify
    IdentifyConnectionProperties = _static_domains_models.IdentifyConnectionProperties
    InstallParams = _static_domains_models.InstallParams
    IntegerOption = _static_domains_models.IntegerOption
    Integration = _static_domains_models.Integration
    IntegrationAccount = _static_domains_models.IntegrationAccount
    IntegrationApplication = _static_domains_models.IntegrationApplication
    IntegrationCreate = _static_domains_models.IntegrationCreate
    IntegrationDelete = _static_domains_models.IntegrationDelete
    IntegrationUpdate = _static_domains_models.IntegrationUpdate
    InteractionCallbackAutocomplete = (
        _static_domains_models.InteractionCallbackAutocomplete
    )
    InteractionCallbackData = _static_domains_models.InteractionCallbackData
    InteractionCallbackMessage = _static_domains_models.InteractionCallbackMessage
    InteractionCallbackModal = _static_domains_models.InteractionCallbackModal
    InteractionData = _static_domains_models.InteractionData
    InteractionGuild = _static_domains_models.InteractionGuild
    InteractionResponse = _static_domains_models.InteractionResponse
    Invite = _static_domains_models.Invite
    InviteCreate = _static_domains_models.InviteCreate
    InviteDelete = _static_domains_models.InviteDelete
    InviteGuild = _static_domains_models.InviteGuild
    InviteMetadata = _static_domains_models.InviteMetadata
    InviteStageInstance = _static_domains_models.InviteStageInstance
    InviteTargetUsersJobStatus = _static_domains_models.InviteTargetUsersJobStatus
    LinkChannelToLobbyParams = _static_domains_models.LinkChannelToLobbyParams
    ListActiveGuildThreadsResponse = (
        _static_domains_models.ListActiveGuildThreadsResponse
    )
    ListDefaultSoundboardSoundsResponse = (
        _static_domains_models.ListDefaultSoundboardSoundsResponse
    )
    ListGuildSoundboardSoundsResponse = (
        _static_domains_models.ListGuildSoundboardSoundsResponse
    )
    Lobby = _static_domains_models.Lobby
    LobbyMember = _static_domains_models.LobbyMember
    MembershipScreening = _static_domains_models.MembershipScreening
    MentionableOption = _static_domains_models.MentionableOption
    MessageActivity = _static_domains_models.MessageActivity
    MessageCall = _static_domains_models.MessageCall
    MessageComponentData = _static_domains_models.MessageComponentData
    MessageEditParams = _static_domains_models.MessageEditParams
    MessageGet = _static_domains_models.MessageGet
    MessageInteraction = _static_domains_models.MessageInteraction
    MessageInteractionMetadata = _static_domains_models.MessageInteractionMetadata
    MessageReference = _static_domains_models.MessageReference
    MessageSend = _static_domains_models.MessageSend
    MessageSnapshot = _static_domains_models.MessageSnapshot
    MessageSnapshotMessage = _static_domains_models.MessageSnapshotMessage
    ModalSubmitData = _static_domains_models.ModalSubmitData
    ModifyChannelParams = _static_domains_models.ModifyChannelParams
    ModifyCurrentMemberParams = _static_domains_models.ModifyCurrentMemberParams
    ModifyCurrentUserParams = _static_domains_models.ModifyCurrentUserParams
    ModifyCurrentUserVoiceStateParams = (
        _static_domains_models.ModifyCurrentUserVoiceStateParams
    )
    ModifyGuildChannelPositionParams = (
        _static_domains_models.ModifyGuildChannelPositionParams
    )
    ModifyGuildEmojiParams = _static_domains_models.ModifyGuildEmojiParams
    ModifyGuildIncidentActionsParams = (
        _static_domains_models.ModifyGuildIncidentActionsParams
    )
    ModifyGuildMemberParams = _static_domains_models.ModifyGuildMemberParams
    ModifyGuildOnboardingParams = _static_domains_models.ModifyGuildOnboardingParams
    ModifyGuildParams = _static_domains_models.ModifyGuildParams
    ModifyGuildRoleParams = _static_domains_models.ModifyGuildRoleParams
    ModifyGuildRolePositionParams = _static_domains_models.ModifyGuildRolePositionParams
    ModifyGuildScheduledEventParams = (
        _static_domains_models.ModifyGuildScheduledEventParams
    )
    ModifyGuildSoundboardSoundParams = (
        _static_domains_models.ModifyGuildSoundboardSoundParams
    )
    ModifyGuildStickerParams = _static_domains_models.ModifyGuildStickerParams
    ModifyGuildTemplateParams = _static_domains_models.ModifyGuildTemplateParams
    ModifyGuildWelcomeScreenParams = (
        _static_domains_models.ModifyGuildWelcomeScreenParams
    )
    ModifyGuildWidgetParams = _static_domains_models.ModifyGuildWidgetParams
    ModifyLobbyParams = _static_domains_models.ModifyLobbyParams
    ModifyThreadParams = _static_domains_models.ModifyThreadParams
    NumberOption = _static_domains_models.NumberOption
    OnboardingPrompt = _static_domains_models.OnboardingPrompt
    OnboardingPromptOption = _static_domains_models.OnboardingPromptOption
    OptionChoice = _static_domains_models.OptionChoice
    OptionalAuditEntryInfo = _static_domains_models.OptionalAuditEntryInfo
    Overwrite = _static_domains_models.Overwrite
    PartialOverwrite = _static_domains_models.PartialOverwrite
    Poll = _static_domains_models.Poll
    PollAnswer = _static_domains_models.PollAnswer
    PollAnswerCount = _static_domains_models.PollAnswerCount
    PollAnswerRequest = _static_domains_models.PollAnswerRequest
    PollMedia = _static_domains_models.PollMedia
    PollRequest = _static_domains_models.PollRequest
    PollResults = _static_domains_models.PollResults
    PresenceUpdate = _static_domains_models.PresenceUpdate
    PresenceUpdateUser = _static_domains_models.PresenceUpdateUser
    Reaction = _static_domains_models.Reaction
    Ready = _static_domains_models.Ready
    RecurrenceRule = _static_domains_models.RecurrenceRule
    RequestGuildMembers = _static_domains_models.RequestGuildMembers
    ResolvedData = _static_domains_models.ResolvedData
    Resume = _static_domains_models.Resume
    Role = _static_domains_models.Role
    RoleColors = _static_domains_models.RoleColors
    RoleOption = _static_domains_models.RoleOption
    RoleSubscriptionData = _static_domains_models.RoleSubscriptionData
    RoleTags = _static_domains_models.RoleTags
    SelectDefaultValue = _static_domains_models.SelectDefaultValue
    SelectMenu = _static_domains_models.SelectMenu
    SelectMenuResolved = _static_domains_models.SelectMenuResolved
    SelectOption = _static_domains_models.SelectOption
    SendSoundboardSoundParams = _static_domains_models.SendSoundboardSoundParams
    SessionStartLimit = _static_domains_models.SessionStartLimit
    Snowflake = _static_domains_models.Snowflake
    SnowflakeType = _static_domains_models.SnowflakeType
    SoundboardSound = _static_domains_models.SoundboardSound
    SourceChannel = _static_domains_models.SourceChannel
    SourceGuild = _static_domains_models.SourceGuild
    StageInstance = _static_domains_models.StageInstance
    StageInstanceCreate = _static_domains_models.StageInstanceCreate
    StageInstanceDelete = _static_domains_models.StageInstanceDelete
    StageInstanceUpdate = _static_domains_models.StageInstanceUpdate
    StartThreadFromMessageParams = _static_domains_models.StartThreadFromMessageParams
    StartThreadInForumChannelParams = (
        _static_domains_models.StartThreadInForumChannelParams
    )
    StartThreadWithoutMessageParams = (
        _static_domains_models.StartThreadWithoutMessageParams
    )
    Sticker = _static_domains_models.Sticker
    StickerItem = _static_domains_models.StickerItem
    StickerPack = _static_domains_models.StickerPack
    StickerPacksResponse = _static_domains_models.StickerPacksResponse
    StringOption = _static_domains_models.StringOption
    SubCommandGroupOption = _static_domains_models.SubCommandGroupOption
    SubCommandOption = _static_domains_models.SubCommandOption
    Subscription = _static_domains_models.Subscription
    SubscriptionCreate = _static_domains_models.SubscriptionCreate
    SubscriptionDelete = _static_domains_models.SubscriptionDelete
    SubscriptionUpdate = _static_domains_models.SubscriptionUpdate
    Team = _static_domains_models.Team
    TeamMember = _static_domains_models.TeamMember
    TeamMemberUser = _static_domains_models.TeamMemberUser
    TextInput = _static_domains_models.TextInput
    ThreadCreate = _static_domains_models.ThreadCreate
    ThreadDelete = _static_domains_models.ThreadDelete
    ThreadListSync = _static_domains_models.ThreadListSync
    ThreadMember = _static_domains_models.ThreadMember
    ThreadMemberUpdate = _static_domains_models.ThreadMemberUpdate
    ThreadMembersUpdate = _static_domains_models.ThreadMembersUpdate
    ThreadMetadata = _static_domains_models.ThreadMetadata
    ThreadUpdate = _static_domains_models.ThreadUpdate
    TriggerMetadata = _static_domains_models.TriggerMetadata
    UnavailableGuild = _static_domains_models.UnavailableGuild
    UpdatePresence = _static_domains_models.UpdatePresence
    UpdateVoiceState = _static_domains_models.UpdateVoiceState
    User = _static_domains_models.User
    UserOption = _static_domains_models.UserOption
    UserUpdate = _static_domains_models.UserUpdate
    VoiceChannelEffectSend = _static_domains_models.VoiceChannelEffectSend
    VoiceChannelStartTimeUpdate = _static_domains_models.VoiceChannelStartTimeUpdate
    VoiceChannelStatusUpdate = _static_domains_models.VoiceChannelStatusUpdate
    VoiceRegion = _static_domains_models.VoiceRegion
    VoiceServerUpdate = _static_domains_models.VoiceServerUpdate
    VoiceState = _static_domains_models.VoiceState
    VoiceStateUpdate = _static_domains_models.VoiceStateUpdate
    Webhook = _static_domains_models.Webhook
    WebhookMessageEditParams = _static_domains_models.WebhookMessageEditParams
    WebhooksUpdate = _static_domains_models.WebhooksUpdate
    WelcomeScreen = _static_domains_models.WelcomeScreen
    WelcomeScreenChannel = _static_domains_models.WelcomeScreenChannel
    _LobbyMemberWriteParamsBase = _static_lobby_member_write_params_base
    _SoundboardSoundsListResponse = _static_soundboard_sounds_list_response
    UNSET = _static_domains_models.UNSET
    UnsetType = _static_domains_models.UnsetType
    Missing = _static_domains_models.Missing
    MissingOrNullable = _static_domains_models.MissingOrNullable
    is_unset = _static_domains_models.is_unset
    is_not_unset = _static_domains_models.is_not_unset
    ActivityAssetImage = _static_domains_models.ActivityAssetImage
    ActivityFlags = _static_domains_models.ActivityFlags
    ActivityType = _static_domains_models.ActivityType
    AllowedMentionType = _static_domains_models.AllowedMentionType
    AnimationType = _static_domains_models.AnimationType
    ApplicationCommandOptionType = _static_domains_models.ApplicationCommandOptionType
    ApplicationCommandPermissionsType = (
        _static_domains_models.ApplicationCommandPermissionsType
    )
    ApplicationCommandType = _static_domains_models.ApplicationCommandType
    ApplicationFlag = _static_domains_models.ApplicationFlag
    ApplicationIntegrationType = _static_domains_models.ApplicationIntegrationType
    ApplicationRoleConnectionMetadataType = (
        _static_domains_models.ApplicationRoleConnectionMetadataType
    )
    AttachmentFlag = _static_domains_models.AttachmentFlag
    AuditLogEventType = _static_domains_models.AuditLogEventType
    AutoModerationActionType = _static_domains_models.AutoModerationActionType
    AutoModerationRuleEventType = _static_domains_models.AutoModerationRuleEventType
    ButtonStyle = _static_domains_models.ButtonStyle
    ChannelFlags = _static_domains_models.ChannelFlags
    ChannelType = _static_domains_models.ChannelType
    ComponentType = _static_domains_models.ComponentType
    ConnectionServiceType = _static_domains_models.ConnectionServiceType
    DefaultMessageNotificationLevel = (
        _static_domains_models.DefaultMessageNotificationLevel
    )
    EmbedTypes = _static_domains_models.EmbedTypes
    EntitlementType = _static_domains_models.EntitlementType
    ExplicitContentFilterLevel = _static_domains_models.ExplicitContentFilterLevel
    ForumLayoutTypes = _static_domains_models.ForumLayoutTypes
    GuildFeature = _static_domains_models.GuildFeature
    GuildMemberFlags = _static_domains_models.GuildMemberFlags
    GuildNSFWLevel = _static_domains_models.GuildNSFWLevel
    GuildScheduledEventEntityType = _static_domains_models.GuildScheduledEventEntityType
    GuildScheduledEventPrivacyLevel = (
        _static_domains_models.GuildScheduledEventPrivacyLevel
    )
    GuildScheduledEventRecurrenceRuleFrequency = (
        _static_domains_models.GuildScheduledEventRecurrenceRuleFrequency
    )
    GuildScheduledEventRecurrenceRuleMonth = (
        _static_domains_models.GuildScheduledEventRecurrenceRuleMonth
    )
    GuildScheduledEventRecurrenceRuleWeekday = (
        _static_domains_models.GuildScheduledEventRecurrenceRuleWeekday
    )
    GuildScheduledEventStatus = _static_domains_models.GuildScheduledEventStatus
    IntegrationExpireBehaviors = _static_domains_models.IntegrationExpireBehaviors
    InteractionCallbackType = _static_domains_models.InteractionCallbackType
    InteractionContextType = _static_domains_models.InteractionContextType
    InteractionType = _static_domains_models.InteractionType
    InviteTargetType = _static_domains_models.InviteTargetType
    InviteType = _static_domains_models.InviteType
    KeywordPresetType = _static_domains_models.KeywordPresetType
    LobbyMemberFlags = _static_domains_models.LobbyMemberFlags
    MFALevel = _static_domains_models.MFALevel
    MembershipState = _static_domains_models.MembershipState
    MessageActivityType = _static_domains_models.MessageActivityType
    MessageFlag = _static_domains_models.MessageFlag
    MessageReferenceType = _static_domains_models.MessageReferenceType
    MessageType = _static_domains_models.MessageType
    MutableGuildFeature = _static_domains_models.MutableGuildFeature
    OnboardingMode = _static_domains_models.OnboardingMode
    OnboardingPromptType = _static_domains_models.OnboardingPromptType
    OverwriteType = _static_domains_models.OverwriteType
    PremiumTier = _static_domains_models.PremiumTier
    PremiumType = _static_domains_models.PremiumType
    PresenceStatus = _static_domains_models.PresenceStatus
    ReactionType = _static_domains_models.ReactionType
    RoleFlag = _static_domains_models.RoleFlag
    SKUFlag = _static_domains_models.SKUFlag
    SKUType = _static_domains_models.SKUType
    SortOrderTypes = _static_domains_models.SortOrderTypes
    StagePrivacyLevel = _static_domains_models.StagePrivacyLevel
    StickerFormatType = _static_domains_models.StickerFormatType
    StickerType = _static_domains_models.StickerType
    SubscriptionStatus = _static_domains_models.SubscriptionStatus
    SystemChannelFlags = _static_domains_models.SystemChannelFlags
    TeamMemberRoleType = _static_domains_models.TeamMemberRoleType
    TextInputStyle = _static_domains_models.TextInputStyle
    TimeStampStyle = _static_domains_models.TimeStampStyle
    TriggerType = _static_domains_models.TriggerType
    UpdatePresenceStatusType = _static_domains_models.UpdatePresenceStatusType
    UserFlags = _static_domains_models.UserFlags
    VerificationLevel = _static_domains_models.VerificationLevel
    VideoQualityMode = _static_domains_models.VideoQualityMode
    VisibilityType = _static_domains_models.VisibilityType
    WebhookType = _static_domains_models.WebhookType
    AddGroupDMRecipientParams = _static_domains_models.AddGroupDMRecipientParams
    AddGuildMemberParams = _static_domains_models.AddGuildMemberParams
    BeginGuildPruneParams = _static_domains_models.BeginGuildPruneParams
    BulkDeleteMessagesParams = _static_domains_models.BulkDeleteMessagesParams
    BulkGuildBanParams = _static_domains_models.BulkGuildBanParams
    CreateApplicationEmojiParams = _static_domains_models.CreateApplicationEmojiParams
    CreateChannelInviteParams = _static_domains_models.CreateChannelInviteParams
    CreateDMParams = _static_domains_models.CreateDMParams
    CreateGroupDMParams = _static_domains_models.CreateGroupDMParams
    CreateGuildBanParams = _static_domains_models.CreateGuildBanParams
    CreateGuildEmojiParams = _static_domains_models.CreateGuildEmojiParams
    CreateStageInstanceParams = _static_domains_models.CreateStageInstanceParams
    CreateTestEntitlementParams = _static_domains_models.CreateTestEntitlementParams
    EditApplicationCommandPermissionsParams = (
        _static_domains_models.EditApplicationCommandPermissionsParams
    )
    EditChannelPermissionsParams = _static_domains_models.EditChannelPermissionsParams
    FollowAnnouncementChannelParams = (
        _static_domains_models.FollowAnnouncementChannelParams
    )
    ModifyApplicationEmojiParams = _static_domains_models.ModifyApplicationEmojiParams
    ModifyCurrentUserNickParams = _static_domains_models.ModifyCurrentUserNickParams
    ModifyDMParams = _static_domains_models.ModifyDMParams
    ModifyGuildMFAParams = _static_domains_models.ModifyGuildMFAParams
    ModifyStageInstanceParams = _static_domains_models.ModifyStageInstanceParams
    ModifyUserVoiceStateParams = _static_domains_models.ModifyUserVoiceStateParams
    ModifyWebhookParams = _static_domains_models.ModifyWebhookParams
    ModifyWebhookWithTokenParams = _static_domains_models.ModifyWebhookWithTokenParams
    UpdateUserApplicationRoleConnectionParams = (
        _static_domains_models.UpdateUserApplicationRoleConnectionParams
    )

_MODEL_MODULES: tuple[ModuleType, ...] = tuple(
    import_module(module_name) for module_name in DOMAIN_MODEL_MODULES
)
_CANONICAL_MODULES: tuple[ModuleType, ...] = (_model_support, *_MODEL_MODULES)

__all__ = [  # noqa: RUF022 - preserve the 1.x public API snapshot order.
    "ActionRow",
    "Activity",
    "ActivityAssets",
    "ActivityButtons",
    "ActivityEmoji",
    "ActivityInstance",
    "ActivityLocation",
    "ActivityParty",
    "ActivitySecrets",
    "ActivityTimestamps",
    "AddGroupDMRecipientParams",
    "AddGuildMemberParams",
    "AddLobbyMemberParams",
    "AllowedMention",
    "AnswerVoters",
    "AnyCommandOption",
    "Application",
    "ApplicationCommand",
    "ApplicationCommandBulkOverwriteParams",
    "ApplicationCommandCreate",
    "ApplicationCommandData",
    "ApplicationCommandInteractionDataOption",
    "ApplicationCommandOption",
    "ApplicationCommandOptionChoice",
    "ApplicationCommandPermissions",
    "ApplicationEmojis",
    "ApplicationIntegrationTypeConfiguration",
    "ApplicationReady",
    "ApplicationRoleConnection",
    "ApplicationRoleConnectionMetadata",
    "ArchivedThreadsResponse",
    "Attachment",
    "AttachmentOption",
    "AttachmentSend",
    "AuditLog",
    "AuditLogChange",
    "AuditLogChangeException",
    "AuditLogEntry",
    "AuthorizationResponse",
    "AutoModerationAction",
    "AutoModerationActionExecution",
    "AutoModerationActionMetadata",
    "AutoModerationRule",
    "AutoModerationRuleCreate",
    "AutoModerationRuleDelete",
    "AutoModerationRuleUpdate",
    "AvatarDecorationData",
    "Ban",
    "BaseModel",
    "BeginGuildPruneParams",
    "BooleanOption",
    "BulkBan",
    "BulkDeleteMessagesParams",
    "BulkGuildBanParams",
    "Button",
    "Channel",
    "ChannelCreate",
    "ChannelDelete",
    "ChannelMention",
    "ChannelOption",
    "ChannelPinsUpdate",
    "ChannelUpdate",
    "ClientStatus",
    "CommandOptionBase",
    "Component",
    "ComponentEmoji",
    "Connection",
    "CountDetails",
    "CreateApplicationEmojiParams",
    "CreateAutoModerationRuleParams",
    "CreateFollowupMessageParams",
    "CreateChannelInviteParams",
    "CreateDMParams",
    "CreateGroupDMParams",
    "CreateGuildBanParams",
    "CreateGuildChannelParams",
    "CreateGuildEmojiParams",
    "CreateGuildParams",
    "CreateGuildScheduledEventParams",
    "CreateGuildSoundboardSoundParams",
    "CreateLobbyMemberParams",
    "CreateLobbyParams",
    "CreateStageInstanceParams",
    "CreateTestEntitlementParams",
    "CurrentUserGuild",
    "DefaultReaction",
    "DirectComponent",
    "EditApplicationCommandPermissionsParams",
    "EditChannelPermissionsParams",
    "Embed",
    "EmbedAuthor",
    "EmbedField",
    "EmbedFooter",
    "EmbedImage",
    "EmbedProvider",
    "EmbedThumbnail",
    "EmbedVideo",
    "Emoji",
    "Entitlement",
    "EntitlementCreate",
    "EntitlementDelete",
    "EntitlementUpdate",
    "ExecuteWebhookParams",
    "File",
    "FollowAnnouncementChannelParams",
    "FollowedChannel",
    "ForumTag",
    "ForumTagRequest",
    "Gateway",
    "GatewayBot",
    "Guild",
    "GuildApplicationCommandPermissions",
    "GuildApplicationCommandCreateParams",
    "GuildApplicationCommandEditParams",
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
    "GuildIncidentsData",
    "GuildIntegrationsUpdate",
    "GuildMember",
    "GuildMemberAdd",
    "GuildMemberRemove",
    "GuildMemberUpdate",
    "GuildMembersChunk",
    "GuildOnboarding",
    "GuildPreview",
    "GuildRoleCreate",
    "GuildRoleDelete",
    "GuildRoleUpdate",
    "GuildScheduledEvent",
    "GuildScheduledEventCreate",
    "GuildScheduledEventDelete",
    "GuildScheduledEventEntityMetadata",
    "GuildScheduledEventRecurrenceRuleN_WeekdayStructure",
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
    "IntegrationUpdate",
    "InteractionCallbackAutocomplete",
    "InteractionCallbackData",
    "InteractionCallbackMessage",
    "InteractionCallbackModal",
    "InteractionData",
    "InteractionResponse",
    "Invite",
    "InviteCreate",
    "InviteDelete",
    "InviteGuild",
    "InviteMetadata",
    "InviteStageInstance",
    "InviteTargetUsersJobStatus",
    "LinkChannelToLobbyParams",
    "ListActiveGuildThreadsResponse",
    "ListDefaultSoundboardSoundsResponse",
    "ListGuildSoundboardSoundsResponse",
    "Lobby",
    "LobbyMember",
    "MembershipScreening",
    "MentionableOption",
    "MessageActivity",
    "MessageComponentData",
    "MessageGet",
    "MessageInteraction",
    "MessageInteractionMetadata",
    "MessageReference",
    "MessageSend",
    "MessageSnapshot",
    "MessageSnapshotMessage",
    "ModalSubmitData",
    "ModifyApplicationEmojiParams",
    "ModifyAutoModerationRuleParams",
    "ModifyChannelParams",
    "ModifyCurrentUserNickParams",
    "ModifyDMParams",
    "ModifyGuildIncidentActionsParams",
    "ModifyGuildMFAParams",
    "ModifyGuildOnboardingParams",
    "ModifyGuildParams",
    "ModifyGuildScheduledEventParams",
    "ModifyGuildSoundboardSoundParams",
    "ModifyGuildWelcomeScreenParams",
    "ModifyLobbyParams",
    "ModifyStageInstanceParams",
    "ModifyUserVoiceStateParams",
    "ModifyWebhookParams",
    "ModifyWebhookWithTokenParams",
    "NumberOption",
    "OnboardingPrompt",
    "OnboardingPromptOption",
    "OptionChoice",
    "OptionalAuditEntryInfo",
    "Overwrite",
    "Poll",
    "PollAnswer",
    "PollAnswerCount",
    "PollAnswerRequest",
    "PollMedia",
    "PollRequest",
    "PollResults",
    "PresenceUpdate",
    "PresenceUpdateUser",
    "Reaction",
    "Ready",
    "RecurrenceRule",
    "RequestGuildMembers",
    "ResolvedData",
    "Resume",
    "Role",
    "RoleColors",
    "RoleOption",
    "RoleSubscriptionData",
    "RoleTags",
    "SKU",
    "SelectDefaultValue",
    "SelectMenu",
    "SelectMenuResolved",
    "SelectOption",
    "SendSoundboardSoundParams",
    "SessionStartLimit",
    "Snowflake",
    "SnowflakeType",
    "SoundboardSound",
    "StageInstance",
    "StageInstanceCreate",
    "StageInstanceDelete",
    "StageInstanceUpdate",
    "StartThreadInForumChannelParams",
    "Sticker",
    "StickerItem",
    "StickerPack",
    "StickerPacksResponse",
    "StringOption",
    "SubCommandGroupOption",
    "SubCommandOption",
    "Subscription",
    "SubscriptionCreate",
    "SubscriptionDelete",
    "SubscriptionUpdate",
    "Team",
    "TeamMember",
    "TeamMemberUser",
    "TextInput",
    "ThreadCreate",
    "ThreadDelete",
    "ThreadListSync",
    "ThreadMember",
    "ThreadMemberUpdate",
    "ThreadMembersUpdate",
    "ThreadMetadata",
    "ThreadUpdate",
    "TriggerMetadata",
    "UnavailableGuild",
    "UpdatePresence",
    "UpdateUserApplicationRoleConnectionParams",
    "UpdateVoiceState",
    "User",
    "UserOption",
    "UserUpdate",
    "VoiceChannelEffectSend",
    "VoiceChannelStartTimeUpdate",
    "VoiceChannelStatusUpdate",
    "VoiceRegion",
    "VoiceServerUpdate",
    "VoiceState",
    "VoiceStateUpdate",
    "Webhook",
    "WebhooksUpdate",
    "WelcomeScreen",
    "WelcomeScreenChannel",
]


for _canonical_module in _CANONICAL_MODULES:
    for _canonical_name in _canonical_module.__all__:
        globals()[_canonical_name] = getattr(_canonical_module, _canonical_name)

bind_public_module(
    __name__,
    globals(),
    [*__all__, "Snowflake"],
)
