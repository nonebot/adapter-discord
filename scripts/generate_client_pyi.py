#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "loguru>=0.7.3",
#     "rich>=14.3.3",
#     "richuru>=0.1.1",
# ]
# ///
"""Generate client.pyi from HandleMixin methods in handle.py.

This script extracts method signatures from HandleMixin and generates
the ApiClient stub file for type checking.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import re

from loguru import logger
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.theme import Theme
from richuru import install

LINE_LENGTH = 88
HASH_HEADER_PREFIX = "# Source SHA256: "
SCRIPT_HASH_HEADER_PREFIX = "# Script SHA256: "

CONSOLE = Console(
    stderr=True,
    theme=Theme(
        {
            "logging.level.success": "green",
            "logging.level.trace": "bright_black",
        }
    ),
)


@dataclass(frozen=True, slots=True)
class MethodSignature:
    public_name: str
    params: list[str]
    returns: str | None
    docstring: str | None
    has_kwonly: bool
    is_overload: bool


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

    annotated_pattern = r"Annotated\[(.+)\]"
    annotated_match = re.match(annotated_pattern, annotation.strip())
    if annotated_match:
        inner = annotated_match.group(1)
        parts = _split_union_args(inner)
        if parts:
            return _format_annotation(parts[0])

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
    default_value: str | None,
) -> str:
    ann = _format_annotation(annotation)
    ann_str = f": {ann}" if ann else ""
    if has_default:
        normalized_default = "..."
        if default_value is not None:
            candidate = " ".join(default_value.split())
            if _is_simple_stub_default(candidate):
                normalized_default = candidate
        default_str = f" = {normalized_default}"
    else:
        default_str = ""
    return f"{name}{ann_str}{default_str}"


def _is_simple_stub_default(default_expr: str) -> bool:
    try:
        node = ast.parse(default_expr, mode="eval").body
    except SyntaxError:
        return False

    if isinstance(node, ast.Constant):
        return node.value is None or isinstance(
            node.value, bool | int | float | str | bytes
        )

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return isinstance(node.operand, ast.Constant) and isinstance(
            node.operand.value, int | float
        )

    return False


def _extract_method_signature(
    source: str, method: ast.AsyncFunctionDef
) -> MethodSignature:
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
        default_node = defaults[idx - default_start] if has_default else None
        default_value = _get_source_segment(source, default_node)
        params.append(
            _format_param(
                arg.arg,
                ann,
                has_default=has_default,
                default_value=default_value,
            )
        )

    for arg, default in zip(args.kwonlyargs, args.kw_defaults, strict=False):
        ann = _get_source_segment(source, arg.annotation)
        has_default = default is not None
        default_value = _get_source_segment(source, default)
        params.append(
            _format_param(
                arg.arg,
                ann,
                has_default=has_default,
                default_value=default_value,
            )
        )

    if args.kwarg is not None:
        ann = _get_source_segment(source, args.kwarg.annotation)
        if ann:
            params.append(f"**{args.kwarg.arg}: {_format_annotation(ann)}")
        else:
            params.append(f"**{args.kwarg.arg}")

    returns = _get_source_segment(source, method.returns)

    is_overload = any(
        (isinstance(decorator, ast.Name) and decorator.id == "overload")
        or (isinstance(decorator, ast.Attribute) and decorator.attr == "overload")
        for decorator in method.decorator_list
    )
    return MethodSignature(
        public_name=public_name,
        params=params,
        returns=returns,
        docstring=docstring,
        has_kwonly=has_kwonly,
        is_overload=is_overload,
    )


def _collect_available_imports(source: str) -> dict[str, str]:
    """Collect all importable names from model/types modules."""
    mod = ast.parse(source)
    available: dict[str, str] = {}

    for node in mod.body:
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            is_model = (
                module in ("model", "models", ".model", ".models")
                or module.endswith((".model", ".models"))
                or module.startswith(("model.", "models."))
                or ".model." in module
                or ".models." in module
            )
            is_types = module in ("types", ".types") or module.endswith(".types")
            if is_model or is_types:
                category = "model" if is_model else "types"
                for alias in node.names:
                    available[alias.name] = category

    return available


def _collect_local_aliases(source: str) -> dict[str, str]:
    mod = ast.parse(source)
    aliases: dict[str, str] = {}
    for node in mod.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        value = _get_source_segment(source, node.value)
        if value is None:
            continue
        normalized = _format_annotation(value)
        normalized = re.sub(r",\s*\]", "]", normalized)
        aliases[target.id] = normalized
    return aliases


def _extract_used_types(
    signatures: list[MethodSignature],
) -> set[str]:
    """Extract type names actually used in method signatures."""
    used: set[str] = set()
    type_pattern = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\b")

    for signature in signatures:
        for param in signature.params:
            used.update(type_pattern.findall(param))
        if signature.returns:
            used.update(type_pattern.findall(signature.returns))

    return used


def _find_handle_mixin(mod: ast.Module) -> ast.ClassDef:
    for node in mod.body:
        if isinstance(node, ast.ClassDef) and node.name == "HandleMixin":
            return node
    msg = "HandleMixin class not found in handle.py"
    raise RuntimeError(msg)


def _collect_method_signatures(
    source: str, mixin_class: ast.ClassDef
) -> list[MethodSignature]:
    async_methods = [
        node
        for node in mixin_class.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name.startswith("_api_")
    ]
    logger.debug(
        "Preparing to collect method signatures",
        alt=f"Found {len(async_methods)} _api_ methods in HandleMixin",
    )

    signatures: list[MethodSignature] = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=None),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        console=CONSOLE,
        transient=True,
    ) as progress:
        task_id = progress.add_task(
            "Collecting method signatures", total=len(async_methods)
        )
        for method in async_methods:
            signature = _extract_method_signature(source, method)
            signatures.append(signature)
            logger.debug(
                "Collected signature name={name} overload={overload}",
                name=signature.public_name,
                overload=signature.is_overload,
                alt=f"Collected {signature.public_name} (overload={signature.is_overload})",
            )
            progress.advance(task_id)

    return signatures


def _collect_actual_imports(
    source: str,
    methods: list[MethodSignature],
) -> tuple[dict[str, str], dict[str, str]]:
    available_imports = _collect_available_imports(source)
    local_aliases = _collect_local_aliases(source)
    used_types = _extract_used_types(methods)
    imports = {
        name: cat for name, cat in available_imports.items() if name in used_types
    }
    aliases = {
        name: value for name, value in local_aliases.items() if name in used_types
    }
    return imports, aliases


def _annotation_texts(
    methods: list[MethodSignature],
) -> list[str]:
    texts: list[str] = []
    for signature in methods:
        texts.extend(signature.params)
        if signature.returns:
            texts.append(signature.returns)
    return texts


def _append_import_block(lines: list[str], module: str, imports: list[str]) -> None:
    if not imports:
        return
    lines.append(f"from .{module} import (")
    lines.extend(f"    {imp}," for imp in imports)
    lines.append(")")


def _import_sort_key(name: str) -> tuple[int, str]:
    return (0 if name.isupper() else 1, name)


def _build_import_lines(  # noqa: C901
    methods: list[MethodSignature],
    actual_imports: dict[str, str],
    local_aliases: dict[str, str],
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
    need_overload = any(method.is_overload for method in methods)

    typing_imports: list[str] = []
    if need_any:
        typing_imports.append("Any")
    if need_literal:
        typing_imports.append("Literal")
    if need_overload:
        typing_imports.append("overload")
    if local_aliases:
        typing_imports.append("TypeAlias")
    typing_imports = sorted(set(typing_imports))

    if need_datetime:
        lines.append("from datetime import datetime")
    if typing_imports:
        lines.append(f"from typing import {', '.join(typing_imports)}")
    if need_datetime or typing_imports:
        lines.append("")

    _append_import_block(lines, "models", model_imports)
    _append_import_block(lines, "types", type_imports)

    if model_imports or type_imports:
        lines.append("")

    for name, value in sorted(local_aliases.items()):
        lines.append(f"{name}: TypeAlias = {value}")
    if local_aliases:
        lines.append("")

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
    annotation = rest
    default = ""
    if " = " in rest:
        annotation, default_value = rest.rsplit(" = ", 1)
        default = f" = {default_value}"

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
    methods: list[MethodSignature],
) -> list[str]:
    lines = ["class ApiClient:"]
    index = 0
    while index < len(methods):
        public_name = methods[index].public_name
        grouped: list[MethodSignature] = []
        while index < len(methods) and methods[index].public_name == public_name:
            grouped.append(methods[index])
            index += 1

        overloads = [sig for sig in grouped if sig.is_overload]
        implementations = [sig for sig in grouped if not sig.is_overload]

        if overloads:
            for signature in overloads:
                lines.append("    @overload")
                lines.extend(
                    _build_method_stub(
                        public_name,
                        signature.params,
                        signature.returns,
                        None,
                        has_kwonly=signature.has_kwonly,
                    )
                )
            continue

        if implementations:
            signature = implementations[0]
            lines.extend(
                _build_method_stub(
                    public_name,
                    signature.params,
                    signature.returns,
                    signature.docstring,
                    has_kwonly=signature.has_kwonly,
                )
            )
    return lines


def _calc_file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _extract_recorded_hashes(client_path: Path) -> tuple[str | None, str | None]:
    if not client_path.exists():
        return None, None

    source_hash: str | None = None
    script_hash: str | None = None

    for line in client_path.read_text("utf-8").splitlines()[:20]:
        if line.startswith(HASH_HEADER_PREFIX):
            source_hash = line[len(HASH_HEADER_PREFIX) :].strip()
        if line.startswith(SCRIPT_HASH_HEADER_PREFIX):
            script_hash = line[len(SCRIPT_HASH_HEADER_PREFIX) :].strip()

    return source_hash, script_hash


def _build_generated_header(
    *,
    root: Path,
    handle_path: Path,
    source_hash: str,
    script_hash: str,
    generated_at: str,
) -> list[str]:
    relative_source = handle_path.relative_to(root).as_posix()
    return [
        "# This file is auto-generated by scripts/generate_client_pyi.py.",
        "# Do not edit this file directly.",
        f"# Generated at: {generated_at}",
        f"# Source file: {relative_source}",
        f"{HASH_HEADER_PREFIX}{source_hash}",
        f"{SCRIPT_HASH_HEADER_PREFIX}{script_hash}",
        "",
    ]


def _generate_stub(
    root: Path,
    handle_path: Path,
    *,
    source_hash: str,
    script_hash: str,
    generated_at: str,
) -> str:
    source = handle_path.read_text("utf-8")
    mod = ast.parse(source)
    mixin_class = _find_handle_mixin(mod)
    methods = _collect_method_signatures(source, mixin_class)
    overload_count = sum(1 for method in methods if method.is_overload)
    signature_summary = Table(title="Method Signatures", show_header=True)
    signature_summary.add_column("Metric", style="cyan")
    signature_summary.add_column("Value", style="green")
    signature_summary.add_row("Total", str(len(methods)))
    signature_summary.add_row("Overloads", str(overload_count))
    logger.debug(
        "Collected method signatures",
        rich=signature_summary,
        alt=f"Method signatures: total={len(methods)}, overloads={overload_count}",
    )
    actual_imports, local_aliases = _collect_actual_imports(source, methods)

    lines = _build_generated_header(
        root=root,
        handle_path=handle_path,
        source_hash=source_hash,
        script_hash=script_hash,
        generated_at=generated_at,
    )
    lines.extend(_build_import_lines(methods, actual_imports, local_aliases))
    lines.extend(_build_class_lines(methods))
    return "\n".join(lines)


def main() -> None:
    install(rich_console=CONSOLE, level="DEBUG")
    root = Path(__file__).resolve().parents[1]
    handle_path = root / "nonebot/adapters/discord/api/handle.py"
    client_path = root / "nonebot/adapters/discord/api/client.pyi"
    script_path = Path(__file__).resolve()

    source_hash = _calc_file_sha256(handle_path)
    script_hash = _calc_file_sha256(script_path)
    previous_source_hash, previous_script_hash = _extract_recorded_hashes(client_path)

    hash_table = Table(title="client.pyi generation hashes", show_header=True)
    hash_table.add_column("Type", style="cyan")
    hash_table.add_column("Current", style="green")
    hash_table.add_column("Previous", style="magenta")
    hash_table.add_row("Source", source_hash, str(previous_source_hash))
    hash_table.add_row("Script", script_hash, str(previous_script_hash))
    logger.info(
        "Checking client.pyi generation hashes",
        rich=hash_table,
        alt=(
            "Checking client.pyi generation "
            f"source={source_hash} script={script_hash} "
            f"prev_source={previous_source_hash} prev_script={previous_script_hash}"
        ),
    )

    if previous_source_hash == source_hash and previous_script_hash == script_hash:
        logger.success("Skip generation because hashes are unchanged")
        return

    generated_at = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    stub_content = _generate_stub(
        root,
        handle_path,
        source_hash=source_hash,
        script_hash=script_hash,
        generated_at=generated_at,
    )
    client_path.write_text(stub_content, "utf-8")
    logger.success("Generated client.pyi")


if __name__ == "__main__":
    main()
