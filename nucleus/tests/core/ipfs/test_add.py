import responses
import nucleus.core.ipfs as ipfs

from nucleus.core.types import Path
from nucleus.core.ipfs import Add, File


@responses.activate
def test_add(api_add_request_output: str, mock_local_video_path: Path):
    """Should return a valid ipfs api response for valid file"""

    api = ipfs.api()  # call to local ipfs
    command = Add(File(mock_local_video_path))
    output = api(command)
    assert output == api_add_request_output
