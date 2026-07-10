"""Non-public enum support shared by canonical domain type modules."""

from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    """String enum."""


__all__: tuple[str, ...] = ()
