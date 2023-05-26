import json

import pytest

from nucleus.core.types import JSON, Path


@pytest.fixture
def json_content():
    return JSON({'test': 'hi'})


def test_write_json(json_content: JSON, mock_local_json_path: Path):
    """Should write json file with defined content"""
    new_created_dir = json_content.write(mock_local_json_path)
    with open(
        new_created_dir,
    ) as json_file:
        assert json.load(json_file) == json_content


def test_read_json(json_content: JSON, mock_local_json_path: Path):
    """Should read json file with defined content"""
    assert json_content.read(mock_local_json_path) == json_content


def test_fail_read_json(json_content: JSON):
    """Should fail reading json file with invalid file path"""
    new_dir = Path('bad.json')
    with pytest.raises(FileNotFoundError):
        json_content.read(new_dir)
