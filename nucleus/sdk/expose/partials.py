from .marshall import Marshall
from .types import Serializer, SEP001, Header, Payload


def dispatch(serializer: Serializer) -> Marshall:
    """StdDist factory

    :param serializer: the serialization handler
    :return: StdDist object
    :rtype: StdDist
    """
    return Marshall(serializer)


def public(type: str) -> SEP001:
    """SEP001 factory

    :param type: the type of media to expose
    :return: new standard implementation sep-001 object
    :rtype: SEP001
    """

    header = Header(
        type,
    )
    payload = Payload()
    return SEP001(header, payload)


__all__ = (
    "public",
    "dispatch",
)
