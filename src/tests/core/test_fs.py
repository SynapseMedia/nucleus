import os
import re
import pytest
import src.core.fs as fs

from pathlib import Path
from src.core.types import Directory

custom_dir = "src/tests/core"
directory = Directory("_mock")
image = Directory(f"{directory}/watchit.png")
license = Directory("LICENSE")
invalid = Directory("NOT_EXIST")

def test_valid_read_file():
    """Should return a valid file content with valid directory"""
    with fs.read(license) as content:
        pattern = "GNU AFFERO GENERAL PUBLIC LICENSE"
        assert content is not None
        assert re.search(pattern, content)


def test_invalid_read_file():
    """Should raise FileNotFoundError exception with invalid directory"""
    with pytest.raises(FileNotFoundError):
        with fs.read(invalid):
            ...


# Unit tests
def test_exists_file():
    """Should return True for valid path"""
    existing_file = fs.exists(license)
    assert existing_file is True


# Unit tests
def test_exists_invalid_file():
    """Should return False for invalid path"""
    existing_file = fs.exists(invalid)
    assert existing_file is False

def test_make_destination_dir():
    """Should create directory"""
    new_dir = Directory("assets/mock_test_dir/")
    new_created_dir = fs.make(new_dir)
    expected_new_path = Path(new_created_dir)
    assert expected_new_path.exists()
    os.rmdir(new_created_dir)


def test_extract_extension_for_file():
    """Should extract extension from file path"""
    expected = "png"
    provided = Directory("watchit.png")
    assert fs.extension(provided) == expected
    assert fs.extension(image) == expected
