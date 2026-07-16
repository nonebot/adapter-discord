import re
from typing import Annotated
from typing_extensions import NotRequired, Required, TypedDict

from nonebot.adapters.discord.api.types import UNSET
from nonebot.adapters.discord.api.validation import validate_outbound_value
from nonebot.adapters.discord.domains.interaction.write import (
    InteractionCallbackMessage,
)
from nonebot.adapters.discord.domains.message.write import MessageSend
from nonebot.adapters.discord.domains.webhook.write import ExecuteWebhookParams
from nonebot.adapters.discord.utils import reject_unset_values

from nonebot.compat import PYDANTIC_V2
from pydantic import ValidationError
import pytest


class NestedPayload(TypedDict, total=False):
    required: Required[int]
    optional: NotRequired[str | None]


class Payload(TypedDict, total=False):
    nested: Required[NestedPayload]
    values: NotRequired[list[int]]


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ({}, "Missing required Discord REST fields at $: ['nested']"),
        (
            {"nested": {}},
            "Missing required Discord REST fields at $.nested: ['required']",
        ),
        (
            {"nested": {"required": 1, "extra": 2}},
            "Unknown Discord REST fields at $.nested: ['extra']",
        ),
    ],
)
def test_validate_outbound_value_rejects_invalid_typed_dict_structure(
    value: object,
    message: str,
) -> None:
    with pytest.raises(TypeError, match=f"^{re.escape(message)}$"):
        validate_outbound_value(Payload, value)


def test_validate_outbound_value_returns_original_mapping() -> None:
    value: Payload = {"nested": {"required": 1}, "values": [2]}
    assert validate_outbound_value(Payload, value) is value


def test_validate_outbound_value_rejects_strict_bool_as_int() -> None:
    value = {"nested": {"required": True}}
    if PYDANTIC_V2:
        with pytest.raises(ValidationError):
            validate_outbound_value(Payload, value)
    else:
        assert validate_outbound_value(Payload, value) is value


@pytest.mark.parametrize(
    ("value", "path"),
    [
        ({"field": UNSET}, "$.field"),
        ({UNSET: 1}, "$[key=<UNSET>]"),
        ([UNSET], "$[0]"),
        ((1, UNSET), "$[1]"),
        ({"value", UNSET}, "$[1]"),
    ],
)
def test_reject_unset_values_reports_deterministic_path(
    value: object,
    path: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=re.escape(
            "REST request mappings must omit absent fields instead of using "
            f"UNSET at {path}"
        ),
    ):
        reject_unset_values(value)


@pytest.mark.skipif(not PYDANTIC_V2, reason="strict TypedDict validation needs v2")
@pytest.mark.parametrize(
    ("annotation", "value"),
    [
        (MessageSend, {"content": None}),
        (ExecuteWebhookParams, {"content": None}),
        (InteractionCallbackMessage, {"content": None}),
    ],
)
def test_omission_only_write_fields_reject_explicit_none(
    annotation: object,
    value: object,
) -> None:
    with pytest.raises(ValidationError):
        validate_outbound_value(annotation, value)


def test_annotated_required_wrapper_is_unwrapped() -> None:
    class AnnotatedPayload(TypedDict):
        value: Annotated[int, "metadata"]

    value: AnnotatedPayload = {"value": 1}
    assert validate_outbound_value(AnnotatedPayload, value) is value
