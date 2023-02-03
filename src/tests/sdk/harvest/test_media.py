import os
import src.sdk.harvest as harvest
from src.core.types import Directory, URI, Any

custom_dir = "src/tests/_mock"
directory = Directory("files")
image = Directory(f"{directory}/watchit.png")


def test_copy_local_file(mock_local_file_path: Any):
    """Should copy for local file and not attempt download"""
    new_file_directory = Directory("src/tests/_mock/files/watchit!.png")
    current_path = harvest.fetch(URI(mock_local_file_path), new_file_directory)
    assert current_path
    assert str(current_path) == new_file_directory
    assert current_path.is_file()
    os.remove(current_path)


def test_omit_existing_file(mock_local_file_path: Any):
    """Should omit copy for local file and download attempt if file exist in destination directory"""
    current_path = harvest.fetch(
        URI(mock_local_file_path),
        mock_local_file_path)
    assert current_path
    assert str(current_path) == mock_local_file_path
    assert current_path.is_file()


def test_resolve_root_for_prod():
    """Should resolve PROD_DIR for param is_prod = True"""
    harvest.media.PROD_PATH = custom_dir
    result_dir = harvest.resolve(directory, is_prod=True)
    # (Path expected result for prod, if path exists  = True)
    expected = ("%s/%s" % (harvest.media.PROD_PATH, directory), True)

    assert result_dir == expected


def test_resolve_root_for_raw():
    """Should resolve RAW_DIR for param is_prod = False"""
    harvest.media.RAW_PATH = custom_dir
    harvest.media.PROD_PATH = "prod"  # just to be sure that this is not called
    result_dir = harvest.resolve(directory, is_prod=False)
    # (Path expected for raw, if path exists = True)
    expected = ("%s/%s" % (harvest.media.RAW_PATH, directory), True)

    assert result_dir == expected
