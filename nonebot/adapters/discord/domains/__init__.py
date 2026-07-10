"""Bootstrap canonical Discord model modules without aggregating business names."""

from __future__ import annotations

from importlib import import_module

from . import _model_support
from ._manifest import DOMAIN_MODEL_MODULES, DOMAIN_TYPE_MODULES
from ._model_registry import rebuild_domain_models

_FORWARD_REFERENCE_NAMESPACE = {
    name: getattr(_model_support, name)
    for name in (
        "Any",
        "BaseModel",
        "Generic",
        "GenericModel",
        "Literal",
        "T",
        "TypeVar",
        "datetime",
    )
}


def bootstrap() -> dict[str, object]:
    """Load manifest modules and rebuild their shared Pydantic namespace."""
    type_modules = tuple(import_module(name) for name in DOMAIN_TYPE_MODULES)
    model_modules = tuple(import_module(name) for name in DOMAIN_MODEL_MODULES)
    return rebuild_domain_models(
        type_modules,
        model_modules,
        extra_namespace=_FORWARD_REFERENCE_NAMESPACE,
    )


MODEL_NAMESPACE = bootstrap()

__all__ = ["bootstrap"]
