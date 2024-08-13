from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Generator

from .logger import info


class Trigger(ABC):
    agent_idx: str | None = None

    @abstractmethod
    async def run(self, callback: Callable[[], Awaitable[None]]) -> Generator[None, None, None]:
        pass

    def register_agent(self, agent_idx: str) -> None:
        self.agent_idx = agent_idx
        info("[agent %s] registered %s trigger", self.agent_idx, self)


class TimeIntervalTrigger(Trigger):

    def __init__(self, interval_s: float) -> None:
        self.interval_s = interval_s

    async def run(self, callback: Callable[[], Awaitable[None]]) -> Generator[None, None, None]:
        while True:
            info("[agent %s] timer tick", self.agent_idx)
            await callback()
            await asyncio.sleep(self.interval_s)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(interval_s={self.interval_s})>"
