from .marshall import StdDist, Broker
from .standard import SEP001, Header, Payload


def dispatch(broker: Broker) -> StdDist:
    """StdDist factory

    :param broker: the broadcaster
    :return: StdDist object
    :rtype: StdDist
    """
    return StdDist(broker)


def public(type: str) -> SEP001:
    """SEP001 factory

    :param type: the type of media to expose
    :return: new standard implementation sep-001 object
    :rtype: SEP001
    """

    return SEP001(Header(type), Payload())


__all__ = (
    "public",
    "dispatch",
)
