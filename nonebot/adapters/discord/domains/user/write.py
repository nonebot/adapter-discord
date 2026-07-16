"""Canonical user.write models."""

from typing_extensions import Required

from .._model_support import OutboundTypedDict
from ...protocol import SnowflakeType


class ModifyCurrentUserParams(OutboundTypedDict, total=False):
    """Modify Current User Params.

    see https://discord.com/developers/docs/resources/user#modify-current-user
    """

    username: str
    avatar: str | None
    banner: str | None


class CreateDMParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_create_DM``."""

    recipient_id: Required["SnowflakeType"]


class CreateGroupDMParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_create_group_DM``."""

    access_tokens: Required["list[str]"]
    nicks: Required["dict[SnowflakeType, str]"]


class UpdateUserApplicationRoleConnectionParams(OutboundTypedDict, total=False):
    """Parameters for ``_api_update_user_application_role_connection``."""

    platform_name: str
    platform_username: str
    metadata: "dict[str, str]"


__all__ = [
    "CreateDMParams",
    "CreateGroupDMParams",
    "ModifyCurrentUserParams",
    "UpdateUserApplicationRoleConnectionParams",
]
