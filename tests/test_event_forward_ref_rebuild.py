from typing import Any

from nonebot.adapters.discord.event import (
    DirectMessageCreateEvent,
    GuildCreateEvent,
    GuildMessageCreateEvent,
    MessageCreateEvent,
)

from nonebot.compat import type_validate_python
from pydantic import ValidationError
import pytest


def test_guild_create_event_forward_refs_are_resolved() -> None:
    with pytest.raises(ValidationError):
        type_validate_python(GuildCreateEvent, {})


def test_message_create_union_forward_refs_are_resolved() -> None:
    event_union: Any = (
        GuildMessageCreateEvent | DirectMessageCreateEvent | MessageCreateEvent
    )
    with pytest.raises(ValidationError):
        type_validate_python(event_union, {})
