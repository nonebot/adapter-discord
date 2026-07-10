"""Canonical user.write models."""

from __future__ import annotations

from .._model_support import UNSET, BaseModel, Missing, MissingOrNullable


class ModifyCurrentUserParams(BaseModel):
    """Modify Current User Params.

    see https://discord.com/developers/docs/resources/user#modify-current-user
    """

    username: Missing[str] = UNSET
    avatar: MissingOrNullable[str] = UNSET
    banner: MissingOrNullable[str] = UNSET


__all__ = ["ModifyCurrentUserParams"]
