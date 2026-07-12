import importlib
from typing_extensions import is_typeddict

from nonebot.adapters.discord.domains import bootstrap

from nonebot.compat import PYDANTIC_V2

if PYDANTIC_V2:
    from pydantic import TypeAdapter


WRITE_DOMAINS = (
    "application",
    "channel",
    "command",
    "emoji",
    "guild",
    "interaction",
    "lobby",
    "message",
    "moderation",
    "soundboard",
    "sticker",
    "user",
    "voice",
    "webhook",
)


def test_all_rest_write_exports_are_resolved_typed_dicts() -> None:
    bootstrap()
    for domain in WRITE_DOMAINS:
        module = importlib.import_module(
            f"nonebot.adapters.discord.domains.{domain}.write"
        )
        for name in module.__all__:
            model = getattr(module, name)
            if not is_typeddict(model):
                continue
            assert is_typeddict(model), f"{domain}.write.{name}"
            assert not (model.__required_keys__ & model.__optional_keys__)
            assert model.__required_keys__ | model.__optional_keys__ == set(
                model.__annotations__
            )
            assert all(
                not isinstance(value, str) for value in model.__annotations__.values()
            )
            if PYDANTIC_V2:
                TypeAdapter(model)
