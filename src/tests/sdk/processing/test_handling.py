import os
import src.sdk.processing as processing

from src.core.types import Path

custom_dir = "src/tests/_mock"
directory = Path("files")
image = Path(f"{directory}/watchit.png")


def test_copy_local_file(mock_local_file_path: Path):
    """Should copy for local file and not attempt download"""
    new_file_directory = Path("src/tests/_mock/files/watchit!.png")
    current_path = processing.fetch(mock_local_file_path, new_file_directory)
    assert current_path
    assert str(current_path) == new_file_directory
    assert current_path.is_file()
    os.remove(current_path)


def test_omit_existing_file(mock_local_file_path: Path):
    """Should omit copy for local file and download attempt if file exist in destination directory"""
    current_path = processing.fetch(mock_local_file_path, mock_local_file_path)
    assert current_path
    assert str(current_path) == mock_local_file_path
    assert current_path.is_file()


def test_resolve_root_for_prod():
    """Should resolve PROD_DIR for param is_prod = True"""
    processing.handling.PROD_PATH = custom_dir
    result_dir = processing.resolve(directory, is_prod=True)
    # (Path expected result for prod, if path exists  = True)
    expected = ("%s/%s" % (processing.handling.PROD_PATH, directory), True)

    assert result_dir == expected


def test_resolve_root_for_raw():
    """Should resolve RAW_DIR for param is_prod = False"""
    processing.handling.RAW_PATH = custom_dir
    processing.handling.PROD_PATH = "prod"  # just to be sure that this is not called
    result_dir = processing.resolve(directory, is_prod=False)
    # (Path expected for raw, if path exists = True)
    expected = ("%s/%s" % (processing.handling.RAW_PATH, directory), True)

    assert result_dir == expected
