from __future__ import annotations

import pydantic
import ast
import sqlite3
import enum
import validators  # type: ignore
import cid  # type: ignore
import pathlib
import src.core.cache as cache

from src.core.types import Any, Iterator, List, Type
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
            db_name = f"{cls.alias}.db"  # keep .db file name
            cls._conn = cache.connect(db_path=db_name)
            cls._conn.execute(cls.migrate())

        return cls._conn


class MediaType(enum.Enum):
    """Enumeration of resource types.
    Any resource type should be listed here
    """

    IMAGE = 0
    VIDEO = 1


class Media(pydantic.BaseModel):
    """Media define needed field for the multimedia assets schema."""

    route: str
    type: MediaType

    @pydantic.validator("route")
    def valid_route(cls, v: str):
        is_path = pathlib.Path(v).exists()  # type: ignore
        is_url = bool(validators.url(v))  # type: ignore
        is_cid = bool(cid.is_cid(v))  # type: ignore

        if not is_url and not is_path and not is_cid:
            raise ValueError("Route must be a CID | URI | Path")

        return v

    @pydantic.validator("type")
    def serialize_media_pre(cls, v: Any):
        """Pre serialize media to object"""
        if isinstance(v, MediaType):
            return v.value
        return v


class Meta(pydantic.BaseModel):
    class Config:
        use_enum_values = True
        validate_assignment = True

    ...


class Model(_Manager, pydantic.BaseModel):
    """Model based SQL manager"""

    media: List[Media]
    metadata: Meta

    def __init__(self, **kwargs: Any):
        super(Model, self).__init__(**kwargs)
        sqlite3.register_converter(self.alias, self.__convert__)

    @classmethod
    def annotate(cls, **kwargs: Any) -> Type[Model]:
        """Dynamic typing for metadata from Meta subtypes.
        Enhance the model by annotating new properties to it from a specific model.

        :para type_: type to treat metadata
        :return: Enhanced model
        :rtype: Model
        """
        cls = type(
            "Model",
            (cls,),
            {
                **{"__annotations__": kwargs},
                **{k: pydantic.Field(k) for k in kwargs.keys()},
            },
        )
        return cls

    @pydantic.validator("media", pre=True)
    def serialize_media_pre(cls, v: Any):
        """Pre serialize media to object"""
        if isinstance(v, bytes):
            parsed = ast.literal_eval(v.decode())
            instances = map(lambda x: Media(**x), parsed)
            return list(instances)
        return v

    @classmethod
    def __convert__(cls, raw: bytes) -> Model:
        """Convert data from sqlite to  model
        ref: https://docs.python.org/3/library/sqlite3.html#how-to-write-adaptable-objects

        :param raw: data from database
        :param model: model to convert raw input
        :return: Model instanced with data from db
        :rtype: Model
        """

        fields = cls.__fields__.keys()
        values = map(ast.literal_eval, raw.decode().split(";"))
        params = dict(zip(fields, values))
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
