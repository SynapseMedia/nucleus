__copyright__ = "Copyright (c) 2020 ZorrillosDev"
__version__ = "0.2.0"
__license__ = "AGPL V3"

import click
import logging

import src.commands as commands
from src.sdk import logger

__author__ = 'gmena'
if __name__ == '__main__':
    @click.command(cls=commands.CLI)
    @click.option('--debug/--no-debug', default=True)
    def cli(debug):
        # Overwrite log level
        log_level = logging.DEBUG if debug else logging.NOTSET
        logger.log.warning(f"Debug mode is {'on' if debug else 'off'}")
        logger.log.setLevel(log_level)

    cli()
    exit(0)
