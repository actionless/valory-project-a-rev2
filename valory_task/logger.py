from __future__ import annotations

import concurrent.futures
from logging import DEBUG, ERROR, INFO, WARNING
from typing import Any


class AsyncPrint:
    executor: concurrent.futures.ThreadPoolExecutor | None = None

    @classmethod
    def get_executor(cls) -> concurrent.futures.ThreadPoolExecutor:
        if cls.executor is None:
            cls.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        return cls.executor

    @staticmethod
    def do_print(msg: str) -> None:
        print(msg)  # noqa: T201

    @classmethod
    def print(cls, msg: str) -> None:
        cls.get_executor().submit(cls.do_print, msg)


class AsyncLogging:
    level: int = INFO

    @staticmethod
    def log(msg: str, *args: Any) -> None:
        AsyncPrint.print(msg % args)

    @classmethod
    def debug(cls, msg: str, *args: Any) -> None:
        if cls.level <= DEBUG:
            cls.log(f"DEBUG {msg}", *args)

    @classmethod
    def info(cls, msg: str, *args: Any) -> None:
        if cls.level <= INFO:
            cls.log(f"INFO  {msg}", *args)

    @classmethod
    def warning(cls, msg: str, *args: Any) -> None:
        if cls.level <= WARNING:
            cls.log(f"WARN  {msg}", *args)

    @classmethod
    def error(cls, msg: str, *args: Any) -> None:
        if cls.level <= ERROR:
            cls.log(f"ERROR {msg}", *args)


def debug(msg: str, *args: Any) -> None:
    AsyncLogging.debug(msg, *args)


def info(msg: str, *args: Any) -> None:
    AsyncLogging.info(msg, *args)


def warn(msg: str, *args: Any) -> None:
    AsyncLogging.warning(msg, *args)


def error(msg: str, *args: Any) -> None:
    AsyncLogging.error(msg, *args)
