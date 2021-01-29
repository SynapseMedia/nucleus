from .definition import MovieSchema


def check(data):
    """
    Bypass check data in scheme
    """
    return MovieSchema(many=True).load(data)


__all__ = ['check']
