__author__ = "Geolffrey Mena (gmjun2000@gmail.com)"
__version__ = "1.0.0"
__copyright__ = "Copyright (c) 2020 ZorrillosDev"
__license__ = "MIT"

import logging

# create logger
logger = logging.getLogger('migrate')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class Log:
    HEADER = '\033[95m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


__all__ = ["Log", "logger"]
