import responses
import nucleus.core.ipfs as ipfs

from nucleus.core.types import JSON, CID
from nucleus.core.ipfs import Put, Get, Text


@responses.activate
def test_block_put(rpc_api_block_put_request: JSON):
    """Should return a valid ipfs block put response for text"""

    api = ipfs.rpc()  # call to local ipfs
    command = Put(Text(b"hello"))
    output = api(command)  # call the command in api
    assert output == rpc_api_block_put_request


@responses.activate
def test_block_get(rpc_api_block_get_request: JSON):
    """Should return ipfs block get content for valid cid"""

    api = ipfs.rpc()  # call to local ipfs
    command = Get(CID("baebbeid3naxqil6ioq5v7hdups3qwztact4woyrqgd4avwbt3rk7ckdinq"))
    output = api(command)  # call the command in api
    assert output == rpc_api_block_get_request


@responses.activate
def test_block_remove(rpc_api_block_remove_request: JSON):
    """Should return a valid ipfs block remove response for valid cid"""

    api = ipfs.rpc()  # call to local ipfs
    command = Get(CID("baebbeid3naxqil6ioq5v7hdups3qwztact4woyrqgd4avwbt3rk7ckdinq"))
    output = api(command)  # call the command in api
    assert output == rpc_api_block_remove_request
