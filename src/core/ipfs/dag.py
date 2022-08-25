from src.core.types import CIDStr
from .types import Dag, DagLink
from .cmd import CLI


def get(cid: CIDStr) -> Dag:
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
    :raises IPFSFailedExecution:
    """

    # Exec command and get output
    exec = CLI("/dag/get", cid)
    output = exec().get("output")

    data = output.get("Data")
    raw_links = output.get("Links")

    # map iterator for nested links
    links = map(
        lambda l: DagLink(
            name=l.get("Name"),
            hash=l.get("Hash"),
            tsize=l.get("Tsize"),
        ),
        raw_links,
    )

    return Dag(data=data, links=links)
