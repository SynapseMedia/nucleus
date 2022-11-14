from ..scheme.resolver import Resolver
from ...core import logger, scheme


def resolvers_to_str(resolver: Resolver):
    """Get names from resolvers

    :param resolver: resolver class
    :return: resolver name
    :rtype: str
    """
    return str(resolver())


def trigger_resolver(resolver: Resolver):
    """Proxy __call__ resolver
    Resolver::
        class Dummy:
            def __str__(self)
            def __call__(self, scheme)

    :param: resolver class
    :return: __call__ result
    :rtype: typing.Generator
    """
    resolver = resolver()  # Init class
    logger.log.notice(f"Generating migrations from {resolver}")
    return resolver(scheme)  # Call class and start migration

