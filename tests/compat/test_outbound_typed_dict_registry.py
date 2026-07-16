import importlib
import inspect
import json
from pathlib import Path
from typing import get_origin
from typing_extensions import Unpack, is_typeddict

from nonebot.adapters.discord.domains import bootstrap
from tests.fake.doubles import DummyAdapter

from nonebot.compat import PYDANTIC_V2

if PYDANTIC_V2:
    from pydantic import TypeAdapter, ValidationError

import pytest

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

_BODY_FIXTURE = json.loads(
    (
        Path(__file__).parents[1] / "fixtures" / "rest_body_characterization.json"
    ).read_text()
)
_STRUCTURED_BODY_ENDPOINTS = {
    "_api_bulk_overwrite_global_application_commands",
    "_api_bulk_overwrite_guild_application_commands",
    "_api_create_guild_from_guild_template",
    "_api_create_guild_sticker",
    "_api_create_interaction_response",
    "_api_execute_github_compatible_webhook",
    "_api_execute_slack_compatible_webhook",
    "_api_modify_guild_channel_positions",
    "_api_modify_guild_role_positions",
    "_api_update_application_role_connection_metadata_records",
    "_api_update_invite_target_users",
}
TYPED_BODY_ENDPOINTS = tuple(
    sorted(
        name
        for name, expected in _BODY_FIXTURE.items()
        if (expected["json"] is not None or expected["files"] is not None)
        and name not in _STRUCTURED_BODY_ENDPOINTS
    )
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


@pytest.mark.parametrize("name", TYPED_BODY_ENDPOINTS)
def test_rest_body_endpoints_expose_typed_dict_unpack(name: str) -> None:
    signature = inspect.signature(getattr(DummyAdapter, name))

    assert "fields" in signature.parameters
    fields = signature.parameters["fields"]
    assert fields.kind is inspect.Parameter.VAR_KEYWORD
    assert get_origin(fields.annotation) is Unpack


@pytest.mark.skipif(not PYDANTIC_V2, reason="Pydantic v2 TypedDict config")
def test_all_rest_write_typed_dicts_forbid_extra_fields() -> None:
    bootstrap()
    for domain in WRITE_DOMAINS:
        module = importlib.import_module(
            f"nonebot.adapters.discord.domains.{domain}.write"
        )
        for name in module.__all__:
            model = getattr(module, name)
            if not is_typeddict(model):
                continue
            with pytest.raises(ValidationError) as excinfo:
                TypeAdapter(model).validate_python({"__unknown__": None})
            assert any(
                error["type"] == "extra_forbidden" for error in excinfo.value.errors()
            ), f"{domain}.write.{name}"
