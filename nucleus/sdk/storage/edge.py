import functools

from .services import Estuary
from .clients import EstuaryClient
from .types import Service, Edge


@functools.singledispatch
def service(svc: Service) -> Edge:
    """Service single dispatch factory.
    Use the model input to infer the right storage service.

    :param model: the model to dispatch
    :return: service client instance
    :rtype: ServiceClient
    """
    raise NotImplementedError(f"cannot process not registered storable `{svc}")


@service.register
def _(svc: Estuary):
    """Return a estuary api client with the specified service settings."""
    return EstuaryClient(
        endpoint=svc.endpoint(),
        key=svc.key(),
    )


__all__ = ("service",)
