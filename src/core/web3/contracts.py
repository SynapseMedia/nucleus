from . import Contract, Network, Proxy
from ..constants import PROJECT_ROOT
from ..util import read_json
from ..types import Directory, Address


class ERC1155(Contract):
    """ERC1155 contract type"""

    _address: Address
    _network: Network
    _proxy: Proxy

    def __init__(self, network: Network):
        self._network = network
        self._address = network._chain.erc1155
        # dynamic callable function handled by attribute accessor
        self._proxy = network.contract_factory(self._address, self.abi)

    def __getattr__(self, name: str):
        return getattr(self._proxy, name)

    @property
    def abi(self):
        """Return abi from json for NFT contract"""
        abi_json = read_json(Directory("%s/abi/WNFT.json" % PROJECT_ROOT))
        return abi_json["abi"]
