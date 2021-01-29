import os
from datetime import date

from src.core import logger, Log
import src.core.scheme as scheme
import resolvers

__author__ = 'gmena'
if __name__ == '__main__':

    DB_DATE_VERSION = date.today().strftime('%Y%m%d')
    ROOT_PROJECT = os.environ.get('PROJECT_ROOT', '/data/watchit')


    # Process each resolver and merge it
    for resolver in resolvers.load():
        _resolver = resolver(scheme)  # Init class with scheme
        logger.info(f"{Log.BOLD}Starting migrations from {_resolver} {DB_DATE_VERSION}{Log.ENDC}")
        migration_result = _resolver()  # Call class and start migration
        logger.info(migration_result)
        # scheme.validator.check(migration_result)

        logger.info(f"{Log.OKGREEN}Migration Complete for {_resolver}{Log.ENDC}")
        # logger.info(f"{Log.OKGREEN}Inserting entries in mongo{Log.ENDC}")

    # logger.info(f"{Log.UNDERLINE}Entries yts indexed: {len(migration_result)}{Log.ENDC}")
