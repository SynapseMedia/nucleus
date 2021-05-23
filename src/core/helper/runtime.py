from src.core import helper
from src.core import Log, logger
from pymongo.errors import BulkWriteError
import src.core.scheme as scheme
import asyncio
import typing


async def call_orbit_subprocess(resolvers=None, regen=False):
    """
    Spawn nodejs subprocess
    :param resolvers: List of loaded resolvers
    :param regen: Regenerate db
    """
    resolvers = resolvers or []
    is_mixed_migration = len(resolvers) > 0

    # Formulate params
    regen_param = regen and '-g' or ''
    command = f"npm run migrate -- {regen_param}"

    # If mixed sources run each process to generate DB
    # else run all in one process and ingest all in same DB
    resolvers_call = is_mixed_migration and [
        helper.subprocess.run(
            f"{command} --key={r} --source={r}"
        ) for r in resolvers
    ] or [helper.subprocess.run(command)]

    await asyncio.gather(*resolvers_call)


def rewrite_entries(db, data):
    """
    Just remove old data and replace it with new data
    :param db:
    :param data:
    """
    try:
        db.movies.delete_many({})  # Clean all
        db.movies.insert_many(data)
    except BulkWriteError:
        pass


def flush_ipfs(cursor_db, tmp_db):
    """
    Reset old entries and restore
    available entries to process in tmp_db
    :param cursor_db:
    :param tmp_db:
    :return:
    """

    cursor_db.movies.delete_many({})
    tmp_db.movies.update_many(
        {"updated": True},
        {'$unset': {"updated": None}}
    )


def resolvers_to_str(resolver) -> str:
    """
    Get names from resolvers
    :param resolver:
    :return:
    """
    return str(resolver())


def results_generator(resolver) -> typing.Generator:
    """
    Dummy resolver generator call
    :param resolver
    :returns: Iterable result
    """
    resolver = resolver()  # Init class
    logger.info(f"{Log.WARNING}Generating migrations from {resolver}{Log.ENDC}")
    return resolver(scheme)  # Call class and start migration
