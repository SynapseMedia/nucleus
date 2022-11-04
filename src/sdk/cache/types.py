"""
Scheme definition for movies. 
Each scheme here defined help us to keep a standard for runtime processing of movies. 
All processed data is later used in the creation of standard metadata (ERC-1155, ..), pipeline cache, marshalling, etc; 
"""
import sqlite3
import pydantic
import src.core.cache as cache
import enum

# Convention for importing constants
from src.core.types import Any, Iterator
from src.core.cache.types import Cursor, Condition
from .constants import INSERT_MOVIE, FETCH_MOVIE


class MediaType(enum.Enum):
    """Any resource type should be listed here"""

    IMAGE = 0
    VIDEO = 1


class CoreModel(pydantic.BaseModel):
    """Model based SQL manager"""

    class Config:
        query: str = FETCH_MOVIE
        mutation: str = INSERT_MOVIE
        use_enum_values = True
        validate_assignment = True

    def __conform__(self, protocol: sqlite3.PrepareProtocol):
        """Sqlite3 adapter
        ref: https://docs.python.org/3/library/sqlite3.html#sqlite3-adapters
        """
        if protocol is sqlite3.PrepareProtocol:
            raw_fields = self.dict().values()
            map_fields = map(str, raw_fields)
            return ";".join(map_fields)

    # def batch():

    @classmethod
    def filter(cls, condition: Condition):
        """Filter query adding extra conditions to conditions

        :param condition: Condition to append to query
        :raises exceptions.InvalidQuery: If not previous query builtin
        :return: self
        :rtype: Self
        """

        ...

    @classmethod
    def get(cls) -> Any:
        """Exec query and fetch one entry from database.

        :return: Any derived model
        :rtype: Any
        """

        with cache.connected() as conn:
            response = conn.execute(cls.Config.query)
            rows = response.fetchone()  # raw data
            return rows[0]

    @classmethod
    def fetch(cls) -> Iterator[Any]:
        """Exec query and fetch a list of data from database.

        :return: Any list of derived model
        :rtype: Iterator[Any]
        """

        with cache.connected() as conn:
            response = conn.execute(cls.Config.query)
            rows = response.fetchall()  # raw data
            return rows[0]

    def save(self, **kwargs: Any) -> bool:
        """Exec insertion into database using built query

        :raises exceptions.InvalidMutation: If not query builtin
        :return: True if query was saved or False otherwise
        :rtype: bool
        """

        with cache.connected() as conn:
            # q: Query = self.Config.query
            cursor: Cursor = conn.execute(self.Config.mutation, (self,))
            return cursor.rowcount > 0
