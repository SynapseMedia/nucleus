from . import Contract, Network
from web3.types import ABIFunction
from ..constants import PROJECT_ROOT
from ..util import read_json


class ERC1155(Contract):
    """ERC1155 contract type"""

    def __init__(self, network: Network):

        if not isinstance(network, Network):
            raise TypeError("provided `network` must implement Network interface")

        super().__init__(network)
        self.address = network.chain.erc1155
        # dynamic callable function handled by attribute accessor
        _contract = network.contract(self.address, self.abi)
        self.functions = _contract.functions

    def __getattr__(self, name: str) -> ABIFunction:
        return getattr(self.functions, name)

    @property
    def abi(self):
        """Return abi from json for NFT contract"""
        abi_json = read_json("%s/abi/WNFT.json" % PROJECT_ROOT)
        return abi_json.get("abi")
