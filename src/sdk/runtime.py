from .scheme.resolver import Resolver
from ..core import logger, scheme


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


async def migrate(sources: Sequence[str], recreate: bool = False) -> None:
    """Spawn nodejs subprocess

    :param sources: list of sources to migrate into orbit
    :param recreate: if recreate equal True new orbit repo is created else use existing
    :return: None since is just a subprocess call
    :rtype: None
    """

    # Formulate params
    recreate_param = recreate and "-g" or ""
    commands = map(
        lambda r: Subprocess(
            "migrate", (recreate_param, f"--key={r}", f"--source={r}")
        ),
        sources,
    )

    process_list = [command() for command in commands]
    await asyncio.gather(*process_list)
