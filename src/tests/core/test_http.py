import os
import pytest
import requests
import responses
import src.core.http as http

from src.core.types import Directory, URI, Any

new_file_directory = Directory("src/tests/core/fixture/watchit_.png")
mock_local_file = Directory(new_file_directory.replace("_", ""))
mock_link = URI("https://example.org/assets/tests/watchit.png")


def _setup_file_response_ok(mock_file: Any, **kwargs: Any):
    responses.add(
        responses.GET,
        mock_link,
        **{
            **{
                "body": mock_file.read(),
                "status": 200,
                "content_type": "image/jpeg",
                "stream": True,
            },
            **kwargs,
        }
    )


# Unit tests
@responses.activate
def test_valid_remote_file():
    """Should fetch remote file from valid URL"""
    with open(mock_local_file, "rb") as mock_file:
        _setup_file_response_ok(mock_file)
        current_path = http.download(mock_link, new_file_directory)

        assert current_path
        assert str(current_path) == new_file_directory
        assert current_path.is_file()
        os.remove(current_path)


@responses.activate
def test_invalid_remote_file():
    """Should fail for remote file from invalid URL"""
    responses.add(responses.GET, mock_link, status=404)
    with pytest.raises(requests.exceptions.HTTPError):
        http.download(mock_link, new_file_directory)


def test_copy_local_file(mocker: Any):
    """Should copy for local file and not attempt download"""
    with open(mock_local_file, "rb") as mock_file:
        _setup_file_response_ok(mock_file, body=Exception("Should not be called"))
        mocker.patch("src.core.files.resolve", return_value=(new_file_directory, False))

        current_path = http.fetch(URI(mock_local_file), new_file_directory)
        assert current_path
        assert str(current_path) == new_file_directory
        assert current_path.is_file()
        os.remove(current_path)


def test_omit_existing_file(mocker: Any):
    """Should omit copy for local file and download attempt if file exist in destination directory"""
    with open(mock_local_file, "rb") as mock_file:
        _setup_file_response_ok(mock_file, body=Exception("Should not be called"))
        mocker.patch("src.core.files.resolve", return_value=(mock_local_file, True))

        current_path = http.fetch(URI(mock_local_file), mock_local_file)
        assert current_path
        assert str(current_path) == mock_local_file
        assert current_path.is_file()
