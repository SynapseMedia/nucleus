import functools

import nucleus.core.ipfs as ipfs_
from nucleus.core.ipfs import Add, BlockPut, DagPut, Dir, File, Text
from nucleus.core.types import CID, JSON, Optional, Path
from nucleus.sdk.processing import File as FileType

from .types import Object, Storable, Store


def ipfs(endpoint: Optional[str] = None) -> Store:
    """Higher-order function to handle storage endpoint and
    return a singledispatch generic function with preset storage strategies.
    This is a form of generic function dispatch where the
    implementation is chosen based on the type of a single argument.

    Usage:

        store = storage.ipfs() # default localhost:5001
        stored_object = store(b'test bytes') # auto-choose the storage strategy


    :param endpoint: Endpoint to connect to the API. If the endpoint is not specified, localhost is used instead.
    :return: Singledispatch decorated function
    """

    # Connect to the IPFS API interface
    api = ipfs_.rpc(endpoint)

    @functools.singledispatch
    def store(data: Storable) -> Object:
        """Storage single dispatch factory.
        Uses the data input type to infer the right storage strategy.

        :param data: The model to dispatch
        :return: Object instance
        """
        raise NotImplementedError(f'cannot process not registered storable `{data}')

    @store.register
    def _(data: FileType) -> Object:
        """Store files in IPFS.

        :param data: File to store
        :return: Object instance
        """
        command = Add(File(data.path))
        # expected /add output from API
        # {Hash: .., Name: .., Size: ...}
        file_output = api(command)

        return Object(
            name=file_output['Name'],
            hash=CID(file_output['Hash']),
            size=int(file_output['Size']),
        )

    @store.register
    def _(data: Path) -> Object:
        """Store directory in IPFS.

        :param data: Directory path to store
        :return: Object instance
        """
        command = Add(
            input=Dir(data),
            wrap_with_directory=True,
        )

        # expected /add output from API
        # {Hash: .., Name: .., Size: ...}
        dir_output = api(command)

        return Object(
            name=dir_output['Name'],
            hash=CID(dir_output['Hash']),
            size=int(dir_output['Size']),
        )

    @store.register
    def _(data: bytes) -> Object:
        """Store bytes in IPFS.
        Store bytes in raw blocks.

        :param data: Bytes to store
        :return: Object instance
        """

        command = BlockPut(Text(data))
        # expected block/put output from API
        # {Key: .., Size: ..}
        output = api(command)

        return Object(
            name=output['Key'],
            hash=CID(output['Key']),
            size=len(data),
        )

    @store.register
    def _(data: str) -> Object:
        """String string in IPFS.
        Encode string to bytes and store it in raw blocks.

        :param data: String to store
        :return: Object instance
        """

        bytes_ = bytes(data, 'utf-8')
        return store(bytes_)

    @store.register
    def _(data: JSON) -> Object:
        """Store JSON in IPFS Dag.

        :param data: JSON to store
        :return: Object instance
        """

        bytes_ = bytes(data)
        command = DagPut(Text(bytes_))
        # expected block/put output from API
        # {"Cid": { "/": "<cid-string>" }}
        output = api(command)
        raw_cid = output['Cid']['/']

        return Object(
            name=raw_cid,
            hash=CID(raw_cid),
            size=len(data),
        )

    return store


__all__ = ('ipfs',)
