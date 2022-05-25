from re import L
from . import Contract, Network
from ..constants import PROJECT_ROOT
from ..util import read_json


class NFT(Contract):
    """NFT contract type"""

    def connect(self, network: Network):
        self.network = network
        self.address = network.chain.erc1155

        # dynamic callable function handled by attribute accessor
        _contract = network.contract(self.address, self.abi)
        self.functions = _contract.functions
        return network

    def __getattr__(self, name):
        return self.functions[name]

    @property
    def abi(self):
        """Return abi from json for NFT contract"""
        abi_json = read_json("%s/abi/WNFT.json" % PROJECT_ROOT)
        return abi_json.get("abi")
