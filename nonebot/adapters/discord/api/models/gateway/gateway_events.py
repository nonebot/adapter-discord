import datetime
from typing import Literal

from pydantic import BaseModel

from ..common.embeds import Embed
from ..common.messages import (
    Attachment,
    ChannelMention,
    MessageActivity,
    MessageCall,
    MessageGet,
    MessageReference,
    MessageSnapshot,
    Reaction,
    RoleSubscriptionData,
)
from ..common.snowflake import Snowflake
from ..common.user import User
from ..http.application import Application
from ..http.channels import Channel
from ..http.emoji import Emoji
from ..http.guild_members import GuildMember
from ..http.monetization import Entitlement
from ..http.polls import Poll
from ..http.stickers import Sticker, StickerItem
from ..interactions.interactions import (
    ApplicationCommandData,
    InteractionData,
    InteractionGuild,
    MessageComponentData,
    MessageInteraction,
    MessageInteractionMetadata,
    ModalSubmitData,
    ResolvedData,
)
from ..interactions.message_components import DirectComponent
from ...types import (
    UNSET,
    ApplicationIntegrationType,
    InteractionContextType,
    InteractionType,
    MessageFlag,
    MessageType,
    Missing,
    MissingOrNullable,
    ReactionType,
)


class InteractionCreateBasePayload(BaseModel):
    id: Snowflake
    application_id: Snowflake
    attachment_size_limit: int
    guild: Missing[InteractionGuild] = UNSET
    guild_id: Missing[Snowflake] = UNSET
    channel: Missing[Channel] = UNSET
    channel_id: Missing[Snowflake] = UNSET
    member: Missing[GuildMember] = UNSET
    user: Missing[User] = UNSET
    token: str
    version: int
    app_permissions: Missing[str] = UNSET
    locale: Missing[str] = UNSET
    guild_locale: Missing[str] = UNSET
    entitlements: Missing[list[Entitlement]] = UNSET
    authorizing_integration_owners: dict[
        ApplicationIntegrationType, Snowflake | Literal["0"]
    ]
    context: Missing[InteractionContextType] = UNSET


class PingInteractionCreatePayload(InteractionCreateBasePayload):
    type: Literal[InteractionType.PING]
    data: Missing[InteractionData] = UNSET
    message: Missing[MessageGet] = UNSET


class ApplicationCommandInteractionCreatePayload(InteractionCreateBasePayload):
    type: Literal[InteractionType.APPLICATION_COMMAND]
    data: ApplicationCommandData
    message: Missing[MessageGet] = UNSET


class ApplicationCommandAutoCompleteInteractionCreatePayload(
    InteractionCreateBasePayload
):
    type: Literal[InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE]
    data: ApplicationCommandData
    message: Missing[MessageGet] = UNSET


class MessageComponentInteractionCreatePayload(InteractionCreateBasePayload):
    type: Literal[InteractionType.MESSAGE_COMPONENT]
    data: MessageComponentData
    message: MessageGet


class ModalSubmitInteractionCreatePayload(InteractionCreateBasePayload):
    type: Literal[InteractionType.MODAL_SUBMIT]
    data: ModalSubmitData
    message: Missing[MessageGet] = UNSET


class MessageCreateBasePayload(MessageGet):
    member: Missing[GuildMember] = UNSET


class MessageCreatePayload(MessageCreateBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessageCreatePayload(MessageCreateBasePayload):
    guild_id: Snowflake


class DirectMessageCreatePayload(MessageCreateBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessageUpdateBasePayload(BaseModel):
    id: Snowflake
    channel_id: Snowflake
    member: Missing[GuildMember] = UNSET
    author: Missing[User] = UNSET
    content: Missing[str] = UNSET
    timestamp: Missing[datetime.datetime] = UNSET
    edited_timestamp: MissingOrNullable[datetime.datetime] = UNSET
    tts: Missing[bool] = UNSET
    mention_everyone: Missing[bool] = UNSET
    mentions: Missing[list[User]] = UNSET
    mention_roles: Missing[list[Snowflake]] = UNSET
    mention_channels: Missing[list[ChannelMention]] = UNSET
    attachments: Missing[list[Attachment]] = UNSET
    embeds: Missing[list[Embed]] = UNSET
    reactions: Missing[list[Reaction]] = UNSET
    nonce: Missing[int | str] = UNSET
    pinned: Missing[bool] = UNSET
    webhook_id: Missing[Snowflake] = UNSET
    type: Missing[MessageType] = UNSET
    activity: Missing[MessageActivity] = UNSET
    application: Missing[Application] = UNSET
    application_id: Missing[Snowflake] = UNSET
    message_reference: Missing[MessageReference] = UNSET
    flags: Missing[MessageFlag] = UNSET
    message_snapshots: Missing[list[MessageSnapshot]] = UNSET
    referenced_message: MissingOrNullable[MessageGet] = UNSET
    interaction_metadata: Missing[MessageInteractionMetadata] = UNSET
    interaction: Missing[MessageInteraction] = UNSET
    thread: Missing[Channel] = UNSET
    components: Missing[list[DirectComponent]] = UNSET
    sticker_items: Missing[list[StickerItem]] = UNSET
    stickers: Missing[list[Sticker]] = UNSET
    position: Missing[int] = UNSET
    role_subscription_data: Missing[RoleSubscriptionData] = UNSET
    resolved: Missing[ResolvedData] = UNSET
    poll: Missing[Poll] = UNSET
    call: Missing[MessageCall] = UNSET


class MessageUpdatePayload(MessageUpdateBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessageUpdatePayload(MessageUpdateBasePayload):
    guild_id: Snowflake


class DirectMessageUpdatePayload(MessageUpdateBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessageDeleteBasePayload(BaseModel):
    id: Snowflake
    channel_id: Snowflake


class MessageDeletePayload(MessageDeleteBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessageDeletePayload(MessageDeleteBasePayload):
    guild_id: Snowflake


class DirectMessageDeletePayload(MessageDeleteBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessageDeleteBulkBasePayload(BaseModel):
    ids: list[Snowflake]
    channel_id: Snowflake


class MessageDeleteBulkPayload(MessageDeleteBulkBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessageDeleteBulkPayload(MessageDeleteBulkBasePayload):
    guild_id: Snowflake


class DirectMessageDeleteBulkPayload(MessageDeleteBulkBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessageReactionAddBasePayload(BaseModel):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    member: Missing[GuildMember] = UNSET
    emoji: Emoji
    message_author_id: Missing[Snowflake] = UNSET
    burst: bool
    burst_colors: Missing[list[str]] = UNSET
    type: ReactionType


class MessageReactionAddPayload(MessageReactionAddBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessageReactionAddPayload(MessageReactionAddBasePayload):
    guild_id: Snowflake


class DirectMessageReactionAddPayload(MessageReactionAddBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessageReactionRemoveBasePayload(BaseModel):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji
    burst: bool
    type: ReactionType


class MessageReactionRemovePayload(MessageReactionRemoveBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessageReactionRemovePayload(MessageReactionRemoveBasePayload):
    guild_id: Snowflake


class DirectMessageReactionRemovePayload(MessageReactionRemoveBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessageReactionRemoveAllBasePayload(BaseModel):
    channel_id: Snowflake
    message_id: Snowflake


class MessageReactionRemoveAllPayload(MessageReactionRemoveAllBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessageReactionRemoveAllPayload(MessageReactionRemoveAllBasePayload):
    guild_id: Snowflake


class DirectMessageReactionRemoveAllPayload(MessageReactionRemoveAllBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessageReactionRemoveEmojiBasePayload(BaseModel):
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji


class MessageReactionRemoveEmojiPayload(MessageReactionRemoveEmojiBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessageReactionRemoveEmojiPayload(MessageReactionRemoveEmojiBasePayload):
    guild_id: Snowflake


class DirectMessageReactionRemoveEmojiPayload(MessageReactionRemoveEmojiBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessagePollVoteBasePayload(BaseModel):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    answer_id: int


class MessagePollVoteAddPayload(MessagePollVoteBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessagePollVoteAddPayload(MessagePollVoteBasePayload):
    guild_id: Snowflake


class DirectMessagePollVoteAddPayload(MessagePollVoteBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class MessagePollVoteRemovePayload(MessagePollVoteBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class GuildMessagePollVoteRemovePayload(MessagePollVoteBasePayload):
    guild_id: Snowflake


class DirectMessagePollVoteRemovePayload(MessagePollVoteBasePayload):
    guild_id: Missing[Snowflake] = UNSET


class TypingStartBasePayload(BaseModel):
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: datetime.datetime


class TypingStartPayload(TypingStartBasePayload):
    guild_id: Missing[Snowflake] = UNSET
    member: Missing[GuildMember] = UNSET


class GuildTypingStartPayload(TypingStartBasePayload):
    guild_id: Snowflake
    member: GuildMember


class DirectTypingStartPayload(TypingStartBasePayload):
    guild_id: Missing[Snowflake] = UNSET
    member: Missing[GuildMember] = UNSET
