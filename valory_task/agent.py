from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from .logger import debug, error, info, warn

if TYPE_CHECKING:
    from .trigger import Trigger

Message = TypeVar("Message")


class Agent(Protocol[Message]):

    trigger: Trigger | None
    emit_to: Agent[Message] | None = None
    idx: str | None = None

    def __init__(self, trigger: Trigger | None = None) -> None:
        self.trigger = trigger

    async def consume_message(self, message: Message) -> None:
        raise NotImplementedError

    async def emit_message(self) -> Message:
        raise NotImplementedError

    def register(self, idx: str) -> None:
        self.idx = idx
        if self.trigger:
            self.trigger.register_agent(idx)
        debug(
            "[agent %s] registered%s",
            self.idx,
            f" with trigger {self.trigger}" if self.trigger else "",
        )

    def register_output(self, agent: Agent[Message]) -> None:
        self.emit_to = agent
        info("[agent %s] registered output to %s", self.idx, agent.idx)

    async def error_handler(self, exc: Exception | None = None, details: str | None = None) -> None:
        error(
            "[agent %s] error happened %s%s",
            self.idx,
            details or "",
            f": {exc.__class__.__name__} {exc.args}" if exc else "",
        )

    async def do_consume(self, message: Message) -> None:
        info("[agent %s] consuming message `%s`...", self.idx, message)
        try:
            await self.consume_message(message)
        except Exception as exc:
            await self.error_handler(exc, "while consuming a message")

    async def do_emit(self) -> None:
        if not self.emit_to:
            warn("[agent %s] no consumer registered for the agent! Can't emit.")
            return
        try:
            message: Message = await self.emit_message()
        except Exception as exc:
            await self.error_handler(exc, "while emitting a message")
        info("[agent %s] emitting to %s message `%s`...", self.idx, self.emit_to.idx, message)
        await self.emit_to.do_consume(message)
