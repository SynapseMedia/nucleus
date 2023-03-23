from __future__ import annotations


import ast
import pydantic
import sqlite3
import pickle
import nucleus.sdk.exceptions as exceptions

# Convention for importing constants/types
from pydantic import ValidationError
from nucleus.core.cache import Cursor, Manager
from nucleus.core.types import Any, Union, Iterator, List, Path, URL, CID, Generic, T


class _Model(Manager, pydantic.BaseModel):
    """This model defines a template for managing the cache associated with each model"""

    def __init__(self, **kwargs: Any):
        try:
            super(_Model, self).__init__(**kwargs)
        except ValidationError as e:
            raise exceptions.ModelValidationError(
                f"raised exception during model initialization: {str(e)}"
            )

        sqlite3.register_converter(self.alias, pickle.loads)
        sqlite3.register_adapter(self.__class__, pickle.dumps)

    @classmethod
    def get(cls) -> _Model:
        """Exec query and fetch one entry from database.

        :return: one result as model instance
        :rtype: _Model
        :raises ModelManagerError: if there is an error fetching entry
        """

        try:
            response = cls.conn.execute(cls.query())
            row = response.fetchone()
            return row[0]
        except sqlite3.ProgrammingError as e:
            raise exceptions.ModelManagerError(
                f"raised exception during fetching stored model: {str(e)}"
            )

    @classmethod
    def all(cls) -> Iterator[_Model]:
        """Exec query and fetch a list of data from database.

        :return: all query result as model instance
        :rtype: Iterator[_Model]
        :raises ModelManagerError: if there is an error fetching entries
        """
        try:
            response = cls.conn.execute(cls.query())
            rows = response.fetchall()
            return map(lambda r: r[0], rows)
        except sqlite3.ProgrammingError as e:
            raise exceptions.ModelManagerError(
                f"raised exception during fetching all stored models: {str(e)}"
            )

    def save(self) -> Union[int, None]:
        """Exec insertion into database using built query

        :return: true if query was saved or False otherwise
        :rtype: bool
        :raises ModelManagerError: if there is an error saving entry
        """
        try:
            cursor: Cursor = self.conn.execute(self.mutate(), (self,))
            return cursor.lastrowid
        except sqlite3.ProgrammingError as e:
            raise exceptions.ModelManagerError(
                f"raised exception while saving model: {str(e)}"
            )


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


class Collection(_Model):
    """Collection is in charge of link the metadata and it corresponding media"""

    media: List[Union[Media[CID], Collectable]]
    metadata: Meta

    @pydantic.validator("media", pre=True)
    def serialize_media_pre(cls, v: Any):
        """Pre serialize media to object"""
        if isinstance(v, bytes):
            parsed = ast.literal_eval(v.decode())
            instances = map(lambda x: Media(**x), parsed)
            return list(instances)
        return v
