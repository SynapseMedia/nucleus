from __future__ import annotations


import pydantic
import sqlite3
import pickle
import nucleus.core.cache as cache
import nucleus.sdk.exceptions as exceptions

from pydantic import ValidationError
from nucleus.core.cache import Connection
from nucleus.core.types import Any, Union, Iterator, Path, URL, Generic, T

from .constants import MIGRATE, INSERT, FETCH, MODELS_PATH
from .decorators import with_standard_errors


class _Manager(pydantic.main.ModelMetaclass):
    """Database connection behavior.

    Each database file is created based on the class name.
    This metaclass routes queries to the correct database .
    """

    def __new__(mcs, name: Any, bases: Any, attrs: Any, **kwargs: Any):  # type: ignore
        """Start a new connection to cache database and ensure that the database is ready to receive requests."""
        db_path = Path(MODELS_PATH)
        db_file = f"{db_path}/{name}.db"
        
        # ensure that model directory exists
        if not db_path.exists():
            db_path.mkdir(parents=True)
            
        conn = cache.connect(db_path=db_file)
        # run migration before run any operations on the database
        conn.execute(MIGRATE % (name, name))
        # add new attributes to class
        new_attrs = {**{"_conn": conn, "_alias": name}, **attrs}
        return super().__new__(mcs, name, bases, new_attrs, **kwargs)  # type: ignore


class _Model(pydantic.BaseModel, metaclass=_Manager):
    """This model defines a template for managing the cache associated with each model

    Each database file is created based on the model name.
    This generic model routes queries to the right database according to the model name.
    """

    _alias: str
    _conn: Connection

    def __init__(self, *args: Any, **kwargs: Any):
        try:
            super(_Model, self).__init__(*args, **kwargs)
        except ValidationError as e:
            raise exceptions.ModelValidationError(
                f"raised exception during model initialization: {str(e)}"
            )

        sqlite3.register_converter(self._alias, pickle.loads)
        sqlite3.register_adapter(self.__class__, pickle.dumps)

    @classmethod
    @with_standard_errors
    def get(cls) -> _Model:
        """Exec query and fetch one entry from database.

        :return: one result as model instance
        :rtype: _Model
        :raises ModelManagerError: if there is an error fetching entry
        """

        response = cls._conn.execute(FETCH % cls._alias)
        row = response.fetchone()
        return row[0]

    @classmethod
    @with_standard_errors
    def all(cls) -> Iterator[_Model]:
        """Exec query and fetch a list of data from database.

        :return: all query result as model instance
        :rtype: Iterator[_Model]
        :raises ModelManagerError: if there is an error fetching entries
        """
        response = cls._conn.execute(FETCH % cls._alias)
        rows = response.fetchall()
        return map(lambda r: r[0], rows)

    @with_standard_errors
    def save(self) -> Union[int, None]:
        """Exec insertion into database using built query

        :return: true if query was saved or False otherwise
        :rtype: bool
        :raises ModelManagerError: if there is an error saving entry
        """
        cursor = self._conn.execute(INSERT % self._alias, (self,))
        return cursor.lastrowid


class _FrozenModel(_Model):
    """Template immutable model"""

    class Config:
        # ref: https://docs.pydantic.dev/usage/model_config/
        frozen = True
        smart_union = True
        use_enum_values = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True


class Meta(_FrozenModel):
    """Template metadata model.
    Extend this model to create your owns.
    Default fields are name and description.
    """

    name: str
    description: str


class Media(_FrozenModel, Generic[T]):
    """Generic media model.
    All derived class are used as types for dispatch actions.
    eg.

        class Video(Media[Path]):
            type: Literal["video"] = "video"


        @singledispatch/assessments
        def process(model: Media[Path]):
            raise NotImplementedError()

        @process.register
        def _(model: Video):
            ...

        process(video)
    """

    route: T
    type: str


# Alias for sources allowed to collect media
Collectable = Media[Union[URL, Path]]

__all__ = ("Meta",)
