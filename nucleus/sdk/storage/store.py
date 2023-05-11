import functools
import nucleus.core.ipfs as ipfs_

from nucleus.core.types import CID, Optional, JSON
from nucleus.core.ipfs import Add, File, Text, Put
from nucleus.sdk.processing import File as FileType
from .types import Storable, Object, Store


def ipfs(endpoint: Optional[str] = None) -> Store:
    """HOF to handle storage endpoint and return a singledispatch generic function.
    A form of generic function dispatch where the implementation is chosen based on the type of a single argument.
    ref: https://docs.python.org/3/glossary.html#term-single-dispatch

    :param endpoint: endpoint to connect api
    :return: singledispatch generic function
    :rtype: Node
    """

    # connected ipfs api interface
    api = ipfs_.rpc(endpoint)

    @functools.singledispatch
    def store(data: Storable) -> Object:
        """Storage single dispatch factory.
        Use the data input type to infer the right storage strategy.

        :param data: the model to dispatch
        :return: Object instance
        :rtype: Object
        """
        raise NotImplementedError(f"cannot process not registered storable `{data}")

    @store.register
    def _(data: FileType) -> Object:
        """Add a file to IPFS

        :param data: the file model to store
        :return: stored instance
        :rtype: Stored

        """
        command = Add(File(data.path))
        # expected /add output from API
        # {Hash: .., Name: .., Size: ...}
        file_output = api(command)

        return Object(
            name=file_output["Name"],
            hash=CID(file_output["Hash"]),
            size=int(file_output["Size"]),
        )

    @store.register
    def _(data: bytes) -> Object:
        """Add bytes to ipfs

        :param data: bytes to store
        :return: object instance
        :rtype: Object
        """

        command = Put(Text(data))
        # expected block/put output from API
        # {Key: .., Size: ..}
        output = api(command)

        return Object(
            name=output["Key"],
            hash=CID(output["Key"]),
            size=len(data),
        )

    @store.register
    def _(data: str) -> Object:
        """Add JSON metadata representation to ipfs

        :param data: string to store
        :return: object instance
        :rtype: Object
        """

        bytes_ = data.encode("utf-8")
        return store(bytes_)

    @store.register
    def _(data: JSON) -> Object:
        """Add JSON metadata representation to ipfs

        :param data: json to store
        :return: object instance
        :rtype: Object
        """

        bytes_ = bytes(data)
        return store(bytes_)

    return store


__all__ = ("ipfs",)
