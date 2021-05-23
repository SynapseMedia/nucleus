from collections import OrderedDict
import importlib
import click

# Here we're doing an explicit listing of available sub-commands.
# But we could also gather this list automatically using any collection
# method we like, e.g. grepping source code files or some registration pattern
# like e.g. class decorator or a metaclass.
commands = OrderedDict([
    ('resolve', dict(
        module='resolve', function='resolve',
        description='Run resolvers to get metadata and store it in `tmp db`'
    )),
    ('fetch', dict(
        module='fetch', function='fetch',
        description='Fetch media from source stores in `tmp db` and copy them to `raw`'
    )),
    ('ingest', dict(
        module='ingest', function='ingest',
        description='Add media ready for prod into IPFS'
    )),
    ('cache', dict(
        module='cache', function='cache',
        description='Clean cache and storage'
    ))
])


class CLI(click.MultiCommand):

    def list_commands(self, ctx):
        return list(commands)

    def get_command(self, ctx, name):
        module = importlib.import_module('commands.' + commands[name]['module'])
        return getattr(module, commands[name]['function'])
