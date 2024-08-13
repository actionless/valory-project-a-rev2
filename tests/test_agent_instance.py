"""Test module for Project A."""

import asyncio
from io import StringIO
from logging import WARNING
from typing import Awaitable, Callable
from unittest import TestCase, mock

from valory_task.example import AgentInstance
from valory_task.pipeline import Pipeline
from valory_task.trigger import Trigger


class InterceptedStdout:

    def __enter__(self) -> StringIO:
        out_file = StringIO()
        self.patches = (
            mock.patch("sys.stdout", new=out_file),
            mock.patch("valory_task.logger.AsyncLogging.level", new=WARNING),
        )
        for patch in self.patches:
            patch.start()
        return out_file

    def __exit__(self, *_exc_details: object) -> None:
        for patch in self.patches:
            patch.stop()


def handler_test_common(text: str) -> str:
    with InterceptedStdout() as out_file:
        asyncio.run(AgentInstance().consume_message(text))
    return out_file.getvalue().strip()


class AgentInstanceTestCase(TestCase):

    def test_handler_triggered(self) -> None:
        self.assertIn(
            "hello",
            handler_test_common("hello"),
            "should print if message contain `hello`",
        )

    def test_handler_skipped(self) -> None:
        self.assertEqual(
            "",
            handler_test_common("spam"),
            "shouldn't print if message doesn't contain `hello`",
        )

    def test_behaviour(self) -> None:
        test_result = asyncio.run(AgentInstance().emit_message())
        self.assertEqual(len(test_result.split(" ")), 2, "should be 2 words")

    def test_integration(self) -> None:
        with InterceptedStdout() as out_file:

            class TestTrigger(Trigger):
                async def run(  # noqa: PLR6301
                        self, callback: Callable[[], Awaitable[None]],
                ) -> None:
                    while not out_file.getvalue().strip():
                        await callback()

            Pipeline([
                AgentInstance(trigger=TestTrigger()),
                AgentInstance(),
            ]).execute()

        for line in out_file.getvalue().splitlines():
            self.assertIn("hello", line, "each printed line should contain `hello`")
