class IPFSRuntimeException(Exception):
    def __init__(self, message: str):
        self.message = f"Core :: IPFS -> {message}"
