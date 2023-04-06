from functools import singledispatch

from .services import Estuary
from .clients import EstuaryClient
from .types import Service, ServiceClient, Pin


@singledispatch
def _service(svc: Service) -> ServiceClient:
    """Service single dispatch factory.
    Use the model input to infer the right storage service.

    :param model: the model to dispatch
    :return: service client instance
    :rtype: ServiceClient
    """
    raise NotImplementedError(f"cannot process not registered storable `{svc}")


@_service.register
def _(svc: Estuary):
    """Return a estuary api client with the specified service settings."""
    return EstuaryClient(
        endpoint=svc.endpoint(),
        key=svc.key(),
    )


# TODO add handling for pinning
# def edge(svc: Service) -> Pin:

#     service = _service(svc)

#     def pin()

#     def pin(cid: CID)
