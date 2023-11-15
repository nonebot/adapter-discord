from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Literal

from ..api import ApplicationCommandCreate, Snowflake
from ..bot import Bot

if TYPE_CHECKING:
    from .matcher import ApplicationCommandConfig

_application_command_storage: Dict[str, "ApplicationCommandConfig"] = {}

OPTION_KEY: Literal[
    "_discord_application_command_options"
] = "_discord_application_command_options"


async def sync_application_command(bot: Bot):
    commands_global: List[ApplicationCommandCreate] = []
    commands_guild: Dict[Snowflake, List[ApplicationCommandCreate]] = defaultdict(List)
    if "*" in bot.bot_info.application_commands:
        if "*" in bot.bot_info.application_commands["*"]:
            commands_global = [
                ApplicationCommandCreate(
                    **a.dict(exclude={"guild_ids"}, exclude_none=True)
                )
                for a in _application_command_storage.values()
            ]
        else:
            for command in _application_command_storage.values():
                command.guild_ids = [
                    g for g in bot.bot_info.application_commands["*"] if g != "*"
                ]
                for guild in command.guild_ids:
                    commands_guild[guild].append(
                        ApplicationCommandCreate(
                            **command.dict(exclude={"guild_ids"}, exclude_none=True)
                        )
                    )
    else:
        for name, config in bot.bot_info.application_commands.items():
            command = _application_command_storage.get(name)
            if command:
                if "*" in config:
                    commands_global.append(
                        ApplicationCommandCreate(
                            **command.dict(exclude={"guild_ids"}, exclude_none=True)
                        )
                    )
                else:
                    command.guild_ids = [g for g in config if g != "*"]
                    for guild in command.guild_ids:
                        commands_guild[guild].append(
                            ApplicationCommandCreate(
                                **command.dict(exclude={"guild_ids"}, exclude_none=True)
                            )
                        )
    if commands_global:
        await bot.bulk_overwrite_global_application_commands(
            application_id=bot.application_id, commands=commands_global
        )
    for guild, commands in commands_guild.items():
        if commands:
            await bot.bulk_overwrite_guild_application_commands(
                application_id=bot.application_id,
                guild_id=guild,
                commands=commands,
            )
