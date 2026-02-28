from __future__ import annotations

import datetime

from pydantic import BaseModel

from ...types import UNSET, EmbedTypes, Missing


class Embed(BaseModel):
    """Embed

    see https://discord.com/developers/docs/resources/channel#embed-object"""

    title: Missing[str] = UNSET
    type: Missing[EmbedTypes] = UNSET
    description: Missing[str] = UNSET
    url: Missing[str] = UNSET
    timestamp: Missing[datetime.datetime] = UNSET
    color: Missing[int] = UNSET
    footer: Missing[EmbedFooter] = UNSET
    image: Missing[EmbedImage] = UNSET
    thumbnail: Missing[EmbedThumbnail] = UNSET
    video: Missing[EmbedVideo] = UNSET
    provider: Missing[EmbedProvider] = UNSET
    author: Missing[EmbedAuthor] = UNSET
    fields: Missing[list[EmbedField]] = UNSET


class EmbedThumbnail(BaseModel):
    """Embed thumbnail.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-thumbnail-structure
    """

    url: str
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedVideo(BaseModel):
    """Embed video.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-video-structure
    """

    url: Missing[str] = UNSET
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedImage(BaseModel):
    """Embed image.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-image-structure
    """

    url: str
    proxy_url: Missing[str] = UNSET
    height: Missing[int] = UNSET
    width: Missing[int] = UNSET


class EmbedProvider(BaseModel):
    """Embed provider.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-provider-structure
    """

    name: Missing[str] = UNSET
    url: Missing[str] = UNSET


class EmbedAuthor(BaseModel):
    """Embed author.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-author-structure
    """

    name: str
    url: Missing[str] = UNSET
    icon_url: Missing[str] = UNSET
    proxy_icon_url: Missing[str] = UNSET


class EmbedFooter(BaseModel):
    """Embed footer.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-footer-structure
    """

    text: str
    icon_url: Missing[str] = UNSET
    proxy_icon_url: Missing[str] = UNSET


class EmbedField(BaseModel):
    """Embed field.

    see https://discord.com/developers/docs/resources/message#embed-object-embed-field-structure
    """

    name: str
    value: str
    inline: Missing[bool] = UNSET
