from collections.abc import Mapping, Sequence


def bind_public_module(
    module_name: str, namespace: Mapping[str, object], names: Sequence[str]
) -> None:
    """Set exported class/enum ``__module__`` to the stable public facade module."""
    for name in names:
        value = namespace.get(name)
        if not isinstance(value, type):
            continue
        try:
            value.__module__ = module_name
        except (AttributeError, TypeError):
            continue
