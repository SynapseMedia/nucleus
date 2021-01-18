from .yts import YTS

# Source movies metadata

# Add here any source needed
ALLOWED_SOURCES = {
    'YTS': YTS
}


def migrate(source='YTS', **kwargs):
    """
    Migrate from chosen source
    :param source:
    :return:
    """

    if source in ALLOWED_SOURCES:
        return ALLOWED_SOURCES[source](**kwargs).migrate(
            # All resource class must implement `migrate` method
        )
    raise ImportError
