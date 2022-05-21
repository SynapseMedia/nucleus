from web3 import types
from src.core.web3.factory import w3
from src.core.constants import WALLET_PUBLIC_KEY
from src.core import logger


# TODO test this
def status(chain_id: int, tx: types.TxData):
    """Show generic transaction stats

    :param chain_id: Chain id eg. 4 -> Rinkeby
    :param tx: tx string hash
    """
    _w3 = w3(chain_id).web3
    tx_details = _w3.eth.get_transaction(tx)

    logger.log.info(f"Owner: {WALLET_PUBLIC_KEY}")
    logger.log.info(f"Tx Gas #: {tx_details.get('gas')}")
    logger.log.info(f"Tx Gas Price #: {tx_details.get('gasPrice')}")
    logger.log.info(f"Tx Block Hash: {tx_details.get('blockHash')}")
    logger.log.info(f"Tx Block #: {tx_details.get('blockNumber')}")
    logger.log.info(f"Tx Nonce #: {tx_details.get('nonce')}")
