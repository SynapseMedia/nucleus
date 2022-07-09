from web3 import Web3, types
from ..constants import WALLET_PUBLIC_KEY
from .. import logger


# TODO test this
def status(w3: Web3, tx: types.TxData):
    """Show generic transaction stats

    :param w3: web3 interface
    :param tx: tx string hash
    """

    tx_details = w3.web3.eth.get_transaction(tx)
    logger.log.info(f"Owner: {WALLET_PUBLIC_KEY}")
    logger.log.info(f"Tx Gas #: {tx_details.get('gas')}")
    logger.log.info(f"Tx Gas Price #: {tx_details.get('gasPrice')}")
    logger.log.info(f"Tx Block Hash: {tx_details.get('blockHash')}")
    logger.log.info(f"Tx Block #: {tx_details.get('blockNumber')}")
    logger.log.info(f"Tx Nonce #: {tx_details.get('nonce')}")
