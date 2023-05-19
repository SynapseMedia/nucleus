import datetime
import os

from nucleus.core.constants import ROOT_DIR

# Alias for ordering flags
ASC = 1
DESC = -1

# Sqlite Cache settings
DB_NAME = os.getenv('DB_NAME')
DB_DEFAULT = f'{ROOT_DIR}/{DB_NAME}'
DB_ISOLATION_LEVEL = os.getenv('DB_ISOLATION')
DB_DATE_VERSION = datetime.date.today().strftime('%Y%m%d')
