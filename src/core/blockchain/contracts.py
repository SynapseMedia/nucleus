import src.core.json as json

# Convention for importing types and constants
from src.core.types import Path
from .constants import NFT_ABI_PATH
from .types import Contract, Network, Proxy


class ERC1155(Contract):
    """ERC1155 contract type"""

    _proxy: Proxy

    def __init__(self, network: Network):
        # Proxy call to contract methods
        self._proxy = network.contract(
            network.chain.erc1155,
            self.abi,
        )

    def __getattr__(self, name: str):
        return getattr(self._proxy, name)

    @property
    def abi(self):
        """Return abi from json for NFT contract"""
        abi_path = Path(NFT_ABI_PATH)
        abi_json = json.read(abi_path)
        return abi_json["abi"]
