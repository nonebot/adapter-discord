from __future__ import annotations

from pydantic import BaseModel

from ...types import UNSET, Missing, MissingOrNullable


class CreateGuildTemplateParams(BaseModel):
    name: str
    description: MissingOrNullable[str] = UNSET


class ModifyGuildTemplateParams(BaseModel):
    name: Missing[str] = UNSET
    description: MissingOrNullable[str] = UNSET


__all__ = ["CreateGuildTemplateParams", "ModifyGuildTemplateParams"]
