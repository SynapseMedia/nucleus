import os, click, resolvers, asyncio
from src.core import helper

# Default - Refresh movies on each epoch?
REGEN_ORBITDB = os.environ.get('REGEN_ORBITDB', 'False') == 'True'
MIXED_RESOURCES = os.environ.get('MIXED_RESOURCES', 'False') == 'True'


@click.command()
@click.option('--regen', default=REGEN_ORBITDB)
@click.option('--mixed', default=MIXED_RESOURCES)
def resolve(regen, mixed):
    """
    Run resolvers to get metadata and store it in `tmp db`
    :param regen: Recreate orbit-db
    :param mixed: Mix resources or create a new db for each
    :return:
    """
    # Add resolvers if not mixed allowed
    resolvers_names = not mixed and list(map(
        helper.runtime.resolvers_to_str, resolvers.load()
    )) or None

    # Start node subprocess migration
    asyncio.run(helper.subprocess.call_orbit(
        resolvers=resolvers_names,  # Add resolvers if not mixed allowed
        regen=regen,  # Regen orbit directory
    ))
