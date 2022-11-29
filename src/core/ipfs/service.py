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
    :rtype: Services
    :raises IPFSFailedExecution: if ipfs cmd execution fail
    """

    exec = CLI("/pin/remote/service/ls")
    output = exec().get("output")
    raw_services = output.get("RemoteServices")

    # map registered services
    services_iter = map(
        lambda x: Service(
            service=x["Service"],
            endpoint=x["ApiEndpoint"],
            key=None,
        ),
        raw_services,
    )

    return Services(remote=services_iter)


def register(service: Service) -> Service:
    """Add service to ipfs
    ref: https://docs.ipfs.tech/reference/kubo/cli/#ipfs-pin-remote-add

    :params service: to register service
    :return: reflected param service
    :rtype: Service
    :raises IPFSFailedExecution: if service is already registered
    """

    # Using ignore here because this is an issue with python typing
    # https://github.com/python/mypy/issues/7981
    params = service.values()
    CLI("/pin/remote/service/add", *params)()  # type: ignore
    return service
