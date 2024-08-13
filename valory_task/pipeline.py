from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from .generate_name import UniqueNames
from .logger import info

if TYPE_CHECKING:
    from .agent import Agent


class Pipeline:

    agents: list[Agent]
    idx: str

    def __init__(self, agents: list[Agent]) -> None:
        self.agents = agents
        self.idx = UniqueNames.generate()
        for agent_idx in range(len(agents)):
            agent = self.agents[agent_idx]
            agent.register(UniqueNames.generate())
            info(
                "[pipeline %s] registered %s agent %s",
                self.idx, agent.__class__.__name__, agent.idx,
            )
            if agent_idx > 0:
                self.agents[agent_idx - 1].register_output(agent)

    async def run(self) -> None:
        await asyncio.gather(
            *(agent.trigger.run(agent.do_emit) for agent in self.agents if agent.trigger),
        )

    def execute(self) -> None:
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            info("Exiting...")
