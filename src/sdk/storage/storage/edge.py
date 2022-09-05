from src.core.types import Sequence
from .types import Edge, Service, RemotePin

# TODO WIP
# TODO Facade edge classes
# TODO: create pinata and filebase providers here
# TODO this probably should be in sdk upper abstraction level


class Pinata(Edge):
    _service: Service

    def __init__(self, service: Service):
        self._service = service

    @property
    def name(self):
        return self._service.get("service")

    def pin(self, cid: str) -> RemotePin:
        """Pin cid in remote edge cache
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add

        :param cid: cid to pin
        :return: RemotePin object
        :rtype: RemotePin
        """
        # TODO check if has registered service
        ...

    @property
    def background_mode(self):
        """Pin cid in async mode
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-add

        :return: True if running in async mode else False
        :rtype: bool
        """
        return True

    @property
    def is_registered(self) -> bool:
        """Check if service is registered

        :return: True if service is registered else False
        :rtype: bool
        """
        ...

    @property
    def status(self) -> bool:
        """Check status for edge service

        :return: True if auth ready and registered else False
        :rtype: bool
        """
        ...

    def ls(self, limit: int) -> Sequence[RemotePin]:
        """Return current remote pin list
        ref: http://docs.ipfs.io/reference/cli/#ipfs-pin-remote-ls

        :param limit: Number of remote pins to return
        :return: List of current remote pin list
        :rtype: Sequence[RemotePin]
        """
        ...

    def unpin(self, cid: str) -> bool:
        """Remove pin from edge cache service

        :param cid: Cid to remove from cache
        :return: True if pin was removed else False
        :rtype: bool
        """
        ...

    def flush(self, limit: int) -> int:
        """Remove all pinned cid from edge cache service

        :param limit: Maximum number of remote pins to remove
        :return: Number of remote pins removed
        :rtype: int
        """
        ...
