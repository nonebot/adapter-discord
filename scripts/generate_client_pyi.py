#!/usr/bin/env python3
"""Generate client.pyi from HandleMixin methods in handle.py.

This script extracts method signatures from HandleMixin and generates
the ApiClient stub file for type checking.
"""

from __future__ import annotations

import ast
from pathlib import Path
import re

LINE_LENGTH = 88


def _get_source_segment(source: str, node: ast.AST | None) -> str | None:
    if node is None:
        return None
    return ast.get_source_segment(source, node)


def _extract_docstring(node: ast.AsyncFunctionDef) -> str | None:
    if (
        node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
        and isinstance(node.body[0].value.value, str)
    ):
        return node.body[0].value.value
    return None


def _strip_leading_underscore(name: str) -> str:
    if name.startswith("_api_"):
        return name[5:]
    if name.startswith("_") and not name.startswith("__"):
        return name[1:]
    return name


def _format_annotation(annotation: str | None) -> str:
    if annotation is None:
        return ""

    annotation = " ".join(annotation.split())
    annotation = re.sub(r"\[\s+", "[", annotation)
    annotation = re.sub(r"\s+\]", "]", annotation)
    annotation = re.sub(r"\(\s+", "(", annotation)
    annotation = re.sub(r"\s+\)", ")", annotation)
    annotation = re.sub(r"\s+,", ",", annotation)
    annotation = re.sub(r",\s*", ", ", annotation)

    stripped = annotation.strip()
    if (
        stripped.startswith('"')
        and stripped.endswith('"')
        and '"' not in stripped[1:-1]
    ):
        annotation = stripped[1:-1]

    optional_pattern = r"Optional\[(.+)\]"
    match = re.match(optional_pattern, annotation.strip())
    if match:
        inner = match.group(1)
        inner_formatted = _format_annotation(inner)
        return f"{inner_formatted} | None"

    union_pattern = r"Union\[(.+)\]"
    union_match = re.match(union_pattern, annotation.strip())
    if union_match:
        inner = union_match.group(1)
        parts = _split_union_args(inner)
        formatted_parts = [_format_annotation(p) for p in parts]
        return " | ".join(formatted_parts)

    return annotation


def _split_union_args(inner: str) -> list[str]:
    """Split Union arguments by comma, respecting bracket nesting."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in inner:
        if char in "([{":
            depth += 1
            current.append(char)
        elif char in ")]}":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        parts.append("".join(current).strip())
    return parts


def _format_param(
    name: str,
    annotation: str | None,
    *,
    has_default: bool,
) -> str:
    ann = _format_annotation(annotation)
    ann_str = f": {ann}" if ann else ""
    default_str = " = ..." if has_default else ""
    return f"{name}{ann_str}{default_str}"


def _extract_method_signature(
    source: str, method: ast.AsyncFunctionDef
) -> tuple[str, list[str], str | None, str | None, bool]:
    public_name = _strip_leading_underscore(method.name)
    docstring = _extract_docstring(method)

    args = method.args
    params: list[str] = []
    has_kwonly = bool(args.kwonlyargs)

    regular = args.args
    defaults = list(args.defaults)
    default_start = len(regular) - len(defaults)

    for idx, arg in enumerate(regular):
        if arg.arg in ("self", "bot"):
            continue
        ann = _get_source_segment(source, arg.annotation)
        has_default = idx >= default_start
        params.append(_format_param(arg.arg, ann, has_default=has_default))

    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        ann = _get_source_segment(source, arg.annotation)
        has_default = default is not None
        params.append(_format_param(arg.arg, ann, has_default=has_default))

    if args.kwarg is not None:
        ann = _get_source_segment(source, args.kwarg.annotation)
        if ann:
            params.append(f"**{args.kwarg.arg}: {_format_annotation(ann)}")
        else:
            params.append(f"**{args.kwarg.arg}")

    returns = _get_source_segment(source, method.returns)

    return public_name, params, returns, docstring, has_kwonly


def _collect_available_imports(source: str) -> dict[str, str]:
    """Collect all importable names from model/types modules."""
    mod = ast.parse(source)
    available: dict[str, str] = {}

    for node in mod.body:
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            is_model = module in ("model", ".model") or module.endswith(".model")
            is_types = module in ("types", ".types") or module.endswith(".types")
            if is_model or is_types:
                category = "model" if is_model else "types"
                for alias in node.names:
                    available[alias.name] = category

    return available


def _extract_used_types(
    signatures: list[tuple[str, list[str], str | None, str | None, bool]],
) -> set[str]:
    """Extract type names actually used in method signatures."""
    used: set[str] = set()
    type_pattern = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\b")

    for _, params, returns, _, _ in signatures:
        for param in params:
            used.update(type_pattern.findall(param))
        if returns:
            used.update(type_pattern.findall(returns))

    return used


def _find_handle_mixin(mod: ast.Module) -> ast.ClassDef:
    for node in mod.body:
        if isinstance(node, ast.ClassDef) and node.name == "HandleMixin":
            return node
    msg = "HandleMixin class not found in handle.py"
    raise RuntimeError(msg)


def _collect_method_signatures(
    source: str, mixin_class: ast.ClassDef
) -> list[tuple[str, list[str], str | None, str | None, bool]]:
    return [
        _extract_method_signature(source, node)
        for node in mixin_class.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name.startswith("_api_")
    ]


def _collect_actual_imports(
    source: str,
    methods: list[tuple[str, list[str], str | None, str | None, bool]],
) -> dict[str, str]:
    available_imports = _collect_available_imports(source)
    used_types = _extract_used_types(methods)
    return {name: cat for name, cat in available_imports.items() if name in used_types}


def _annotation_texts(
    methods: list[tuple[str, list[str], str | None, str | None, bool]],
) -> list[str]:
    texts: list[str] = []
    for _, params, returns, _, _ in methods:
        texts.extend(params)
        if returns:
            texts.append(returns)
    return texts


def _append_import_block(lines: list[str], module: str, imports: list[str]) -> None:
    if not imports:
        return
    lines.append(f"from .{module} import (")
    lines.extend(f"    {imp}," for imp in imports)
    lines.append(")")


def _import_sort_key(name: str) -> tuple[int, str]:
    return (0 if name.isupper() else 1, name)


def _build_import_lines(
    methods: list[tuple[str, list[str], str | None, str | None, bool]],
    actual_imports: dict[str, str],
) -> list[str]:
    lines: list[str] = []
    model_imports = sorted(
        (name for name, cat in actual_imports.items() if cat == "model"),
        key=_import_sort_key,
    )
    type_imports = sorted(
        (name for name, cat in actual_imports.items() if cat == "types"),
        key=_import_sort_key,
    )

    texts = _annotation_texts(methods)
    need_datetime = any("datetime" in text for text in texts)
    need_literal = any("Literal" in text for text in texts)
    need_any = any(re.search(r"\bAny\b", text) for text in texts)

    typing_imports: list[str] = []
    if need_any:
        typing_imports.append("Any")
    if need_literal:
        typing_imports.append("Literal")

    if need_datetime:
        lines.append("from datetime import datetime")
    if typing_imports:
        lines.append(f"from typing import {', '.join(typing_imports)}")
    if need_datetime or typing_imports:
        lines.append("")

    _append_import_block(lines, "model", model_imports)
    _append_import_block(lines, "types", type_imports)
    lines.append("")
    return lines


def _render_docstring(docstring: str) -> list[str]:
    doc_lines = [line.strip() for line in docstring.strip().split("\n")]
    if len(doc_lines) == 1:
        return [f'        """{doc_lines[0]}"""']

    rendered = [f'        """{doc_lines[0]}']
    rendered.extend(f"        {line}" if line else "" for line in doc_lines[1:])
    rendered.append('        """')
    return rendered


def _build_method_stub(
    public_name: str,
    params: list[str],
    returns: str | None,
    docstring: str | None,
    *,
    has_kwonly: bool,
) -> list[str]:
    lines = [f"    async def {public_name}(", "        self,"]

    if has_kwonly:
        lines.append("        *,")
    for param in params:
        lines.extend(_render_param_lines(param))

    ret_ann = _format_annotation(returns) if returns else "None"
    lines.append(f"    ) -> {ret_ann}:")
    if docstring:
        lines.extend(_render_docstring(docstring))
    else:
        lines.append("        ...")
    lines.append("")
    return lines


def _render_param_lines(param: str) -> list[str]:
    single_line = f"        {param},"
    if len(single_line) <= LINE_LENGTH or ": " not in param:
        return [single_line]

    name, rest = param.split(": ", 1)
    has_default = rest.endswith(" = ...")
    annotation = rest[:-6] if has_default else rest
    default = " = ..." if has_default else ""

    if " | " in annotation:
        left, right = annotation.rsplit(" | ", 1)
        return [
            f"        {name}: {left}",
            f"        | {right}{default},",
        ]

    if "[" in annotation and "]" in annotation:
        base, inner = annotation.split("[", 1)
        inner_content = inner.rsplit("]", 1)[0]
        return [
            f"        {name}: {base}[",
            f"            {inner_content}",
            f"        ]{default},",
        ]

    return [single_line]


def _build_class_lines(
    methods: list[tuple[str, list[str], str | None, str | None, bool]],
) -> list[str]:
    lines = ["class ApiClient:"]
    for public_name, params, returns, docstring, has_kwonly in methods:
        lines.extend(
            _build_method_stub(
                public_name,
                params,
                returns,
                docstring,
                has_kwonly=has_kwonly,
            )
        )
    return lines


def _generate_stub(handle_path: Path) -> str:
    source = handle_path.read_text("utf-8")
    mod = ast.parse(source)
    mixin_class = _find_handle_mixin(mod)
    methods = _collect_method_signatures(source, mixin_class)
    actual_imports = _collect_actual_imports(source, methods)

    lines = _build_import_lines(methods, actual_imports)
    lines.extend(_build_class_lines(methods))
    return "\n".join(lines)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    handle_path = root / "nonebot/adapters/discord/api/handle.py"
    client_path = root / "nonebot/adapters/discord/api/client.pyi"

    stub_content = _generate_stub(handle_path)
    client_path.write_text(stub_content, "utf-8")


if __name__ == "__main__":
    main()
