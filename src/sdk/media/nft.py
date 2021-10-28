from src.sdk import util, logger
from src.sdk.scheme.definition.nft import MovieNFTProperties, MovieNFT
from src.sdk.scheme.definition.movies import MovieScheme


def nft_erc1155_metadata(mv: MovieScheme):
    """
    Go and conquer the world little child!!:
    Add directory to ipfs
    :param mv: MovieScheme
    :return: The resulting CID
    """

    logger.log.warning(f"Processing NFT meta for {mv.get('imdb_code')}")
    # Logs on ready ingested
    current_dir = util.build_dir(mv)
    directory, path_exists = util.resolve_root_for(current_dir)
    nft_movies_properties = MovieNFTProperties().load(
        {"name": mv.get("title"), "description": mv.get("synopsis"), "properties": mv}
    )

    nft_movie = MovieNFT().load(
        {
            "title": "WNFT Metadata",
            "type": "object",
            "properties": nft_movies_properties,
        }
    )

    del nft_movie["properties"]["properties"][
        "resource"
    ]  # We dont want to share this XD
    del nft_movie["properties"]["properties"][
        "group_name"
    ]  # We dont want to share this too XD
    del nft_movie["properties"]["properties"][
        "date_uploaded_unix"
    ]  # We dont want to share this too XD

    util.write_json(f"{directory}/index.json", nft_movie)
    logger.log.success(f"Written metadata for {mv.get('imdb_code')}\n")
