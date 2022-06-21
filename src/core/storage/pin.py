from ..types import PinRemote, PinLocal
from . import CLI


def remote(cid: str, service: str, background: bool) -> PinRemote:
    """Pin cid into edge pinata remote cache

    :param cid: the cid to pin
    :return
    """
    args = (
        cid,
        f"--service={service}",
        f"--background={background}",
    )

    # Exec command and get output
    exec = CLI("/pin/remote/add", args)
    output = exec().get("result")

    return PinRemote(
        status=output.get("Status"),  # status: queue using background
        cid=output.get("Cid"),  # resulting cid
        name=output.get("Name"),  # named pin
    )


def local(cid: str) -> PinLocal:
    """Pin cid into local node

    :param cid: the cid to pin
    :return
    """
    # Exec command and get output
    exec = CLI("/pin/add/", cid)
    output = exec().get("result")
    
    return PinLocal(pins=output.get("Pins"))
