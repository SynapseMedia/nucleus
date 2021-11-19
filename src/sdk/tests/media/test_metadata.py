import responses
from src.sdk.constants import WALLET_PUBLIC_KEY
from src.sdk.scheme.definition.movies import MovieScheme, MultiMediaScheme
from src.sdk.media.metadata import generate_erc1155, _build_paths_from

directory = "assets/tests/watchit_.png"
mock_local_file = directory.replace("_", "")
mock_link = "https://example.org/assets/tests/watchit.png"

input_paths = {
    "posters": {
        "small": {"route": "https://test.com/BigBuckBunny.jpg"},
        "medium": {"route": "https://test.com/BigBuckBunny.jpg"},
        "large": {"route": "https://test.com/BigBuckBunny.jpg"},
    },
    "videos": [
        {"route": "https://test.com/BigBuckBunny.mp4", "quality": "720p", "type": "hls"}
    ],
}

built_paths = {
    "posters": {
        "small": {"route": "/small.jpg"},
        "medium": {"route": "/medium.jpg"},
        "large": {"route": "large.jpg"},
    },
    "videos": [{"720p": "/720/index.m3u8"}],
}


def input_movie(raw=True):
    return {
        "imdb_code": "tt00000",
        "title": "A Fork in the Road",
        "year": 2010,
        "rating": 6,
        "runtime": 105,
        "group_name": "test",
        "genres": ["Action", "Comedy", "Crime"],
        "synopsis": "Baby loves have fun",
        "trailer_code": "uIrQ9535RFo",
        "language": "en",
        "date_uploaded_unix": 1446321498,
        "resource": input_paths if raw else built_paths,
    }


nft_properties = {
    "name": input_movie()["title"],
    "image": "/medium.jpg",
    "description": input_movie()["synopsis"],
    "creator": WALLET_PUBLIC_KEY,
    "properties": input_movie(False),
}

expected_erc1155 = {
    "title": "WNFT Metadata",
    "type": "object",
    "properties": nft_properties,
}


# Unit tests
@responses.activate
def test_build_paths_from():
    """Should sanitize paths for metadata resources"""
    multimedia = MultiMediaScheme().load(input_paths)
    assert sorted(_build_paths_from(multimedia)) == sorted(built_paths)


# Unit tests
@responses.activate
def test_generate_erc1155():
    """Should generate valid erc1155 metadata"""
    mv = MovieScheme().load(input_movie())
    assert sorted(generate_erc1155(mv)) == sorted(expected_erc1155)
