from web3 import Web3
from src.sdk.web3.chain import _kovan, _rinkeby, get_network_settings_by_name
from src.sdk.constants import (
    KOVAN_PROVIDER,
    KOVAN_ALCHEMY_API_KEY,
    RINKEBY_PROVIDER,
    RINKEBY_CONTRACT_NFT,
    KOVAN_CONTRACT_NFT,
    RINKEBY_ALCHEMY_API_KEY,
)


def test_kovan_chain():
    """Should return expected uri for kovan network"""
    expected_value = f"{KOVAN_PROVIDER}/{KOVAN_ALCHEMY_API_KEY}"
    assert _kovan().endpoint_uri == Web3.HTTPProvider(expected_value).endpoint_uri


def test_rinkeby_chain():
    """Should return expected uri for rinkeby network"""
    expected_value = f"{RINKEBY_PROVIDER}/{RINKEBY_ALCHEMY_API_KEY}"
    assert _rinkeby().endpoint_uri == Web3.HTTPProvider(expected_value).endpoint_uri


def test_get_network_settings_by_name():
    """Should return expected network setting based on network name"""
    kovan = {"connect": _kovan, "nft": KOVAN_CONTRACT_NFT}
    rinkeby = {"connect": _rinkeby, "nft": RINKEBY_CONTRACT_NFT}
    assert get_network_settings_by_name("rinkeby") == rinkeby
    assert get_network_settings_by_name("kovan") == kovan
    assert get_network_settings_by_name("invalid") is None
