import os
import re
import pytest

from pathlib import Path
from src.core import files
from src.core.types import Directory

custom_dir = "assets"
directory = Directory("tests")
image = Directory(f"{directory}/watchit.png")


def test_valid_read_file():
    """Should return a valid file content with valid directory"""
    with files.read("LICENSE") as content:
        pattern = "GNU AFFERO GENERAL PUBLIC LICENSE"
        assert content is not None
        assert re.search(pattern, content)


def test_invalid_read_file():
    """Should raise FileNotFoundError exception with invalid directory"""
    with pytest.raises(FileNotFoundError):
        with files.read("NOT_EXIST"):
            ...


# Unit tests
def test_exists_file():
    """Should return True for valid path"""
    existing_file = files.exists("LICENSE")
    assert existing_file is True


# Unit tests
def test_exists_invalid_file():
    """Should return False for invalid path"""
    existing_file = files.exists("INVALID")
    assert existing_file is False


# Unit tests
def test_resolve_root_for_prod():
    """Should resolve PROD_DIR for param is_prod = True"""
    files.PROD_PATH = custom_dir
    result_dir = files.resolve(directory, is_prod=True)
    # (Path expected result for prod, if path exists  = True)
    expected = ("%s/%s" % (files.PROD_PATH, directory), True)

    assert result_dir == expected


# Unit tests
def test_resolve_root_for_raw():
    """Should resolve RAW_DIR for param is_prod = False"""
    files.RAW_PATH = custom_dir
    files.PROD_PATH = "prod"  # just to be sure that this is not called
    result_dir = files.resolve(directory, is_prod=False)
    # (Path expected for raw, if path exists = True)
    expected = ("%s/%s" % (files.RAW_PATH, directory), True)

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
    assert files.extension(image) == expected
