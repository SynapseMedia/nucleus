from web3 import Web3, types
from eth_account import Account
from .chains import EVM
from . import Network


class Ethereum(Network):
    """Ethereum network type"""

    web3: Web3

    def __init__(self, chain: EVM):
        # Connect network to chain provider
        if not isinstance(chain, EVM):
            raise TypeError("provided `chain` for ethereum network not supported")
        
        super().__init__(chain)
        self.web3 = Web3(chain.connector())

    def set_default_account(self, account: Account):
        self.web3.eth.default_account = account
        return account

    # TODO Receive as param generic type to support different networks
    def sign_transaction(self, tx: types.TxParams):
        return self.web3.eth.account.sign_transaction(
            tx, private_key=self.chain.private_key
        )

    # TODO return EthereumTransaction
    def get_transaction(self, hash: types._Hash32):
        return self.web3.eth.get_transaction(hash)

    def send_transaction(self, tx: types.TxParams):
        # Return result from commit signed transaction
        signed_tx = self.sign_transaction(tx)
        transaction = signed_tx.rawTransaction
        return self.web3.eth.send_raw_transaction(transaction)

    def contract(self, address: str, abi: str):
        return self.web3.eth.contract(
            # Contract address
            address=Web3.toChecksumAddress(address),
            # Abi from contract deployed
            abi=abi,
        )
