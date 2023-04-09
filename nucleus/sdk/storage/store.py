import nucleus.core.ipfs as ipfs_

from functools import singledispatch
from nucleus.core.ipfs import Add, Text, File
from nucleus.core.types import CID, Optional, Callable, JSON
from nucleus.sdk.harvest import Meta, File as FileType, Distributed

from .types import Storable, Stored


def ipfs(endpoint: Optional[str] = None) -> Callable[[Storable], Stored]:
    """HOF to handle storage endpoint and return a singledispatch generic function.
    A form of generic function dispatch where the implementation is chosen based on the type of a single argument.
    ref: https://docs.python.org/3/glossary.html#term-single-dispatch

    :param endpoint: endpoint to connect api
    :return: singledispatch generic function
    :rtype: Callable[[Storable], Stored]
    """

    # connected ipfs api interface
    api = ipfs_.rpc(endpoint)

    @singledispatch
    def store(model: Storable) -> Stored:
        """Storage single dispatch factory.
        Use the model input to infer the right storage strategy.

        :param model: the model to dispatch
        :return: stored instance
        :rtype: Stored
        """
        raise NotImplementedError(f"cannot process not registered storable `{model}")

    @store.register
    def _(model: Distributed) -> Stored:
        # encode to bytes to then get the size
        bytes_ = bytes(JSON(model.dict()))
        command = Add(Text(bytes_))

        # expected /add output from API
        # {Hash: .., Name: ..}
        output = api(command)

        # construct stored object
        return Stored(
            cid=CID(output["Hash"]),
            name=output["Name"],
            size=int(output["Size"]),
        )

    @store.register
    def _(model: FileType) -> Stored:
        # 1 - store the file
        # 2 - assoc the file cid with a distributed media type
        # 3 - store distributed media type schema

        command = Add(File(model.route))
        # expected /add output from API
        # {Hash: .., Name: .., Size: ...}
        file_output = api(command)
        file_cid = CID(file_output["Hash"])
        file_size = int(file_output["Size"])

        # Create the new storable schema
        distributed = Distributed(route=file_cid, type=model.type, size=file_size)
        stored_distributed_schema = store(distributed)

        # construct stored object
        return Stored(
            cid=stored_distributed_schema.cid,
            name=stored_distributed_schema.name,
            size=file_size + stored_distributed_schema.size,
        )

    @store.register
    def _(model: Meta) -> Stored:
        # encode to bytes to then get the size
        bytes_ = bytes(JSON(model.dict()))
        command = Add(Text(bytes_))

        # expected /add output from API
        # {Hash: .., Name: ..}
        output = api(command)

        # construct stored object
        return Stored(
            cid=CID(output["Hash"]),
            name=output["Name"],
            size=len(bytes_),
        )

    return store


__all__ = ("ipfs",)
