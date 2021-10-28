import os
import click
import resolvers
import asyncio
from src.sdk import subprocess, runtime

# Default - Refresh movies on each epoch?
REGEN_ORBITDB = os.environ.get("REGEN_ORBITDB", "False") == "True"
MIXED_RESOURCES = os.environ.get("MIXED_RESOURCES", "False") == "True"


@click.command()
@click.option("--regen", default=REGEN_ORBITDB)
@click.option("--mixed", default=MIXED_RESOURCES)
def expose(regen, mixed):
    """
    Publish production ready channel
    """
    # Add resolvers if not mixed allowed
    resolvers_names = (
            not mixed and list(map(runtime.resolvers_to_str, resolvers.load())) or None
    )

    # Start node subprocess migration
    asyncio.run(
        subprocess.call_orbit(
            resolvers=resolvers_names,  # Add resolvers if not mixed allowed
            regen=regen,  # Regen orbit directory
        )
    )
