"""Non-public enum support shared by canonical domain type modules."""

from enum import Enum


class StrEnum(str, Enum):
    """String enum."""


__all__: tuple[str, ...] = ()
