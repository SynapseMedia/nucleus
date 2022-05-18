from src.sdk.web3.factory import nft_contract, w3, Web3Wrapper
from src.sdk.web3.chain import RINKEBY, get_network_settings_by_name
from src.sdk.exception import InvalidProvider
import web3


def test_nft_contract_factory(monkeypatch):
    """Should return expected contract based on chain name"""
    wrapper, expected_contract = nft_contract(w3(RINKEBY), ".")
    assert isinstance(wrapper, Web3Wrapper)
    assert isinstance(expected_contract, web3.eth.Contract)


def test_w3_valid_provider():
    """Should return valid w3 wrapper with valid provider"""

    valid_chain = RINKEBY
    settings = get_network_settings_by_name(valid_chain)
    wrapper = w3(valid_chain)
    assert isinstance(wrapper, Web3Wrapper)
    assert isinstance(wrapper.w3, web3.Web3)
    assert wrapper.chain == RINKEBY
    assert wrapper.settings == settings


def test_w3_invalid_provider():
    """Should fail on bad contract chain name"""

    invalid_chain = "invalid"
    try:
        w3(invalid_chain)
    except Exception as e:
        assert isinstance(e, InvalidProvider)
