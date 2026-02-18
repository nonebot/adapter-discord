from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
import inspect
from typing import Annotated, Any, get_args, get_origin

from nonebot.compat import type_validate_python
from pydantic import ValidationError


class Range:
    def __init__(
        self,
        *,
        message: str,
        ge: int | None = None,
        le: int | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> None:
        self.message = message
        self.ge = ge
        self.le = le
        self.min_length = min_length
        self.max_length = max_length


@dataclass(frozen=True)
class AtMostOne:
    fields: tuple[str, ...]
    message: str


@dataclass(frozen=True)
class ForbidIfEquals:
    field: str
    when_field: str
    equals: object
    message: str


@dataclass(frozen=True)
class RequireIfEquals:
    field: str
    when_field: str
    equals: object
    message: str


@dataclass(frozen=True)
class RequireIfNotEquals:
    field: str
    when_field: str
    equals: object
    message: str


CrossRule = AtMostOne | ForbidIfEquals | RequireIfEquals | RequireIfNotEquals


def _is_annotated_constraint(annotation: object) -> bool:
    if get_origin(annotation) is not Annotated:
        return False
    metadata = get_args(annotation)[1:]
    return any(isinstance(item, Range) for item in metadata)


def _collect_annotated_validators(
    signature: inspect.Signature,
) -> dict[str, tuple[object, list[Range]]]:
    validators: dict[str, tuple[object, list[Range]]] = {}
    for name, parameter in signature.parameters.items():
        annotation = parameter.annotation
        if not _is_annotated_constraint(annotation):
            continue
        args = get_args(annotation)
        base_type = args[0]
        ranges = [item for item in args[1:] if isinstance(item, Range)]
        validators[name] = (base_type, ranges)
    return validators


def _validate_range(value: object, range_meta: Range) -> None:
    if value is None:
        return

    msg = range_meta.message

    if range_meta.min_length is not None or range_meta.max_length is not None:
        if not isinstance(value, (str, bytes, list, tuple, dict, set)):
            raise ValueError(msg)
        size = len(value)
        if range_meta.min_length is not None and size < range_meta.min_length:
            raise ValueError(msg)
        if range_meta.max_length is not None and size > range_meta.max_length:
            raise ValueError(msg)

    if range_meta.ge is not None or range_meta.le is not None:
        if not isinstance(value, (int, float)):
            raise ValueError(msg)
        if range_meta.ge is not None and value < range_meta.ge:
            raise ValueError(msg)
        if range_meta.le is not None and value > range_meta.le:
            raise ValueError(msg)


def _validate_annotated_argument(
    *,
    value: object,
    base_type: Any,  # noqa: ANN401
    ranges: list[Range],
) -> None:
    try:
        converted = type_validate_python(base_type, value)
    except ValidationError as exception:
        msg = ranges[0].message
        raise ValueError(msg) from exception

    for range_meta in ranges:
        _validate_range(converted, range_meta)


def _validate_annotated_bound(
    *,
    bound: inspect.BoundArguments,
    validators: dict[str, tuple[object, list[Range]]],
) -> None:
    for name, (base_type, ranges) in validators.items():
        _validate_annotated_argument(
            value=bound.arguments[name],
            base_type=base_type,
            ranges=ranges,
        )


def _validate_cross_rule(*, arguments: dict[str, object], rule: CrossRule) -> None:
    if isinstance(rule, AtMostOne):
        selected = sum(arguments[field] is not None for field in rule.fields)
        if selected > 1:
            raise ValueError(rule.message)
        return
    if isinstance(rule, ForbidIfEquals):
        if (
            arguments[rule.when_field] == rule.equals
            and arguments[rule.field] is not None
        ):
            raise ValueError(rule.message)
        return
    if isinstance(rule, RequireIfEquals):
        if arguments[rule.when_field] == rule.equals and arguments[rule.field] is None:
            raise ValueError(rule.message)
        return
    if (
        isinstance(rule, RequireIfNotEquals)
        and arguments[rule.when_field] != rule.equals
        and arguments[rule.field] is None
    ):
        raise ValueError(rule.message)


def _validate_cross_rules(
    *,
    bound: inspect.BoundArguments,
    cross_rules: tuple[CrossRule, ...],
) -> None:
    arguments = dict(bound.arguments)
    for rule in cross_rules:
        _validate_cross_rule(arguments=arguments, rule=rule)


def validate(
    func: Callable[..., Any] | None = None,
    *,
    cross_rules: tuple[CrossRule, ...] = (),
) -> Callable[..., Any]:
    if func is None:

        def decorator(inner: Callable[..., Any]) -> Callable[..., Any]:
            return validate(inner, cross_rules=cross_rules)

        return decorator

    signature = inspect.signature(func)
    validators = _collect_annotated_validators(signature)

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            _validate_annotated_bound(bound=bound, validators=validators)
            _validate_cross_rules(bound=bound, cross_rules=cross_rules)
            return await func(*args, **kwargs)

        return async_wrapper

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        _validate_annotated_bound(bound=bound, validators=validators)
        _validate_cross_rules(bound=bound, cross_rules=cross_rules)
        return func(*args, **kwargs)

    return wrapper


__all__ = (
    "AtMostOne",
    "CrossRule",
    "ForbidIfEquals",
    "Range",
    "RequireIfEquals",
    "RequireIfNotEquals",
    "validate",
)
