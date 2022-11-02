


class InvalidQuery(ValueError):
    """Raised trying to build query"""
    def __init__(self):
        message = """
            Invalid query to fetch.
            Please build the query before use it.
            """

        super().__init__(message)


class InvalidMutation(ValueError):
    """Raised trying to save a not set mutation."""

    def __init__(self):
        message = """
            Invalid mutation to save.
            Please build the query before use it.
            """

        super().__init__(message)
