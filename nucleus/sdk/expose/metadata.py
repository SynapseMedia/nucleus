from nucleus.core.types import CID, Dynamic, Optional


class Structural(Dynamic):
    """Structural metadata implementation.
    https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    cid: CID
    path: Optional[str] = None

    def __str__(self):
        return 's'


class Descriptive(Dynamic):
    """Descriptive metadata implementation.
    https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    name: str
    desc: str

    def __str__(self):
        return 'd'


class Technical(Dynamic):
    """Technical metadata implementation.
    https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md
    """

    size: int

    def __str__(self):
        return 't'


__all__ = ['Structural', 'Descriptive', 'Technical']
