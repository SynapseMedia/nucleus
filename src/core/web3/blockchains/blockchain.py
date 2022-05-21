from web3 import Web3, types
from eth_account import Account
from .chains import EVM
from . import Blockchain


class Ethereum(Blockchain):
    """Ethereum blockchain type"""

    _instance = None

    def __init__(self, chain: EVM):
        self.web3 = Web3(chain.connector())
        super().__init__(chain)

    @staticmethod
    def get_instance(chain: EVM):
        """Singleton method to keep an unique instance
        
        :param chain: contextual chain object
        :return: Ethereum instance
        :rtype: Ethereum
        """
        if Ethereum._instance == None:
            Ethereum._instance = Ethereum(chain)
            return Ethereum._instance
        return Ethereum._instance

    def set_default_account(self, account: Account):
        self.web3.eth.default_account = account
        return account

    def sign_transaction(self, tx: types.TxParams):
        return self.web3.eth.account.sign_transaction(
            tx, private_key=self.chain.private_key
        )

    def send_transaction(self, tx: types.TxParams):
        # Return result from commit signed transaction
        signed_tx = self.sign_transaction(tx)
        return self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    def contract_factory(self, address, abi):
        return self.web3.eth.contract(
            # Contract address
            address=Web3.toChecksumAddress(address),
            # Abi from contract deployed
            abi=abi,
        )
