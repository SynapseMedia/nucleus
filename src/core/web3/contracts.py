from .blockchains import Contract, Blockchain


class NFT(Contract):
    def __init__(self, blockchain: Blockchain, address: str, abi: str):
        self.functions = blockchain.build_contract(address, abi).functions
        super().__init__(self, blockchain)

    def __getattr__(self, name):
        return self.functions[name]
