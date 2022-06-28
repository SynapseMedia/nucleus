from . import CLI, EdgeServices, EdgeService


def services() -> EdgeServices:
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
        lambda x: EdgeService(
            service=x["Service"],
            endpoint=x["ApiEndpoint"],
        ),
        output.get("RemoteServices"),
    )

    return EdgeServices(remote=services_iter)


def register(service: EdgeService) -> EdgeService:
    """Add service to ipfs
    https://docs.ipfs.io/reference/http/api/#api-v0-pin-remote-service-add

    :params service: to register service
    :return: None
    :raises IPFSFailedExecution
    """
    params = service.values()
    # Using ignore here because this is an issue with python typing
    # https://github.com/python/mypy/issues/7981
    CLI("/pin/remote/service/add", *params)()  # type: ignore
    return service
