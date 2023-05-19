import copy

import pytest

from nucleus.core.types import Any
from nucleus.tests._mock.models import Movie


@pytest.fixture
def mock_raw_media():
    return {
        'path': 'nucleus/tests/_mock/files/watchit.png',
    }


@pytest.fixture
def mock_raw_metadata():
    """Fixture to provide a mocking for movie"""

    return {
        'name': 'A Fork in the Road',
        'imdb_code': 'wtt00000000',
        'creator_key': '0xee99ceff640d37edd9cac8c7cff4ed4cd609f435',
        'mpa_rating': 'PG',
        'rating': 6.0,
        'runtime': 105.0,
        'desc': 'Baby loves have fun',
        'release_year': 2010,
        'genres': ['Action', 'Comedy', 'Crime'],
        'speech_language': 'en',
        'publish_date': 1669911990.9270618,
    }


@pytest.fixture
def mock_raw_collected(mock_raw_metadata: Any, mock_raw_media: Any):
    return {'metadata': mock_raw_metadata, 'media': [mock_raw_media]}


@pytest.fixture
def mock_raw_collected2(mock_raw_collected: Any):
    mock_raw_collected2 = copy.deepcopy(mock_raw_collected)
    mock_raw_collected2['metadata'].update({'name': 'A in the Road'})
    return mock_raw_collected2


@pytest.fixture
def mock_models(mock_raw_metadata: Any):
    return Movie.parse_obj(mock_raw_metadata)


@pytest.fixture
def mock_models_B(mock_raw_metadata: Any):
    mock_raw_metadata.update({'name': 'A in the Road'})
    return Movie.parse_obj(mock_raw_metadata)
