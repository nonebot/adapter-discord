"""Forward-reference rebuild support for canonical domain models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import inspect
from types import ModuleType

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


def rebuild_domain_models(
    type_modules: Sequence[ModuleType],
    model_modules: Sequence[ModuleType],
    *,
    extra_namespace: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Build one duplicate-free namespace and rebuild all canonical BaseModel classes."""
    namespace: dict[str, object] = {}

    _collect_module_names(namespace, protocol)
    for module in type_modules:
        _collect_module_names(namespace, module)
    for module in model_modules:
        _collect_module_names(namespace, module)
    if extra_namespace is not None:
        _collect_extra_names(namespace, extra_namespace)

    canonical_models: dict[type[BaseModel], None] = {}
    for module in model_modules:
        for name in module.__all__:
            value = getattr(module, name)
            if (
                inspect.isclass(value)
                and value is not BaseModel
                and issubclass(value, BaseModel)
            ):
                canonical_models[value] = None

    for model in canonical_models:
        if PYDANTIC_V2:
            model.model_rebuild(force=True, _types_namespace=namespace)
        else:
            model.update_forward_refs(**namespace)
    return namespace


__all__ = ["rebuild_domain_models"]
