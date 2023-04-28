from nucleus.core.types import Protocol, Literal


class Metadata(Protocol):
    """Metadata defines the expected behavior of contained metadata types.
    eg:
        - Descriptive
        - Structural
        - Technical
    """

    def __str__(self) -> Literal["s", "d", "t"]:
        """Metadata types MUST return the  specified claims"""
        ...


class SEP(Protocol):
    """Specifies the behaviors of SEPs implementations"""

    def add_metadata(self, meta: Metadata):
        """Proxy procedure to add metadata into payload

        :param meta: the metadata type to store in payload
        :return: none
        :rtype: None
        """
        ...
