import responses

import nucleus.core.ipfs as ipfs
from nucleus.core.ipfs import Add, File
from nucleus.core.types import JSON, Path


@responses.activate
def test_add(rpc_api_add_request: JSON, mock_local_video_path: Path):
    """Should return a valid ipfs api response for valid file"""

    api = ipfs.rpc()  # call to local ipfs
    command = Add(File(mock_local_video_path))
    output = api(command)  # call the command in api
    assert output == rpc_api_add_request
