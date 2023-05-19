import logging
import os

import rich
from rich.logging import RichHandler

# Get log level from env vars
LOG_LEVEL = os.environ.get('LOGLEVEL', 'DEBUG')


# ref: https://rich.readthedocs.io/en/stable/console.html
console = rich.console.Console(record=True)
handler = RichHandler(
    rich_tracebacks=False,
    tracebacks_show_locals=False,
    console=console,
)


def factory(name: str, level: str = LOG_LEVEL):
    # create logger
    fmt = '%(message)s'
    formatter = logging.Formatter(fmt)
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


# Default logging
core = factory('CORE')
sdk = factory('SDK')

__all__ = (
    'core',
    'sdk',
    'logging',
    'factory',
    'console',
)
