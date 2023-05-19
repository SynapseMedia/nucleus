from nucleus.core.types import Any


class HarvestingError(Exception):
    """Exception raised for errors related to harvesting tasks"""

    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f'SDK :: Harvesting -> {message}'
        super().__init__(self.message, *args, **kwargs)


class ProcessingError(Exception):
    """Exception raised for errors related to processing tasks"""

    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f'SDK :: Processing -> {message}'
        super().__init__(self.message, *args, **kwargs)


class StorageError(Exception):
    """Exception raised for errors related to storage tasks"""

    def __init__(self, message: str, *args: Any, **kwargs: Any):
        self.message = f'SDK :: Storage -> {message}'
        super().__init__(self.message, *args, **kwargs)  # type: ignore


class ModelManagerError(HarvestingError):
    """Raised when a model fails to persist or interact with the underlying cache.
    ModelManagerError error is a subclass from HarvestingError.
    """

    ...


class ModelValidationError(HarvestingError):
    """Raised when a model fails during schema validation.
    ModelValidationError error is a subclass from HarvestingError.
    """

    ...


class StorageServiceError(StorageError):
    """Raised when something fails when trying to operate on the edge services.
    StorageServiceError error is a subclass from StorageError.
    """

    ...


class ProcessingEngineError(ProcessingError):
    """Raised when something fail during media processing.
    ProcessingEngineError error is a subclass from ProcessingError.
    """

    ...


class FFProbeError(ProcessingError):
    """Raised when something fail during ffprobe call.
    FFProbeError error is a subclass from ProcessingError.
    """

    ...
