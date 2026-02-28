import ast
from pathlib import Path

# 针对 NoneBot 命名空间包的特殊处理,确保能够导入本地代码
try:
    import nonebot.adapters

    local_adapters_path = str(Path(__file__).parent.parent / "nonebot" / "adapters")
    if local_adapters_path not in nonebot.adapters.__path__:
        nonebot.adapters.__path__.append(local_adapters_path)
except (ImportError, AttributeError):
    pass

from nonebot.adapters.discord.api import models


def test_models_facade_all_consistent() -> None:
    """断言 __all__ 中每个名字都能 getattr(models, name)"""
    for name in models.__all__:
        assert hasattr(models, name), (
            f"models.__all__ contains {name}, but models has no such attribute"
        )
        assert getattr(models, name) is not None


def test_models_facade_all_no_duplicates() -> None:
    """断言 __all__ 无重复"""
    assert len(models.__all__) == len(set(models.__all__)), (
        "models.__all__ contains duplicate names"
    )


def test_models_layer_dependencies() -> None:
    """AST 扫描分层依赖"""
    base_path = (
        Path(__file__).parent.parent
        / "nonebot"
        / "adapters"
        / "discord"
        / "api"
        / "models"
    )

    # 规则1: common/ 禁止 import-from request*/response*/gateway*
    common_path = base_path / "common"
    for py_file in common_path.rglob("*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                forbidden = ("request", "response", "gateway")
                if any(node.module.startswith(f) for f in forbidden):
                    msg = (
                        f"Illegal import in {py_file}: from {node.module} import ... "
                        "(common layer should not depend on request/response/gateway)",
                    )
                    raise AssertionError(msg)

    # 规则2: gateway/ 禁止 import-from request*/response*
    gateway_path = base_path / "gateway"
    for py_file in gateway_path.rglob("*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                forbidden = ("request", "response")
                if any(node.module.startswith(f) for f in forbidden):
                    msg = (
                        f"Illegal import in {py_file}: from {node.module} import ... "
                        "(gateway layer should not depend on request/response)",
                    )
                    raise AssertionError(msg)
