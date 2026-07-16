from enum import IntEnum
from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field

from .domains.models import (
    Hello as HelloData,
    Identify as IdentifyData,
    Resume as ResumeData,
)


class Opcode(IntEnum):
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    RESUME = 6
    RECONNECT = 7
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class Payload(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        validate_by_alias=True,
        validate_by_name=True,
    )


class Dispatch(Payload):
    opcode: Literal[Opcode.DISPATCH] = Field(Opcode.DISPATCH, alias="op")
    data: dict[str, object] = Field(alias="d")
    sequence: int = Field(alias="s")
    type: str = Field(alias="t")


class Heartbeat(Payload):
    opcode: Literal[Opcode.HEARTBEAT] = Field(Opcode.HEARTBEAT, alias="op")
    data: int | None = Field(None, alias="d")


class Identify(Payload):
    opcode: Literal[Opcode.IDENTIFY] = Field(Opcode.IDENTIFY, alias="op")
    data: IdentifyData = Field(alias="d")


class Resume(Payload):
    opcode: Literal[Opcode.RESUME] = Field(Opcode.RESUME, alias="op")
    data: ResumeData = Field(alias="d")


class Reconnect(Payload):
    opcode: Literal[Opcode.RECONNECT] = Field(Opcode.RECONNECT, alias="op")


class InvalidSession(Payload):
    opcode: Literal[Opcode.INVALID_SESSION] = Field(Opcode.INVALID_SESSION, alias="op")


class Hello(Payload):
    opcode: Literal[Opcode.HELLO] = Field(Opcode.HELLO, alias="op")
    data: HelloData = Field(alias="d")


class HeartbeatAck(Payload):
    opcode: Literal[Opcode.HEARTBEAT_ACK] = Field(Opcode.HEARTBEAT_ACK, alias="op")


PayloadType: TypeAlias = (
    Annotated[
        Dispatch | Heartbeat | Reconnect | InvalidSession | Hello | HeartbeatAck,
        Field(discriminator="opcode"),
    ]
    | Payload
)
