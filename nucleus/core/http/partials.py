import functools

import requests

from .session import LiveSession

live_session = functools.partial(LiveSession)
session = functools.partial(requests.Session)
post = functools.partial(requests.post)
get = functools.partial(requests.get)
put = functools.partial(requests.put)
delete = functools.partial(requests.delete)


__all__ = (
    'live_session',
    'session',
    'post',
    'get',
    'put',
    'delete',
)
