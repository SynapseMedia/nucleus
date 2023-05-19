from __future__ import annotations

import pickle
import sqlite3

import pydantic
from pydantic import ValidationError

import nucleus.core.cache as cache
import nucleus.core.decorators as decorators
from nucleus.core.cache import Connection
from nucleus.core.types import Any, Generic, Iterator, Path, T, Union
from nucleus.sdk.exceptions import ModelManagerError, ModelValidationError

from .constants import FETCH, INSERT, MIGRATE, MODELS_PATH


class _Manager(pydantic.main.ModelMetaclass):
    """Database manager behavior.

    Each database file is created based on the class name.
    This metaclass prepare the connection to query to the right database according to the class name.
    """

    def __new__(mcs, name: Any, bases: Any, attrs: Any, **kwargs: Any):  # type: ignore
        """Start a new connection to cache database and ensure that the database is ready to receive requests."""
        db_path = Path(MODELS_PATH)
        db_file = f'{db_path}/{name}.db'

        super_new = super().__new__  # type: ignore
        # Ensure initialization is only performed for subclasses of _Model
        is_subclass_instance = any(map(lambda x: isinstance(x, _Manager), bases))
        if not is_subclass_instance:
            return super_new(mcs, name, bases, attrs, **kwargs)  # type: ignore

        # ensure that model directory exists
        if not db_path.exists():
            db_path.mkdir(parents=True)

        # connect and run migrations for model database
        conn = cache.connect(db_path=db_file)
        conn.execute(MIGRATE % (name, name))
        # add new attributes to class
        new_attrs = {**{'_conn': conn, '_alias': name}, **attrs}
        return super_new(mcs, name, bases, new_attrs, **kwargs)  # type: ignore


class _BaseModel(pydantic.BaseModel, metaclass=_Manager):
    """This model defines a template to handle cache associated with each derived model"""

    _alias: str
    _conn: Connection

    class Config:
        # Frozen model behavior
        # ref: https://docs.pydantic.dev/usage/model_config/
        frozen = True
        smart_union = True
        use_enum_values = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

    def __init__(self, *args: Any, **kwargs: Any):
        try:
            super().__init__(*args, **kwargs)
        except ValidationError as e:
            raise ModelValidationError(f'raised exception during model initialization: {str(e)}')

        sqlite3.register_converter(self._alias, pickle.loads)
        sqlite3.register_adapter(type(self), pickle.dumps)

    @classmethod
    @decorators.proxy_exception(
        expected=sqlite3.ProgrammingError,
        target=ModelManagerError,
    )
    def get(cls) -> _BaseModel:
        """Exec query and fetch one entry from database.

        :return: one result as model instance
        :rtype: _Model
        :raises ModelManagerError: if there is an error fetching entry
        """

        response = cls._conn.execute(FETCH % cls._alias)
        row = response.fetchone()
        return row[0]

    @classmethod
    @decorators.proxy_exception(
        expected=sqlite3.ProgrammingError,
        target=ModelManagerError,
    )
    def all(cls) -> Iterator[_BaseModel]:
        """Exec query and fetch a list of data from database.

        :return: all query result as model instance
        :rtype: Iterator[_Model]
        :raises ModelManagerError: if there is an error fetching entries
        """
        response = cls._conn.execute(FETCH % cls._alias)
        rows = response.fetchall()
        return map(lambda r: r[0], rows)

    @decorators.proxy_exception(
        expected=sqlite3.ProgrammingError,
        target=ModelManagerError,
    )
    def save(self) -> Union[int, None]:
        """Exec insertion into database using built query

        :return: true if query was saved or False otherwise
        :rtype: bool
        :raises ModelManagerError: if there is an error saving entry
        """
        cursor = self._conn.execute(INSERT % self._alias, (self,))
        return cursor.lastrowid


class Model(_BaseModel):
    """Base Metadata model."""

    name: str
    desc: str


class Media(_BaseModel, Generic[T]):
    """Generic media model.
    All derived class are used as types for dispatch actions.
    eg.

        class Video(Media[Path]):
            ...


        @singledispatch/assessments
        def process(model: Media[Path]):
            raise NotImplementedError()

        @process.register
        def _(model: Video):
            ...

        process(video)
    """

    path: T


__all__ = ('Model', 'Media')
