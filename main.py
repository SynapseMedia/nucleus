import os, click, logging, resolvers, asyncio
import src.core.commands as commands
from src.core import helper
from src.core import logger, Log, set_level

__author__ = 'gmena'
if __name__ == '__main__':

    # Defaults

    REGEN_ORBITDB = os.environ.get('REGEN_ORBITDB', 'False') == 'True'
    MIXED_RESOURCES = os.environ.get('MIXED_RESOURCES', 'False') == 'True'


    @click.command(cls=commands.CLI)
    @click.option('--debug/--no-debug', default=True)
    def cli(debug):
        # Overwrite log level
        log_level = logging.DEBUG if debug else logging.NOTSET
        click.echo(f"Debug mode is {'on' if debug else 'off'}")
        set_level(log_level)


    empty_ = empty_cache or empty_tmp
    if REFRESH_IPFS or empty_:
        logger.info('\n')
        logger.info(f"{Log.WARNING}Starting ingestion to IPFS{Log.ENDC}")
        if FLUSH_CACHE_IPFS or empty_:
            helper.runtime.flush_ipfs(cache_db, temp_db)

        # Get stored movies data and process it
        migration_result = temp_db.movies.find({
            "updated": {'$exists': False}
        }, no_cursor_timeout=True).batch_size(1000)

        # Start IPFS ingestion
        helper.runtime.init_ingestion(
            cache_db, temp_db,
            migration_result
        )

    # Add resolvers if not mixed allowed
    resolvers_names = not MIXED_RESOURCES and list(map(
        helper.runtime.resolvers_to_str, resolvers.load()
    )) or None

    # Start node subprocess migration
    asyncio.run(helper.call_orbit_subprocess(
        resolvers=resolvers_names,  # Add resolvers if not mixed allowed
        regen=REGEN_ORBITDB,  # Regen orbit directory
    ))
    exit(0)
