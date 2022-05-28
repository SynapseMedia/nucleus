from . import Contract, Network
from ..constants import PROJECT_ROOT
from ..util import read_json


class ERC1155(Contract):
    """ERC1155 contract type"""

    def __init__(self, network: Network):
        super().__init__(network)
        self.address = network.chain.erc1155
        # dynamic callable function handled by attribute accessor
        self._proxy = network.build_contract(self.address, self.abi)

    def __getattr__(self, name: str):
        return getattr(self._proxy, name)

    @property
    def abi(self):
        """Return abi from json for NFT contract"""
        abi_json = read_json("%s/abi/WNFT.json" % PROJECT_ROOT)
        return abi_json.get("abi")
