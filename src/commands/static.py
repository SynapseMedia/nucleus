import sys

import click
from src.sdk.scheme.validator import check
from src.sdk import cache, logger
from src.sdk.exec import static as statics


@click.group("static")
def static():
    """Statics toolkit"""
    pass


@static.group("images")
def images():
    """Image toolkit"""
    pass


@images.group("ingest")
def ingest():
    pass


@ingest.command()
def cached():
    """
    Convert/Process image static defined in cached metadata \n
    Note: Please ensure that metadata exists in local temp db before run this command.
    eg. Resolve -> Static
    """
    # Get stored movies in tmp_db and process it
    # Total size of entries to fetch
    result, result_count = cache.manager.safe_retrieve()
    logger.log.warning(f"Processing {result_count} results")

    # Fetch from each row in tmp db the resources
    for current_movie in check(result):
        statics.boot(current_movie)
        sys.stdout.write("\n")

    # Close current tmp cache db
    result.close()
