from nonebot.adapters.discord import api, protocol
from nonebot.adapters.discord.api import model, types

from nonebot.compat import type_validate_python


def test_protocol_foundation_preserves_public_facade_identity() -> None:
    assert api.UNSET is protocol.UNSET
    assert model.Snowflake is protocol.Snowflake
    assert types.UnsetType is protocol.UnsetType
    assert types.Missing is protocol.Missing
    assert types.MissingOrNullable is protocol.MissingOrNullable
    assert types.is_unset is protocol.is_unset
    assert types.is_not_unset is protocol.is_not_unset
    assert model.SnowflakeType is protocol.SnowflakeType
    assert model.Missing is protocol.Missing
    assert model.MissingOrNullable is protocol.MissingOrNullable
    assert model.Snowflake("123") == 123
    assert type_validate_python(model.Snowflake, "123") == 123
    assert bool(protocol.UNSET) is False
    assert repr(protocol.UNSET) == "<UNSET>"


def test_protocol_foundation_preserves_public_module_paths() -> None:
    assert types.UNSET.__module__ == "nonebot.adapters.discord.api.types"
    assert types.InteractionType.__module__ == "nonebot.adapters.discord.api.types"
    assert model.Snowflake.__module__ == "nonebot.adapters.discord.api.model"
    assert model.MessageGet.__module__ == "nonebot.adapters.discord.api.model"
