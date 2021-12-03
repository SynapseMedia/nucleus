"""
ERC-1155 Metadata URI JSON Scheme
This JSON schema is loosely based on the “ERC721 Metadata JSON Schema”,
but includes optional formatting to allow for ID substitution by clients.
If the string {id} exists in any JSON value, it MUST be replaced with the actual token ID,
by all client software that follows this standard.

    * The string format of the substituted hexadecimal ID MUST be lowercase alphanumeric: [0-9a-f] with no 0x prefix.
    * The string format of the substituted hexadecimal ID MUST be leading zero padded
    to 64 hex characters length if necessary.

eg.

{
    "title": "Token Metadata",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Identifies the asset to which this token represents"
        },
        "decimals": {
            "type": "integer",
            "description": "The number of decimal places that the token amount should display - e.g. 18, means to
            divide the token amount by 1000000000000000000 to get its user representation."
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this token represents"
        },
        "image": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this
            token represents. Consider making any images at a width between 320 and 1080 pixels and
            aspect ratio between 1.91:1 and 4:5 inclusive."
        },
        "properties": {
            "type": "object",
            "description": "Arbitrary properties. Values may be strings, numbers, object or arrays."
        }
    }
}
"""

from src.sdk import util
from ..media import transcode
from ..constants import WALLET_PUBLIC_KEY
from ..scheme.definition.movies import MovieScheme, MultiMediaScheme


def _build_paths_from(resource: MultiMediaScheme):
    """
    Build new valid paths for metadata
    :param resource: MultimediaScheme
    :return: MultiMediaScheme cleaned
    """
    return {
        "videos": [
            {x.quality: f"/{x.quality}/{transcode.DEFAULT_NEW_FILENAME}"}
            for x in resource.videos
        ],
        "posters": [
            {k: f"/{k}.{util.extract_extension(i.route)}"}
            for k, i in resource.posters.iterable()
        ],
    }


def generate_erc1155(mv: MovieScheme):
    """
    Go and conquer the world little child!!:
    Add directory to ipfs
    :param mv: MovieScheme
    :return: Resulting metadata
    """
    # Overwrite resources with shorten relative path to CID
    movie_serialized = MovieScheme().dump(mv)
    movie_serialized["resource"] = _build_paths_from(mv.resource)
    nft_properties = {
        "name": mv.title,
        "image": "/medium.jpg",
        "description": mv.synopsis,
        "creator": WALLET_PUBLIC_KEY,
        "properties": movie_serialized,
    }

    nft_movie = {
        "title": "WNFT Metadata",
        "type": "object",
        "properties": nft_properties
    }

    return nft_movie
