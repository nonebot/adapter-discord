from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..types import UNSET, Missing

if TYPE_CHECKING:
    from ..model import Application, User


class AuthorizationResponse(BaseModel):
    """Get Current Authorization Information Response

    see https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
    """

    application: Application
    scopes: list[str]
    expires: datetime.datetime
    user: Missing[User] = UNSET
