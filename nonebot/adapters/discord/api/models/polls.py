from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..types import UNSET, Missing

if TYPE_CHECKING:
    from ..model import Emoji


class Poll(BaseModel):
    """The poll object has a lot of levels and nested structures.
    It was also designed to support future extensibility,
    so some fields may appear to be more complex than necessary.

    see https://discord.com/developers/docs/resources/poll#poll-object
    """

    question: PollMedia
    """The question of the poll. Only `text` is supported."""
    answers: list[PollAnswer]
    """Each of the answers available in the poll."""
    expiry: datetime.datetime | None = None
    """The time when the poll ends."""
    allow_multiselect: bool
    """Whether a user can select multiple answers"""
    layout_type: int
    """The layout type of the poll"""
    results: Missing[PollResults] = UNSET
    """The results of the poll"""


class PollRequest(BaseModel):
    """This is the request object used when creating a poll across the
    different endpoints. It is similar but not exactly identical to the
    main poll object. The main difference is that the request has `duration`
    which eventually becomes `expiry`.

    see https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    question: PollMedia
    """The question of the poll. Only `text` is supported."""
    answers: list[PollAnswerRequest]
    """Each of the answers available in the poll, up to 10"""
    duration: Missing[int] = UNSET
    """Number of hours the poll should be open for, up to 32 days. Defaults to 24"""
    allow_multiselect: Missing[bool] = UNSET
    """Whether a user can select multiple answers. Defaults to false"""
    layout_type: Missing[int] = UNSET
    """The layout type of the poll"""


class PollAnswer(BaseModel):
    """answer_id: Only sent as part of responses from Discord's API/Gateway.

    see https://discord.com/developers/docs/resources/poll#poll-answer-object
    """

    answer_id: int
    poll_media: PollMedia


class PollAnswerRequest(BaseModel):
    """Poll answer request object.

    see https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    poll_media: PollMedia


class PollMedia(BaseModel):
    """The poll media object is a common object that backs both the question and
    answers. The intention is that it allows us to extensibly add new ways to
    display things in the future. For now, `question` only supports `text`, while
    answers can have an optional `emoji`.

    see https://discord.com/developers/docs/resources/poll#poll-media-object
    """

    text: Missing[str] = UNSET
    emoji: Missing[Emoji] = UNSET


class PollResults(BaseModel):
    """Poll Results

    see https://discord.com/developers/docs/resources/poll#poll-results-object
    """

    is_finalized: bool
    answer_counts: list[PollAnswerCount]


class PollAnswerCount(BaseModel):
    """Poll Answer Count

    see https://discord.com/developers/docs/resources/poll#poll-results-object-poll-answer-count-object-structure
    """

    id: int
    count: int
    me_voted: bool
