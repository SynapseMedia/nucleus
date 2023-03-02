from src.core.types import CID
from .types import Dag, DagLink
from .cmd import CLI


def get(cid: CID) -> Dag:
    """Retrieve dag information from cid
    ref: https://docs.ipfs.io/reference/cli/#ipfs-dag-get

    Output:
        {
            "Data": {"/": {"bytes": "CAIY1qEQIICAECDWIQ"}},
            "Links": [
                {
                    "Hash": {"/": "QmRoo28ogKQ6ds3jk9x7X7x3sjTs2yTMu5vHUPxLN8vinU"},
                    "Name": "",
                    "Tsize": 262158,
                },
            ],
        }

    :param cid: cid to retrieve from dag
    :return: Dag representation objects
    :rtype: Dag
    :raises IPFSRuntimeException: if ipfs cmd execution fail
    """

    # Exec command and get output
    call = CLI("/dag/get", cid)()
    data = call.output.get("Data")
    raw_links = call.output.get("Links")

    # map iterator for nested links
    links = map(
        lambda links: DagLink(
            name=links.get("Name"),
            hash=links.get("Hash"),
            tsize=links.get("Tsize"),
        ),
        raw_links,
    )

    return Dag(data=data, links=links)
