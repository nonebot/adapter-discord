from collections.abc import Callable, Iterable, Sequence
from datetime import datetime, timedelta
from typing import Any
from typing_extensions import deprecated
import warnings

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
from pydantic import BaseModel

from .params import OptionParam
from .response import get_command_response
from .storage import (
    _application_command_storage,
)
from ..bot import Bot
from ..domains.interaction.conversion import to_origin_edit
from ..domains.message.conversion import compile_message
from ..domains.models import (
    AnyCommandOption,
    ApplicationCommandOptionType,
    ApplicationCommandType,
    ApplicationIntegrationType,
    InteractionContextType,
    MessageFlag,
    MessageGet,
)
from ..event import ApplicationCommandInteractionEvent
from ..message import Message, MessageSegment
from ..protocol import UNSET, Missing, Snowflake, SnowflakeType, is_unset

type_str_mapping = {
    ApplicationCommandOptionType.USER: "users",
    ApplicationCommandOptionType.CHANNEL: "channels",
    ApplicationCommandOptionType.ROLE: "roles",
    ApplicationCommandOptionType.ATTACHMENT: "attachments",
}
_DEFERRED_RESPONSE_DEPRECATION = (
    "ApplicationCommandMatcher.send_deferred_response() is deprecated and will be "
    "removed in 2.0; inject CommandResponse and call response.defer()"
)
_RESPONSE_DEPRECATION = (
    "ApplicationCommandMatcher.send_response() is deprecated and will be removed in "
    "2.0; inject CommandResponse and call response.respond()"
)
_FOLLOWUP_DEPRECATION = (
    "ApplicationCommandMatcher.send_followup_msg() is deprecated and will be "
    "removed in 2.0; inject CommandResponse and call response.followup()"
)


class ApplicationCommandConfig(BaseModel):
    name: str
    name_localizations: dict[str, str] | None = None
    description: str = ""
    description_localizations: dict[str, str] | None = None
    options: Missing[list[AnyCommandOption]] = UNSET
    default_member_permissions: str | None = None
    dm_permission: bool | None = None
    default_permission: Missing[bool] = UNSET
    integration_types: Missing[list[ApplicationIntegrationType]] = UNSET
    contexts: Missing[list[InteractionContextType]] = UNSET
    type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT
    nsfw: Missing[bool] = UNSET
    guild_ids: list[Snowflake] | None = None


class ApplicationCommandMatcher(Matcher):
    application_command: ApplicationCommandConfig

    @classmethod
    @deprecated(_DEFERRED_RESPONSE_DEPRECATION, category=None)
    async def send_deferred_response(cls) -> None:
        del cls
        warnings.warn(_DEFERRED_RESPONSE_DEPRECATION, DeprecationWarning, stacklevel=2)
        event = current_event.get()
        bot = current_bot.get()
        response = get_command_response(event, bot)
        await response.defer()

    @classmethod
    @deprecated(_RESPONSE_DEPRECATION, category=None)
    async def send_response(
        cls, message: str | Message | MessageSegment | MessageTemplate
    ) -> None:
        warnings.warn(_RESPONSE_DEPRECATION, DeprecationWarning, stacklevel=2)
        return await cls.send(message)

    @classmethod
    async def get_response(cls) -> MessageGet:
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            msg = "Invalid event or bot"
            raise ValueError(msg)  # noqa: TRY004
        return await bot.get_origin_interaction_response(
            application_id=event.application_id,
            interaction_token=event.token,
        )

    @classmethod
    async def edit_response(
        cls,
        message: str | Message | MessageSegment | MessageTemplate,
    ) -> None:
        event = current_event.get()
        bot = current_bot.get()
        state = current_matcher.get().state
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            msg = "Invalid event or bot"
            raise ValueError(msg)  # noqa: TRY004
        if isinstance(message, MessageTemplate):
            _message = message.format(**state)
        else:
            _message = message
        request = to_origin_edit(compile_message(_message))
        await bot.edit_origin_interaction_response(
            application_id=event.application_id,
            interaction_token=event.token,
            **request,
        )

    @classmethod
    async def delete_response(cls) -> None:
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            msg = "Invalid event or bot"
            raise ValueError(msg)  # noqa: TRY004
        await bot.delete_origin_interaction_response(
            application_id=event.application_id,
            interaction_token=event.token,
        )

    @classmethod
    @deprecated(_FOLLOWUP_DEPRECATION, category=None)
    async def send_followup_msg(
        cls,
        message: str | Message | MessageSegment | MessageTemplate,
        flags: MessageFlag | None = None,
    ) -> MessageGet:
        warnings.warn(_FOLLOWUP_DEPRECATION, DeprecationWarning, stacklevel=2)
        event = current_event.get()
        bot = current_bot.get()
        state = current_matcher.get().state
        response = get_command_response(event, bot)
        if isinstance(message, MessageTemplate):
            _message = message.format(**state)
        else:
            _message = message
        return await response.followup_with_flags(_message, flags=flags)

    @classmethod
    async def get_followup_msg(cls, message_id: SnowflakeType) -> MessageGet:
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            msg = "Invalid event or bot"
            raise ValueError(msg)  # noqa: TRY004
        return await bot.get_followup_message(
            application_id=event.application_id,
            interaction_token=event.token,
            message_id=message_id,
        )

    @classmethod
    async def edit_followup_msg(
        cls,
        message_id: SnowflakeType,
        message: str | Message | MessageSegment | MessageTemplate,
    ) -> MessageGet:
        event = current_event.get()
        bot = current_bot.get()
        state = current_matcher.get().state
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            msg = "Invalid event or bot"
            raise ValueError(msg)  # noqa: TRY004
        if isinstance(message, MessageTemplate):
            _message = message.format(**state)
        else:
            _message = message
        request = to_origin_edit(compile_message(_message))
        return await bot.edit_followup_message(
            application_id=event.application_id,
            interaction_token=event.token,
            message_id=message_id,
            **request,
        )

    @classmethod
    async def delete_followup_msg(cls, message_id: SnowflakeType) -> None:
        event = current_event.get()
        bot = current_bot.get()
        if not isinstance(event, ApplicationCommandInteractionEvent) or not isinstance(
            bot, Bot
        ):
            msg = "Invalid event or bot"
            raise ValueError(msg)  # noqa: TRY004
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
        cls, *commands: str, parameterless: Iterable[Any] | None = None
    ) -> Callable[..., T_Handler]:
        def _sub_command_rule(
            event: ApplicationCommandInteractionEvent,
            matcher: Matcher,
            state: T_State,  # noqa: ARG001 # TODO)): 验证state作用
        ) -> None:
            options = event.data.options
            if commands and is_unset(options):
                matcher.skip()
            for command in commands:
                if is_unset(options):
                    matcher.skip()
                option = options[0]
                if option.name != command or option.type not in (
                    ApplicationCommandOptionType.SUB_COMMAND_GROUP,
                    ApplicationCommandOptionType.SUB_COMMAND,
                ):
                    matcher.skip()
                options = option.options

        parameterless = [Depends(_sub_command_rule), *(parameterless or [])]

        def _decorator(func: T_Handler) -> T_Handler:
            cls.append_handler(func, parameterless=parameterless)
            return func

        return _decorator


class UserMessageCommandMatcher(ApplicationCommandMatcher):
    pass


def on_slash_command(  # noqa: PLR0913
    name: str,
    description: str,
    options: Missing[Sequence[AnyCommandOption]] = UNSET,
    internal_id: str | None = None,
    rule: Rule | T_RuleChecker | None = None,
    permission: Permission | T_PermissionChecker | None = None,
    *,
    name_localizations: dict[str, str] | None = None,
    description_localizations: dict[str, str] | None = None,
    default_member_permissions: str | None = None,
    dm_permission: bool | None = None,
    default_permission: Missing[bool] = UNSET,
    nsfw: Missing[bool] = UNSET,
    handlers: list[T_Handler | Dependent] | None = None,
    temp: bool = False,
    expire_time: datetime | timedelta | None = None,
    priority: int = 1,
    block: bool = True,
    state: T_State | None = None,
    _depth: int = 0,
) -> type[SlashCommandMatcher]:
    config = ApplicationCommandConfig(
        type=ApplicationCommandType.CHAT_INPUT,
        name=name,
        name_localizations=name_localizations,
        description=description,
        description_localizations=description_localizations,
        options=UNSET if is_unset(options) else list(options),
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
        return bool(
            event.data.guild_id
            and config.guild_ids
            and event.data.guild_id in config.guild_ids
        )

    matcher.rule = matcher.rule & Rule(_application_command_rule)

    store_matcher(matcher)
    matcher.application_command = config
    return matcher


def on_user_command(  # noqa: PLR0913
    name: str,
    internal_id: str | None = None,
    rule: Rule | T_RuleChecker | None = None,
    permission: Permission | T_PermissionChecker | None = None,
    *,
    name_localizations: dict[str, str] | None = None,
    default_member_permissions: str | None = None,
    dm_permission: bool | None = None,
    default_permission: Missing[bool] = UNSET,
    nsfw: Missing[bool] = UNSET,
    handlers: list[T_Handler | Dependent] | None = None,
    temp: bool = False,
    expire_time: datetime | timedelta | None = None,
    priority: int = 1,
    block: bool = True,
    state: T_State | None = None,
    _depth: int = 0,
) -> type[UserMessageCommandMatcher]:
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
        return bool(
            event.data.guild_id
            and config.guild_ids
            and event.data.guild_id in config.guild_ids
        )

    matcher.rule = matcher.rule & Rule(_application_command_rule)

    store_matcher(matcher)
    matcher.application_command = config
    return matcher


def on_message_command(  # noqa: PLR0913
    name: str,
    internal_id: str | None = None,
    rule: Rule | T_RuleChecker | None = None,
    permission: Permission | T_PermissionChecker | None = None,
    *,
    name_localizations: dict[str, str] | None = None,
    default_member_permissions: str | None = None,
    dm_permission: bool | None = None,
    default_permission: Missing[bool] = UNSET,
    nsfw: Missing[bool] = UNSET,
    handlers: list[T_Handler | Dependent] | None = None,
    temp: bool = False,
    expire_time: datetime | timedelta | None = None,
    priority: int = 1,
    block: bool = True,
    state: T_State | None = None,
    _depth: int = 0,
) -> type[UserMessageCommandMatcher]:
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
        return bool(
            event.data.guild_id
            and config.guild_ids
            and event.data.guild_id in config.guild_ids
        )

    matcher.rule = matcher.rule & Rule(_application_command_rule)

    store_matcher(matcher)
    matcher.application_command = config
    return matcher
