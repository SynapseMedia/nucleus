from __future__ import annotations

"""
Scheme definition for movies.
Each scheme here defined help us to keep a standard for runtime processing of movies.
All processed data is later used in the creation of standard metadata (ERC-1155, ..), pipeline cache, marshalling, etc;
"""
import enum
import sqlite3
import pydantic
import src.core.cache as cache

# Convention for importing constants/types
from abc import ABC, abstractmethod
from src.core.types import Any, Iterator
from src.core.cache.types import Cursor, Connection
from .constants import INSERT, FETCH, MIGRATE


class MediaType(enum.Enum):
    """Enumeration of resource types.
    Any resource type should be listed here
    """

    IMAGE = 0
    VIDEO = 1


class Collector(ABC):
    """Abstract class for collecting metadata.
    Collector define an "strict abstraction" with methods needed to handle metadata collection process.
    Subclasses should implement the __iter__ method to collect metadata from various data inputs.
    """

    def __str__(self) -> str:
        """Context name for current data.

        We use this context name to keep a reference to data.
        """
        return "__collectable__"

    @abstractmethod
    def __iter__(self) -> Iterator[Model]:
        """Collect metadata from any kind of data input.

        Please see pydantic helper functions:
        https://docs.pydantic.dev/usage/models/#helper-functions

        eg:
        -
        source_file = "src/tests/_mock/files/dummy.json"
        return iter(pydantic.parse_file_as(List[Music], source_file))

        """
        ...


class _Manager:
    """SQL manager for managing database connections and queries.

    Each database file is created based on the model name.
    This manager routes queries to the correct database model for different collectors.
    """

    _conn: Connection | None = None

    @classmethod
    @property
    def alias(cls) -> str:
        """Return class name as alias for model"""
        return cls.__name__.lower()

    @classmethod
    def migrate(cls) -> str:
        """Return a migration query string.
        Expected behavior if "table do not exist" before run other queries.
        This query is used to handle migrations related to models.
        See more: https://docs.python.org/3/library/sqlite3.html#default-adapters-and-converters
        """
        return MIGRATE % (cls.alias, cls.alias)

    @classmethod
    def mutate(cls) -> str:
        """Return a insert query based on class name.
        See more: https://docs.python.org/3/library/sqlite3.html#default-adapters-and-converters
        """
        return INSERT % cls.alias

    @classmethod
    def query(cls) -> str:
        """Return a query based on class name.
        See more: https://docs.python.org/3/library/sqlite3.html#default-adapters-and-converters
        """
        return FETCH % cls.alias

    @classmethod
    @property
    def conn(cls) -> Connection:
        """Singleton connection factory

        :return: connection to use during operations
        :rtype: Connections
        """

        if cls._conn is None:
            # we need to keep a reference in db name related to model
            db_name = f"{cls.alias}.db"  # keep .db file name
            cls._conn = cache.connect(db_path=db_name)
            cls._conn.execute(cls.migrate())

        return cls._conn


class Model(_Manager, pydantic.BaseModel):
    """Model based SQL manager"""

    class Config:
        use_enum_values = True
        validate_assignment = True

    def __init__(self, **kwargs: Any):
        super(Model, self).__init__(**kwargs)
        sqlite3.register_converter(self.alias, self.__convert__)

    @classmethod
    def __convert__(cls, raw: bytes) -> Model:
        """Convert data from sqlite to  model
        ref: https://docs.python.org/3/library/sqlite3.html#how-to-write-adaptable-objects

        :param raw: data from database
        :param model: model to convert raw input
        :return: Model instanced with data from db
        :rtype: Model
        """
        values = list(raw.split(b";"))  # type: ignore
        fields = cls.__fields__.keys()  # fields defined in models
        params = dict(zip(fields, values))  # type: ignore
        return cls(**params)

    def __conform__(self, protocol: sqlite3.PrepareProtocol):
        """Sqlite3 adapter
        ref: https://docs.python.org/3/library/sqlite3.html#sqlite3-adapters
        """
        if protocol is sqlite3.PrepareProtocol:
            raw_fields = self.dict().values()
            map_fields = map(str, raw_fields)
            return ";".join(map_fields)

    @classmethod
    def get(cls) -> Any:
        """Exec query and fetch one entry from database.

        :return: Any derived model
        :rtype: Any
        """

        response = cls.conn.execute(cls.query())
        rows = response.fetchone()  # raw data
        return rows[0]

    @classmethod
    def all(cls) -> Iterator[Model]:
        """Exec query and fetch a list of data from database.

        :return: Any list of derived model
        :rtype: Iterator[Any]
        """

        response = cls.conn.execute(cls.query())
        rows = response.fetchall()  # raw data
        return rows[0]

    def save(self) -> int | None:
        """Exec insertion into database using built query

        :return: True if query was saved or False otherwise
        :rtype: bool
        """

        cursor: Cursor = self.conn.execute(self.mutate(), (self,))
        return cursor.lastrowid
