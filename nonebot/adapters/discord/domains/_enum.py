"""Non-public enum support shared by canonical domain type modules."""

from enum import Enum


class StrEnum(str, Enum):  # noqa: UP042 - preserve qualified member names in str()
    """String enum."""


__all__: tuple[str, ...] = ()
