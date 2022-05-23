import pytest
import web3
import eth_account
import hexbytes
from web3 import Web3
from src.core.web3.contracts import NFT
from src.core.web3.blockchain import Ethereum
from src.core.web3.chains import Rinkeby, Kovan
from src.core.exception import InvalidChain, InvalidPrivateKey
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
    expected_contract = contract(4, 1155)
    assert isinstance(expected_contract, NFT)

    with pytest.raises(InvalidChain):
        contract(0, 1155)


def test_w3_valid_provider():
    """Should return valid w3 wrapper with valid provider"""

    rinkeby = chain(4)
    kovan = chain(42)

    assert isinstance(rinkeby, Rinkeby)
    assert isinstance(kovan, Kovan)


def test_w3_invalid_provider():
    """Should fail on bad contract chain name"""

    invalid_chain = "invalid"
    with pytest.raises(InvalidChain):
        w3(invalid_chain)


def test_kovan_chain():
    """Should return expected assets and connector for kovan network"""
    kovan = chain(42)
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
    rinkeby = chain(4)
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


def test_blockchain():
    """Should return expected blockchain based on chain id"""
    # first object
    from_rinkeby = network(4)
    # second object = first object
    from_kovan = network(42)

    assert isinstance(from_rinkeby, Ethereum)
    assert isinstance(from_kovan, Ethereum)

    # Check if chain persisting
    assert isinstance(from_rinkeby.chain, Rinkeby)
    # expected equal objects
    # Singleton create a single global object
    assert from_rinkeby == from_kovan

    # Expected error trying to find kovan with same object
    # First object was created with rinkeby, second object keep same
    with pytest.raises(AssertionError):
        assert isinstance(from_kovan.chain, Kovan)
