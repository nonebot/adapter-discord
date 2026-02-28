from __future__ import annotations

from pydantic import BaseModel

from ..common.snowflake import Snowflake
from ..common.integrations import Integration
from ...types import UNSET, Missing


class IntegrationCreate(Integration):
    guild_id: Snowflake


class IntegrationUpdate(Integration):
    guild_id: Snowflake


class IntegrationDelete(BaseModel):
    id: Snowflake
    guild_id: Snowflake
    application_id: Missing[Snowflake] = UNSET
