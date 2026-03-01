from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ...types import UNSET, Missing

if TYPE_CHECKING:
    from .emoji import Emoji
    from .user import User


class Poll(BaseModel):
    question: PollMedia
    answers: list[PollAnswer]
    expiry: datetime.datetime | None = None
    allow_multiselect: bool
    layout_type: int
    results: Missing[PollResults] = UNSET


class PollAnswer(BaseModel):
    answer_id: int
    poll_media: PollMedia


class PollMedia(BaseModel):
    text: Missing[str] = UNSET
    emoji: Missing[Emoji] = UNSET


class PollResults(BaseModel):
    is_finalized: bool
    answer_counts: list[PollAnswerCount]


class PollAnswerCount(BaseModel):
    id: int
    count: int
    me_voted: bool


class AnswerVoters(BaseModel):
    users: list[User]
