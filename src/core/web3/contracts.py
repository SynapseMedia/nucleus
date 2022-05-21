from . import Contract, Blockchain
from ..constants import PROJECT_ROOT
from ..util import read_json


class NFT(Contract):
    """NFT contract type"""

    def __init__(self, blockchain: Blockchain):
        self.address = blockchain.chain.erc1155
        self._contract = blockchain.contract_factory(self.address, self.abi)
        self.functions = self._contract.functions
        super().__init__(blockchain)

    def __getattr__(self, name):
        return self.functions[name]

    @property
    def abi(self):
        """Return abi from json for NFT contract"""
        abi_json = read_json("%s/abi/WNFT.json" % PROJECT_ROOT)
        return abi_json.get("abi")
