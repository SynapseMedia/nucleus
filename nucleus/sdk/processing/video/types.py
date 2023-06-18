from __future__ import annotations

from nucleus.core.types import Protocol, Settings


class Codec(Settings, Protocol):
    """Codec specify the behavior of video compression formats."""

    def __contains__(self, codec: str) -> bool:
        """Check if the available codecs contain the specified codec.
        This method can be useful to avoid re-encoding by checking if a codec match exists
        allowing for a direct copy operation.

        :param codec: The name of the codec to match
        :returns: True if match else False
        """
        ...
