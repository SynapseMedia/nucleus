import pytest
import sqlite3
from nucleus.core.types import Path


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
