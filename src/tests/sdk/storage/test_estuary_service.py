import responses
import src.sdk.storage as storage

from src.core.types import Any, Path

@responses.activate
def test_valid_remote_file(file_response_ok: Any):
    """Should fetch remote file from valid URL"""
    storage.Estuary()
    ...
