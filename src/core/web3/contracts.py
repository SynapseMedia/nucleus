import src.core.json as json

# Convention for importing types and constants
from src.core.types import Directory
from src.core.constants import PROJECT_ROOT
from .types import Contract, Network, Proxy, Address


class ERC1155(Contract):
    """ERC1155 contract type"""

    _address: Address
    _proxy: Proxy

    def __init__(self, network: Network):
        self._address = network.chain.erc1155
        self._proxy = network.contract(self._address, self.abi)

    def __getattr__(self, name: str):
        return getattr(self._proxy, name)

    @property
    def abi(self):
        """Return abi from json for NFT contract"""
        abi_path = Directory("%s/abi/WNFT.json" % PROJECT_ROOT)
        abi_json = json.read(abi_path)
        return abi_json["abi"]
