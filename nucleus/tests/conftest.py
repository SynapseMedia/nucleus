import pytest
import sqlite3
import responses
from nucleus.core.types import Any, Path


@pytest.fixture()
def mock_local_path():
    return Path("nucleus/tests/_mock/files")



@pytest.fixture()
def mock_local_image_path():
    return Path("nucleus/tests/_mock/files/spidy.png")


@pytest.fixture()
def mock_local_video_path():
    return Path("nucleus/tests/_mock/files/video.mp4")


@pytest.fixture()
def mock_local_file(mock_local_image_path: str):
    return open(mock_local_image_path, "rb")


@pytest.fixture()
def file_response_ok(mock_local_file: Any, **kwargs: Any):
    mock_link = "https://example.org/assets/tests/watchit.png"

    responses.add(
        responses.GET,
        mock_link,
        **{
            **{
                "body": mock_local_file.read(),
                "status": 200,
                "content_type": "image/jpeg",
                "stream": True,
            },
            **kwargs,
        },
    )

    return mock_link


@pytest.fixture
def setup_database():
    """Fixture to set up the in-memory database with test data"""
    conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("CREATE TABLE IF NOT EXISTS movies(m movie);")
    yield conn
