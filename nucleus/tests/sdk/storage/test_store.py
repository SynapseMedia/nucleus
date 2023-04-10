import responses
import nucleus.sdk.storage as storage

from nucleus.core.types import Path, JSON
from nucleus.sdk.harvest import File, MediaType
from nucleus.sdk.storage import Stored


@responses.activate
def test_storage_file(rpc_api_add_request: JSON, mock_local_video_path: Path):
    """Should dispatch the right request based on storable input"""

    # retrieve the storage node, by default local ipfs local node
    local_node = storage.ipfs()

    # store a new file in local node
    storable = File(route=mock_local_video_path, type=MediaType.VIDEO)
    stored = local_node(storable)  # expected Stored output

    output_hash = rpc_api_add_request.get("Hash")
    output_name = rpc_api_add_request.get("Name")

    assert stored.cid.valid()
    assert stored.cid == output_hash
    assert stored.name == output_name
    assert stored.size == 197 + 96  # the file size + object struct size
    assert isinstance(stored, Stored)
