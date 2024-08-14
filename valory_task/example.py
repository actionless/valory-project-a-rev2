import random

from .agent import Agent
from .logger import AsyncPrint
from .pipeline import Pipeline
from .trigger import TimeIntervalTrigger

Message = str


class AgentInstance(Agent[Message]):

    DICTIONARY = (
        "hello",
        "sun",
        "world",
        "space",
        "moon",
        "crypto",
        "sky",
        "ocean",
        "universe",
        "human",
    )

    WAIT_FOR = "hello"

    async def emit_message(self) -> Message:
        # `nosec` because random is used not for cryptography here:
        return " ".join(
            random.choice(self.DICTIONARY) for _ in range(2)  # noqa:S311
        )

    async def consume_message(self, message: Message) -> None:
        if self.WAIT_FOR in message:
            # normal print() would also work,
            # but messages might get wrong order in compare to log messages:
            # print(message)  # noqa: T201,RUF100
            AsyncPrint.print(message)


def main() -> None:
    Pipeline([
        AgentInstance(trigger=TimeIntervalTrigger(interval_s=2)),
        AgentInstance(),
    ]).execute()


if __name__ == "__main__":
    main()
