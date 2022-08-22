from .decorator import connected
from .database import Connection

# TODO finish migrate functions
@connected
def tables(conn: Connection):
    ...


@connected
def indexes(conn: Connection):
    ...


@connected
def verify(conn: Connection):
    ...
