import os

import responses
from src.core.sdk.media import fetch
from pathlib import Path

directory = "assets/tests/watchit_.png"
mock_local_file = directory.replace("_", "")
mock_link = "https://example.org/assets/tests/watchit.png"


def _setup_file_response_ok(mock_file, **kwargs):
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
    with open("assets/tests/watchit.png", "rb") as mock_file:
        _setup_file_response_ok(mock_file)
        result_dir = fetch.remote_file(mock_link, directory)
        current_path = Path(result_dir)

        assert result_dir
        assert str(current_path) == directory
        assert current_path.is_file()
        os.remove(result_dir)


def test_invalid_remote_file():
    """Should fail for remote file from invalid URL"""
    responses.add(responses.GET, mock_link, status=404)

    result_dir = fetch.remote_file(mock_link, directory)
    assert not result_dir


def test_copy_local_file(mocker):
    """Should copy for local file and not attempt download"""
    with open("assets/tests/watchit.png", "rb") as mock_file:
        _setup_file_response_ok(mock_file, body=Exception("Should not be called"))
        mocker.patch(
            "src.core.sdk.util.resolve_root_for",
            return_value=(directory, False)
        )

        result_dir = fetch.file(mock_local_file, directory)
        current_path = Path(result_dir)

        assert result_dir
        assert str(current_path) == directory
        assert current_path.is_file()

        os.remove(result_dir)


def test_omit_existing_file(mocker):
    """Should omit copy for local file and download attempt if file exist in destination directory"""
    with open("assets/tests/watchit.png", "rb") as mock_file:
        _setup_file_response_ok(mock_file, body=Exception("Should not be called"))
        mocker.patch('src.core.sdk.util.resolve_root_for', return_value=(mock_local_file, True))

        result_dir = fetch.file(mock_local_file, mock_local_file)
        current_path = Path(result_dir)

        assert str(current_path) == mock_local_file
        assert current_path.is_file()
