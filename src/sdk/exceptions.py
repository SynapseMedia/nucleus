from src.core.types import Any


class HarvestingError(Exception):
    """Exception raised for errors related to harvesting tasks"""

    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f"SDK :: Harvesting -> {message}"
        super(HarvestingError, self).__init__(self.message, *args, **kwargs)


class ProcessingError(Exception):
    """Exception raised for errors related to processing tasks"""

    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f"SDK :: Processing -> {message}"
        super(ProcessingError, self).__init__(self.message, *args, **kwargs)


class StorageError(Exception):
    """Exception raised for errors related to storage tasks"""

    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f"SDK :: Storage -> {message}"
        super(StorageError, self).__init__(self.message, *args, **kwargs)  # type: ignore


class ManagerError(HarvestingError):
    """Raised when a model fails to persist or interact with the underlying cache"""

    ...


class ModelValidationError(HarvestingError):
    """Raised when a model fails during schema validation"""

    ...


class EdgeServiceError(StorageError):
    """Raised when something fails when trying to operate on the edge services."""

    ...


class EngineError(ProcessingError):
    """Raised when something fail during media processing"""

    ...
