from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path

from nonebot.adapters.discord import protocol
from nonebot.adapters.discord.api import model as public_model, types as public_types
from nonebot.adapters.discord.domains import bootstrap
from nonebot.adapters.discord.domains._manifest import (
    DOMAIN_MODEL_MODULES,
    DOMAIN_TYPE_MODULES,
    PROTOCOL_TYPE_EXPORTS,
    TYPE_EXPORT_OWNERS,
)

from pydantic import BaseModel

ROOT = Path(__file__).parents[2]
TYPE_FIXTURE = ROOT / "tests" / "fixtures" / "domain_type_exports.json"


def test_type_manifest_is_complete_ordered_and_identity_preserving() -> None:
    baseline = json.loads(TYPE_FIXTURE.read_text("utf-8"))
    assert list(public_types.__all__) == baseline
    assert not set(PROTOCOL_TYPE_EXPORTS) & set(TYPE_EXPORT_OWNERS)
    assert set(PROTOCOL_TYPE_EXPORTS) | set(TYPE_EXPORT_OWNERS) == set(
        public_types.__all__
    )

    type_modules = {
        module.rsplit(".", 2)[-2]: importlib.import_module(module)
        for module in DOMAIN_TYPE_MODULES
    }
    for name in public_types.__all__:
        if name in PROTOCOL_TYPE_EXPORTS:
            assert getattr(public_types, name) is getattr(protocol, name)
            continue
        owner = TYPE_EXPORT_OWNERS[name]
        owner_module = type_modules[owner]
        assert name in owner_module.__all__
        value = getattr(owner_module, name)
        assert getattr(public_types, name) is value
        assert value.__module__ == "nonebot.adapters.discord.api.types"


def test_model_manifest_exports_are_duplicate_free_and_facade_identical() -> None:
    canonical: dict[str, object] = {}
    for module_name in DOMAIN_MODEL_MODULES:
        module = importlib.import_module(module_name)
        assert hasattr(module, "__all__")
        for name in module.__all__:
            assert name not in canonical, f"duplicate canonical model name: {name}"
            canonical[name] = getattr(module, name)

    special = {
        "BaseModel": BaseModel,
        "Snowflake": protocol.Snowflake,
        "SnowflakeType": protocol.SnowflakeType,
    }
    assert set(public_model.__all__) == set(canonical) & set(
        public_model.__all__
    ) | set(special)
    for name in public_model.__all__:
        expected = special[name] if name in special else canonical[name]
        assert getattr(public_model, name) is expected
        if isinstance(expected, type) and name != "BaseModel":
            assert expected.__module__ == "nonebot.adapters.discord.api.model"


def test_manifest_modules_and_public_facades_have_no_canonical_definitions() -> None:
    for module_name in (*DOMAIN_TYPE_MODULES, *DOMAIN_MODEL_MODULES):
        module = importlib.import_module(module_name)
        assert isinstance(module.__all__, list)
    for path in (
        ROOT / "nonebot/adapters/discord/api/types.py",
        ROOT / "nonebot/adapters/discord/api/model.py",
    ):
        tree = ast.parse(path.read_text("utf-8"))
        assert not any(isinstance(node, ast.ClassDef) for node in tree.body)


def test_rebuild_uses_manifest_classes_after_public_module_binding() -> None:
    namespace = bootstrap()
    assert namespace["MessageGet"] is public_model.MessageGet
