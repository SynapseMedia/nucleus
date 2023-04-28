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
    def store(model: Storable) -> Object:
        """Storage single dispatch factory.
        Use the model input to infer the right storage strategy.

        :param model: the model to dispatch
        :return: Object instance
        :rtype: Object
        """
        raise NotImplementedError(f"cannot process not registered storable `{model}")

    @store.register
    def _(model: FileType) -> Object:
        """Add a file to IPFS

        :param model: the file model to store
        :return: stored instance
        :rtype: Stored

        """
        command = Add(File(model.path))
        # expected /add output from API
        # {Hash: .., Name: .., Size: ...}
        file_output = api(command)

        return Object(
            name=file_output["Name"],
            hash=CID(file_output["Hash"]),
            size=int(file_output["Size"]),
        )

    @store.register
    def _(model: str) -> Object:
        """Add string to ipfs

        :param model: string to store
        :return: object instance
        :rtype: Object
        """

        bytes_ = model.encode("utf-8")
        command = Put(Text(bytes_))
        # expected block/put output from API
        # {Key: .., Size: ..}
        output = api(command)

        return Object(
            name=output["Key"],
            hash=CID(output["Key"]),
            size=len(bytes_),
        )

    @store.register
    def _(model: JSON) -> Object:
        """Add JSON metadata representation to ipfs

        :param model: string to store
        :return: object instance
        :rtype: Object
        """

        bytes_ = bytes(model)
        command = Add(Text(bytes_))
        # expected block/put output from API
        # {Hash: .., Name: .., Size: ...}
        output = api(command)

        return Object(
            name=output["Hash"],
            hash=CID(output["Hash"]),
            size=int(output["Size"]),
        )

    return store


__all__ = ("ipfs",)
