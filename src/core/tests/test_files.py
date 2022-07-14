import os
from pathlib import Path

from src.core import files
from src.core.types import Directory

_custom_dir = "assets"
_directory = Directory("tests")
_file = Directory(f"{_directory}/watchit.png")


# Unit tests
def test_resolve_root_for_prod():
    """Should resolve PROD_DIR for param is_prod = True"""
    files.PROD_PATH = _custom_dir
    result_dir = files.resolve(_directory, is_prod=True)
    # (Path expected result for prod, if path exists  = True)
    expected = ("%s/%s" % (files.PROD_PATH, _directory), True)

    assert result_dir == expected


# Unit tests
def test_resolve_root_for_raw():
    """Should resolve RAW_DIR for param is_prod = False"""
    files.RAW_PATH = _custom_dir
    files.PROD_PATH = "prod"  # just to be sure that this is not called
    result_dir = files.resolve(_directory, is_prod=False)
    # (Path expected for raw, if path exists = True)
    expected = ("%s/%s" % (files.RAW_PATH, _directory), True)

    assert result_dir == expected


def test_make_destination_dir():
    """Should create directory"""
    new_dir = Directory("assets/mock_test_dir/")
    new_created_dir = files.make(new_dir)
    expected_new_path = Path(new_created_dir)
    assert expected_new_path.exists()
    os.rmdir(new_created_dir)



def test_extract_extension_for_file():
    """Should extract extension from file path"""
    expected = "png"
    provided = Directory("watchit.png")
    assert files.extension(provided) == expected
    assert files.extension(_file) == expected
