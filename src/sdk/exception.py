from werkzeug.exceptions import HTTPException


class EmptyCache(Exception):
    """Base class for exceptions in this module."""

    def __init__(self):
        _message = """
            No data to fetch.
            Please run resolvers to get metadata and try again.
            If REGEN_MOVIES is true a new dated version of metadata its generated.
            """

        super().__init__(_message)


class InvalidCID(Exception):
    """Base class for exceptions in this module."""

    def __init__(self):
        _message = """
                Invalid CID provided, please provide a v1 blake2b-208 IPFS CID.
                eg. bafyjvzacdlpl5pwtwiyvhm7pkyd4p55nq5vghfxfqbjwwj2lhkva
                """

        super().__init__(_message)


class InvalidRequest(HTTPException):
    code = 400
    description = 'Invalid request.'
