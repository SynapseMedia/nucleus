import click
import importlib

# Here we're doing an explicit listing of available sub-commands.
# But we could also gather this list automatically using any collection
# method we like, e.g. grepping source code files or some registration pattern
# like e.g. class decorator or a metaclass.
commands = ("resolve", "fetch", "ingest", "expose", "cache", "nft")


class CLI(click.MultiCommand):
    def list_commands(self, ctx):
        return commands

    def get_command(self, ctx, name):
        module = importlib.import_module("." + name, package=__package__)
        return getattr(module, name)
