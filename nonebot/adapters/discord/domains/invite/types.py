from enum import IntEnum


class InviteTargetType(IntEnum):
    """Invite target type.

    see https://discord.com/developers/docs/resources/invite#invite-object-invite-target-types
    """

    STREAM = 1
    EMBEDDED_APPLICATION = 2


class InviteType(IntEnum):
    """Invite Types

    see https://discord.com/developers/docs/resources/invite#invite-object-invite-types
    """

    GUILD = 0
    GROUP_DM = 1
    FRIEND = 2


__all__ = ["InviteTargetType", "InviteType"]
