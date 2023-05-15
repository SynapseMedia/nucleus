from nucleus.core.types import Protocol, Literal

Claims = Literal["s", "d", "t"]


class Metadata(Protocol):
    """Metadata defines the expected behavior of metadata types.
    Examples of metadata types include:

    - Descriptive
    - Structural
    - Technical

    """

    def __str__(self) -> Claims:
        """Metadata types MUST return the specified claims as a string.
        Examples of valid claims include: s, t, d
        """
        ...


class Serializer(Protocol):
    """Serializer specifies the methods needed to handle SEP001 serialization.
    Defines how to handle serialization for each strategy according to the specification, which includes:

    - Compact
    - DAG-JOSE

    This template class must be implemented by other classes that provide concrete serialization logic.
    ref: https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    ...


__all__ = ()
