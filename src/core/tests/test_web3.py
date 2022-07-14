import web3
import eth_account
from web3 import Web3
from src.core.web3.contracts import ERC1155
from src.core.web3.network import Ethereum
from src.core.web3.chains import Rinkeby, Goerli
from src.core.web3.crypto import to_hex, cid_to_uint256

from src.core.types import CIDStr
from src.core.web3.types import Connector
from src.core.constants import (
    GOERLI_PROVIDER,
    GOERLI_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
)


class InvalidEVM:
    def __str__(self):
        return "fake"

    @property
    def endpoint(self):
        return ""

    @property
    def id(self):
        pass

    @property
    def provider(self):
        pass

    @property
    def erc1155(self):
        pass

    @property
    def private_key(self):
        pass


def test_valid_account_for_network():
    """Should return a valid Account key if valid key is provided"""
    wallet_key = "8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f"
    _chain = Goerli()
    _network = Ethereum(_chain)
    _network.set_default_account(wallet_key)

    expected = eth_account.Account.from_key(wallet_key)
    assert _network._web3.eth.default_account == expected  # type: ignore


def test_nft_contract_factory():
    """Should return expected contract based on chain name"""
    # Chain rinkeby and ERC1155 standard
    _chain = Rinkeby()
    _network = Ethereum(_chain)
    expected_contract = ERC1155(_network)
    assert isinstance(expected_contract, ERC1155)


def test_goerli_chain():
    """Should return expected assets and connector for goerli network"""
    kovan = Goerli()
    connector: Connector = kovan.provider()
    provider = connector(kovan.endpoint)
    assert isinstance(provider, web3.HTTPProvider)

    expected_value = f"{GOERLI_PROVIDER}/{GOERLI_ALCHEMY_API_KEY}"
    assert provider.endpoint_uri == Web3.HTTPProvider(expected_value).endpoint_uri
    assert kovan.erc1155 == "0x0B33Fe1Bb738B7c3e981978d7E5a9f2b980853Ed"
    assert (
        kovan.private_key
        == "8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f"
    )


def test_rinkeby_chain():
    """Should return expected assets and connector for rinkeby network"""
    rinkeby = Rinkeby()
    connector: Connector = rinkeby.provider()
    provider = connector(rinkeby.endpoint)
    assert isinstance(provider, web3.HTTPProvider)

    expected_value = f"{RINKEBY_PROVIDER}/{RINKEBY_ALCHEMY_API_KEY}"
    assert provider.endpoint_uri == Web3.HTTPProvider(expected_value).endpoint_uri
    assert rinkeby.erc1155 == "0x58Aa6dD8aA078385496441F3ABa691d472feBaF5"
    assert (
        rinkeby.private_key
        == "8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f"
    )



def test_cid_to_uint256():
    """Should return expected output uint256 in deterministic way from input"""
    current_value = CIDStr("bafyjvzacdk3rngktzetikg3w2gf7nxvxsq5y4t4xryzijalyazsa")
    expected_value = (
        651268735865305864933405567136027539147782079973983219801233220330061301348
    )
    assert cid_to_uint256(current_value) == expected_value


def test_to_hex():
    """Should return expected output hex in deterministic way from input"""
    current_value = "bafyjvzacdk3rngktzetikg3w2gf7nxvxsq5y4t4xryzijalyazsa"
    expected_value = (
        "0x626166796a767a6163646b33726e676b747a6574696b673"
        "377326766376e787678737135793474347872797a696a616c79617a7361"
    )
    assert to_hex(current_value.encode()) == expected_value
