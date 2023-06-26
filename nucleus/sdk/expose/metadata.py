from nucleus.core.types import CID, Dynamic, Optional


class Structural(Dynamic):
    """Structural "s" claim metadata implementation.

    Usage:

        # example of populating "s" claim
        s = Structural(cid="QmZG1jK2zYyzdHZtkZb9f9Uu3qQ2Ru6yvLjWFRV8ZuM6aM")
        s_with_path = Structural(cid="QmZG1jK2zYyzdHZtkZb9f9Uu3qQ2Ru6yvLjWFRV8ZuM6aM", path="/videos/example_video.mp4")

    """

    cid: CID
    path: Optional[str] = None

    def __str__(self):
        return 's'


class Descriptive(Dynamic):
    """Descriptive "d" claim metadata implementation.

    Usage:

        # example of populating "d" claim
        d = Descriptive(
            name="Example",
            description="Example description",
            language="English",
            author="NASA",
        )

    """

    name: str
    description: str

    def __str__(self):
        return 'd'


class Technical(Dynamic):
    """Technical "t" claim metadata implementation.

    Usage:

        # example of populating "t" claim
        t = Technical(
            size=1024,
            width=256,
            height=256,
            length=90
        )

    """

    size: int

    def __str__(self):
        return 't'


__all__ = ['Structural', 'Descriptive', 'Technical']
