from pathlib import Path

import nonebot.adapters
from tests.fake.doubles import DummyAdapter, DummyBot

from nonebug import NONEBOT_INIT_KWARGS, NONEBOT_START_LIFESPAN
import pytest

nonebot.adapters.__path__.append(
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "nonebot.drivers.none",
    }
    config.stash[NONEBOT_START_LIFESPAN] = False


@pytest.fixture
def dummy_adapter() -> DummyAdapter:
    return DummyAdapter()


@pytest.fixture
def dummy_adapter_list_response() -> DummyAdapter:
    return DummyAdapter(content=b"[]")


@pytest.fixture
def dummy_bot() -> DummyBot:
    return DummyBot()
