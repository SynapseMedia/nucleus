from .blockchains import Contract, Blockchain
from ..constants import PROJECT_ROOT
from ..util import read_json


class NFT(Contract):
    """NFT contract type"""

    def __init__(self, blockchain: Blockchain):
        self.address = blockchain.chain.erc1155
        self._contract = blockchain.contract_factory(self.address, self.abi)
        self.functions = self._contract.functions
        super().__init__(self, blockchain)

    def __getattr__(self, name):
        return self.functions[name]

    @property
    def abi(root_path: str = PROJECT_ROOT):
        return read_json("%s/abi/WNFT.json" % root_path).get("abi")
