import json
import nucleus.core.ipfs as ipfs

from functools import singledispatch
from nucleus.core.ipfs import Add, Text, File, Stored
from nucleus.core.types import Path, CID
from nucleus.sdk.harvest import Media, Meta
from .types import Storable


@singledispatch
def store(model: Storable) -> Stored:
    """Storage single dispatch factory.
    Use the model input to infer the right storage strategy.

    :param model: the model to dispatch
    :return: stored instance
    :rtype: Stored
    """
    raise NotImplementedError(
        f"cannot process not registered storable `{model}")


@store.register
def _(model: Media[Path]) -> Stored:
    api = ipfs.api()  # ipfs api interface
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
    api = ipfs.api()  # ipfs api interface
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
