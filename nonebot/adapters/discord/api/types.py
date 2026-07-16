"""Stable public facade for Discord enum and sentinel types."""

from typing import TYPE_CHECKING

from ._public_module import bind_public_module
from .. import protocol as _protocol
from ..domains import _types as _types_module

if TYPE_CHECKING:
    from ..domains import models as _static_domains_models

    UNSET = _static_domains_models.UNSET
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
    Missing = _static_domains_models.Missing
    MissingOrNullable = _static_domains_models.MissingOrNullable
    UnsetType = _static_domains_models.UnsetType
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
    is_not_unset = _static_domains_models.is_not_unset
    is_unset = _static_domains_models.is_unset

for _type_name in _types_module.__all__:
    globals()[_type_name] = getattr(_types_module, _type_name)

for _protocol_name in (
    "UNSET",
    "Missing",
    "MissingOrNullable",
    "UnsetType",
    "is_not_unset",
    "is_unset",
):
    globals()[_protocol_name] = getattr(_protocol, _protocol_name)

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
    "LobbyMemberFlags",
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


bind_public_module(__name__, globals(), __all__)
