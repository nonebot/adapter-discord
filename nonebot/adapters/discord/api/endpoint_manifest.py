"""Ordered endpoint ownership shared by runtime assembly and stub generation."""

ENDPOINT_GROUPS: tuple[tuple[str, str], ...] = (
    ("nonebot.adapters.discord.domains.command.endpoints", "CommandEndpointMixin"),
    (
        "nonebot.adapters.discord.domains.interaction.endpoints",
        "InteractionEndpointMixin",
    ),
    (
        "nonebot.adapters.discord.domains.application.endpoints",
        "ApplicationEndpointMixin",
    ),
    (
        "nonebot.adapters.discord.domains.moderation.endpoints",
        "ModerationEndpointMixin",
    ),
    ("nonebot.adapters.discord.domains.channel.endpoints", "ChannelEndpointMixin"),
    ("nonebot.adapters.discord.domains.message.endpoints", "MessageEndpointMixin"),
    ("nonebot.adapters.discord.domains.emoji.endpoints", "EmojiEndpointMixin"),
    (
        "nonebot.adapters.discord.domains.soundboard.endpoints",
        "SoundboardEndpointMixin",
    ),
    ("nonebot.adapters.discord.domains.lobby.endpoints", "LobbyEndpointMixin"),
    ("nonebot.adapters.discord.domains.guild.endpoints", "GuildEndpointMixin"),
    ("nonebot.adapters.discord.domains.invite.endpoints", "InviteEndpointMixin"),
    ("nonebot.adapters.discord.domains.voice.endpoints", "VoiceEndpointMixin"),
    ("nonebot.adapters.discord.domains.sticker.endpoints", "StickerEndpointMixin"),
    ("nonebot.adapters.discord.domains.user.endpoints", "UserEndpointMixin"),
    ("nonebot.adapters.discord.domains.webhook.endpoints", "WebhookEndpointMixin"),
    ("nonebot.adapters.discord.domains.gateway.endpoints", "GatewayEndpointMixin"),
)

__all__ = ["ENDPOINT_GROUPS"]
