from typing import Literal, TypeAlias, TypeVar, final
from typing_extensions import TypeIs, override

T = TypeVar("T")


class _UNSET(type):
    @override
    def __str__(cls) -> Literal["<UNSET>"]:
        return "<UNSET>"

    @override
    def __repr__(cls) -> Literal["<UNSET>"]:
        return "<UNSET>"

    def __bool__(cls) -> Literal[False]:
        return False


@final
class UNSET(metaclass=_UNSET):
    """UNSET means that the field maybe not given in the data.

    see https://discord.com/developers/docs/reference#nullable-and-optional-resource-fields
    """


UnsetType: TypeAlias = type[UNSET]

Missing: TypeAlias = UnsetType | T
"""Missing means that the field maybe not given in the data.

Missing[T] equal to Union[UnsetType, T].

example: Missing[int] == Union[UnsetType, int]

see https://discord.com/developers/docs/reference#nullable-and-optional-resource-fields"""

MissingOrNullable: TypeAlias = UnsetType | T | None
"""MissingOrNullable means that the field maybe not given in the data or value is None.

MissingOrNullable[T] equal to Union[UnsetType, T, None].

example: MissingOrNullable[int] == Union[UnsetType, int, None]

see https://discord.com/developers/docs/reference#nullable-and-optional-resource-fields"""


def is_unset(value: object) -> TypeIs[UnsetType]:
    """Check if the value is UNSET."""
    return value is UNSET


def is_not_unset(value: T | UnsetType) -> TypeIs[T]:
    """Check if the value is not UNSET."""
    return value is not UNSET


__all__ = [
    "UNSET",
    "Missing",
    "MissingOrNullable",
    "UnsetType",
    "is_not_unset",
    "is_unset",
]
