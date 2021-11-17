import click
from src.sdk.scheme.validator import check
from src.sdk import cache, logger, exception, media
from src.sdk.constants import FLUSH_CACHE_IPFS, AUTO_PIN_FILES
from src.sdk.cache.pinata import check_pinata_status, pin_remote


def _pin_files():
    """
    Pin ingested file from cursor cache db
    :return:
    """
    logger.log.warning("Starting pinning to IPFS")
    entries, _ = cache.ingested()
    files_cid = map(lambda x: x["hash"], entries)
    media.ingest.pin_cid_list_remote(files_cid)
    entries.close()


@click.group("storage")
@click.pass_context
def storage(ctx):
    pass


@storage.command()
@click.option("--no-cache", default=FLUSH_CACHE_IPFS)
@click.option("--pin", default=AUTO_PIN_FILES)
@click.pass_context
def ingest(ctx, no_cache, pin):
    """
    Ingest media ready for production into IPFS
    """
    media.ingest.ipfs = media.ingest.start_node()  # Init ipfs node
    logger.log.warning("Starting ingestion to IPFS")
    if no_cache or cache.empty_tmp:  # Clean already ingested cursor
        cache.flush()

    # Total size of entries to fetch
    # Return available and not processed entries
    result, result_count = cache.pending()
    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    logger.log.notice(f"Ingesting {result_count} results")
    logger.log.info("\n")

    # Ingest from each row in tmp db the resources
    for current_movie in check(result):
        _id = current_movie.imdb_code  # Current id
        ingested_data = media.ingest.to_ipfs_from(current_movie)
        cache.set_ingested_with(_id, ingested_data)

    if pin:  # If allowed pin files
        _pin_files()

    result.close()


@storage.group('edge')
@click.pass_context
def edge(ctx):
    pass


@edge.command()
@click.pass_context
def status(ctx):
    media.ingest.ipfs = media.ingest.start_node()  # Init ipfs node
    edge_status = check_pinata_status()
    if edge_status:
        logger.log.success("Edge cache: Success")
    else:
        logger.log.error('Edge cache: Offline')


@edge.command()
@click.option("--cid", default=None)
@click.pass_context
def pinned(ctx, cid):
    media.ingest.ipfs = media.ingest.start_node()  # Init ipfs node
    logger.log.warning(f"Start pinning for cid: {cid}")
    edge_pinned = pin_remote(cid)
    logger.log.info(edge_pinned)

