import pytest
import sqlite3
import responses
import json

from nucleus.core.types import Path, Any


@pytest.fixture()
def mock_local_path():
    return Path("nucleus/tests/_mock/files")


@pytest.fixture()
def mock_local_json_path():
    return Path("nucleus/tests/_mock/files/index.json")


@pytest.fixture()
def mock_local_image_path():
    return Path("nucleus/tests/_mock/files/spidy.png")


@pytest.fixture()
def mock_local_video_path():
    return Path("nucleus/tests/_mock/files/video.mp4")


@pytest.fixture()
def mock_local_file(mock_local_image_path: str):
    return open(mock_local_image_path, "rb")


@pytest.fixture
def setup_database():
    """Fixture to set up the in-memory database with test data"""
    conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("CREATE TABLE IF NOT EXISTS movies(m movie);")
    yield conn


@pytest.fixture()
def rpc_api_add_request(**kwargs: Any):
    mock_link = "http://localhost:5001/api/v0/add?pin=False&quieter=True&hash=blake2b-208&cid_version=1"
    expected_output = '{"Hash": "bafyjvzacdjrk37kqvy5hbqepmcraz3txt3igs7dbjwwhlfm3433a", "Name": "meta", "Size": "197"}'

    responses.add(
        responses.POST,
        mock_link,
        **{
            **{
                "body": expected_output,
                "status": 200,
            },
            **kwargs,
        },
    )

    return json.loads(expected_output)
