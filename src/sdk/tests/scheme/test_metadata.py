import pytest
from deepdiff import DeepDiff
from marshmallow.exceptions import ValidationError

from src.sdk.media.metadata import generate_erc1155
from src.sdk.scheme.definition.movies import MovieScheme

directory = "assets/tests/watchit_.png"
mock_local_file = directory.replace("_", "")
mock_link = "https://example.org/assets/tests/watchit.png"

input_paths = {
    "image": {"route": "https://test.com/BigBuckBunny.jpg"},
    "video": {"route": "https://test.com/BigBuckBunny.mp4"},
}


def input_movie(raw=True):
    return {
        **{
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
        },
        **({"resource": input_paths} if raw else {}),
    }


nft_properties = {
    "name": input_movie()["title"],
    "image": "/image/medium.jpg",
    "description": input_movie()["synopsis"],
    "properties": input_movie(False),
}

expected_erc1155 = {
    "title": "WNFT Metadata",
    "type": "object",
    "properties": nft_properties,
}


# Unit tests
def test_generate_erc1155():
    """Should generate valid erc1155 metadata"""
    mv = MovieScheme().load(input_movie())
    assert DeepDiff(generate_erc1155(mv), expected_erc1155) == {}


# Unit tests
def test_fail_with_invalid_raw_metadata():
    """Should fail with invalid metadata"""
    with pytest.raises(ValidationError):
        invalid_meta = input_movie()
        invalid_meta["title"] = ""
        invalid_meta["rating"] = -1
        MovieScheme().load(invalid_meta)
