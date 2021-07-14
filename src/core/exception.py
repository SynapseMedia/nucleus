class EmptyCache(Exception):
    """Base class for exceptions in this module."""

    def __init__(self):
        _message = """ 
            No data to fetch.
            Please run resolvers to get metadata and try again. 
            If REGEN_MOVIES is true a new dated version of metadata its generated.
            """

        super().__init__(_message)
