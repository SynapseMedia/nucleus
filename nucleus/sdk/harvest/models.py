from __future__ import annotations

import pickle
import sqlite3

import pydantic
from pydantic import ValidationError

import nucleus.core.cache as cache
import nucleus.core.decorators as decorators
from nucleus.core.cache import Connection
from nucleus.core.types import Any, Generic, Iterator, Path, T
from nucleus.sdk.exceptions import ModelManagerError, ModelValidationError

from .constants import FETCH, INSERT, MIGRATE, MODELS_PATH


class _Manager(pydantic.main.ModelMetaclass):
    """Database manager behavior.

    Each database file is created based on the class name.
    This metaclass prepare the connection to query to the right database according to the class name.
    """

    def __new__(mcs, name: Any, bases: Any, attrs: Any, **kwargs: Any):
        """Start a new connection to cache database and ensure that the database is ready to receive requests."""
        db_path = Path(MODELS_PATH)
        db_file = f'{db_path}/{name}.db'

        super_new = super().__new__
        # Ensure initialization is only performed for subclasses of _Model
        is_subclass_instance = any(map(lambda x: isinstance(x, _Manager), bases))
        if not is_subclass_instance:
            return super_new(mcs, name, bases, attrs, **kwargs)

        # ensure that model directory exists
        if not db_path.exists():
            db_path.mkdir(parents=True)

        # connect and run migrations for model database
        conn = cache.connect(db_path=db_file)
        conn.execute(MIGRATE % (name, name))
        # add new attributes to class
        new_attrs = {**{'_conn': conn, '_alias': name}, **attrs}
        return super_new(mcs, name, bases, new_attrs, **kwargs)


class Base(pydantic.BaseModel, metaclass=_Manager):
    """Base model provides efficient model persistence and data validation capabilities.
    The persistence mechanism relies on sqlite and pickle, allowing the entire model to be stored as a snapshot

    Usage:

        class MyModel(BaseModel):
            name: str

        # store a snapshot of the model
        stored_model = MyModel(name="Model")
        stored_model.save()

        # we should be able to retrieve the same model
        assert MyModel.all() == [stored_model] # True
    """

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
    def get(cls) -> Base:
        """Exec query and fetch first entry from local database.

        :return: First registered snapshot
        :raises ModelManagerError: If there is an error fetching entry
        """

        response = cls._conn.execute(FETCH % cls._alias)
        row = response.fetchone()
        return row[0]

    @classmethod
    @decorators.proxy_exception(
        expected=sqlite3.ProgrammingError,
        target=ModelManagerError,
    )
    def all(cls) -> Iterator[Base]:
        """Exec query and fetch a list of data from local database.

        :return: all registered snapshots
        :raises ModelManagerError: If there is an error fetching entries
        """
        response = cls._conn.execute(FETCH % cls._alias)
        rows = response.fetchall()
        return map(lambda r: r[0], rows)

    @decorators.proxy_exception(
        expected=sqlite3.ProgrammingError,
        target=ModelManagerError,
    )
    def save(self) -> bool:
        """Exec insertion query into local database

        :return: True if successful else False
        :raises ModelManagerError: If there is an error saving entry
        """

        # https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.lastrowid
        cursor = self._conn.execute(INSERT % self._alias, (self,))
        return cursor.rowcount > 0


class Model(Base):
    """Model class specifies by default the attributes needed for the metadata model
    and allows its extension to create metadata sub-models with custom attributes.

    Usage:

        class Nucleus(Model):
            name: str # default property
            description: str # default property
            address: str # my custom property
    """

    name: str  # the name of the resource
    description: str  # the description of the resource


class Media(Base, Generic[T]):
    """Generic media model to create media subtypes.
    Each subtype represents a specific media type and provides a generic specification
    of the sources from which it can be collected.

    Usage:

        class Video(Media[Path]):
            # represents a video file type .
            ...

        class Image(Media[URL]):
            # represents an image url type.
            ...
    """

    path: T


__all__ = ('Model', 'Media')
