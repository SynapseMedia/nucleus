import json as JSON
import pytest

from src.core import json 
from src.core.types import Directory


def test_write_json():
    """Should write json file with defined content"""

    new_dir = "assets/tests/index.json"
    json_content = {"test": "hi"}
    new_created_dir = json.write(new_dir, json_content)
    with open(
        new_created_dir,
    ) as json_file:
        assert JSON.load(json_file) == json_content


def test_read_json():
    """Should read json file with defined content"""
    new_dir = Directory("assets/tests/index.json")
    json_content = {"test": "hi"}
    assert json.read(new_dir) == json_content


def test_fail_read_json():
    """Should fail reading json file with invalid file path"""
    new_dir = Directory("bad.json")
    with pytest.raises(FileNotFoundError):
        json.read(new_dir)
