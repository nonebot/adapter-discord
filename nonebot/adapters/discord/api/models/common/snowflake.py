import datetime
from typing import Any, final
from typing_extensions import Self

from nonebot.compat import PYDANTIC_V2

if PYDANTIC_V2:
    from pydantic import GetCoreSchemaHandler
    from pydantic_core import CoreSchema, core_schema


@final
class Snowflake(int):
    """Snowflake is a type of discord uniquely identifiable descriptors.

    It can be treated as a regular `int` for most purposes.

    see https://discord.com/developers/docs/reference#snowflakes
    """

    __slots__ = ()

    if PYDANTIC_V2:

        @classmethod
        def __get_pydantic_core_schema__(
            cls,
            source: Any,  # noqa: ANN401
            handler: GetCoreSchemaHandler,
        ) -> CoreSchema:
            return core_schema.with_info_plain_validator_function(cls.validate)

        @classmethod
        def validate(cls, value: Any, _) -> Self:  # noqa: ANN001, ANN401
            if isinstance(value, str) and value.isdigit():
                value = int(value)
            if not isinstance(value, int):
                msg = f"{value!r} is not int or str of int"
                raise TypeError(msg)
            return cls(value)

    else:

        @classmethod
        def __get_validators__(cls):  # noqa: ANN206
            yield cls.validate

        @classmethod
        def validate(cls, value: Any):  # noqa: ANN206, ANN401
            if isinstance(value, str) and value.isdigit():
                value = int(value)
            if not isinstance(value, int):
                msg = f"{value!r} is not int or str of int"
                raise TypeError(msg)
            return cls(value)

    @property
    def timestamp(self) -> int:
        """Milliseconds since Discord Epoch,
        the first second of 2015 or 1420070400000.

        """

        return (self >> 22) + 1420070400000

    @property
    def create_at(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(
            self.timestamp / 1000, datetime.timezone.utc
        )

    @property
    def internal_worker_id(self) -> int:
        return (self & 0x3E0000) >> 17

    @property
    def internal_process_id(self) -> int:
        return (self & 0x1F000) >> 12

    @property
    def increment(self) -> int:
        """For every ID that is generated on that process, this number is incremented"""

        return self & 0xFFF

    @classmethod
    def from_data(
        cls, timestamp: int, worker_id: int, process_id: int, increment: int
    ) -> "Snowflake":
        """Convert the pieces of info that comprise an ID into a Snowflake.
        Args:
            timestamp (int): Milliseconds timestamp.
            worker_id: worker_id
            process_id: process_id
            increment: increment
        """

        return cls(
            (timestamp - 1420070400000) << 22
            | (worker_id << 17)
            | (process_id << 12)
            | increment
        )

    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> "Snowflake":
        """Get a Snowflake from a datetime object."""

        return cls.from_data(int(dt.timestamp() * 1000), 0, 0, 0)


SnowflakeType = Snowflake | int
"""Snowflake or int"""
