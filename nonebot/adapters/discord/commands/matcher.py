from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional, Type, Union

from nonebot.adapters import MessageTemplate
from nonebot.dependencies import Dependent
from nonebot.internal.matcher import (
    Matcher,
    current_bot,
    current_event,
    current_matcher,
)
from nonebot.internal.params import (
    ArgParam,
    BotParam,
    DefaultParam,
    DependParam,
    Depends,
    EventParam,
    MatcherParam,
    StateParam,
)
from nonebot.permission import Permission
from nonebot.plugin.on import get_matcher_module, get_matcher_plugin, store_matcher
from nonebot.rule import Rule
from nonebot.typing import T_Handler, T_PermissionChecker, T_RuleChecker, T_State

from .params import OptionParam
from .storage import (
    _application_command_storage,
)
from ..api import (
    AnyCommandOption,
    ApplicationCommandCreate,
    ApplicationCommandOptionType,
    ApplicationCommandType,
    InteractionCallbackType,
    InteractionResponse,
    MessageFlag,
    MessageGet,
    Snowflake,
    SnowflakeType,
)
from ..bot import Bot
from ..event import ApplicationCommandInteractionEvent
from ..message import Message, MessageSegment, parse_message

type_str_mapping = {
    ApplicationCommandOptionType.USER: "users",
    ApplicationCommandOptionType.CHANNEL: "channels",
    ApplicationCommandOptionType.ROLE: "roles",
    ApplicationCommandOptionType.ATTACHMENT: "attachments",
}


class ApplicationCommandConfig(ApplicationCommandCreate):
    guild_ids: Optional[List[Snowflake]] = None


# def _application_command_rule(event: ApplicationCommandInteractionEvent) -> bool:
#     application_command = _application_command_storage.get(event.data.name)
#     if not application_command or event.data.type != application_command.type:
#         return False
#     if not event.data.guild_id and application_command.guild_ids is None:
#         return True
#     if (
#         event.data.guild_id
#         and application_command.guild_ids
#         and event.data.guild_id in application_command.guild_ids
#     ):
#         return True
#     return False


class ApplicationCommandMatcher(Matcher):
    application_command: ApplicationCommandConfig

    @classmethod
    async def send_deferred_response(cls) -> None:
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            raise ValueError("Invalid event or bot")
        await bot.create_interaction_response(
            interaction_id=event.id,
            interaction_token=event.token,
            response=InteractionResponse(
                type=InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
            ),
        )

    @classmethod
    async def send_response(
        cls, message: Union[str, Message, MessageSegment, MessageTemplate]
    ) -> None:
        return await cls.send(message)

    @classmethod
    async def get_response(cls) -> MessageGet:
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            raise ValueError("Invalid event or bot")
        return await bot.get_origin_interaction_response(
            application_id=event.application_id,
            interaction_token=event.token,
        )

    @classmethod
    async def edit_response(
        cls,
        message: Union[str, Message, MessageSegment, MessageTemplate],
    ) -> None:
        event = current_event.get()
        bot = current_bot.get()
        state = current_matcher.get().state
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            raise ValueError("Invalid event or bot")
        if isinstance(message, MessageTemplate):
            _message = message.format(**state)
        else:
            _message = message
        message_data = parse_message(_message)
        await bot.edit_origin_interaction_response(
            application_id=event.application_id,
            interaction_token=event.token,
            **message_data,
        )

    @classmethod
    async def delete_response(cls) -> None:
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            raise ValueError("Invalid event or bot")
        await bot.delete_origin_interaction_response(
            application_id=event.application_id,
            interaction_token=event.token,
        )

    @classmethod
    async def send_followup_msg(
        cls,
        message: Union[str, Message, MessageSegment, MessageTemplate],
        flags: Optional[MessageFlag] = None,
    ) -> MessageGet:
        event = current_event.get()
        bot = current_bot.get()
        state = current_matcher.get().state
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            raise ValueError("Invalid event or bot")
        if isinstance(message, MessageTemplate):
            _message = message.format(**state)
        else:
            _message = message
        message_data = parse_message(_message)
        if flags:
            message_data["flags"] = int(flags)
        return await bot.create_followup_message(
            application_id=event.application_id,
            interaction_token=event.token,
            **message_data,
        )

    @classmethod
    async def get_followup_msg(cls, message_id: SnowflakeType):
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            raise ValueError("Invalid event or bot")
        return await bot.get_followup_message(
            application_id=event.application_id,
            interaction_token=event.token,
            message_id=message_id,
        )

    @classmethod
    async def edit_followup_msg(
        cls,
        message_id: SnowflakeType,
        message: Union[str, Message, MessageSegment, MessageTemplate],
    ) -> MessageGet:
        event = current_event.get()
        bot = current_bot.get()
        state = current_matcher.get().state
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            raise ValueError("Invalid event or bot")
        if isinstance(message, MessageTemplate):
            _message = message.format(**state)
        else:
            _message = message
        message_data = parse_message(_message)
        return await bot.edit_followup_message(
            application_id=event.application_id,
            interaction_token=event.token,
            message_id=message_id,
            **message_data,
        )

    @classmethod
    async def delete_followup_msg(cls, message_id: SnowflakeType) -> None:
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            raise ValueError("Invalid event or bot")
        await bot.delete_followup_message(
            application_id=event.application_id,
            interaction_token=event.token,
            message_id=message_id,
        )


class SlashCommandMatcher(ApplicationCommandMatcher):
    HANDLER_PARAM_TYPES = (
        DependParam,
        BotParam,
        EventParam,
        StateParam,
        ArgParam,
        MatcherParam,
        DefaultParam,
        OptionParam,
    )

    @classmethod
    def handle_sub_command(
        cls, *commands: str, parameterless: Optional[Iterable[Any]] = None
    ):
        def _sub_command_rule(
            event: ApplicationCommandInteractionEvent, matcher: Matcher, state: T_State
        ):
            if commands and not event.data.options:
                matcher.skip()
            options = event.data.options
            for command in commands:
                if not options:
                    matcher.skip()
                option = options[0]
                if option.name != command or options[0].type not in (
                    ApplicationCommandOptionType.SUB_COMMAND_GROUP,
                    ApplicationCommandOptionType.SUB_COMMAND,
                ):
                    matcher.skip()
                options = options[0].options if options[0].options else None
            # if options:
            #     state[OPTION_KEY] = {}
            #     for option in options:
            #         if (
            #             option.type
            #             in (
            #                 ApplicationCommandOptionType.USER,
            #                 ApplicationCommandOptionType.CHANNEL,
            #                 ApplicationCommandOptionType.ROLE,
            #                 ApplicationCommandOptionType.ATTACHMENT,
            #             )
            #             and event.data.resolved
            #             and (
            #                 data := getattr(
            #                     event.data.resolved, type_str_mapping[option.type]
            #                 )
            #             )
            #         ):
            #             state[OPTION_KEY][option.name] = data[
            #                 Snowflake(option.value)  # type: ignore
            #             ]
            #         elif (
            #             option.type == ApplicationCommandOptionType.MENTIONABLE
            #             and event.data.resolved
            #             and event.data.resolved.users
            #         ):
            #             sid = Snowflake(option.value)  # type: ignore
            #             state[OPTION_KEY][option.name] = (
            #                 event.data.resolved.users.get(sid),
            #                 (
            #                     event.data.resolved.members.get(sid)
            #                     if event.data.resolved.members
            #                     else None
            #                 ),
            #             )
            #         elif option.type in (
            #             ApplicationCommandOptionType.INTEGER,
            #             ApplicationCommandOptionType.STRING,
            #             ApplicationCommandOptionType.NUMBER,
            #             ApplicationCommandOptionType.BOOLEAN,
            #         ):
            #             state[OPTION_KEY][option.name] = option.value

        parameterless = [Depends(_sub_command_rule), *(parameterless or [])]

        def _decorator(func: T_Handler) -> T_Handler:
            cls.append_handler(func, parameterless=parameterless)
            return func

        return _decorator


class UserMessageCommandMatcher(ApplicationCommandMatcher):
    pass


def on_slash_command(
    name: str,
    description: str,
    options: Optional[List[AnyCommandOption]] = None,
    internal_id: Optional[str] = None,
    rule: Union[Rule, T_RuleChecker, None] = None,
    permission: Union[Permission, T_PermissionChecker, None] = None,
    *,
    name_localizations: Optional[Dict[str, str]] = None,
    description_localizations: Optional[Dict[str, str]] = None,
    default_member_permissions: Optional[str] = None,
    dm_permission: Optional[bool] = None,
    default_permission: Optional[bool] = None,
    nsfw: Optional[bool] = None,
    handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
    temp: bool = False,
    expire_time: Union[datetime, timedelta, None] = None,
    priority: int = 1,
    block: bool = True,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> Type[SlashCommandMatcher]:
    config = ApplicationCommandConfig(
        type=ApplicationCommandType.CHAT_INPUT,
        name=name,
        name_localizations=name_localizations,
        description=description,
        description_localizations=description_localizations,
        options=options,
        default_member_permissions=default_member_permissions,
        dm_permission=dm_permission,
        default_permission=default_permission,
        nsfw=nsfw,
    )
    _application_command_storage[internal_id or name] = config
    matcher: type[SlashCommandMatcher] = SlashCommandMatcher.new(
        "notice",
        Rule() & rule,
        Permission() | permission,
        handlers=handlers,
        temp=temp,
        expire_time=expire_time,
        priority=priority,
        block=block,
        default_state=state,
        plugin=get_matcher_plugin(_depth + 1),
        module=get_matcher_module(_depth + 1),
    )

    def _application_command_rule(event: ApplicationCommandInteractionEvent) -> bool:
        if event.data.name != config.name or event.data.type != config.type:
            return False
        if not event.data.guild_id and config.guild_ids is None:
            return True
        if (
            event.data.guild_id
            and config.guild_ids
            and event.data.guild_id in config.guild_ids
        ):
            return True
        return False

    matcher.rule = matcher.rule & Rule(_application_command_rule)

    store_matcher(matcher)
    matcher.application_command = config
    return matcher


def on_user_command(
    name: str,
    internal_id: Optional[str] = None,
    rule: Union[Rule, T_RuleChecker, None] = None,
    permission: Union[Permission, T_PermissionChecker, None] = None,
    *,
    name_localizations: Optional[Dict[str, str]] = None,
    default_member_permissions: Optional[str] = None,
    dm_permission: Optional[bool] = None,
    default_permission: Optional[bool] = None,
    nsfw: Optional[bool] = None,
    handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
    temp: bool = False,
    expire_time: Union[datetime, timedelta, None] = None,
    priority: int = 1,
    block: bool = True,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> Type[UserMessageCommandMatcher]:
    config = ApplicationCommandConfig(
        type=ApplicationCommandType.USER,
        name=name,
        name_localizations=name_localizations,
        default_member_permissions=default_member_permissions,
        dm_permission=dm_permission,
        default_permission=default_permission,
        nsfw=nsfw,
    )
    _application_command_storage[internal_id or name] = config
    matcher: type[UserMessageCommandMatcher] = UserMessageCommandMatcher.new(
        "notice",
        Rule() & rule,
        Permission() | permission,
        handlers=handlers,
        temp=temp,
        expire_time=expire_time,
        priority=priority,
        block=block,
        default_state=state,
        plugin=get_matcher_plugin(_depth + 1),
        module=get_matcher_module(_depth + 1),
    )

    def _application_command_rule(event: ApplicationCommandInteractionEvent) -> bool:
        if event.data.name != config.name or event.data.type != config.type:
            return False
        if not event.data.guild_id and config.guild_ids is None:
            return True
        if (
            event.data.guild_id
            and config.guild_ids
            and event.data.guild_id in config.guild_ids
        ):
            return True
        return False

    matcher.rule = matcher.rule & Rule(_application_command_rule)

    store_matcher(matcher)
    matcher.application_command = config
    return matcher


def on_message_command(
    name: str,
    internal_id: Optional[str] = None,
    rule: Union[Rule, T_RuleChecker, None] = None,
    permission: Union[Permission, T_PermissionChecker, None] = None,
    *,
    name_localizations: Optional[Dict[str, str]] = None,
    default_member_permissions: Optional[str] = None,
    dm_permission: Optional[bool] = None,
    default_permission: Optional[bool] = None,
    nsfw: Optional[bool] = None,
    handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
    temp: bool = False,
    expire_time: Union[datetime, timedelta, None] = None,
    priority: int = 1,
    block: bool = True,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> Type[UserMessageCommandMatcher]:
    config = ApplicationCommandConfig(
        type=ApplicationCommandType.MESSAGE,
        name=name,
        name_localizations=name_localizations,
        default_member_permissions=default_member_permissions,
        dm_permission=dm_permission,
        default_permission=default_permission,
        nsfw=nsfw,
    )
    _application_command_storage[internal_id or name] = config
    matcher: type[UserMessageCommandMatcher] = UserMessageCommandMatcher.new(
        "notice",
        Rule() & rule,
        Permission() | permission,
        handlers=handlers,
        temp=temp,
        expire_time=expire_time,
        priority=priority,
        block=block,
        default_state=state,
        plugin=get_matcher_plugin(_depth + 1),
        module=get_matcher_module(_depth + 1),
    )

    def _application_command_rule(event: ApplicationCommandInteractionEvent) -> bool:
        if event.data.name != config.name or event.data.type != config.type:
            return False
        if not event.data.guild_id and config.guild_ids is None:
            return True
        if (
            event.data.guild_id
            and config.guild_ids
            and event.data.guild_id in config.guild_ids
        ):
            return True
        return False

    matcher.rule = matcher.rule & Rule(_application_command_rule)

    store_matcher(matcher)
    matcher.application_command = config
    return matcher
