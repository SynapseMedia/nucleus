import click
import collectors
import asyncio
from src.sdk import subprocess
from src.sdk.constants import REGEN_ORBITDB, MIXED_RESOURCES
from src.sdk import runtime


@click.command()
@click.option("--regen", default=REGEN_ORBITDB)
@click.option("--mixed", default=MIXED_RESOURCES)
def expose(regen, mixed):
    """Publish production ready channel"""
    # Add resolvers if not mixed allowed
    resolvers_names = (
        not mixed and list(map(runtime.resolvers_to_str, collectors.load())) or None
    )

    # Start node subprocess migration
    asyncio.run(
        subprocess.call_orbit(
            resolvers=resolvers_names,  # Add resolvers if not mixed allowed
            recreate=regen,  # Regen orbit directory
        )
    )
