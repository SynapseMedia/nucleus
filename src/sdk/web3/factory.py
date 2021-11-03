from src.sdk import util
from src.sdk.constants import WALLET_KEY

from . import chain
from web3 import Web3


def w3(chain_name):
    """
    Build Web3 interface with provider settings
    :param chain_name: Kovan, mainnet, rinkeby...
    """
    chain_settings = chain.get_network_settings_by_name(chain_name)
    if not chain_settings:  # Fail if not supported provided
        raise ConnectionError("Invalid provider entered")
    _w3 = Web3(chain_settings["connect"]())
    _w3.eth.default_account = _w3.eth.account.privateKeyToAccount(WALLET_KEY).address
    return _w3


def nft_contract(chain_name):
    """
    Create contract NFT configuration for provider
    :param chain_name: the provider name
    :return: web3.Contract
    """
    _w3 = w3(chain_name)
    _chain = chain.get_network_settings_by_name(chain_name)
    chain_contract_nft = _chain.get("nft")
    abi = util.read_json("/data/watchit/abi/WNFT.json")

    return _w3, _w3.eth.contract(
        address=Web3.toChecksumAddress(chain_contract_nft), 
        abi=abi.get("abi")
    )
