from . import logger
import src.core.scheme as scheme

import typing


def resolvers_to_str(resolver) -> str:
    """
    Get names from resolvers
    :param resolver:
    :return:
    """
    return str(resolver())


def trigger_resolver(resolver) -> typing.Generator:
    """
    Dummy resolver generator call
    :param resolver
    :returns: Iterable result
    """
    resolver = resolver()  # Init class
    logger.notice(f"Generating migrations from {resolver}")
    return resolver(scheme)  # Call class and start migration
