from typing import Annotated, Optional

from nonebot.adapters.discord.api.types import TriggerType
from nonebot.adapters.discord.api.validation import (
    AtMostOne,
    ForbidIfEquals,
    Range,
    RequireIfNotEquals,
    validate,
)

import pytest


def test_range_numeric_validation() -> None:
    @validate
    def func(
        limit: Annotated[
            Optional[int],
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> Optional[int]:
        return limit

    assert func(limit=1) == 1
    assert func(limit=100) == 100
    with pytest.raises(ValueError, match="limit must be between 1 and 100"):
        func(limit=101)


def test_range_length_validation() -> None:
    @validate
    def func(
        records: Annotated[
            list[int],
            Range(message="metadata records must be 0-5 items", max_length=5),
        ],
    ) -> int:
        return len(records)

    assert func(records=[1, 2, 3]) == 3
    with pytest.raises(ValueError, match="metadata records must be 0-5 items"):
        func(records=[1, 2, 3, 4, 5, 6])


def test_cross_rule_at_most_one() -> None:
    @validate(
        cross_rules=(
            AtMostOne(
                fields=("before", "after"),
                message="before and after are mutually exclusive",
            ),
        )
    )
    def func(before: Optional[int] = None, after: Optional[int] = None) -> str:
        if before is None and after is None:
            return "ok"
        return "ok"

    assert func(before=1) == "ok"
    assert func(after=2) == "ok"
    with pytest.raises(ValueError, match="before and after are mutually exclusive"):
        func(before=1, after=2)


def test_cross_rules_forbid_and_require() -> None:
    @validate(
        cross_rules=(
            ForbidIfEquals(
                field="trigger_metadata",
                when_field="trigger_type",
                equals=TriggerType.SPAM,
                message="trigger_metadata must be omitted for SPAM rules",
            ),
            RequireIfNotEquals(
                field="trigger_metadata",
                when_field="trigger_type",
                equals=TriggerType.SPAM,
                message="trigger_metadata is required for this trigger_type",
            ),
        )
    )
    def func(
        trigger_type: TriggerType,
        trigger_metadata: Optional[str] = None,
    ) -> str:
        if trigger_type == TriggerType.SPAM and trigger_metadata is None:
            return "ok"
        return "ok"

    assert func(trigger_type=TriggerType.SPAM, trigger_metadata=None) == "ok"
    assert func(trigger_type=TriggerType.KEYWORD, trigger_metadata="abc") == "ok"
    with pytest.raises(
        ValueError, match="trigger_metadata must be omitted for SPAM rules"
    ):
        func(trigger_type=TriggerType.SPAM, trigger_metadata="abc")
    with pytest.raises(
        ValueError, match="trigger_metadata is required for this trigger_type"
    ):
        func(trigger_type=TriggerType.KEYWORD, trigger_metadata=None)


@pytest.mark.asyncio
async def test_async_wrapper_cross_rules() -> None:
    @validate(
        cross_rules=(
            AtMostOne(
                fields=("around", "before", "after"),
                message="around, before and after are mutually exclusive",
            ),
        )
    )
    async def func(
        around: Optional[int] = None,
        before: Optional[int] = None,
        after: Optional[int] = None,
    ) -> str:
        del around, before, after
        return "ok"

    assert await func(around=1) == "ok"
    with pytest.raises(
        ValueError, match="around, before and after are mutually exclusive"
    ):
        await func(around=1, before=2)
