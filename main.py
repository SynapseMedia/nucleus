import click, logging
import src.core.commands as commands
from src.core import set_level

__author__ = 'gmena'
if __name__ == '__main__':
    @click.command(cls=commands.CLI)
    @click.option('--debug/--no-debug', default=True)
    def cli(debug):
        # Overwrite log level
        log_level = logging.DEBUG if debug else logging.NOTSET
        click.echo(f"Debug mode is {'on' if debug else 'off'}")
        set_level(log_level)


    exit(0)
