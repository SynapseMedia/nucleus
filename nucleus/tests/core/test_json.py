import pytest
import json as JSON
import nucleus.core.json as json

from nucleus.core.types import Path, JSON as JSONType

file_dir = "nucleus/tests/_mock/files/index.json"


@pytest.fixture
def json_content():
    return {"test": "hi"}


def test_write_json(json_content: JSONType):
    """Should write json file with defined content"""
    new_dir = Path(file_dir)
    new_created_dir = json.write(new_dir, json_content)
    with open(
        new_created_dir,
    ) as json_file:
        assert JSON.load(json_file) == json_content


def test_read_json(json_content: JSONType):
    """Should read json file with defined content"""
    new_dir = Path(file_dir)
    assert json.read(new_dir) == json_content


def test_fail_read_json():
    """Should fail reading json file with invalid file path"""
    new_dir = Path("bad.json")
    with pytest.raises(FileNotFoundError):
        json.read(new_dir)


def test_to_object(json_content: JSONType):
    """Should convert json to object with proper structure"""

    json_object = json.to_object(json_content)
    assert json_object.test == "hi"
