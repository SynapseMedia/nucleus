import pytest
import json as JSON
import src.core.json as json

from src.core.types import Directory, Any

file_dir = "src/tests/_mock/files/index.json"

@pytest.fixture
def json_content():
    return {"test": "hi"}

def test_write_json(json_content: Any):
    """Should write json file with defined content"""
    new_dir = Directory(file_dir)
    new_created_dir = json.write(new_dir, json_content)
    with open(
        new_created_dir,
    ) as json_file:
        assert JSON.load(json_file) == json_content


def test_read_json(json_content: Any):
    """Should read json file with defined content"""
    new_dir = Directory(file_dir)
    assert json.read(new_dir) == json_content


def test_fail_read_json():
    """Should fail reading json file with invalid file path"""
    new_dir = Directory("bad.json")
    with pytest.raises(FileNotFoundError):
        json.read(new_dir)
