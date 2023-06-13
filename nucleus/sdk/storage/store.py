import functools

import nucleus.core.ipfs as ipfs_
from nucleus.core.ipfs import Add, BlockPut, DagPut, File, Text
from nucleus.core.types import CID, JSON, Optional
from nucleus.sdk.processing import File as FileType

from .types import Object, Storable, Store


def ipfs(endpoint: Optional[str] = None) -> Store:
    """HOF to handle storage endpoint and return a singledispatch generic function.
    A form of generic function dispatch where the implementation is chosen based on the type of a single argument.
    ref: https://docs.python.org/3/glossary.html#term-single-dispatch

    :param endpoint: Endpoint to connect api
    :return: Singledispatch generic function
    """

    # connected ipfs api interface
    api = ipfs_.rpc(endpoint)

    @functools.singledispatch
    def store(data: Storable) -> Object:
        """Storage single dispatch factory.
        Use the data input type to infer the right storage strategy.

        :param data: The model to dispatch
        :return: Object instance
        """
        raise NotImplementedError(f'cannot process not registered storable `{data}')

    @store.register
    def _(data: FileType) -> Object:
        """Add a file to IPFS

        :param data: The file model to store
        :return: stored instance

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
    def _(data: bytes) -> Object:
        """Add bytes to ipfs

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
        """Add JSON metadata representation to ipfs

        :param data: String to store
        :return: Object instance
        """

        bytes_ = data.encode('utf-8')
        return store(bytes_)

    @store.register
    def _(data: JSON) -> Object:
        """Add JSON metadata representation to ipfs

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
