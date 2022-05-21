from abc import ABC, abstractmethod
from eth_account import Account

class Chain(ABC):
    
    @abstractmethod
    def connector(self):
        pass

    @property
    @abstractmethod
    def private_key(self):
        pass

    @property 
    @abstractmethod
    def nft_contract(self):
        pass


class Blockchain(ABC):
    def __init__(self, chain: Chain):
        self.chain = chain
        super().__init__()

    def set_default_account(self, account: Account):
        pass
    
    @abstractmethod
    def get_contract(self):
        pass

    @abstractmethod
    def sign_transaction(self):
        pass

    @abstractmethod
    def send_transaction(self):
        pass


class Contract(ABC):
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        super().__init__()

    def __getattr__(self, name):
        pass
    
