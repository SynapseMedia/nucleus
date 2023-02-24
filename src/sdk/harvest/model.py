from __future__ import annotations


import ast
import pydantic
import sqlite3
import pickle
import src.core.cache as cache

# Convention for importing constants/types
from src.core.types import Any, Iterator, Union, List, Path, CID, URL
from src.core.cache import Cursor, Connection

from .constants import INSERT, FETCH, MIGRATE


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
            db_name = f".models/{cls.alias}.db"  # keep .db file name
            cls._conn = cache.connect(db_path=db_name)
            cls._conn.execute(cls.migrate())

        return cls._conn


class Model(_Manager, pydantic.BaseModel):
    """Model based SQL manager"""

    def __init__(self, **kwargs: Any):
        super(Model, self).__init__(**kwargs)
        sqlite3.register_converter(self.alias, pickle.loads)
        sqlite3.register_adapter(self.__class__, pickle.dumps)

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
        return map(lambda r: r[0], rows)

    def save(self) -> int | None:
        """Exec insertion into database using built query

        :return: True if query was saved or False otherwise
        :rtype: bool
        """

        cursor: Cursor = self.conn.execute(self.mutate(), (self,))
        return cursor.lastrowid


class Meta(Model):
    """Abstract metadata model"""

    class Config:
        # ref: https://docs.pydantic.dev/usage/model_config/
        frozen = True
        smart_union = True
        use_enum_values = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True


class Media(Meta):
    """Abstract media model.
    All derived class are used as types for dispatch actions.
    eg.

        class Video(Media):
            type: Literal["video"] = "video"


        @singledispatch
        def process(model: Media):
            raise NotImplementedError()

        @process.register
        def _(model: Video):
            ...

        process(video)
    """

    route: Union[URL, Path, CID]
    type: str


class Collection(Model):

    """The purpose of Collection is to link the metadata and it corresponding media"""

    media: List[Media]
    metadata: Meta

    @pydantic.validator("media", pre=True)
    def serialize_media_pre(cls, v: Any):
        """Pre serialize media to object"""
        if isinstance(v, bytes):
            parsed = ast.literal_eval(v.decode())
            instances = map(lambda x: Media(**x), parsed)
            return list(instances)
        return v