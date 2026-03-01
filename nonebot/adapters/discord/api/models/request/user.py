from __future__ import annotations

from pydantic import BaseModel

from ...types import UNSET, Missing, MissingOrNullable


class ModifyCurrentUserParams(BaseModel):
    username: Missing[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET
