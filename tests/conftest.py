from pathlib import Path

import nonebot.adapters

from nonebug import NONEBOT_INIT_KWARGS, NONEBOT_START_LIFESPAN
import pytest

nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "nonebot.drivers.none",
    }
    config.stash[NONEBOT_START_LIFESPAN] = False
