import pytest
from marshmallow.exceptions import ValidationError
from src.sdk.scheme.definition.movies import MovieScheme, MultiMediaScheme
from src.sdk.media.metadata import generate_erc1155, build_paths
from deepdiff import DeepDiff

directory = "assets/tests/watchit_.png"
mock_local_file = directory.replace("_", "")
mock_link = "https://example.org/assets/tests/watchit.png"

input_paths = {
    "video": {
        "route": "QmbWqxBEKC3P8tqsKc98xmWNzrzDtRLMiMPL8wBuTGsMnR",
        "index": {"hls": "index.m3u8"},
    },
    "image": {
        "route": "QmbWqxBEKC3P8tqsKc98xmWNzrzDtRLMiMPL8wBuTGsMnR",
        "index": {
            "small": "/small.jpg",
            "medium": "/medium.jpg",
            "large": "/large.jpg",
        },
    },
}


def input_movie():
    return {
        "imdb_code": "tt00000",
        "title": "A Fork in the Road",
        "year": 2010,
        "rating": 6.0,
        "runtime": 105.0,
        "price": 0.0,
        "mpa_rating": "PG",
        "group_name": "test",
        "creator": "0xee99ceff640d37edd9cac8c7cff4ed4cd609f435",
        "genres": ["Action", "Comedy", "Crime"],
        "synopsis": "Baby loves have fun",
        "trailer_code": "uIrQ9535RFo",
        "language": "en",
        "date_uploaded_unix": 1446321498.0,
        "resource": input_paths,
    }


nft_properties = {
    "name": input_movie()["title"],
    "image": "/medium.jpg",
    "description": input_movie()["synopsis"],
    "properties": input_movie(),
}

expected_erc1155 = {
    "title": "WNFT Metadata",
    "type": "object",
    "properties": nft_properties,
}


# Unit tests
def test_build_paths_from():
    """Should sanitize paths for metadata resources"""
    multimedia = MultiMediaScheme().load(input_paths)
    assert DeepDiff(build_paths(multimedia), input_paths, ignore_order=True) == {}


# Unit tests
def test_generate_erc1155():
    """Should generate valid erc1155 metadata"""
    mv = MovieScheme().load(input_movie())
    print(generate_erc1155(mv))
    assert DeepDiff(generate_erc1155(mv), expected_erc1155) == {}


# Unit tests
def test_fail_with_invalid_raw_metadata():
    """Should fail with invalid metadata"""
    with pytest.raises(ValidationError):
        invalid_meta = input_movie()
        invalid_meta["title"] = ""
        invalid_meta["rating"] = -1
        MovieScheme().load(invalid_meta)
