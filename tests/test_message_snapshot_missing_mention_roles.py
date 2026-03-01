from nonebot.adapters.discord.api.models import MessageGet
from nonebot.adapters.discord.api.types import is_unset

from nonebot.compat import type_validate_python


def test_message_snapshot_allows_missing_mention_roles() -> None:
    payload = {
        "id": "1476606533273129173",
        "channel_id": "1471584311823171679",
        "author": {
            "id": "516240373413183488",
            "username": "scdhh",
            "discriminator": "0",
            "avatar": None,
        },
        "content": "",
        "timestamp": "2026-02-26T15:47:11.555000+00:00",
        "edited_timestamp": None,
        "tts": False,
        "mention_everyone": False,
        "mentions": [],
        "mention_roles": [],
        "attachments": [],
        "embeds": [],
        "pinned": False,
        "type": 0,
        "message_snapshots": [
            {
                "message": {
                    "type": 0,
                    "timestamp": "2026-02-26T12:12:49.395000+00:00",
                    "mentions": [],
                    "flags": 0,
                    "embeds": [],
                    "edited_timestamp": None,
                    "content": "bar",
                    "components": [],
                    "attachments": [],
                }
            }
        ],
    }

    msg = type_validate_python(MessageGet, payload)
    assert not is_unset(msg.message_snapshots)
    assert len(msg.message_snapshots) == 1
    assert is_unset(msg.message_snapshots[0].message.mention_roles)
