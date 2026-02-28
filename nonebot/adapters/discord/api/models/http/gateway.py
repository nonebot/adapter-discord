from __future__ import annotations

from pydantic import BaseModel


class Gateway(BaseModel):
    """Get Gateway Response

    see https://discord.com/developers/docs/topics/gateway#get-gateway
    """

    url: str


class GatewayBot(BaseModel):
    """Get Gateway Bot Response

    see https://discord.com/developers/docs/topics/gateway#get-gateway-bot
    """

    url: str
    shards: int
    session_start_limit: SessionStartLimit


class SessionStartLimit(BaseModel):
    """Session start limit

    see https://discord.com/developers/docs/topics/gateway#session-start-limit-object
    """

    total: int
    remaining: int
    reset_after: int
    max_concurrency: int
