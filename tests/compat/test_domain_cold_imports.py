import importlib
from pathlib import Path
import sys
from types import ModuleType
from typing import cast, get_args, get_type_hints

import nonebot.adapters

import pytest

ROOT = Path(__file__).parents[2]
SOURCE_ADAPTERS = ROOT / "nonebot" / "adapters"
_DISCORD_MODULE_PREFIX = "nonebot.adapters.discord"


def _assert_cold_import_contract(target: str, module: ModuleType) -> None:
    if target == "nonebot.adapters.discord.domains.message.read":
        assert module.Snowflake("123") == 123
        assert bool(module.UNSET) is False
        assert module.MessageType.DEFAULT == 0
        assert get_type_hints(module.MessageGet)["referenced_message"] is not None
    elif target == "nonebot.adapters.discord.domains.interaction.read":
        component_module = importlib.import_module(
            "nonebot.adapters.discord.domains.component.read"
        )
        assert len(get_args(module.InteractionData)) == 3
        assert len(get_args(component_module.Component)) == 4
        assert module.ApplicationCommandData.__name__ == "ApplicationCommandData"
    elif target == "nonebot.adapters.discord.api.model":
        message_module = importlib.import_module(
            "nonebot.adapters.discord.domains.message.read"
        )
        protocol_module = importlib.import_module("nonebot.adapters.discord.protocol")
        assert module.MessageGet is message_module.MessageGet
        assert module.Snowflake is protocol_module.Snowflake
    elif target == "nonebot.adapters.discord.event":
        fields = (
            getattr(module.GuildMessageCreateEvent, "model_fields", None)
            or module.GuildMessageCreateEvent.__fields__
        )
        assert "id" in fields
        assert module.GuildMessageCreateEvent.__mro__[2] is module.MessageEvent
    else:
        message = f"Unexpected cold-import target: {target}"
        raise AssertionError(message)


@pytest.mark.parametrize(
    "target",
    [
        "nonebot.adapters.discord.domains.message.read",
        "nonebot.adapters.discord.domains.interaction.read",
        "nonebot.adapters.discord.api.model",
        "nonebot.adapters.discord.event",
    ],
)
def test_cold_imports_rebuild_canonical_forward_references(target: str) -> None:
    original_modules = {
        name: module
        for name, module in sys.modules.items()
        if name.startswith(_DISCORD_MODULE_PREFIX)
    }
    adapters_namespace = cast("dict[str, object]", vars(nonebot.adapters))
    original_discord = adapters_namespace.get("discord")
    original_paths = list(nonebot.adapters.__path__)
    for name in original_modules:
        del sys.modules[name]
    nonebot.adapters.__path__.insert(0, str(SOURCE_ADAPTERS))
    try:
        module = importlib.import_module(target)
        _assert_cold_import_contract(target, module)
    finally:
        nonebot.adapters.__path__[:] = original_paths
        for name in tuple(sys.modules):
            if name.startswith(_DISCORD_MODULE_PREFIX):
                del sys.modules[name]
        sys.modules.update(original_modules)
        if original_discord is None:
            adapters_namespace.pop("discord", None)
        else:
            adapters_namespace["discord"] = original_discord
