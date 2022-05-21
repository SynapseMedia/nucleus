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

from src.core.util import extract_extension
from src.sdk.scheme.definition.movies import MovieScheme


def generate_erc1155(mv: MovieScheme):
    """Generate erc1155 metadata from scheme

    :param mv: MovieScheme
    :return: Ready to use ERC1155 metadata
    :rtype: dict
    """
    # Overwrite resources with shorten relative path to CID
    movie_serialized = MovieScheme().dump(mv)
    file_extension = extract_extension(mv.resource.image.route)
    del movie_serialized["resource"]

    nft_properties = {
        "name": mv.title,
        "image": f"/image/medium.{file_extension}",
        "description": mv.synopsis,
        "properties": movie_serialized,
    }

    nft_movie = {
        "title": "WNFT Metadata",
        "type": "object",
        "properties": nft_properties,
    }

    return nft_movie
