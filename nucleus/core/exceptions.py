"""
Observations:
We need consistency with standard exceptions to help users to handle it in a predictive way.
 - Errors should never pass silently, even if it's just raising the underlying exception wrapped in our own exceptions.

"""


class HttpError(Exception):
    """Exception raised for errors relation to http operations."""

    def __init__(self, message: str):
        self.message = f'Core :: Http -> {message}'


class IPFSRuntimeError(Exception):
    """Exception raised for errors related to ipfs API."""

    def __init__(self, message: str):
        self.message = f'Core :: IPFS -> {message}'


class DatabaseError(Exception):
    """Exception raised for errors that are related to the database."""

    def __init__(self, message: str):
        self.message = f'Core :: Cache -> {message}'


class DatabaseTransactionError(DatabaseError):
    """Exception raised for errors that are related to database transaction.
    DatabaseTransactionError error is a subclass from DatabaseError.
    """

    ...
