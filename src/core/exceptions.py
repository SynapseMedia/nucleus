"""
Observations: 
We need consistency with standard exceptions to help users to handle it in a predictive way.
 - Errors should never pass silently, even if it's just raising the underlying exception wrapped in our own exceptions.

"""


class IPFSRuntimeError(Exception):
    def __init__(self, message: str):
        self.message = f"Core :: IPFS -> {message}"


class ConnectionError(Exception):
    def __init__(self, message: str):
        self.message = f"Core :: Cache -> {message}"
