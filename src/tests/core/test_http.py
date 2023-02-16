import pytest
import requests
import responses
import src.core.http as http

from src.core.types import Path, URL, Any


# Unit tests
@responses.activate
def test_valid_remote_file(file_response_ok: Any):
    """Should fetch remote file from valid URL"""

    new_file_directory = Path("src/tests/_mock/files/watchit.png")
    current_path = http.download(file_response_ok, new_file_directory)

    assert current_path
    assert str(current_path) == new_file_directory
    assert current_path.is_file()


@responses.activate
def test_invalid_remote_file():
    """Should fail for remote file from invalid URL"""
    invalid_link = URL("https://invalid.org/assets/tests/watchit.png")
    responses.add(responses.GET, invalid_link, status=404)
    with pytest.raises(requests.exceptions.HTTPError):
        http.download(invalid_link, Path("/tmp"))
