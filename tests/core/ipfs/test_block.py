import responses

import nucleus.core.ipfs as ipfs
from nucleus.core.ipfs import BlockPut, Text
from nucleus.core.types import JSON


@responses.activate
def test_block_put(rpc_api_block_put_request: JSON):
    """Should return a valid ipfs block put response for text"""

    api = ipfs.rpc()  # call to local ipfs
    command = BlockPut(Text(b'hello'))
    output = api(command)  # call the command in api
    assert output == rpc_api_block_put_request
