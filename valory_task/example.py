from .agent import Agent, Message
from .logger import AsyncPrint
from .pipeline import Pipeline
from .trigger import TimeIntervalTrigger


class AgentInstance(Agent):

    MSG = "foobar"

    async def emit_message(self) -> Message:
        return self.MSG

    async def consume_message(self, message: Message) -> None:
        if self.MSG in message:
            # normal print() would also work,
            # but messages might get wrong order in compare to log messages:
            # print(f"got {message}!")  # noqa: T201,RUF100
            AsyncPrint.print(f"got {message}!")


def main() -> None:
    Pipeline([
        AgentInstance(trigger=TimeIntervalTrigger(interval_s=2)),
        AgentInstance(),
    ]).execute()


if __name__ == "__main__":
    main()
