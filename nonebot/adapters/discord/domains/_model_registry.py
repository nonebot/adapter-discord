"""Forward-reference rebuild support for canonical domain models."""

from collections.abc import Mapping, Sequence
import inspect
from types import ModuleType
from typing import get_type_hints
from typing_extensions import is_typeddict

from nonebot.compat import PYDANTIC_V2
from pydantic import BaseModel

from .. import protocol


def _duplicate_name_error(name: str, origin: str) -> RuntimeError:
    message = f"Duplicate canonical domain name {name!r} from {origin}"
    return RuntimeError(message)


def _collect_module_names(namespace: dict[str, object], module: ModuleType) -> None:
    for name in getattr(module, "__all__", ()):
        if name in namespace:
            raise _duplicate_name_error(name, module.__name__)
        namespace[name] = getattr(module, name)


def _collect_extra_names(
    namespace: dict[str, object], extra_namespace: Mapping[str, object]
) -> None:
    for name, value in extra_namespace.items():
        if name in namespace:
            raise _duplicate_name_error(name, "extra namespace")
        namespace[name] = value


def rebuild_domain_models(  # noqa: C901
    type_modules: Sequence[ModuleType],
    model_modules: Sequence[ModuleType],
    *,
    extra_namespace: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Build one duplicate-free namespace and resolve all canonical models."""
    namespace: dict[str, object] = {}

    _collect_module_names(namespace, protocol)
    for module in type_modules:
        _collect_module_names(namespace, module)
    for module in model_modules:
        _collect_module_names(namespace, module)
    if extra_namespace is not None:
        _collect_extra_names(namespace, extra_namespace)

    canonical_models: dict[type[BaseModel], None] = {}
    canonical_typed_dicts: dict[type[object], None] = {}
    for module in model_modules:
        for name in module.__all__:
            value = getattr(module, name)
            if is_typeddict(value):
                canonical_typed_dicts[value] = None
            elif (
                inspect.isclass(value)
                and value is not BaseModel
                and issubclass(value, BaseModel)
            ):
                canonical_models[value] = None

    for typed_dict in canonical_typed_dicts:
        required_keys = getattr(typed_dict, "__required_keys__", frozenset())
        optional_keys = getattr(typed_dict, "__optional_keys__", frozenset())
        annotation_keys = typed_dict.__annotations__.keys()
        if (
            required_keys & optional_keys
            or required_keys | optional_keys != annotation_keys
        ):
            msg = f"Invalid TypedDict key metadata for {typed_dict.__qualname__}"
            raise RuntimeError(msg)
        typed_dict.__annotations__ = get_type_hints(
            typed_dict,
            globalns=namespace,
            localns=namespace,
            include_extras=True,
        )

    for model in canonical_models:
        if PYDANTIC_V2:
            model.model_rebuild(force=True, _types_namespace=namespace)
        else:
            model.update_forward_refs(**namespace)
    return namespace


__all__ = ["rebuild_domain_models"]
