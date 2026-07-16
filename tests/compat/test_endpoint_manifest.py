import ast
import asyncio
import json
from pathlib import Path
import runpy
import shutil
import sys

from nonebot.adapters.discord.api.endpoint_manifest import ENDPOINT_GROUPS
from nonebot.adapters.discord.api.handle import HandleMixin
from tests.fake.doubles import DummyBot

import pytest

ROOT = Path(__file__).parents[2]
GENERATOR = ROOT / "scripts/generate_client_pyi.py"
FIXTURE = ROOT / "tests/fixtures/public_api.json"


def _endpoint_methods() -> dict[str, str]:
    owners: dict[str, str] = {}
    concrete: set[str] = set()
    for module_name, mixin_name in ENDPOINT_GROUPS:
        path = ROOT / Path(*module_name.split(".")).with_suffix(".py")
        module = ast.parse(path.read_text("utf-8"))
        mixin = next(
            node
            for node in module.body
            if isinstance(node, ast.ClassDef) and node.name == mixin_name
        )
        for node in mixin.body:
            if not isinstance(node, ast.AsyncFunctionDef) or not node.name.startswith(
                "_api_"
            ):
                continue
            assert owners.setdefault(node.name, module_name) == module_name
            overload = any(
                isinstance(decorator, ast.Name) and decorator.id == "overload"
                for decorator in node.decorator_list
            )
            if not overload:
                concrete.add(node.name)
    assert len(concrete) == 223
    return owners


def test_endpoint_manifest_exactly_owns_runtime_mro() -> None:
    assert (
        tuple((base.__module__, base.__name__) for base in HandleMixin.__bases__)
        == ENDPOINT_GROUPS
    )
    owners = _endpoint_methods()
    assert {name.removeprefix("_api_") for name in owners} == {
        name.removeprefix("_api_")
        for name in dir(HandleMixin)
        if name.startswith("_api_")
    }


def test_stub_has_stable_230_method_public_surface() -> None:
    fixture = json.loads(FIXTURE.read_text("utf-8"))
    expected = fixture["api_client"]
    assert expected["async_method_count"] == 230
    module = ast.parse(
        (ROOT / "nonebot/adapters/discord/api/client.pyi").read_text("utf-8")
    )
    client = next(
        node
        for node in module.body
        if isinstance(node, ast.ClassDef) and node.name == "ApiClient"
    )
    methods = [node for node in client.body if isinstance(node, ast.AsyncFunctionDef)]
    assert len(methods) == 230
    assert (
        sum(
            any(
                isinstance(decorator, ast.Name) and decorator.id == "overload"
                for decorator in method.decorator_list
            )
            for method in methods
        )
        == 13
    )
    assert "domains." not in (
        ROOT / "nonebot/adapters/discord/api/client.pyi"
    ).read_text("utf-8")


def test_bot_dynamic_api_dispatch_does_not_call_endpoint_parameters(
    dummy_bot: DummyBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owners = _endpoint_methods()
    calls: list[str] = []

    async def record(_bot: object, api: str, **_data: object) -> None:
        calls.append(api)

    adapter = dummy_bot.adapter
    monkeypatch.setattr(adapter, "_call_api", record)

    async def invoke_every_public_api() -> None:
        for endpoint_name in owners:
            await getattr(dummy_bot, endpoint_name.removeprefix("_api_"))()

    asyncio.run(invoke_every_public_api())
    assert calls == [name.removeprefix("_api_") for name in owners]


def _copy_generator_inputs(destination: Path) -> None:
    relative_paths = [
        Path("scripts/generate_client_pyi.py"),
        Path("nonebot/adapters/discord/api/endpoint_manifest.py"),
        Path("nonebot/adapters/discord/api/handle.py"),
        Path("nonebot/adapters/discord/api/model.py"),
        Path("nonebot/adapters/discord/api/types.py"),
        Path("nonebot/adapters/discord/api/client.pyi"),
        Path("nonebot/adapters/discord/domains/models.py"),
    ]
    relative_paths.extend(
        Path(*module_name.split(".")).with_suffix(".py")
        for module_name, _ in ENDPOINT_GROUPS
    )
    for relative_path in relative_paths:
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative_path, target)


async def _run_generator(root: Path, *args: str) -> int:
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        str(root / "scripts/generate_client_pyi.py"),
        *args,
        cwd=root,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()
    return await process.wait()


def test_generator_is_deterministic_and_check_renders_before_comparing(
    tmp_path: Path,
) -> None:
    _copy_generator_inputs(tmp_path)
    assert asyncio.run(_run_generator(tmp_path)) == 0
    client_path = tmp_path / "nonebot/adapters/discord/api/client.pyi"
    first = client_path.read_bytes()
    assert asyncio.run(_run_generator(tmp_path, "--check")) == 0

    endpoint_path = tmp_path / "nonebot/adapters/discord/domains/command/endpoints.py"
    source = endpoint_path.read_text("utf-8")
    endpoint_path.write_text(
        source.replace("application_id: SnowflakeType", "application_id: int", 1),
        "utf-8",
    )
    assert asyncio.run(_run_generator(tmp_path, "--check")) == 1
    assert asyncio.run(_run_generator(tmp_path)) == 0
    assert asyncio.run(_run_generator(tmp_path, "--check")) == 0
    second = client_path.read_bytes()
    assert asyncio.run(_run_generator(tmp_path)) == 0
    assert client_path.read_bytes() == second
    assert first != second


def test_generator_rejects_manifest_or_assembly_drift() -> None:
    generator = runpy.run_path(str(GENERATOR))
    assert callable(generator["generate"])
    assert generator["generate"](ROOT) == (
        ROOT / "nonebot/adapters/discord/api/client.pyi"
    ).read_text("utf-8")
