"""
Scheme definition for movies. 
Each scheme here defined help us to keep a standard for runtime processing of movies. 
All processed data is later used in the creation of standard metadata (ERC-1155, ..), pipeline cache, marshalling, etc; 
"""

import pydantic
import src.core.cache as cache
import src.sdk.exceptions as exceptions
import functools

# Convention for importing constants
from src.core.types import Any, Literal, Iterator, Callable
from src.core.cache.types import Query, Cursor, Condition
from .constants import INSERT_MOVIE, FETCH_MOVIE

# Allowed actions to execute in cache
Action = Literal["mutation", "query"]


def _query_required(f: Callable[..., Any]) -> Any:
    """Decorate required previously query built

    :param f: A function to execute in wrapper
    :returns: Wrapper function
    :rtype: Callable[..., T]
    """

    @functools.wraps(f)
    def _wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not self.Config.query:
            raise exceptions.InvalidQuery()

        # Get connection a pass it to func call
        return f(self, *args, *kwargs)

    # Return wrapper function
    return _wrapper


class CoreModel(pydantic.BaseModel):
    """Model based SQL builder"""

    class Config:
        sql: str
        query: Query

    @property
    def mutation(self):
        """Build a mutation based on model

        :return: self
        :rtype: Self
        """

        model_dict = self.dict()
        values = model_dict.values()
        fields = ",".join(model_dict.keys())
        fields_range = range(len(model_dict))
        escaped_values = ",".join(map(lambda _: "?", fields_range))

        # Build query based on input model
        sql: str = INSERT_MOVIE % (fields, escaped_values)
        self.Config.query = Query(sql, list(values))
        return self

    @classmethod
    @property
    def query(cls):
        """Build a query based on model

        :return self
        :rtype: Self
        """
        model = cls.construct()
        fields = model.__fields__.keys()
        resources_fields = ",".join(fields)

        sql = FETCH_MOVIE % resources_fields
        model.Config.query = Query(sql)
        return model

    @_query_required
    def filter(self, condition: Condition):
        """Filter query adding extra conditions to conditions

        :param condition: Condition to append to query
        :raises exceptions.InvalidQuery: If not previous query builtin
        :return: self
        :rtype: Self
        """

        # chained query
        sql = self.Config.query.sql
        # get fields defined in condition
        model_dict = self.dict(include={*condition.fields})
        # concat base query with condition
        with_condition = f"{sql} {condition}"
        condition_values = model_dict.values()
        # rebuild chained query 
        q: Query = Query(with_condition, list(condition_values))
        self.Config.query = q
        return self

    @_query_required
    def fetch(self) -> Iterator[Any]:
        """Exec query and fetch data from database.
        The result of fetch its handled by query build process.
        eg. model.filter(...).fetch()

        :raises exceptions.InvalidQuery: If not previous  query builtin
        :return: List of movies
        :rtype: List[Movies]
        """

        def _map_fields(f: Any):
            # ref: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.description
            return f[0]  # first element is the column name

        def _map_result(x: Any):
            params = dict(zip(fields, x))
            return self.construct(**params)

        with cache.connected() as conn:
            q = self.Config.query
            response = conn.execute(q.sql, q.params)
            rows = response.fetchall()  # raw data
            # Get fields from query and join with result to build model
            fields = tuple(map(_map_fields, response.description))
            return map(_map_result, rows)

    def save(self, **kwargs: Any) -> bool:
        """Exec insertion into database using built query

        :raises exceptions.InvalidMutation: If not query builtin
        :return: True if query was saved or False otherwise
        :rtype: bool
        """

        if not self.Config.query:
            raise exceptions.InvalidMutation()

        with cache.connected() as conn:
            q: Query = self.Config.query
            cursor: Cursor = conn.execute(q.sql, q.params)
            return cursor.rowcount > 0
