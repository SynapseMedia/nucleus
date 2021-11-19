import click
import resolvers
import asyncio
from src.sdk import subprocess, runtime
from src.sdk.constants import REGEN_ORBITDB, MIXED_RESOURCES


@click.command()
@click.option("--regen", default=REGEN_ORBITDB)
@click.option("--mixed", default=MIXED_RESOURCES)
def expose(regen, mixed):
    """Publish production ready channel"""
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
