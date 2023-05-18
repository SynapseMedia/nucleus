import functools

from .services import Estuary
from .clients import EstuaryClient
from .types import Service, Client


@functools.singledispatch
def client(svc: Service) -> Client:
    """Client single dispatch factory.
    Use the model input to infer the right storage service.

    :param model: the model to dispatch
    :return: edge service client instance
    :rtype: Edge
    """
    raise NotImplementedError(f"cannot process not registered storable `{svc}")


@client.register
def _(svc: Estuary):
    """Return a estuary api client with the specified service settings."""
    return EstuaryClient(
        endpoint=svc.endpoint(),
        key=svc.key(),
    )


__all__ = ("client",)
