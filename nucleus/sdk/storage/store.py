import json
import nucleus.core.ipfs as ipfs_

from functools import singledispatch
from nucleus.core.ipfs import Add, Text, File
from nucleus.core.types import CID, Optional, Callable
from nucleus.sdk.harvest import Meta, File as FileType

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
    def _(model: FileType) -> Stored:
        command = Add(File(model.route))
        # expected /add output from API
        # {Hash: .., Name: .., Size: ...}
        output = api(command)
        # construct stored object
        return Stored(
            cid=CID(output.get("Hash", "")),
            name=output.get("Name", ""),
            size=output.get("Size", 0.0),
        )

    @store.register
    def _(model: Meta) -> Stored:
        # transform meta in json string
        json_string = json.dumps(model.dict())

        # encode to bytes to then get the size
        bytes_ = bytes(json_string, "utf-8")
        command = Add(Text(bytes_))

        # expected /add output from API
        # {Hash: .., Name: ..}
        output = api(command)

        # construct stored object
        return Stored(
            cid=CID(output.get("Hash", "")),
            name=output.get("Name", ""),
            size=len(bytes_),
        )

    return store


__all__ = ("ipfs",)
