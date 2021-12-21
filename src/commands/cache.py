import click


@click.group("cache")
def cache():
    """
    Clean cache and storage
    """
    pass


@cache.group("flush")
def flush():
    pass


@flush.command()
def frozen():
    pass


@flush.command()
def pinned():
    pass
