from src.sdk.constants import WALLET_KEY
from .factory import nft_contract
from .crypto import cid_to_uint256
from .. import logger


def _send_tx(w3, tx):
    """Commit transaction to blockchain

    :param w3: web3.Web3
    :param tx: web3.types.TxParams
    """
    signed_txn = w3.eth.account.sign_transaction(tx, private_key=WALLET_KEY)
    tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.log.info(f"TX: {tx.hex()}")
    return tx


def mint(to: str, cid, chain_name="kovan"):
    """Mint token to address based on cid in defined chain

    :param to: receptor
    :param cid: IPFS cid
    :param chain_name: chain where mint the token
    :return: Transaction Address, Receptor Address, CID
    """

    logger.log.info(f"Minting CID {cid} in {chain_name}")
    w3, contract = nft_contract(chain_name)
    owner = w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = w3.eth.getTransactionCount(owner.address)

    uint256_cid = cid_to_uint256(cid)  # Format base16 => hex => int
    transaction = contract.functions.mint(
        to, uint256_cid  # owner, cid uint256
    ).buildTransaction({"nonce": nonce})

    tx = _send_tx(w3, transaction)
    return tx.hex(), to, cid


def mint_batch(to: str, cid_list: list, chain_name="kovan"):
    """Mint batch token to address based on cid list in defined chain

    :param to: Receptor address
    :param cid_list: IPFS cid list
    :param chain_name: Chain name eg. Rinkeby
    :return: Transaction Address, Receptor Address, CID List
    """
    w3, contract = nft_contract(chain_name)
    owner = w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = w3.eth.getTransactionCount(owner.address)

    uint256_cid_list = [
        cid_to_uint256(x) for x in cid_list
    ]  # Format base16 => hex => int

    transaction = contract.functions.mintBatch(
        to, uint256_cid_list  # owner, cid uint256
    ).buildTransaction({"nonce": nonce})

    tx = _send_tx(w3, transaction)
    return tx.hex(), to, cid_list


def set_holder(to: str, cid: str, chain_name="kovan"):
    """Mint batch token to address based on cid list in defined chain

    :param to: Receptor address
    :param cid: IPFS cid
    :param chain_name: Chain name eg. Rinkeby
    :return: Transaction Address, Receptor Address
    """
    w3, contract = nft_contract(chain_name)
    owner = w3.eth.account.privateKeyToAccount(WALLET_KEY)
    nonce = w3.eth.getTransactionCount(owner.address)

    uint256_cid = cid_to_uint256(cid)  # Format base16 => hex => int
    # Format base16 => hex => int
    transaction = contract.functions.setHolder(
        uint256_cid, to  # cid uint256, holder
    ).buildTransaction({"nonce": nonce})

    tx = _send_tx(w3, transaction)
    return tx.hex(), to
