from __future__ import annotations

from pydantic import BaseModel

from ..common.channels import Channel, ThreadMember


class ArchivedThreadsResponse(BaseModel):
    threads: list[Channel]
    members: list[ThreadMember]
    has_more: bool


class ListActiveGuildThreadsResponse(BaseModel):
    threads: list[Channel]
    members: list[ThreadMember]


__all__ = [
    "ArchivedThreadsResponse",
    "ListActiveGuildThreadsResponse",
]
