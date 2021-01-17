from .yts import YTS

# Source movies metadata
ROOT_API = 'https://yts.mx'
# Add here any source needed
ALLOWED_SOURCES = {
    'YTS': YTS
}


def migrate(source='YTS', **kwargs):
    """
    Migrate from chosen source
    All resources class must implement `migrate` method
    :param source:
    :return:
    """

    if source in ALLOWED_SOURCES:
        return ALLOWED_SOURCES[source](**kwargs)
    raise ImportError
