import sys

import click
from src.sdk.scheme.validator import check
from src.sdk.exception import InvalidCID
from src.sdk.constants import FLUSH_CACHE_IPFS
from src.sdk import cache, logger, exception, media, scheme
from src.sdk.scheme.definition.movies import MovieScheme


@click.group("storage")
def storage():
    """Storage toolkit"""
    pass


@storage.command()
@click.option("--no-cache", default=FLUSH_CACHE_IPFS, is_flag=True)
def ingest(no_cache):
    """
    Ingest media ready for production into IPFS. \n
    Note: Please ensure that binaries is pre-processed before run this command.
    eg. Resolve meta -> Transcode media -> Generate NFT metadata -> ingest
    """
    logger.log.warning("Starting ingestion to IPFS")
    if no_cache or cache.empty_tmp:  # Clean already ingested cursor
        cache.manager.flush()

    # Total size of entries to fetch
    # Return available and not processed entries
    result, result_count = cache.ingest.pending()
    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    logger.log.notice(f"Ingesting {result_count} results")
    sys.stdout.write("\n")

    # Ingest from each row in tmp db the resources
    for current_movie in check(result):
        _id = current_movie.imdb_code  # Current id
        # 1 - Add ingested directory hash to movie
        # 2 - Fit scheme from dag resources paths
        # 3 - Store in cursor db current processed movie
        current_movie.hash = media.storage.ingest.to_ipfs(current_movie)
        current_movie.resource = scheme.util.fit_resources_from_dag(current_movie.hash)
        cache.ingest.freeze(_id, MovieScheme().dump(current_movie))
        logger.log.success(f"Done {current_movie.imdb_code}\n")


@storage.group("edge")
def edge():
    """Edge cache"""
    pass


@edge.command()
def status():
    """Check for edge cache status"""
    is_edge_active = media.storage.remote.check_status()
    if is_edge_active:
        logger.log.success("Edge cache: Success")
        exit(0)  # Success termination
    logger.log.error("Edge cache: Offline")


@edge.group("pin")
@click.option("--remote", default=True, is_flag=True)
@click.pass_context
def pin(ctx, remote):
    """Pin cid tools"""
    ctx.ensure_object(dict)
    ctx.obj["remote"] = remote
    pass


@pin.command()
@click.option("--cid", default=None)
@click.pass_context
def single(ctx, cid):
    """Pin arbitrary cid"""
    if not cid:
        raise InvalidCID()

    logger.log.warning(f"Start pinning for cid: {cid}")
    media.storage.ingest.pin_cid_list([cid], ctx.obj["remote"])


@pin.command()
@click.option("--skip", default=0)
@click.option("--limit", default=0)
@click.pass_context
def cached(ctx, skip, limit):
    """Pin batch cid from ingested cache cid list \n
    Note: Please ensure that binaries are already ingested before run this command.
    eg. Resolve -> Transcode/Static -> Generate NFT metadata -> Ingest -> Pin batch
    """
    entries, _ = cache.ingest.frozen()  # Retrieve already ingested cid list
    entries = entries.skip(skip).limit(limit)
    cid_list = map(lambda x: x["hash"], entries)

    logger.log.warning("Starting pinning to IPFS")
    media.storage.ingest.pin_cid_list(cid_list, ctx.obj["remote"])
