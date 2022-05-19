from src.sdk.web3.factory import nft_contract, w3, account, Web3Wrapper
from src.sdk.web3.chain import get_network_settings_by_name
from src.sdk.exception import InvalidProvider, InvalidPrivateKey
from eth_keys.exceptions import ValidationError
import web3
import eth_account
import hexbytes


def test_valid_account():
    """Should return a valid Account key if valid key is provided"""
    wallet_key = "3ee90d8549b9b0293df40346106c81bc7eac663e799d97cb872b024186e70da0"
    wallet_account = account(wallet_key)
    expected = eth_account.Account.from_key(wallet_key)
    assert hexbytes.HexBytes("0x%s" % wallet_key) == wallet_account.key
    assert wallet_account == expected


def test_invalid_account():
    """Should return a valid Account key if valid key is provided"""
    wallet_key = "3ee90d8549b9b0293df40346106"
    try:
        account(wallet_key)
    except Exception as e:
        assert isinstance(e, ValidationError)

    try:
        account("")
    except Exception as e:
        assert isinstance(e, InvalidPrivateKey)


def test_invalid_account():
    """Should return a valid Account key if valid key is provided"""
    wallet_key = hexbytes.HexBytes(
        "0x3ee90d8549b9b0293df40346106c81bc7eac663e799d97cb872b024186e70da0"
    )
    expected = eth_account.Account.from_key(wallet_key)
    assert wallet_key == expected.key


def test_nft_contract_factory(monkeypatch):
    """Should return expected contract based on chain name"""
    w3, expected_contract = nft_contract("rinkeby", ".")
    assert isinstance(expected_contract, web3.eth.Contract)
    assert isinstance(w3, web3.Web3)


def test_w3_valid_provider():
    """Should return valid w3 wrapper with valid provider"""

    valid_chain = "rinkeby"
    settings = get_network_settings_by_name(valid_chain)
    # w3 use default wallet key
    wrapper = w3(valid_chain)
    # Using default wallet key
    expected_account = account()

    assert isinstance(wrapper, Web3Wrapper)
    assert isinstance(wrapper.web3, web3.Web3)
    assert wrapper.web3.eth.default_account == expected_account
    assert wrapper.chain == "rinkeby"
    assert wrapper.settings == settings


def test_w3_invalid_provider():
    """Should fail on bad contract chain name"""

    invalid_chain = "invalid"
    try:
        w3(invalid_chain)
    except Exception as e:
        assert isinstance(e, InvalidProvider)
