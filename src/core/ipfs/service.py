from .cmd import CLI
from .types import Services, Service


def ls() -> Services:
    """Return registered services
    ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-service-ls

    Output:
        {
            "RemoteServices":[
                {"Service":"pinata","ApiEndpoint":"https://api.pinata.cloud/psa"}
            ]
        }


    :return: Registered services
    :rtype: EdgeServices
    :raises IPFSFailedExecution
    """

    exec = CLI("/pin/remote/service/ls")
    output = exec().get("output")

    # Get all services from ipfs
    services_iter = map(
        lambda x: Service(service=x["Service"], endpoint=x["ApiEndpoint"], key=None),
        output.get("RemoteServices"),
    )

    return Services(remote=services_iter)


def register(service: Service) -> Service:
    """Add service to ipfs
    https://docs.ipfs.io/reference/http/api/#api-v0-pin-remote-service-add

    :params service: to register service
    :return: reflected param service
    :raises IPFSFailedExecution
    """

    # Using ignore here because this is an issue with python typing
    # https://github.com/python/mypy/issues/7981
    params = service.values()
    CLI("/pin/remote/service/add", *params)()  # type: ignore
    return service
