#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Render the public ApiClient stub from the endpoint ownership manifest."""

import argparse
import ast
import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys

LINE_LENGTH = 88
ENDPOINT_GROUP_ENTRY_LENGTH = 2
CONCRETE_ENDPOINT_COUNT = 223
HASH_HEADER_PREFIX = "# Source SHA256: "


PUBLIC_METHOD_ORDER: tuple[str, ...] = (
    "get_global_application_commands",
    "create_global_application_command",
    "get_global_application_command",
    "edit_global_application_command",
    "delete_global_application_command",
    "bulk_overwrite_global_application_commands",
    "get_guild_application_commands",
    "create_guild_application_command",
    "get_guild_application_command",
    "edit_guild_application_command",
    "delete_guild_application_command",
    "bulk_overwrite_guild_application_commands",
    "get_guild_application_command_permissions",
    "get_application_command_permissions",
    "edit_application_command_permissions",
    "create_interaction_response",
    "get_origin_interaction_response",
    "edit_origin_interaction_response",
    "delete_origin_interaction_response",
    "create_followup_message",
    "get_followup_message",
    "edit_followup_message",
    "delete_followup_message",
    "get_current_application",
    "edit_current_application",
    "get_application_activity_instance",
    "get_application_role_connection_metadata_records",
    "update_application_role_connection_metadata_records",
    "get_guild_audit_log",
    "list_auto_moderation_rules_for_guild",
    "get_auto_moderation_rule",
    "create_auto_moderation_rule",
    "modify_auto_moderation_rule",
    "delete_auto_moderation_rule",
    "get_channel",
    "modify_DM",
    "modify_channel",
    "modify_thread",
    "delete_channel",
    "get_channel_messages",
    "get_channel_message",
    "create_message",
    "crosspost_message",
    "create_reaction",
    "delete_own_reaction",
    "delete_user_reaction",
    "get_reactions",
    "delete_all_reactions",
    "delete_all_reactions_for_emoji",
    "edit_message",
    "delete_message",
    "bulk_delete_message",
    "edit_channel_permissions",
    "get_channel_invites",
    "create_channel_invite",
    "delete_channel_permission",
    "follow_announcement_channel",
    "trigger_typing_indicator",
    "get_pinned_messages",
    "pin_message",
    "unpin_message",
    "group_DM_add_recipient",
    "group_DM_remove_recipient",
    "start_thread_from_message",
    "start_thread_without_message",
    "start_thread_in_forum_channel",
    "join_thread",
    "add_thread_member",
    "leave_thread",
    "remove_thread_member",
    "get_thread_member",
    "list_thread_members",
    "list_public_archived_threads",
    "list_private_archived_threads",
    "list_joined_private_archived_threads",
    "list_guild_emojis",
    "get_guild_emoji",
    "create_guild_emoji",
    "modify_guild_emoji",
    "delete_guild_emoji",
    "list_application_emojis",
    "get_application_emoji",
    "create_application_emoji",
    "modify_application_emoji",
    "delete_application_emoji",
    "send_soundboard_sound",
    "list_default_soundboard_sounds",
    "list_guild_soundboard_sounds",
    "get_guild_soundboard_sound",
    "create_guild_soundboard_sound",
    "modify_guild_soundboard_sound",
    "delete_guild_soundboard_sound",
    "create_lobby",
    "get_lobby",
    "modify_lobby",
    "delete_lobby",
    "add_lobby_member",
    "remove_lobby_member",
    "leave_lobby",
    "link_channel_to_lobby",
    "list_entitlements",
    "get_entitlement",
    "consume_an_entitlement",
    "create_test_entitlement",
    "delete_test_entitlement",
    "create_guild",
    "get_guild",
    "get_guild_role_member_counts",
    "get_guild_preview",
    "modify_guild",
    "modify_guild_incident_actions",
    "delete_guild",
    "get_guild_channels",
    "create_guild_channel",
    "modify_guild_channel_positions",
    "list_active_guild_threads",
    "get_guild_member",
    "list_guild_members",
    "search_guild_members",
    "add_guild_member",
    "modify_guild_member",
    "modify_current_member",
    "modify_current_user_nick",
    "add_guild_member_role",
    "remove_guild_member_role",
    "remove_guild_member",
    "get_guild_bans",
    "get_guild_ban",
    "create_guild_ban",
    "remove_guild_ban",
    "bulk_guild_ban",
    "get_guild_roles",
    "get_guild_role",
    "create_guild_role",
    "modify_guild_role_positions",
    "modify_guild_role",
    "modify_guild_MFA_level",
    "delete_guild_role",
    "get_guild_prune_count",
    "begin_guild_prune",
    "get_guild_voice_regions",
    "get_guild_invites",
    "get_guild_integrations",
    "delete_guild_integration",
    "get_guild_widget_settings",
    "modify_guild_widget",
    "get_guild_widget",
    "get_guild_vanity_url",
    "get_guild_widget_image",
    "get_guild_welcome_screen",
    "modify_guild_welcome_screen",
    "get_guild_onboarding",
    "modify_guild_onboarding",
    "list_voice_regions",
    "get_current_user_voice_state",
    "get_user_voice_state",
    "modify_current_user_voice_state",
    "modify_user_voice_state",
    "list_scheduled_events_for_guild",
    "create_guild_schedule_event",
    "get_guild_scheduled_event",
    "modify_guild_scheduled_event",
    "delete_guild_scheduled_event",
    "get_guild_scheduled_event_users",
    "get_guild_template",
    "create_guild_from_guild_template",
    "get_guild_templates",
    "create_guild_template",
    "sync_guild_template",
    "modify_guild_template",
    "delete_guild_template",
    "get_invite",
    "delete_invite",
    "get_invite_target_users",
    "update_invite_target_users",
    "get_invite_target_users_job_status",
    "get_answer_voters",
    "end_poll",
    "list_SKUs",
    "create_stage_instance",
    "get_stage_instance",
    "modify_stage_instance",
    "delete_stage_instance",
    "get_sticker",
    "list_nitro_sticker_packs",
    "get_sticker_packs",
    "list_guild_stickers",
    "get_guild_sticker",
    "create_guild_sticker",
    "modify_guild_sticker",
    "delete_guild_sticker",
    "list_SKU_subscriptions",
    "get_SKU_subscription",
    "get_current_user",
    "get_user",
    "modify_current_user",
    "get_current_user_guilds",
    "get_current_user_guild_member",
    "leave_guild",
    "create_DM",
    "create_group_DM",
    "get_user_connections",
    "get_user_application_role_connection",
    "update_user_application_role_connection",
    "create_webhook",
    "get_channel_webhooks",
    "get_guild_webhooks",
    "get_webhook",
    "get_webhook_with_token",
    "modify_webhook",
    "modify_webhook_with_token",
    "delete_webhook",
    "delete_webhook_with_token",
    "execute_webhook",
    "execute_slack_compatible_webhook",
    "execute_github_compatible_webhook",
    "get_webhook_message",
    "edit_webhook_message",
    "delete_webhook_message",
    "get_gateway",
    "get_gateway_bot",
    "get_current_bot_application_information",
    "get_current_authorization_information",
)


@dataclass(frozen=True, slots=True)
class MethodSignature:
    public_name: str
    params: list[str]
    returns: str | None
    docstring: str | None
    has_kwonly: bool
    is_overload: bool


@dataclass(frozen=True, slots=True)
class EndpointSource:
    module_name: str
    mixin_name: str
    path: Path
    source: str
    mixin: ast.ClassDef


def _get_source_segment(source: str, node: ast.AST | None) -> str | None:
    return ast.get_source_segment(source, node) if node is not None else None


def _strip_leading_underscore(name: str) -> str:
    return name.removeprefix("_api_")


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
    match = re.fullmatch(r"Annotated\[(.+)\]", annotation)
    if match:
        return _format_annotation(_split_union_args(match.group(1))[0])
    match = re.fullmatch(r"Optional\[(.+)\]", annotation)
    if match:
        return f"{_format_annotation(match.group(1))} | None"
    match = re.fullmatch(r"Union\[(.+)\]", annotation)
    if match:
        return " | ".join(
            _format_annotation(part) for part in _split_union_args(match.group(1))
        )
    return annotation


def _split_union_args(inner: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in inner:
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        if char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        parts.append("".join(current).strip())
    return parts


def _is_simple_stub_default(default_expr: str) -> bool:
    try:
        node = ast.parse(default_expr, mode="eval").body
    except SyntaxError:
        return False
    if isinstance(node, ast.Constant):
        return node.value is None or isinstance(
            node.value, bool | int | float | str | bytes
        )
    return (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and isinstance(node.operand, ast.Constant)
        and isinstance(node.operand.value, int | float)
    )


def _extract_docstring(node: ast.AsyncFunctionDef) -> str | None:
    if (
        node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
        and isinstance(node.body[0].value.value, str)
    ):
        return node.body[0].value.value
    return None


def _is_overload(node: ast.AsyncFunctionDef) -> bool:
    return any(
        (isinstance(decorator, ast.Name) and decorator.id == "overload")
        or (isinstance(decorator, ast.Attribute) and decorator.attr == "overload")
        for decorator in node.decorator_list
    )


def _format_param(
    name: str, annotation: str | None, *, has_default: bool, default_value: str | None
) -> str:
    annotation_text = _format_annotation(annotation)
    default_text = ""
    if has_default:
        candidate = " ".join(default_value.split()) if default_value else ""
        default_text = (
            f" = {candidate if _is_simple_stub_default(candidate) else '...'}"
        )
    return f"{name}{f': {annotation_text}' if annotation_text else ''}{default_text}"


def _extract_method_signature(
    source: str, method: ast.AsyncFunctionDef
) -> MethodSignature:
    args = method.args
    params: list[str] = []
    defaults = list(args.defaults)
    default_start = len(args.args) - len(defaults)
    for index, arg in enumerate(args.args):
        if arg.arg in {"self", "bot"}:
            continue
        default = defaults[index - default_start] if index >= default_start else None
        params.append(
            _format_param(
                arg.arg,
                _get_source_segment(source, arg.annotation),
                has_default=default is not None,
                default_value=_get_source_segment(source, default),
            )
        )
    for arg, default in zip(args.kwonlyargs, args.kw_defaults, strict=False):
        params.append(
            _format_param(
                arg.arg,
                _get_source_segment(source, arg.annotation),
                has_default=default is not None,
                default_value=_get_source_segment(source, default),
            )
        )
    if args.kwarg is not None:
        annotation = _format_annotation(
            _get_source_segment(source, args.kwarg.annotation)
        )
        params.append(f"**{args.kwarg.arg}{f': {annotation}' if annotation else ''}")
    return MethodSignature(
        public_name=_strip_leading_underscore(method.name),
        params=params,
        returns=_get_source_segment(source, method.returns),
        docstring=_extract_docstring(method),
        has_kwonly=bool(args.kwonlyargs),
        is_overload=_is_overload(method),
    )


def _literal_value(module: ast.Module, value: ast.expr) -> object:
    """Evaluate literals and simple list/tuple copies without importing source."""
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
                    msg = f"literal source {source_name!r} must be a list or tuple"
                    raise TypeError(msg)
                return list(source) if value.func.id == "list" else tuple(source)
        msg = f"literal source {source_name!r} assignment not found"
        raise RuntimeError(msg)
    return ast.literal_eval(value)


def _literal_assignment(module: ast.Module, name: str) -> object:
    for node in module.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        ):
            return _literal_value(module, node.value)
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == name
            and node.value is not None
        ):
            return _literal_value(module, node.value)
    msg = f"{name} assignment not found"
    raise RuntimeError(msg)


def _manifest_groups(manifest_path: Path) -> tuple[tuple[str, str], ...]:
    groups = _literal_assignment(
        ast.parse(manifest_path.read_text("utf-8")), "ENDPOINT_GROUPS"
    )
    if not isinstance(groups, tuple) or not all(
        isinstance(item, tuple)
        and len(item) == ENDPOINT_GROUP_ENTRY_LENGTH
        and all(isinstance(value, str) for value in item)
        for item in groups
    ):
        msg = "ENDPOINT_GROUPS must be a tuple of (module, mixin) strings"
        raise RuntimeError(msg)
    return groups


def _load_endpoint_sources(
    root: Path, groups: tuple[tuple[str, str], ...]
) -> list[EndpointSource]:
    endpoint_sources: list[EndpointSource] = []
    for module_name, mixin_name in groups:
        relative = Path(*module_name.split(".")).with_suffix(".py")
        path = root / relative
        if not path.exists():
            msg = f"manifest endpoint module is missing: {module_name}"
            raise RuntimeError(msg)
        source = path.read_text("utf-8")
        module = ast.parse(source)
        mixins = [
            node
            for node in module.body
            if isinstance(node, ast.ClassDef) and node.name == mixin_name
        ]
        if len(mixins) != 1:
            msg = f"manifest mixin is missing or duplicated: {module_name}.{mixin_name}"
            raise RuntimeError(msg)
        endpoint_sources.append(
            EndpointSource(module_name, mixin_name, path, source, mixins[0])
        )
    return endpoint_sources


def _validate_handle_assembly(
    handle_path: Path, groups: tuple[tuple[str, str], ...]
) -> None:
    module = ast.parse(handle_path.read_text("utf-8"))
    mixins = [
        node
        for node in module.body
        if isinstance(node, ast.ClassDef) and node.name == "HandleMixin"
    ]
    if len(mixins) != 1:
        msg = "HandleMixin class not found in api/handle.py"
        raise RuntimeError(msg)
    bases = [base.id for base in mixins[0].bases if isinstance(base, ast.Name)]
    expected = [mixin for _, mixin in groups]
    if bases != expected:
        msg = "HandleMixin bases must exactly match ENDPOINT_GROUPS"
        raise RuntimeError(msg)
    imports: dict[str, str] = {}
    for node in module.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                imports[alias.asname or alias.name] = node.module
    for module_name, mixin_name in groups:
        if imports.get(mixin_name) != module_name.removeprefix(
            "nonebot.adapters.discord."
        ):
            msg = f"HandleMixin import does not match manifest: {mixin_name}"
            raise RuntimeError(msg)


def _methods(endpoint_sources: Iterable[EndpointSource]) -> list[MethodSignature]:
    methods: list[MethodSignature] = []
    owners: dict[str, str] = {}
    implementations: set[str] = set()
    for endpoint in endpoint_sources:
        for node in endpoint.mixin.body:
            if not isinstance(node, ast.AsyncFunctionDef) or not node.name.startswith(
                "_api_"
            ):
                continue
            prior_owner = owners.setdefault(node.name, endpoint.module_name)
            if prior_owner != endpoint.module_name:
                msg = f"duplicate endpoint owner: {node.name}"
                raise RuntimeError(msg)
            if not _is_overload(node):
                if node.name in implementations:
                    msg = f"duplicate endpoint implementation: {node.name}"
                    raise RuntimeError(msg)
                implementations.add(node.name)
            methods.append(_extract_method_signature(endpoint.source, node))
    if len(implementations) != CONCRETE_ENDPOINT_COUNT:
        msg = (
            "expected "
            f"{CONCRETE_ENDPOINT_COUNT} concrete endpoints, found {len(implementations)}"
        )
        raise RuntimeError(msg)
    if {name[5:] for name in implementations} != set(PUBLIC_METHOD_ORDER):
        msg = "endpoint names do not match the stable public client order"
        raise RuntimeError(msg)
    order = {name: index for index, name in enumerate(PUBLIC_METHOD_ORDER)}
    methods.sort(key=lambda method: order[method.public_name])
    return methods


def _local_aliases(endpoint_sources: Iterable[EndpointSource]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for endpoint in endpoint_sources:
        module = ast.parse(endpoint.source)
        for node in module.body:
            if (
                not isinstance(node, ast.Assign)
                or len(node.targets) != 1
                or not isinstance(node.targets[0], ast.Name)
            ):
                continue
            value = _get_source_segment(endpoint.source, node.value)
            if value is None:
                continue
            name = node.targets[0].id
            if name == "__all__":
                continue
            if name in aliases:
                msg = f"duplicate local annotation alias: {name}"
                raise RuntimeError(msg)
            aliases[name] = _format_annotation(value)
    return aliases


def _public_exports(path: Path) -> set[str]:
    exports = _literal_assignment(ast.parse(path.read_text("utf-8")), "__all__")
    if not isinstance(exports, list) or not all(
        isinstance(name, str) for name in exports
    ):
        msg = f"invalid public __all__: {path}"
        raise RuntimeError(msg)
    return set(exports)


def _annotation_texts(
    methods: Iterable[MethodSignature], aliases: dict[str, str]
) -> list[str]:
    texts = [
        text for method in methods for text in (*method.params, method.returns) if text
    ]
    texts.extend(aliases.values())
    return texts


def _imports_for_annotations(
    root: Path, methods: list[MethodSignature], aliases: dict[str, str]
) -> tuple[list[str], list[str]]:
    types = _public_exports(root / "nonebot/adapters/discord/api/types.py")
    models = _public_exports(root / "nonebot/adapters/discord/api/model.py")
    models.update(
        _public_exports(root / "nonebot/adapters/discord/domains/models.py") - types
    )
    used: set[str] = set()
    texts = _annotation_texts(methods, aliases)
    for text in texts:
        if "domains." in text:
            msg = f"domain import leaked into generated annotation: {text}"
            raise RuntimeError(msg)
        used.update(re.findall(r"\b[A-Z][A-Za-z0-9_]*\b", text))
    local = set(aliases)
    ignored = {
        "Any",
        "Annotated",
        "False",
        "Literal",
        "None",
        "Optional",
        "True",
        "Union",
        "KEYWORD",
        "KEYWORD_PRESET",
        "MEMBER_PROFILE",
        "MENTION_SPAM",
        "SPAM",
        "TypeAlias",
    }
    unresolved = used - models - types - local - ignored
    if unresolved:
        msg = f"unresolved public annotation symbols: {', '.join(sorted(unresolved))}"
        raise RuntimeError(msg)
    overlap = models & types
    if overlap:
        msg = f"public facade exports overlap: {', '.join(sorted(overlap))}"
        raise RuntimeError(msg)
    return sorted(used & models, key=_import_sort_key), sorted(
        used & types, key=_import_sort_key
    )


def _import_sort_key(name: str) -> tuple[int, str]:
    return (0 if name.isupper() else 1, name)


def _append_import_block(lines: list[str], module: str, names: list[str]) -> None:
    if names:
        lines.append(f"from .{module} import (")
        lines.extend(f"    {name}," for name in names)
        lines.append(")")


def _render_docstring(docstring: str) -> list[str]:
    values = [line.strip() for line in docstring.strip().split("\n")]
    if len(values) == 1:
        return [f'        """{values[0]}"""']
    return [
        f'        """{values[0]}',
        *(f"        {line}" if line else "" for line in values[1:]),
        '        """',
    ]


def _render_param_lines(param: str) -> list[str]:
    line = f"        {param},"
    if len(line) <= LINE_LENGTH or ": " not in param:
        return [line]
    name, annotation = param.split(": ", 1)
    default = ""
    if " = " in annotation:
        annotation, value = annotation.rsplit(" = ", 1)
        default = f" = {value}"
    if " | " in annotation:
        left, right = annotation.rsplit(" | ", 1)
        return [f"        {name}: {left}", f"        | {right}{default},"]
    if "[" in annotation and "]" in annotation:
        base, inner = annotation.split("[", 1)
        return [
            f"        {name}: {base}[",
            f"            {inner.rsplit(']', 1)[0]}",
            f"        ]{default},",
        ]
    return [line]


def _render_method(
    name: str, signature: MethodSignature, *, overload: bool
) -> list[str]:
    lines: list[str] = ["    @overload"] if overload else []
    lines.extend([f"    async def {name}(", "        self,"])
    if signature.has_kwonly:
        lines.append("        *,")
    for param in signature.params:
        lines.extend(_render_param_lines(param))
    lines.append(f"    ) -> {_format_annotation(signature.returns) or 'None'}:")
    if signature.docstring and not overload:
        lines.extend(_render_docstring(signature.docstring))
    else:
        lines.append("        ...")
    lines.append("")
    return lines


def _render_client(methods: list[MethodSignature]) -> list[str]:
    lines = ["class ApiClient:"]
    index = 0
    while index < len(methods):
        name = methods[index].public_name
        grouped: list[MethodSignature] = []
        while index < len(methods) and methods[index].public_name == name:
            grouped.append(methods[index])
            index += 1
        overloads = [method for method in grouped if method.is_overload]
        if overloads:
            lines.extend(
                line
                for signature in overloads
                for line in _render_method(name, signature, overload=True)
            )
        else:
            lines.extend(_render_method(name, grouped[0], overload=False))
    return lines


def _combined_digest(paths: Iterable[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


async def _run_ruff_format(content: str, root: Path) -> str:
    ruff = shutil.which("ruff") or str(Path(sys.executable).with_name("ruff"))
    command = [ruff, "format", "--stdin-filename", "api/client.pyi", "-"]
    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=root,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate(content.encode())
    if process.returncode:
        raise subprocess.CalledProcessError(
            process.returncode,
            command,
            output=stdout.decode(),
            stderr=stderr.decode(),
        )
    return stdout.decode()


def _format_stub(content: str, root: Path) -> str:
    """Apply the repository's canonical Ruff formatting to generated stub text."""
    return asyncio.run(_run_ruff_format(content, root))


def _typing_imports(
    annotation_texts: list[str],
    methods: list[MethodSignature],
    aliases: dict[str, str],
) -> list[str]:
    imports: list[str] = []
    if any(re.search(r"\bAny\b", text) for text in annotation_texts):
        imports.append("Any")
    if any("Literal" in text for text in annotation_texts):
        imports.append("Literal")
    if any(method.is_overload for method in methods):
        imports.append("overload")
    if aliases:
        imports.append("TypeAlias")
    return sorted(imports)


def generate(root: Path) -> str:
    manifest_path = root / "nonebot/adapters/discord/api/endpoint_manifest.py"
    handle_path = root / "nonebot/adapters/discord/api/handle.py"
    groups = _manifest_groups(manifest_path)
    _validate_handle_assembly(handle_path, groups)
    endpoint_sources = _load_endpoint_sources(root, groups)
    methods = _methods(endpoint_sources)
    aliases = _local_aliases(endpoint_sources)
    model_imports, type_imports = _imports_for_annotations(root, methods, aliases)
    script_path = Path(__file__).resolve()
    digest = _combined_digest(
        [
            script_path,
            manifest_path,
            handle_path,
            *(endpoint.path for endpoint in endpoint_sources),
        ],
        root,
    )
    lines = [
        "# This file is auto-generated by scripts/generate_client_pyi.py.",
        "# Do not edit this file directly.",
        "# Sources: endpoint manifest, HandleMixin assembly, and domain endpoint mixins.",
        f"{HASH_HEADER_PREFIX}{digest}",
        "",
    ]
    annotation_texts = _annotation_texts(methods, aliases)
    if any("datetime" in text for text in annotation_texts):
        lines.append("from datetime import datetime")
    typing = _typing_imports(annotation_texts, methods, aliases)
    if typing:
        lines.append(f"from typing import {', '.join(typing)}")
    if lines[-1] != "":
        lines.append("")
    _append_import_block(lines, "model", model_imports)
    _append_import_block(lines, "types", type_imports)
    if model_imports or type_imports:
        lines.append("")
    for name, value in sorted(aliases.items()):
        lines.append(f"{name}: TypeAlias = {value}")
    if aliases:
        lines.append("")
    lines.append("")
    lines.extend(_render_client(methods))
    return _format_stub("\n".join(lines), root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="verify api/client.pyi without writing it"
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    client_path = root / "nonebot/adapters/discord/api/client.pyi"
    content = generate(root)
    if args.check:
        if (client_path.read_text("utf-8") if client_path.exists() else "") != content:
            parser.exit(
                1,
                "api/client.pyi is out of date; run python scripts/generate_client_pyi.py\n",
            )
        return
    client_path.write_text(content, "utf-8")


if __name__ == "__main__":
    main()
