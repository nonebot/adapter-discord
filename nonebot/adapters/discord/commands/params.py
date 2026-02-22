import inspect
from typing import Annotated, Any, TypeVar, get_args, get_origin
from typing_extensions import override

from nonebot.dependencies import Param
from nonebot.params import Depends

from ..api import (
    ApplicationCommandOptionType,
    ApplicationCommandType,
    MessageGet,
    Snowflake,
    User,
)
from ..api.model import ApplicationCommandInteractionDataOption
from ..api.types import Missing, is_not_unset, is_unset
from ..event import ApplicationCommandInteractionEvent

T = TypeVar("T")

type_str_mapping = {
    ApplicationCommandOptionType.USER: "users",
    ApplicationCommandOptionType.CHANNEL: "channels",
    ApplicationCommandOptionType.ROLE: "roles",
    ApplicationCommandOptionType.ATTACHMENT: "attachments",
}


class CommandOptionType:
    def __init__(self, key: str | None = None) -> None:
        self.key = key

    @override
    def __repr__(self) -> str:
        return f"ACommandOption(key={self.key!r})"


class OptionParam(Param):
    def __init__(self, *args, key: str, **kwargs: Any) -> None:  # noqa: ANN002, ANN401
        super().__init__(*args, **kwargs)
        self.key = key

    @override
    def __repr__(self) -> str:
        return f"OptionParam(key={self.key!r})"

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> "OptionParam | None":
        if isinstance(param.default, CommandOptionType):
            return cls(key=param.default.key or param.name, validate=True)
        if get_origin(param.annotation) is Annotated:
            for arg in get_args(param.annotation):
                if isinstance(arg, CommandOptionType):
                    return cls(key=arg.key or param.name, validate=True)
        return None

    @staticmethod
    def _get_options(
        options: Missing[list[ApplicationCommandInteractionDataOption]],
    ) -> list[ApplicationCommandInteractionDataOption] | None:
        if is_unset(options):
            return None
        if (
            options
            and options[0].type == ApplicationCommandOptionType.SUB_COMMAND_GROUP
        ):
            if is_unset(options[0].options):
                return None
            options = options[0].options
        if options and options[0].type == ApplicationCommandOptionType.SUB_COMMAND:
            if is_unset(options[0].options):
                return None
            options = options[0].options
        return options

    @override
    async def _solve(
        self, event: ApplicationCommandInteractionEvent, **kwargs: Any
    ) -> Any:
        options = self._get_options(event.data.options)
        if options is None:
            return None

        for option in options:
            if option.name != self.key:
                continue
            if option.type in (
                ApplicationCommandOptionType.USER,
                ApplicationCommandOptionType.CHANNEL,
                ApplicationCommandOptionType.ROLE,
                ApplicationCommandOptionType.ATTACHMENT,
                ApplicationCommandOptionType.MENTIONABLE,
            ) and is_not_unset(event.data.resolved):
                if not isinstance(option.value, (str, int)) or isinstance(
                    option.value, bool
                ):
                    return None
                if option.type != ApplicationCommandOptionType.MENTIONABLE:
                    data = getattr(event.data.resolved, type_str_mapping[option.type])
                    if is_not_unset(data):
                        return data[Snowflake(option.value)]
                elif is_not_unset(event.data.resolved.users):
                    sid = Snowflake(option.value)
                    members = (
                        None
                        if is_unset(event.data.resolved.members)
                        else event.data.resolved.members
                    )
                    return (
                        event.data.resolved.users.get(sid),
                        members.get(sid) if members else None,
                    )
            if option.type in (
                ApplicationCommandOptionType.INTEGER,
                ApplicationCommandOptionType.STRING,
                ApplicationCommandOptionType.NUMBER,
                ApplicationCommandOptionType.BOOLEAN,
            ) and is_not_unset(option.value):
                return option.value
        return None


def get_command_message(
    event: ApplicationCommandInteractionEvent,
) -> MessageGet | None:
    if event.data.type != ApplicationCommandType.MESSAGE:
        return None

    if (
        is_unset(event.data.target_id)
        or is_unset(event.data.resolved)
        or is_unset(event.data.resolved.messages)
    ):
        return None

    return event.data.resolved.messages.get(event.data.target_id)


def get_command_user(event: ApplicationCommandInteractionEvent) -> User | None:
    if event.data.type != ApplicationCommandType.USER:
        return None

    if (
        is_unset(event.data.target_id)
        or is_unset(event.data.resolved)
        or is_unset(event.data.resolved.users)
    ):
        return None

    return event.data.resolved.users.get(event.data.target_id)


CommandOption = Annotated[T, CommandOptionType()]


CommandMessage = Annotated[MessageGet, Depends(get_command_message)]
CommandUser = Annotated[User, Depends(get_command_user)]
