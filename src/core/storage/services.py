# def services():
#     """Return registered services

#     :return: False if not registered else True
#     """
#     registered_services = exec_command("/pin/remote/service/ls")
#     registered_services_list = registered_services.get("RemoteServices")
#     return registered_services_list


# def register_service(service, endpoint, key) -> str:
#     """Add service to ipfs
#     https://docs.ipfs.io/reference/http/api/#api-v0-pin-remote-service-add

#     :params service: service name
#     :params endpoint: service endpoint
#     :params key: service jwt
#     :return: ipfs execution output
#     :rtype: str
#     """
#     return exec_command("/pin/remote/service/add", *(service, endpoint, key))
