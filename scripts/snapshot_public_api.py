#!/usr/bin/env python3
"""Snapshot the public 1.x interface without importing the adapter."""

import argparse
import ast
import json
from pathlib import Path
from typing_extensions import TypedDict

EXPECTED_COUNTS = {
    "top_level_exports": 133,
    "api_exports": 373,
    "model_exports": 292,
    "api_client_async_methods": 230,
}


class _ApiClientSnapshot(TypedDict):
    async_method_count: int
    methods: list[dict[str, object]]


class PublicApiSnapshot(TypedDict):
    top_level_exports: list[str]
    api_exports: list[str]
    model_exports: list[str]
    api_client: _ApiClientSnapshot
    message: dict[str, dict[str, object]]
    application_command_matcher: dict[str, dict[str, object]]
    counts: dict[str, int]


def _source_segment(source: str, node: ast.AST | None) -> str | None:
    if node is None:
        return None
    return ast.get_source_segment(source, node)


def _read_module(path: Path) -> tuple[str, ast.Module]:
    source = path.read_text("utf-8")
    return source, ast.parse(source, filename=str(path))


def _literal_value(module: ast.Module, value: ast.expr) -> object:
    """Evaluate literals and a simple list/tuple copy without importing a module."""

    if (
        isinstance(value, ast.Call)
        and isinstance(value.func, ast.Name)
        and value.func.id in {"list", "tuple"}
        and len(value.args) == 1
        and isinstance(value.args[0], ast.Name)
    ):
        source_name = value.args[0].id
        for node in module.body:
            if (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == source_name
            ):
                source = _literal_value(module, node.value)
                if not isinstance(source, (list, tuple)):
                    message = f"literal source {source_name!r} must be a list or tuple"
                    raise TypeError(message)
                return list(source) if value.func.id == "list" else tuple(source)
        message = f"literal source {source_name!r} was not found"
        raise ValueError(message)
    return ast.literal_eval(value)


def _ordered_all(module: ast.Module, path: Path) -> list[str]:
    for node in module.body:
        target: ast.expr | None = None
        value: ast.expr | None = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            value = node.value
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            value = node.value
        if not isinstance(target, ast.Name) or target.id != "__all__" or value is None:
            continue
        exports = _literal_value(module, value)
        if not isinstance(exports, list) or not all(
            isinstance(name, str) for name in exports
        ):
            message = f"{path}: __all__ must be a list of strings"
            raise ValueError(message)
        return exports
    message = f"{path}: __all__ was not found"
    raise ValueError(message)


def _find_class(module: ast.Module, name: str, path: Path) -> ast.ClassDef:
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    message = f"{path}: class {name} was not found"
    raise ValueError(message)


def _find_function(
    nodes: list[ast.stmt], name: str
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in nodes:
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == name
        ):
            return node
    return None


def _parameter_contract(
    source: str, function: ast.FunctionDef | ast.AsyncFunctionDef
) -> list[dict[str, str | None]]:
    args = function.args
    parameters: list[dict[str, str | None]] = []
    positional = [*args.posonlyargs, *args.args]
    defaults_start = len(positional) - len(args.defaults)

    for index, arg in enumerate(positional):
        default = (
            _source_segment(source, args.defaults[index - defaults_start])
            if index >= defaults_start
            else None
        )
        parameters.append(
            {
                "name": arg.arg,
                "kind": "positional_only"
                if index < len(args.posonlyargs)
                else "positional_or_keyword",
                "annotation": _source_segment(source, arg.annotation),
                "default": default,
            }
        )

    if args.vararg is not None:
        parameters.append(
            {
                "name": args.vararg.arg,
                "kind": "var_positional",
                "annotation": _source_segment(source, args.vararg.annotation),
                "default": None,
            }
        )

    for arg, default_node in zip(args.kwonlyargs, args.kw_defaults, strict=True):
        parameters.append(
            {
                "name": arg.arg,
                "kind": "keyword_only",
                "annotation": _source_segment(source, arg.annotation),
                "default": _source_segment(source, default_node),
            }
        )

    if args.kwarg is not None:
        parameters.append(
            {
                "name": args.kwarg.arg,
                "kind": "var_keyword",
                "annotation": _source_segment(source, args.kwarg.annotation),
                "default": None,
            }
        )
    return parameters


def _is_overload(function: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(
        (isinstance(decorator, ast.Name) and decorator.id == "overload")
        or (isinstance(decorator, ast.Attribute) and decorator.attr == "overload")
        for decorator in function.decorator_list
    )


def _function_contract(
    source: str, function: ast.FunctionDef | ast.AsyncFunctionDef
) -> dict[str, object]:
    return {
        "exists": True,
        "is_async": isinstance(function, ast.AsyncFunctionDef),
        "parameters": _parameter_contract(source, function),
        "return_annotation": _source_segment(source, function.returns),
    }


def _api_client_contract(
    source: str, module: ast.Module, path: Path
) -> _ApiClientSnapshot:
    client = _find_class(module, "ApiClient", path)
    methods: list[dict[str, object]] = []
    for node in client.body:
        if not isinstance(node, ast.AsyncFunctionDef) or node.name.startswith("_"):
            continue
        method = _function_contract(source, node)
        method["name"] = node.name
        method["overload"] = _is_overload(node)
        methods.append(method)
    return {"async_method_count": len(methods), "methods": methods}


def _named_function_contracts(
    source: str,
    nodes: list[ast.stmt],
    names: list[str],
) -> dict[str, dict[str, object]]:
    contracts: dict[str, dict[str, object]] = {}
    for name in names:
        function = _find_function(nodes, name)
        contracts[name] = (
            _function_contract(source, function)
            if function is not None
            else {"exists": False}
        )
    return contracts


def build_snapshot(root: Path) -> PublicApiSnapshot:
    package = root / "nonebot/adapters/discord"
    top_source, top_module = _read_module(package / "__init__.py")
    del top_source
    api_source, api_module = _read_module(package / "api/__init__.py")
    del api_source
    model_source, model_module = _read_module(package / "api/model.py")
    del model_source
    client_source, client_module = _read_module(package / "api/client.pyi")
    message_source, message_module = _read_module(package / "message.py")
    matcher_source, matcher_module = _read_module(package / "commands/matcher.py")
    matcher = _find_class(
        matcher_module,
        "ApplicationCommandMatcher",
        package / "commands/matcher.py",
    )

    top_level_exports = _ordered_all(top_module, package / "__init__.py")
    api_exports = _ordered_all(api_module, package / "api/__init__.py")
    model_exports = _ordered_all(model_module, package / "api/model.py")
    api_client = _api_client_contract(
        client_source, client_module, package / "api/client.pyi"
    )

    snapshot: PublicApiSnapshot = {
        "top_level_exports": top_level_exports,
        "api_exports": api_exports,
        "model_exports": model_exports,
        "api_client": api_client,
        "message": _named_function_contracts(
            message_source,
            message_module.body,
            ["parse_message"],
        ),
        "application_command_matcher": _named_function_contracts(
            matcher_source,
            matcher.body,
            [
                "send_deferred_response",
                "send_response",
                "send_followup_msg",
                "get_response",
                "edit_response",
                "delete_response",
                "get_followup_msg",
                "edit_followup_msg",
                "delete_followup_msg",
            ],
        ),
        "counts": {
            "top_level_exports": len(top_level_exports),
            "api_exports": len(api_exports),
            "model_exports": len(model_exports),
            "api_client_async_methods": api_client["async_method_count"],
        },
    }
    return snapshot


def _validate_counts(snapshot: PublicApiSnapshot) -> None:
    actual_counts = {
        "top_level_exports": len(snapshot["top_level_exports"]),
        "api_exports": len(snapshot["api_exports"]),
        "model_exports": len(snapshot["model_exports"]),
        "api_client_async_methods": snapshot["api_client"]["async_method_count"],
    }
    if actual_counts != EXPECTED_COUNTS:
        message = (
            "public API baseline counts changed: "
            f"expected {EXPECTED_COUNTS}, got {actual_counts}"
        )
        raise SystemExit(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="JSON fixture path (defaults to tests/fixtures/public_api.json)",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output or root / "tests/fixtures/public_api.json"
    snapshot = build_snapshot(root)
    _validate_counts(snapshot)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        "utf-8",
    )


if __name__ == "__main__":
    main()
