from . import chain
from .. import util
from ..constants import WALLET_KEY, PROJECT_ROOT

from web3 import Web3


def w3(chain_name: str):
    """Build Web3 interface with provider settings

    :param chain_name: kovan, mainnet, rinkeby...
    :return: web3 interface with provider settings
    :rtype: web3.Web3
    """
    chain_settings = chain.get_network_settings_by_name(chain_name)
    if not chain_settings:  # Fail if not supported provided
        raise ConnectionError("Invalid provider entered")
    
    # Connect to provider based on chain settings    
    _w3 = Web3(chain_settings["connect"]())
    # Set default account for current WALLET_KEY settings
    _w3.eth.default_account = _w3.eth.account.privateKeyToAccount(WALLET_KEY).address
    return _w3


def nft_contract(chain_name: str):
    """Factory NFT contract based on provider settings

    :param chain_name: kovan, mainnet, rinkeby...
    :return: nft contract
    :rtype: web3.Contract
    """
    _w3 = w3(chain_name)
    chain_settings = chain.get_network_settings_by_name(chain_name)

    if not chain_settings:  # Fail if not supported provided
        raise ConnectionError("Invalid provider entered")

    # Get contract address based on chain settings
    chain_contract_nft = chain_settings.get("nft")
    abi = util.read_json("%s/abi/WNFT.json" % PROJECT_ROOT)

    return _w3, _w3.eth.contract(
        # Contract address
        address=Web3.toChecksumAddress(chain_contract_nft),
        # Abi from contract deployed
        abi=abi.get("abi"),
    )
