from .types import SEP001, Header, Payload


def public(type: str) -> SEP001:
    """SEP001 factory

    :param type: the type of media to expose
    :return: new standard implementation sep-001 object
    :rtype: SEP001
    """

    header = Header(type, alg="ES256")  # TODO Signed not encrypted?

    payload = Payload()
    return SEP001(header, payload)


__all__ = ("public",)
