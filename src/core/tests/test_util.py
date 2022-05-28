import json
import os
import pytest
from src.core import util
from pathlib import Path
from ..types import Directory

custom_dir = "assets"
directory = Directory("tests")
file = Directory(f"{directory}/watchit.png")


# Unit tests
def test_resolve_root_for_prod():
    """Should resolve PROD_DIR for param is_prod = True"""
    util.PROD_PATH = custom_dir
    result_dir = util.resolve_root_for(directory, is_prod=True)
    # (Path expected result for prod, if path exists  = True)
    expected = ("%s/%s" % (util.PROD_PATH, directory), True)

    assert result_dir == expected


# Unit tests
def test_resolve_root_for_raw():
    """Should resolve RAW_DIR for param is_prod = False"""
    util.RAW_PATH = custom_dir
    util.PROD_PATH = "prod"  # just to be sure that this is not called
    result_dir = util.resolve_root_for(directory, is_prod=False)
    # (Path expected for raw, if path exists = True)
    expected = ("%s/%s" % (util.RAW_PATH, directory), True)

    assert result_dir == expected


def test_extract_extension_for_file():
    """Should extract extension from file path"""
    expected = "png"
    provided = Directory("watchit.png")
    assert util.extract_extension(provided) == expected
    assert util.extract_extension(file) == expected


def test_make_destination_dir():
    """Should create directory"""
    new_dir = Directory("assets/mock_test_dir/")
    new_created_dir = util.make_destination_dir(new_dir)
    expected_new_path = Path(new_created_dir)
    assert expected_new_path.exists()
    os.rmdir(new_created_dir)


def test_write_json():
    """Should write json file with defined content"""
    new_dir = "assets/tests/index.json"
    json_content = {"test": "hi"}
    new_created_dir = util.write_json(new_dir, json_content)
    with open(
        new_created_dir,
    ) as json_file:
        assert json.load(json_file) == json_content


def test_read_json():
    """Should read json file with defined content"""
    new_dir = Directory("assets/tests/index.json")
    json_content = {"test": "hi"}
    assert util.read_json(new_dir) == json_content


def test_fail_read_json():
    """Should fail reading json file with invalid file path"""
    new_dir = Directory("bad.json")
    with pytest.raises(FileNotFoundError):
        util.read_json(new_dir)
