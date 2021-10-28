import os

import responses
from src.sdk.media import fetch

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
        current_path = fetch.remote_file(mock_link, directory)

        assert current_path
        assert str(current_path) == directory
        assert current_path.is_file()
        os.remove(current_path)


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
            "src.sdk.util.resolve_root_for", return_value=(directory, False)
        )

        current_path = fetch.file(mock_local_file, directory)
        assert current_path
        assert str(current_path) == directory
        assert current_path.is_file()
        os.remove(current_path)


def test_omit_existing_file(mocker):
    """Should omit copy for local file and download attempt if file exist in destination directory"""
    with open("assets/tests/watchit.png", "rb") as mock_file:
        _setup_file_response_ok(mock_file, body=Exception("Should not be called"))
        mocker.patch(
            "src.sdk.util.resolve_root_for", return_value=(mock_local_file, True)
        )

        current_path = fetch.file(mock_local_file, mock_local_file)
        assert current_path
        assert str(current_path) == mock_local_file
        assert current_path.is_file()
