from web3 import Web3, types
from eth_account import Account
from .chains import EVM
from . import Network


class Ethereum(Network):
    """Ethereum network type"""

    web3: Web3

    def __init__(self):
        super().__init__()
        self.web3 = None

    def bind(self, chain: EVM):
        self.chain = chain
        # Connect network to chain provider
        self.web3 = Web3(chain.connector())
        return chain

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
        """Get transaction from network
        
        :param hash: Transaction hash
        :return: Transaction summary
        :rtype: EthereumTransaction
        """
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
