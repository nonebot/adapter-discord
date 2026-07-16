from typing import Annotated, Any

from nonebot.adapters.discord.api.model import TriggerMetadata
from nonebot.adapters.discord.api.types import (
    ApplicationCommandType,
    AutoModerationRuleEventType,
    TriggerType,
)
from nonebot.adapters.discord.api.validation import (
    AtMostOne,
    ForbidIfEquals,
    Range,
    RequireIfNotEquals,
    validate,
)
from nonebot.adapters.discord.domains.command.endpoints import _build_command_payloads
from tests.fake.doubles import DummyAdapter, DummyBot

import pytest


def test_range_numeric_validation() -> None:
    @validate
    def func(
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> int | None:
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
    def func(before: int | None = None, after: int | None = None) -> str:
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
        trigger_metadata: str | None = None,
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
        around: int | None = None,
        before: int | None = None,
        after: int | None = None,
    ) -> str:
        del around, before, after
        return "ok"

    assert await func(around=1) == "ok"
    with pytest.raises(
        ValueError, match="around, before and after are mutually exclusive"
    ):
        await func(around=1, before=2)


def test_bulk_command_materializes_type_and_normalizes_description() -> None:
    assert _build_command_payloads([{"name": "ping", "description": "Ping"}]) == [
        {
            "name": "ping",
            "description": "Ping",
            "type": ApplicationCommandType.CHAT_INPUT,
        }
    ]
    assert _build_command_payloads(
        [{"name": "user", "type": ApplicationCommandType.USER}]
    ) == [
        {
            "name": "user",
            "description": "",
            "type": ApplicationCommandType.USER,
        }
    ]
    with pytest.raises(
        ValueError,
        match="description is required for CHAT_INPUT commands",
    ):
        _build_command_payloads([{"name": "ping"}])


@pytest.mark.asyncio
async def test_metadata_records_preserve_item_count_validation() -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter)
    records: Any = [object()] * 6

    with pytest.raises(ValueError, match="metadata records must be 0-5 items"):
        await adapter._api_update_application_role_connection_metadata_records(  # noqa: SLF001
            bot,
            application_id=1,
            records=records,
        )

    assert adapter.request_calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("messages", [[1], list(range(101))])
async def test_bulk_delete_message_preserves_item_count_validation(
    messages: list[int],
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter)

    with pytest.raises(ValueError, match="messages must contain 2-100 items"):
        await adapter._api_bulk_delete_message(  # noqa: SLF001
            bot,
            channel_id=1,
            messages=messages,
        )

    assert adapter.request_calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "delete_message_days",
            8,
            "delete_message_days must be between 0 and 7",
        ),
        (
            "delete_message_seconds",
            604801,
            "delete_message_seconds must be between 0 and 604800",
        ),
    ],
)
async def test_create_guild_ban_preserves_delete_message_range_validation(
    field: str,
    value: int,
    message: str,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter)

    fields: dict[str, Any] = {field: value}
    with pytest.raises(ValueError, match=message):
        await adapter._api_create_guild_ban(  # noqa: SLF001
            bot,
            guild_id=1,
            user_id=2,
            **fields,
        )

    assert adapter.request_calls == 0


@pytest.mark.asyncio
async def test_create_guild_ban_preserves_mutual_exclusion_validation() -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter)
    fields: dict[str, Any] = {
        "delete_message_days": 1,
        "delete_message_seconds": 1,
    }

    with pytest.raises(
        ValueError,
        match="delete_message_days and delete_message_seconds cannot both be set",
    ):
        await adapter._api_create_guild_ban(  # noqa: SLF001
            bot,
            guild_id=1,
            user_id=2,
            **fields,
        )

    assert adapter.request_calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("field", "values", "message"),
    [
        (
            "exempt_roles",
            list(range(21)),
            "exempt_roles must be 20 items or fewer",
        ),
        (
            "exempt_channels",
            list(range(51)),
            "exempt_channels must be 50 items or fewer",
        ),
    ],
)
async def test_auto_moderation_preserves_exemption_count_validation(
    field: str,
    values: list[int],
    message: str,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter)

    fields: dict[str, Any] = {field: values}
    with pytest.raises(ValueError, match=message):
        await adapter._api_create_auto_moderation_rule(  # noqa: SLF001
            bot,
            guild_id=1,
            name="rule",
            event_type=AutoModerationRuleEventType.MESSAGE_SEND,
            trigger_type=TriggerType.SPAM,
            actions=[],
            **fields,
        )
    with pytest.raises(ValueError, match=message):
        await adapter._api_modify_auto_moderation_rule(  # noqa: SLF001
            bot,
            guild_id=1,
            rule_id=2,
            **fields,
        )

    assert adapter.request_calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("trigger_type", "fields", "message"),
    [
        (
            TriggerType.SPAM,
            {"trigger_metadata": TriggerMetadata(keyword_filter=["blocked"])},
            "trigger_metadata must be omitted for SPAM rules",
        ),
        (
            TriggerType.KEYWORD,
            {},
            "trigger_metadata is required for this trigger_type",
        ),
    ],
)
async def test_auto_moderation_preserves_trigger_metadata_cross_rules(
    trigger_type: TriggerType,
    fields: dict[str, Any],
    message: str,
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter)

    with pytest.raises(ValueError, match=message):
        await adapter._api_create_auto_moderation_rule(  # noqa: SLF001
            bot,
            guild_id=1,
            name="rule",
            event_type=AutoModerationRuleEventType.MESSAGE_SEND,
            trigger_type=trigger_type,
            actions=[],
            **fields,
        )

    assert adapter.request_calls == 0
