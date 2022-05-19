from src.sdk.web3.factory import nft_contract, w3, Web3Wrapper
from src.sdk.web3.chain import get_network_settings_by_name
from src.sdk.exception import InvalidProvider
import web3


def test_nft_contract_factory(monkeypatch):
    """Should return expected contract based on chain name"""
    w3, expected_contract = nft_contract('rinkeby', ".")
    assert isinstance(expected_contract, web3.eth.Contract)
    assert isinstance(w3, web3.Web3)


def test_w3_valid_provider():
    """Should return valid w3 wrapper with valid provider"""

    valid_chain = 'rinkeby'
    settings = get_network_settings_by_name(valid_chain)
    wrapper = w3(valid_chain)
    assert isinstance(wrapper, Web3Wrapper)
    assert isinstance(wrapper.web3, web3.Web3)
    assert wrapper.chain == 'rinkeby'
    assert wrapper.settings == settings


def test_w3_invalid_provider():
    """Should fail on bad contract chain name"""

    invalid_chain = "invalid"
    try:
        w3(invalid_chain)
    except Exception as e:
        assert isinstance(e, InvalidProvider)
