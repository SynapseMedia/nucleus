import pytest
import web3
import eth_account
import hexbytes
from web3 import Web3
from src.sdk.exception import InvalidProvider, InvalidPrivateKey
from src.sdk.web3.factory import (
    w3,
    nft_contract,
    account,
    chain,
    _kovan,
    _rinkeby,
    Web3Wrapper,
    ChainWrapper,
)

from src.sdk.constants import (
    KOVAN_PROVIDER,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_CONTRACT_NFT,
    KOVAN_CONTRACT_NFT,
    RINKEBY_ALCHEMY_API_KEY,
    WALLET_KEY,
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
    w3, expected_contract = nft_contract("rinkeby", ".")
    assert isinstance(expected_contract, web3.eth.Contract)
    assert isinstance(w3, web3.Web3)


def test_w3_valid_provider():
    """Should return valid w3 wrapper with valid provider"""

    valid_chain = "rinkeby"
    settings = chain(valid_chain)
    # w3 use default wallet key
    wrapper = w3(valid_chain)
    # Using default wallet key
    expected_account = account()

    assert isinstance(wrapper, Web3Wrapper)
    assert isinstance(wrapper.web3, web3.Web3)
    assert wrapper.web3.eth.default_account == expected_account
    assert wrapper.name == "rinkeby"
    
    assert isinstance(wrapper.chain, ChainWrapper)
    assert wrapper.chain.nft == settings.nft
    assert wrapper.chain.connector == settings.connector
    assert wrapper.chain.private_key == settings.private_key


def test_w3_invalid_provider():
    """Should fail on bad contract chain name"""

    invalid_chain = "invalid"
    with pytest.raises(InvalidProvider):
        w3(invalid_chain)


def test_kovan_chain():
    """Should return expected uri for kovan network"""
    expected_value = f"{KOVAN_PROVIDER}/{KOVAN_ALCHEMY_API_KEY}"
    assert _kovan().endpoint_uri == Web3.HTTPProvider(expected_value).endpoint_uri


def test_rinkeby_chain():
    """Should return expected uri for rinkeby network"""
    expected_value = f"{RINKEBY_PROVIDER}/{RINKEBY_ALCHEMY_API_KEY}"
    assert _rinkeby().endpoint_uri == Web3.HTTPProvider(expected_value).endpoint_uri


def test_chain():
    """Should return expected network setting based on network name"""
    kovan = ChainWrapper(_kovan, KOVAN_CONTRACT_NFT, WALLET_KEY)
    rinkeby = ChainWrapper(_rinkeby, RINKEBY_CONTRACT_NFT, WALLET_KEY)
    
    assert isinstance(chain("rinkeby"), ChainWrapper)
    assert isinstance(chain("kovan"), ChainWrapper)
    
    assert chain("rinkeby").connector == rinkeby.connector
    assert chain("rinkeby").private_key == rinkeby.private_key
    assert chain("rinkeby").nft == rinkeby.nft
    
    assert chain("kovan").connector == kovan.connector
    assert chain("kovan").private_key == kovan.private_key
    assert chain("kovan").nft == kovan.nft

    with pytest.raises(InvalidProvider):
        chain("invalid")
