from web3 import Web3
from web3.contract import Contract
from eth_typing.evm import Hash32

from eth_account import Account
from . import Network, Proxy, Chain
from ..types import Address, TxCall, Hash, Abi, PrivateKey
from ..exceptions import InvalidPrivateKey


class ProxyWeb3Contract(Proxy):
    interface: Contract

    def __init__(self, interface: Contract):
        self.interface = interface

    def __getattr__(self, name: str):
        return getattr(self.interface.functions, name)


class Ethereum(Network):
    """Ethereum network type"""

    web3: Web3
    chain: Chain

    def __init__(self, chain: Chain):
        self.web3 = Web3(chain.connector())
        self.chain = chain

    def set_default_account(self, private_key: PrivateKey):
        try:
            account = Account.from_key(private_key)
            self.web3.eth.default_account = account
        except ValueError as e:
            raise InvalidPrivateKey(str(e))

    def sign_transaction(self, tx: TxCall):
        return self.web3.eth.account.sign_transaction(
            tx, private_key=self.chain.private_key
        )

    def get_transaction(self, hash: Hash):
        assertion_hash = Hash32(hash)
        return self.web3.eth.get_transaction(assertion_hash)

    def send_transaction(self, tx: TxCall):
        # Return result from commit signed transaction
        signed_tx = self.sign_transaction(tx)
        transaction = signed_tx.rawTransaction
        return self.web3.eth.send_raw_transaction(transaction)

    def contract_factory(self, address: Address, abi: Abi):
        return ProxyWeb3Contract(
            self.web3.eth.contract(
                # Contract address
                address=Web3.toChecksumAddress(address),
                # Abi from contract deployed
                abi=abi,
            )
        )
