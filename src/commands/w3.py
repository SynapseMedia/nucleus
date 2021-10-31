import click
from src.sdk.scheme.validator import check
from src.sdk import cache, media, exception, logger, util, web3


@click.group("w3")
@click.option("--provider", default="kovan")
@click.pass_context
def w3(ctx, provider):
    """
    NFT tools
    """
    ctx.ensure_object(dict)
    ctx.obj["provider"] = provider


@w3.command()
@click.pass_context
def connection(ctx):
    context_provider = ctx.obj["provider"]
    _w3 = web3.factory.w3(context_provider)
    logger.log.success(
        f"{context_provider} connected"
    ) if _w3.isConnected() else logger.log.error(f"{context_provider} offline")


@w3.command()
@click.option("--limit", default=5)
@click.pass_context
def batch(ctx, limit):
    result, result_count = cache.ingested()
    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    context_provider = ctx.obj["provider"]
    cid_list = list(map(lambda x: x["hash"], result))[:limit]

    _w3 = web3.factory.w3(context_provider)
    _to = _w3.eth.account.privateKeyToAccount(web3.factory.WALLET_KEY).address
    web3.nft.mint_batch(_to, cid_list, context_provider)


@w3.command()
@click.option("--cid")
@click.pass_context
def mint(ctx, cid):
    context_provider = ctx.obj["provider"]
    _w3 = web3.factory.w3(context_provider)
    _to = _w3.eth.account.privateKeyToAccount(web3.factory.WALLET_KEY).address
    web3.nft.mint(_to, cid, context_provider)


@w3.group("nft")
@click.pass_context
def nft(_):
    pass


@nft.command()
def generate():
    """Generate metadata json file for ERC1155 NFT"""
    # Return available and not processed entries
    # Total size of entries to fetch
    result, _ = cache.retrieve_with_empty_exception()
    # Generate metadata file from each row in tmp db the resources
    for current_movie in check(result):
        logger.log.warning(f"Processing NFT meta for {current_movie.imdb_code}")
        # Build metadata for current movie
        nft_movie_meta = media.nft.erc1155_metadata(current_movie)
        # Get directory output for current movie meta json
        current_dir = util.build_dir(current_movie)
        directory, _ = util.resolve_root_for(current_dir)
        util.write_json(f"{directory}/index.json", nft_movie_meta)
        logger.log.success(f"Written metadata for {current_movie.imdb_code}\n")
