import pytest
import web3
import eth_account
import hexbytes
from web3 import Web3
from src.core.web3.contracts import ERC1155
from src.core.web3.network import Ethereum
from src.core.web3.chains import Rinkeby, Kovan
from src.core.web3 import ContractID, ChainID, NetworkID, Chain

from src.core.web3.factory import contract, account, chain, network
from src.core.constants import (
    KOVAN_PROVIDER,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
)

from src.core.exceptions import (
    InvalidPrivateKey,
    InvalidContract,
    InvalidNetwork,
)


class InvalidEVM(Chain):
    def __str__(self):
        pass

    @property
    def id(self):
        pass

    def connector(self):
        pass

    @property
    def erc1155(self):
        pass

    @property
    def private_key(self):
        pass


def test_valid_account():
    """Should return a valid Account key if valid key is provided"""
    wallet_key = "8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f"
    wallet_account = account(wallet_key)
    expected = eth_account.Account.from_key(wallet_key)
    assert hexbytes.HexBytes("0x%s" % wallet_key) == wallet_account.key
    assert wallet_account == expected


def test_invalid_account():
    """Should return a valid Account key if valid key is provided"""
    wallet_key = "3ee90d8549b9b0293df40346106"
    with pytest.raises(InvalidPrivateKey):
        account(wallet_key)


def test_nft_contract_factory():
    """Should return expected contract based on chain name"""
    # Chain rinkeby and ERC1155 standard
    chain = Rinkeby()
    ethereum = Ethereum(chain)

    expected_contract = contract(ContractID.ERC1155, network=ethereum)
    assert isinstance(expected_contract, ERC1155)
    assert isinstance(expected_contract.network, Ethereum)


def test_nft_contract_factory_with_invalid_network():
    """Should fail for invalid network"""
    # Chain rinkeby and ERC1155 standard
    with pytest.raises(TypeError):
        # passing chain instance should fail
        contract(ContractID.ERC1155, network=Rinkeby())


def test_nft_invalid_contract():
    """Should return error with invalid contract"""
    # Chain rinkeby and ERC1155 standard
    with pytest.raises(InvalidContract):
        contract(1155, network=None)


def test_kovan_chain():
    """Should return expected assets and connector for kovan network"""
    kovan = chain(ChainID.Kovan)
    assert isinstance(kovan.connector(), web3.HTTPProvider)

    expected_value = f"{KOVAN_PROVIDER}/{KOVAN_ALCHEMY_API_KEY}"
    assert (
        kovan.connector().endpoint_uri == Web3.HTTPProvider(expected_value).endpoint_uri
    )
    assert kovan.erc1155 == "0x0B33Fe1Bb738B7c3e981978d7E5a9f2b980853Ed"
    assert (
        kovan.private_key
        == "8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f"
    )


def test_rinkeby_chain():
    """Should return expected assets and connector for rinkeby network"""
    rinkeby = chain(ChainID.Rinkeby)
    assert isinstance(rinkeby.connector(), web3.HTTPProvider)

    expected_value = f"{RINKEBY_PROVIDER}/{RINKEBY_ALCHEMY_API_KEY}"
    assert (
        rinkeby.connector().endpoint_uri
        == Web3.HTTPProvider(expected_value).endpoint_uri
    )
    assert rinkeby.erc1155 == "0x58Aa6dD8aA078385496441F3ABa691d472feBaF5"
    assert (
        rinkeby.private_key
        == "8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f"
    )


def test_network():
    """Should return expected network based on network id"""

    _network = network(NetworkID.Ethereum, chain=Kovan())
    assert isinstance(_network, Ethereum)


def test_valid_network_with_invalid_chain():
    """Should raise error with valid network id and invalid chain"""

    with pytest.raises(TypeError):
        # Returned network based on chain
        network(NetworkID.Ethereum, chain=InvalidEVM())


def test_invalid_network():
    """Should raise error with invalid network id"""

    with pytest.raises(InvalidNetwork):
        # Returned network based on chain
        network(0, chain=None)