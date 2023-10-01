import inspect
from typing import Any, Optional, Tuple, Type, TypeVar
from typing_extensions import Annotated

from nonebot.dependencies import Param
from nonebot.params import Depends

from pydantic.fields import Required
from pydantic.typing import get_args, get_origin

from ..api import (
    ApplicationCommandOptionType,
    ApplicationCommandType,
    MessageGet,
    Snowflake,
    User,
)
from ..event import ApplicationCommandInteractionEvent

T = TypeVar("T")

type_str_mapping = {
    ApplicationCommandOptionType.USER: "users",
    ApplicationCommandOptionType.CHANNEL: "channels",
    ApplicationCommandOptionType.ROLE: "roles",
    ApplicationCommandOptionType.ATTACHMENT: "attachments",
}


class CommandOptionType:
    def __init__(self, key: Optional[str] = None) -> None:
        self.key = key

    def __repr__(self) -> str:
        return f"ACommandOption(key={self.key!r})"


class OptionParam(Param):
    def __repr__(self) -> str:
        return f"OptionParam(key={self.extra['key']!r})"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["OptionParam"]:
        if isinstance(param.default, CommandOptionType):
            return cls(Required, key=param.default.key or param.name, validate=True)
        elif get_origin(param.annotation) is Annotated:
            for arg in get_args(param.annotation):
                if isinstance(arg, CommandOptionType):
                    return cls(Required, key=arg.key or param.name, validate=True)

    async def _solve(
        self, event: ApplicationCommandInteractionEvent, **kwargs: Any
    ) -> Any:
        if event.data.options:
            options = event.data.options
            if (
                options
                and options[0].type == ApplicationCommandOptionType.SUB_COMMAND_GROUP
            ):
                options = options[0].options
            if options and options[0].type == ApplicationCommandOptionType.SUB_COMMAND:
                options = options[0].options
            if options:
                for option in options:
                    if option.name == self.extra["key"]:
                        if (
                            option.type
                            in (
                                ApplicationCommandOptionType.USER,
                                ApplicationCommandOptionType.CHANNEL,
                                ApplicationCommandOptionType.ROLE,
                                ApplicationCommandOptionType.ATTACHMENT,
                            )
                            and event.data.resolved
                            and (
                                data := getattr(
                                    event.data.resolved, type_str_mapping[option.type]
                                )
                            )
                        ):
                            return data[Snowflake(option.value)]  # type: ignore
                        elif (
                            option.type == ApplicationCommandOptionType.MENTIONABLE
                            and event.data.resolved
                            and event.data.resolved.users
                        ):
                            sid = Snowflake(option.value)  # type: ignore
                            return (
                                event.data.resolved.users.get(sid),
                                (
                                    event.data.resolved.members.get(sid)
                                    if event.data.resolved.members
                                    else None
                                ),
                            )
                        elif option.type in (
                            ApplicationCommandOptionType.INTEGER,
                            ApplicationCommandOptionType.STRING,
                            ApplicationCommandOptionType.NUMBER,
                            ApplicationCommandOptionType.BOOLEAN,
                        ):
                            return option.value
        return None


def get_command_message(event: ApplicationCommandInteractionEvent):
    if (
        event.data.type == ApplicationCommandType.MESSAGE
        and event.data.target_id
        and event.data.resolved
        and event.data.resolved.messages
    ):
        return event.data.resolved.messages.get(event.data.target_id)


def get_command_user(event: ApplicationCommandInteractionEvent):
    if (
        event.data.type == ApplicationCommandType.USER
        and event.data.target_id
        and event.data.resolved
        and event.data.resolved.users
    ):
        return event.data.resolved.users.get(event.data.target_id)


CommandOption = Annotated[T, CommandOptionType()]


CommandMessage = Annotated[MessageGet, Depends(get_command_message)]
CommandUser = Annotated[User, Depends(get_command_user)]
