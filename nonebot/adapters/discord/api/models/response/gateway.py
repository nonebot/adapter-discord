from __future__ import annotations

from pydantic import BaseModel


class Gateway(BaseModel):
    url: str


class GatewayBot(BaseModel):
    url: str
    shards: int
    session_start_limit: SessionStartLimit


class SessionStartLimit(BaseModel):
    total: int
    remaining: int
    reset_after: int
    max_concurrency: int


__all__ = ["Gateway", "GatewayBot", "SessionStartLimit"]
