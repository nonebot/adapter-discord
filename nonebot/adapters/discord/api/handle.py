"""Runtime assembly for domain-owned Discord REST endpoint mixins."""

from typing_extensions import Protocol

from yarl import URL

from ..domains.application.endpoints import ApplicationEndpointMixin
from ..domains.channel.endpoints import ChannelEndpointMixin
from ..domains.command.endpoints import CommandEndpointMixin
from ..domains.emoji.endpoints import EmojiEndpointMixin
from ..domains.gateway.endpoints import GatewayEndpointMixin
from ..domains.guild.endpoints import GuildEndpointMixin
from ..domains.interaction.endpoints import InteractionEndpointMixin
from ..domains.invite.endpoints import InviteEndpointMixin
from ..domains.lobby.endpoints import LobbyEndpointMixin
from ..domains.message.endpoints import MessageEndpointMixin
from ..domains.moderation.endpoints import ModerationEndpointMixin
from ..domains.soundboard.endpoints import SoundboardEndpointMixin
from ..domains.sticker.endpoints import StickerEndpointMixin
from ..domains.user.endpoints import UserEndpointMixin
from ..domains.voice.endpoints import VoiceEndpointMixin
from ..domains.webhook.endpoints import WebhookEndpointMixin
from ..transport.exchange import RestTransport


class AdapterProtocol(RestTransport, Protocol):
    base_url: URL


# Keep these bases in ENDPOINT_GROUPS order. The manifest and stub generator
# reject any MRO drift from this assembly.


class HandleMixin(
    CommandEndpointMixin,
    InteractionEndpointMixin,
    ApplicationEndpointMixin,
    ModerationEndpointMixin,
    ChannelEndpointMixin,
    MessageEndpointMixin,
    EmojiEndpointMixin,
    SoundboardEndpointMixin,
    LobbyEndpointMixin,
    GuildEndpointMixin,
    InviteEndpointMixin,
    VoiceEndpointMixin,
    StickerEndpointMixin,
    UserEndpointMixin,
    WebhookEndpointMixin,
    GatewayEndpointMixin,
):
    """Compose the endpoint implementation groups in manifest order."""


__all__ = ["HandleMixin"]
