import pytest
import web3
import eth_account
import hexbytes
from web3 import Web3
from src.core.web3.contracts import NFT
from src.core.web3.network import Ethereum
from src.core.web3.chains import Rinkeby, Kovan
from src.core.web3 import ContractStandards, ChainID
from src.core.exception import InvalidChain, InvalidPrivateKey, InvalidContract
from src.core.web3.factory import w3, contract, account, chain, network

from src.core.constants import (
    KOVAN_PROVIDER,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_ALCHEMY_API_KEY,
)


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


def test_nft_contract_factory(monkeypatch):
    """Should return expected contract based on chain name"""
    # Chain rinkeby and ERC1155 standard
    network = Ethereum(Rinkeby())
    expected_contract = contract(network, ContractStandards.ERC1155)
    assert isinstance(expected_contract, NFT)


def test_nft_invalid_contract(monkeypatch):
    """Should return error with invalid contract"""
    # Chain rinkeby and ERC1155 standard
    with pytest.raises(InvalidContract):
        contract(0, 1155)


def test_w3_valid_provider():
    """Should return valid w3 with valid chain1"""

    network = w3(ChainID.Rinkeby)
    private_key = account(network.chain.private_key)
    
    assert isinstance(network, Ethereum)
    assert private_key == network.web3.eth.default_account


def test_w3_invalid_provider():
    """Should fail on bad contract chain name"""

    invalid_chain = "invalid"
    with pytest.raises(InvalidChain):
        w3(invalid_chain)


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
    """Should return expected network based on chain id"""
    # first object
    rinkeby = chain(ChainID.Rinkeby)
    kovan = chain(ChainID.Kovan)
    
    # Returned network based on chain
    from_rinkeby = network(rinkeby)
    from_kovan = network(kovan)

    assert isinstance(from_rinkeby, Ethereum)
    assert isinstance(from_kovan, Ethereum)

    # Check if chain persisting
    assert isinstance(from_rinkeby.chain, Rinkeby)
    assert isinstance(from_kovan.chain, Kovan)

def test_invalid_network():
    """Should raise error with invalid chain"""

    with pytest.raises(InvalidChain):
        # first object
        invalid = chain(0)
        # Returned network based on chain
        network(invalid)