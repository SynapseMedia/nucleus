import os
import logging
import rich  # type: ignore

from rich import *  # type: ignore
from rich.logging import RichHandler

# Get log level from env vars
LOG_LEVEL = os.environ.get("LOGLEVEL", "DEBUG")

# ref: https://rich.readthedocs.io/en/stable/console.html
console = rich.console.Console(record=True)
handler = RichHandler(
    rich_tracebacks=True,
    tracebacks_show_locals=True,
    console=console,
)


def factory(name: str, level: str = LOG_LEVEL):
    # create logger
    fmt = "%(message)s"
    logger = logging.getLogger(name)
    logging.basicConfig(
        level=level,
        encoding="utf-8",
        format=fmt,
        datefmt="[%X]",
        handlers=[handler],
    )

    return logger


# Default logging
api = factory("API")
cli = factory("CLI")

__all__ = (
    "api",
    "cli",
    "logging",
    "factory",
    "console",
)
