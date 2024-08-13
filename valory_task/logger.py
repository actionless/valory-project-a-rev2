from __future__ import annotations

import concurrent.futures
from logging import DEBUG, ERROR, INFO, WARNING
from typing import Any, Final

BOLD_START: Final = "\033[0;1m"
BOLD_RESET: Final = "\033[0m"
COLOR_RESET: Final = "\033[0;0m"


class ColorsHighlight:
    black = 8
    red = 9
    # green = 10
    yellow = 11
    # blue = 12
    # purple = 13
    cyan = 14
    # white = 15


def color_start(
        color_number: int,
) -> str:
    result = ""
    if color_number >= ColorsHighlight.black:
        result += "\033[0;1m"
        color_number -= ColorsHighlight.black
    result += f"\033[03{color_number}m"
    return result


def color_line(
        line: str, color_number: int, *, reset: bool = True,
) -> str:
    result = f"{color_start(color_number)}{line}"
    # reset font:
    if reset:
        result += COLOR_RESET
    return result


def bold_line(line: str) -> str:
    return f"{BOLD_START}{line}{BOLD_RESET}"


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
        AsyncPrint.print(msg % tuple(bold_line(arg) for arg in args))

    @classmethod
    def debug(cls, msg: str, *args: Any) -> None:
        if cls.level <= DEBUG:
            cls.log(f"{color_line('DEBUG', ColorsHighlight.black)} {msg}", *args)

    @classmethod
    def info(cls, msg: str, *args: Any) -> None:
        if cls.level <= INFO:
            cls.log(f"{color_line('INFO', ColorsHighlight.cyan)}  {msg}", *args)

    @classmethod
    def warning(cls, msg: str, *args: Any) -> None:
        if cls.level <= WARNING:
            cls.log(f"{color_line('WARN', ColorsHighlight.yellow)}  {msg}", *args)

    @classmethod
    def error(cls, msg: str, *args: Any) -> None:
        if cls.level <= ERROR:
            cls.log(f"{color_line('ERROR', ColorsHighlight.red)} {msg}", *args)


def debug(msg: str, *args: Any) -> None:
    AsyncLogging.debug(msg, *args)


def info(msg: str, *args: Any) -> None:
    AsyncLogging.info(msg, *args)


def warn(msg: str, *args: Any) -> None:
    AsyncLogging.warning(msg, *args)


def error(msg: str, *args: Any) -> None:
    AsyncLogging.error(msg, *args)
