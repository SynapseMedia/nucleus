from .yts import YTS

# Source movies metadata
ROOT_API = 'https://yts.mx'


def migrate(source='YTS', **kwargs):
    """
    Migrate from chosen source
    :param source:
    :return:
    """

    return YTS(
        host='%s/api/v2/list_movies.json' % ROOT_API,
        **kwargs
    ).migrate(resource_name='yts')
