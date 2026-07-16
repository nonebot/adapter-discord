from collections.abc import Callable, Mapping, Set as AbstractSet
from dataclasses import dataclass
from functools import cache, lru_cache, wraps
import inspect
import types
from typing import Annotated, Any, TypeVar, Union, get_args, get_origin
from typing_extensions import NotRequired, Required, is_typeddict
import warnings

from nonebot.compat import PYDANTIC_V2, type_validate_python
from pydantic import BaseModel, ValidationError

from ..utils import reject_unset_values

if PYDANTIC_V2:
    from pydantic import TypeAdapter

_PAIR_ARGUMENT_COUNT = 2
T = TypeVar("T")


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
        selected = sum(arguments.get(field) is not None for field in rule.fields)
        if selected > 1:
            raise ValueError(rule.message)
        return
    if isinstance(rule, ForbidIfEquals):
        if (
            arguments.get(rule.when_field) == rule.equals
            and arguments.get(rule.field) is not None
        ):
            raise ValueError(rule.message)
        return
    if isinstance(rule, RequireIfEquals):
        if (
            arguments.get(rule.when_field) == rule.equals
            and arguments.get(rule.field) is None
        ):
            raise ValueError(rule.message)
        return
    if (
        isinstance(rule, RequireIfNotEquals)
        and arguments.get(rule.when_field) != rule.equals
        and arguments.get(rule.field) is None
    ):
        raise ValueError(rule.message)


def _validate_cross_rules(
    *,
    bound: inspect.BoundArguments,
    cross_rules: tuple[CrossRule, ...],
) -> None:
    arguments = dict(bound.arguments)
    packed_fields = arguments.get("fields")
    if isinstance(packed_fields, Mapping):
        arguments.update(packed_fields)
    for rule in cross_rules:
        _validate_cross_rule(arguments=arguments, rule=rule)


def _unwrap_outbound_annotation(annotation: object) -> object:
    while get_origin(annotation) in (Required, NotRequired, Annotated):
        annotation = get_args(annotation)[0]
    return annotation


def _stable_key(value: object) -> tuple[str, str, str]:
    value_type = type(value)
    return (value_type.__module__, value_type.__qualname__, repr(value))


def _validate_outbound_structure(  # noqa: C901, PLR0911, PLR0912
    annotation: object,
    value: object,
    path: str,
) -> None:
    annotation = _unwrap_outbound_annotation(annotation)
    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin in (types.UnionType, Union):
        errors: list[TypeError] = []
        for candidate in args:
            unwrapped_candidate = _unwrap_outbound_annotation(candidate)
            candidate_origin = get_origin(unwrapped_candidate)
            matches = (
                (is_typeddict(unwrapped_candidate) and isinstance(value, Mapping))
                or (candidate_origin in (dict, Mapping) and isinstance(value, Mapping))
                or (candidate_origin is list and isinstance(value, list))
                or (candidate_origin is tuple and isinstance(value, tuple))
                or (
                    candidate_origin in (set, frozenset, AbstractSet)
                    and isinstance(value, (set, frozenset))
                )
                or (
                    candidate_origin is None
                    and isinstance(unwrapped_candidate, type)
                    and issubclass(unwrapped_candidate, BaseModel)
                    and isinstance(value, (unwrapped_candidate, Mapping))
                )
                or (unwrapped_candidate is type(None) and value is None)
            )
            if not matches:
                continue
            try:
                _validate_outbound_structure(unwrapped_candidate, value, path)
            except TypeError as exception:
                errors.append(exception)
            else:
                return
        if errors:
            raise errors[0]
        return

    if is_typeddict(annotation):
        if not isinstance(value, Mapping):
            return
        annotations = annotation.__annotations__
        required_keys = getattr(annotation, "__required_keys__", frozenset())
        missing = [
            key for key in annotations if key in required_keys and key not in value
        ]
        if missing:
            msg = f"Missing required Discord REST fields at {path}: {missing!r}"
            raise TypeError(msg)
        unknown = sorted(
            (key for key in value if key not in annotations), key=_stable_key
        )
        if unknown:
            msg = f"Unknown Discord REST fields at {path}: {unknown!r}"
            raise TypeError(msg)
        for key, field_annotation in annotations.items():
            if key in value:
                _validate_outbound_structure(
                    field_annotation,
                    value[key],
                    f"{path}.{key}" if key.isidentifier() else f"{path}[{key!r}]",
                )
        return

    if (
        origin is None
        and isinstance(annotation, type)
        and issubclass(annotation, BaseModel)
    ):
        if isinstance(value, Mapping):
            qualified_name = f"{annotation.__module__}.{annotation.__qualname__}"
            msg = f"Expected Discord model {qualified_name} at {path}"
            raise TypeError(msg)
        return

    if origin is list and isinstance(value, list):
        if args:
            for index, item in enumerate(value):
                _validate_outbound_structure(args[0], item, f"{path}[{index}]")
        return
    if origin is tuple and isinstance(value, tuple):
        if len(args) == _PAIR_ARGUMENT_COUNT and args[1] is Ellipsis:
            for index, item in enumerate(value):
                _validate_outbound_structure(args[0], item, f"{path}[{index}]")
        else:
            for index, (item, item_annotation) in enumerate(
                zip(value, args, strict=False)
            ):
                _validate_outbound_structure(item_annotation, item, f"{path}[{index}]")
        return
    if origin in (set, frozenset, AbstractSet) and isinstance(value, (set, frozenset)):
        if args:
            for index, item in enumerate(sorted(value, key=_stable_key)):
                _validate_outbound_structure(args[0], item, f"{path}[{index}]")
        return
    if (
        origin in (dict, Mapping)
        and isinstance(value, Mapping)
        and len(args) == _PAIR_ARGUMENT_COUNT
    ):
        for key, item in sorted(value.items(), key=lambda pair: _stable_key(pair[0])):
            item_path = (
                f"{path}.{key}"
                if isinstance(key, str) and key.isidentifier()
                else f"{path}[{key!r}]"
            )
            _validate_outbound_structure(args[1], item, item_path)


@cache
def _outbound_adapter(annotation: object) -> Any:  # noqa: ANN401
    return TypeAdapter(annotation)


@lru_cache(maxsize=1)
def _warn_pydantic_v1_outbound_validation() -> None:
    warnings.warn(
        "Strict Discord REST outbound value validation is disabled under "
        "Pydantic v1; upgrade to Pydantic v2 to enable it.",
        RuntimeWarning,
        stacklevel=3,
    )


def validate_outbound_value(annotation: object, value: T) -> T:
    """Validate outbound structure without replacing the caller's value."""
    reject_unset_values(value)
    _validate_outbound_structure(annotation, value, "$")
    if PYDANTIC_V2:
        _outbound_adapter(annotation).validate_python(value, strict=True)
    else:
        _warn_pydantic_v1_outbound_validation()
    return value


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
    "validate_outbound_value",
)
