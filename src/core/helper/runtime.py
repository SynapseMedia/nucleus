from src.core import Log, logger
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
    logger.info(f"{Log.WARNING}Generating migrations from {resolver}{Log.ENDC}")
    return resolver(scheme)  # Call class and start migration
