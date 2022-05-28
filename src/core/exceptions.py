class EmptyCache(Exception):
    """Raised trying to process empty cache."""

    def __init__(self):
        _message = """
            No data to fetch.
            Please run resolvers to get metadata and try again.
            If REGEN_MOVIES is true a new dated version of metadata its generated.
            """

        super().__init__(_message)


class InvalidCID(Exception):
    """Raised when a invalid CID is encountered."""

    def __init__(self):
        _message = """
                Invalid CID provided, please provide a v1 blake2b-208 IPFS CID.
                eg. bafyjvzacdlpl5pwtwiyvhm7pkyd4p55nq5vghfxfqbjwwj2lhkva
                """

        super().__init__(_message)


class InvalidStreamingProtocol(Exception):
    """Raised when a invalid/not existing video protocol is set."""

    def __init__(self):
        _message = """
                Invalid protocol provided. 
                Allowed protocol from enum:
                    Protocol.HLS
                    Protocol.DASH
                """

        super().__init__(_message)


class InvalidVideoQuality(Exception):
    """Raised when a invalid/not existing video quality is set."""

    def __init__(self):
        _message = """
                Invalid master video resolution provided.
                Allowed sizes:
                    Size(640, 360): '360p',
                    Size(854, 480): '480p',
                    Size(1280, 720): '720p',
                    Size(1920, 1080): '1080p',
                    Size(2560, 1440): '2k',
                    Size(3840, 2160): '4k'
                """

        super().__init__(_message)


class InvalidImageSize(Exception):
    """Raised if a processing image hasn't the expected ratio."""

    def __init__(self):
        _message = """
                Invalid image size provided.
                Master image should be at least:
                    (width, height) = (500, 750)
                """

        super().__init__(_message)


class IPFSFailedExecution(Exception):
    """Raised on IPFS command execution fail."""

    def __init__(self, message: str = ""):
        _message = f"""
                Failed execution: {message}
                """

        super().__init__(_message)


class InvalidChain(Exception):
    """Raised when an invalid chain is requested."""

    def __init__(self, message: str = ""):
        _message = f"""
                Invalid chain: {message}
                """

        super().__init__(_message)


class InvalidNetwork(Exception):
    """Raised when an invalid network is requested."""

    def __init__(self, message: str = ""):
        _message = f"""
                Not supported network: {message}
                """

        super().__init__(_message)


class InvalidContract(Exception):
    """Raised when an invalid contract is requested."""

    def __init__(self, message: str = ""):
        _message = f"""
                Not supported contract: {message}
                """

        super().__init__(_message)


class InvalidPrivateKey(Exception):
    """Raised when an invalid private is provided."""

    def __init__(self, message: str = ""):
        _message = f"""
                Invalid wallet private key: {message}
                """

        super().__init__(_message)


class InvalidRequest(Exception):
    code = 400
    description = "Invalid request."
