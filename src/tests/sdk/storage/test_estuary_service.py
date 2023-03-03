import responses
import src.sdk.storage as storage

from src.core.ipfs import Service
from src.core.types import Any, Path


ENDPOINT = ""


@responses.activate
def test_valid_remote_file(file_response_ok: Any):
    """Should fetch remote file from valid URL"""
    
    
    service = Service(name="estuary", endpoint=)
    storage.Estuary()
    ...
