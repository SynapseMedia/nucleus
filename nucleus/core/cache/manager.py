# Convention for importing constants/types
from nucleus.core.types import Path, Union

from .types import Connection
from .database import connect
from .constants import INSERT, FETCH, MIGRATE, MODELS_PATH


class QueryManager(object):
    """Manager to handle SQL queries"""

    @classmethod
    @property
    def alias(cls) -> str:
        """Return the class name as an alias for the model."""
        return cls.__name__.lower()

    @classmethod
    def migrate(cls) -> str:
        """Return a migration query string.

        This query is used to handle migrations related to models.
        If the table does not exist, it will be created before running other queries.
        ref: https://docs.python.org/3/library/sqlite3.html#default-adapters-and-converters
        """
        return MIGRATE % (cls.alias, cls.alias)

    @classmethod
    def mutate(cls) -> str:
        """Return an insert query based on the class name.

        See more: https://docs.python.org/3/library/sqlite3.html#default-adapters-and-converters
        """
        return INSERT % cls.alias

    @classmethod
    def query(cls) -> str:
        """Return a query based on the class name.

        See more: https://docs.python.org/3/library/sqlite3.html#default-adapters-and-converters
        """
        return FETCH % cls.alias


class ConnectionManager(QueryManager):
    """Connection manager to handle database connections.

    Each database file is created based on the model name.
    This manager routes queries to the correct database model for different collectors.
    """

    _conn: Union[Connection, None] = None

    @classmethod
    def using(cls, conn: Connection):
        """Set a connection to use during operations.

        :param conn: connection to use
        :return: None
        :rtype: None
        """
        cls._conn = conn

    @classmethod
    @property
    def conn(cls) -> Connection:
        """Singleton connection factory.
        A migration process happen after connection is established to ensure integrity during cache operations.

        :return: connection to use during operations
        :rtype: Connection
        :raises DatabaseError: if any error occurs during connection creation
        """

        if cls._conn is None:
            # we need to keep a reference in db name related to model
            db_path = Path(MODELS_PATH % cls.alias)  # keep .db file name
            # ensure that model file exists
            if not db_path.exists():
                db_path.mkdir(parents=True)

            cls._conn = connect(db_path=db_path)
            cls._conn.execute(cls.migrate())
        return cls._conn


__all__ = ("ConnectionManager",)
