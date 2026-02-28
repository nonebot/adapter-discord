from nonebot.adapters.discord.adapter import Adapter
from nonebot.adapters.discord.api.models import Dispatch, Opcode
from nonebot.adapters.discord.event import GuildCreateCompatEvent

from nonebot.compat import type_validate_python
import pytest


def _build_mixed_guild_create_dispatch() -> Dispatch:
    payload: dict[str, object] = {
        "op": Opcode.DISPATCH,
        "d": {
            "id": "1",
            "roles": [{"id": "1", "permissions": 104320577}],
            "channels": [
                {
                    "id": "10",
                    "permission_overwrites": [
                        {
                            "id": "1",
                            "type": "role",
                            "allow": 0,
                            "deny": 1024,
                        }
                    ],
                }
            ],
        },
        "s": 1,
        "t": "GUILD_CREATE",
    }
    return type_validate_python(Dispatch, payload)


def test_mixed_guild_create_payload_uses_compat_event(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    logs: list[tuple[str, str]] = []

    def fake_log(level: str, message: str, *_args: object) -> None:
        logs.append((level, message))

    monkeypatch.setattr("nonebot.adapters.discord.event.log", fake_log)

    dispatch = _build_mixed_guild_create_dispatch()
    event = Adapter.payload_to_event(dispatch)

    assert isinstance(event, GuildCreateCompatEvent)
    assert any(
        level == "WARNING" and "GuildCreateCompatEvent" in message
        for level, message in logs
    )
