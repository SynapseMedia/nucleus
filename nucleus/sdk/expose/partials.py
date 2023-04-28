from .marshall import StdDist
from .standard import SEP001, Header, Payload


def marshall(std: SEP001) -> StdDist:
    """MarshallDistributor factory

    :param std: the type of media to expose
    :return: MarshallDistributor object
    :rtype: MarshallDistributor
    """
    return StdDist(std)


def public(type: str) -> SEP001:
    """SEP001 factory

    :param type: the type of media to expose
    :return: new standard implementation sep-001 object
    :rtype: SEP001
    """

    return SEP001(Header(type), Payload())


__all__ = (
    "public",
    "marshall",
)
