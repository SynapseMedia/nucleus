import os
import responses
import src.sdk.harvest.multimedia as multimedia

from src.core.types import Directory, URI, Any

custom_dir = "src/tests/core"
directory = Directory("fixture")
image = Directory(f"{directory}/watchit.png")

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
        },
    )


def test_copy_local_file(mocker: Any):
    """Should copy for local file and not attempt download"""
    with open(mock_local_file, "rb") as mock_file:
        _setup_file_response_ok(mock_file, body=Exception("Should not be called"))

        current_path = multimedia.fetch(URI(mock_local_file), new_file_directory)
        assert current_path
        assert str(current_path) == new_file_directory
        assert current_path.is_file()
        os.remove(current_path)


def test_omit_existing_file(mocker: Any):
    """Should omit copy for local file and download attempt if file exist in destination directory"""
    with open(mock_local_file, "rb") as mock_file:
        _setup_file_response_ok(mock_file, body=Exception("Should not be called"))

        current_path = multimedia.fetch(URI(mock_local_file), mock_local_file)
        assert current_path
        assert str(current_path) == mock_local_file
        assert current_path.is_file()


# Unit tests
def test_resolve_root_for_prod():
    """Should resolve PROD_DIR for param is_prod = True"""
    multimedia.PROD_PATH = custom_dir
    result_dir = multimedia.resolve(directory, is_prod=True)
    # (Path expected result for prod, if path exists  = True)
    expected = ("%s/%s" % (multimedia.PROD_PATH, directory), True)

    assert result_dir == expected


# Unit tests
def test_resolve_root_for_raw():
    """Should resolve RAW_DIR for param is_prod = False"""
    multimedia.RAW_PATH = custom_dir
    multimedia.PROD_PATH = "prod"  # just to be sure that this is not called
    result_dir = multimedia.resolve(directory, is_prod=False)
    # (Path expected for raw, if path exists = True)
    expected = ("%s/%s" % (multimedia.RAW_PATH, directory), True)

    assert result_dir == expected
