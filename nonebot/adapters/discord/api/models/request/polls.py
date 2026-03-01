from __future__ import annotations

from pydantic import BaseModel

from ..common.polls import PollMedia
from ...types import UNSET, Missing


class PollRequest(BaseModel):
    question: PollMedia
    answers: list[PollAnswerRequest]
    duration: Missing[int] = UNSET
    allow_multiselect: Missing[bool] = UNSET
    layout_type: Missing[int] = UNSET


class PollAnswerRequest(BaseModel):
    poll_media: PollMedia


__all__ = ["PollAnswerRequest", "PollRequest"]
