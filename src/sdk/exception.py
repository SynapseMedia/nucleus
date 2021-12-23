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


class InvalidVideoQuality(Exception):
    """Base class for exceptions in this module."""

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
    """Base class for exceptions in this module."""

    def __init__(self):
        _message = """
                Invalid image size provided.
                Master image should be at least:
                    (width, height) = (750, 500)
                """

        super().__init__(_message)


class IpfsFailedExecution(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message=""):
        _message = f"""
                Failed execution: {message}
                """

        super().__init__(_message)


class InvalidRequest(Exception):
    code = 400
    description = "Invalid request."
