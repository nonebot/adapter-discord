from nonebot.adapters.discord.event import (
    DirectMessageDeleteEvent,
    GuildMessageCreateEvent,
)

from nonebot.compat import type_validate_python


def _build_message_create_payload() -> dict[str, object]:
    return {
        "id": "1",
        "channel_id": "100",
        "guild_id": "300",
        "author": {
            "id": "2",
            "username": "tester",
            "discriminator": "0",
            "global_name": None,
            "avatar": None,
        },
        "content": "hello\nworld",
        "timestamp": "2026-02-14T00:00:00+00:00",
        "edited_timestamp": None,
        "tts": False,
        "mention_everyone": False,
        "mentions": [],
        "mention_roles": [],
        "attachments": [],
        "embeds": [],
        "pinned": False,
        "type": 0,
    }


def test_message_event_description_is_simplified() -> None:
    event = type_validate_python(
        GuildMessageCreateEvent, _build_message_create_payload()
    )

    desc = event.get_event_description()

    assert "Message 1 from 2(tester)@[Guild 300, Channel 100]" in desc
    assert "hello\\nworld" in desc
    assert "<UNSET>" not in desc


def test_non_message_event_description_omits_unset_fields() -> None:
    event = type_validate_python(
        DirectMessageDeleteEvent, {"id": "1", "channel_id": "100"}
    )

    desc = event.get_event_description()

    assert "<UNSET>" not in desc
    assert "guild_id" not in desc
