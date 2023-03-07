import requests
from src.core.types import Any


class GenericProcessingException(Exception):
    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f"SDK :: Processing -> {message}"
        super(
            GenericProcessingException,
            self).__init__(
            self.message,
            *args,
            **kwargs)


class GenericEdgeException(requests.exceptions.HTTPError):
    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f"SDK :: Storage -> {message}"
        super(GenericEdgeException, self).__init__(
            self.message, *args, **kwargs
        )  # type: ignore


class PinException(GenericEdgeException):
    """Raised when something fail trying to pin any CID into edge services"""

    ...


class ProcessingException(GenericProcessingException):
    """Standard exception to raise when something fail during processing"""

    ...
