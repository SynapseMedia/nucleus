import click


@click.group('cache')
def cache():
    """
    Clean cache and storage
    """
    pass


@cache.group('flush')
def flush():
    pass


@flush.command()
def resolved():
    pass


@flush.command()
def ingested():
    pass


@flush.command()
def pinned():
    pass
