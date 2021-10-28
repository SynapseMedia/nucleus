import click
from src.sdk.scheme.validator import parse
from src.sdk import cache, mongo, media, exception


@click.group("meta")
def nft():
    """
    NFT tools
    """
    pass


@nft.command()
def generate():
    """Generate metadata json file for ERC1155 NFT"""
    # Return available and not processed entries
    result = cache.retrieve(mongo.temp_db)
    result_count = result.count()  # Total size of entries to fetch

    if result_count == 0:  # If not data to fetch
        raise exception.EmptyCache()

    # Generate metadata file from each row in tmp db the resources
    for current_movie in parse(result):
        media.nft.erc1155_metadata(current_movie)
