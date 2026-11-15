import re
from typing import Annotated, cast
from typing_extensions import NotRequired, Required, TypedDict

from nonebot.adapters.discord.api.types import UNSET
from nonebot.adapters.discord.api.validation import validate_outbound_value
from nonebot.adapters.discord.domains.interaction.write import (
    InteractionCallbackMessage,
)
from nonebot.adapters.discord.domains.message.write import MessageSend
from nonebot.adapters.discord.domains.models import File, MessageReference
from nonebot.adapters.discord.domains.webhook.write import ExecuteWebhookParams
from nonebot.adapters.discord.protocol import Snowflake
from nonebot.adapters.discord.utils import reject_unset_values
from tests.fake.doubles import DummyAdapter, DummyBot

from pydantic import ValidationError
import pytest


class NestedPayload(TypedDict, total=False):
    required: Required[int]
    optional: NotRequired[str | None]


class Payload(TypedDict, total=False):
    nested: Required[NestedPayload]
    values: NotRequired[list[int]]


@pytest.mark.parametrize(
    ("value", "location", "error_type"),
    [
        ({}, ("nested",), "missing"),
        ({"nested": {}}, ("nested", "required"), "missing"),
        (
            {"nested": {"required": 1, "extra": 2}},
            ("nested", "extra"),
            "extra_forbidden",
        ),
    ],
)
def test_validate_outbound_value_rejects_invalid_typed_dict_structure(
    value: object,
    location: tuple[str, ...],
    error_type: str,
) -> None:
    with pytest.raises(ValidationError) as error:
        validate_outbound_value(Payload, value)

    assert [(item["loc"], item["type"]) for item in error.value.errors()] == [
        (location, error_type)
    ]


def test_validate_outbound_value_returns_original_mapping() -> None:
    file = File(filename="message.txt", content=b"content")
    reference = MessageReference(message_id=Snowflake(1))
    value: MessageSend = {"files": [file], "message_reference": reference}
    assert validate_outbound_value(MessageSend, value) is value
    assert value["files"][0] is file
    assert value["message_reference"] is reference


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "fields",
    [
        {"files": [{"filename": "message.txt", "content": b"content"}]},
        {"message_reference": {"message_id": 1}},
    ],
)
async def test_message_endpoint_requires_model_instances(
    fields: dict[str, object],
) -> None:
    adapter = DummyAdapter()
    bot = DummyBot(adapter)
    request = cast("MessageSend", {"content": "message", **fields})

    with pytest.raises(TypeError, match="Expected Discord model"):
        await adapter._api_create_message(bot, channel_id=1, **request)  # noqa: SLF001

    assert adapter.request_calls == 0


def test_validate_outbound_value_rejects_strict_bool_as_int() -> None:
    value = {"nested": {"required": True}}
    with pytest.raises(ValidationError):
        validate_outbound_value(Payload, value)


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
