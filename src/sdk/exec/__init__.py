"""
Facade methods to interact with tools.
All methods expect MovieSchema as argument.

@param MovieSchema: The MovieSchema to interact with.

Expected order for movie processing:
# 1 - Transcode uploaded movie
# 2 - Process static image
# 3 - Generate ERC1155 metadata
# 4 - Ingest into IPFS
# 5 - Set creator as holder
"""

from . import transcode
from . import static
from . import storage
from . import w3
from . import nft

__all__ = ["transcode", "static", "storage", "w3", "nft"]
