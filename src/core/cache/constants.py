import os
import datetime

# Convention for importing constants
from src.core.constants import PROJECT_ROOT


# Alias for ordering flags
ASC = 1
DESC = -1

# Sqlite Cache settings
DB_NAME = os.getenv("DB_NAME")
DB_DEFAULT = f"{PROJECT_ROOT}/{DB_NAME}"
DB_ISOLATION_LEVEL = os.getenv("DB_ISOLATION")
DB_DATE_VERSION = datetime.date.today().strftime("%Y%m%d")
DB_TABLES_SCRIPT = f"{PROJECT_ROOT}/src/core/cache/tables.sql"
DB_INDEX_SCRIPT = f"{PROJECT_ROOT}/src/core/cache/indexes.sql"

__all__ = [
    "ASC",
    "DESC",
    "DB_NAME",
    "DB_DEFAULT",
    "DB_ISOLATION_LEVEL",
    "DB_DATE_VERSION",
    "DB_TABLES_SCRIPT",
    "DB_INDEX_SCRIPT",
]
