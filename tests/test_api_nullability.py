from nonebot.adapters.discord.api import ComponentEmoji, Snowflake
from nonebot.adapters.discord.api.types import UNSET
from nonebot.adapters.discord.utils import omit_unset

from nonebot.compat import type_validate_python


def test_omit_unset_filters_unset_in_list() -> None:
    payload = omit_unset({"arr": [1, UNSET, {"a": UNSET, "b": 2}]})
    assert payload == {"arr": [1, {"b": 2}]}


def test_component_emoji_allows_missing_partial_fields() -> None:
    emoji = type_validate_python(ComponentEmoji, {"name": "🔗"})

    assert emoji.id is UNSET
    assert emoji.name == "🔗"
    assert emoji.animated is UNSET


def test_component_emoji_id_is_nullable_snowflake() -> None:
    emoji = type_validate_python(ComponentEmoji, {"id": "41771983429993937"})

    assert isinstance(emoji.id, Snowflake)
    assert emoji.id == Snowflake(41771983429993937)
    assert emoji.name is UNSET
