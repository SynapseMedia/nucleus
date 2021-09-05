import logging
import verboselogs
import coloredlogs


coloredlogs.DEFAULT_FIELD_STYLES = {
    "asctime": {"color": "green"},
    "hostname": {"color": "magenta"},
    "levelname": {"bold": True, "color": "white", "faint": True},
    "name": {"color": "yellow", "faint": True},
    "programname": {"color": "cyan"},
    "username": {"color": "yellow"},
}

coloredlogs.DEFAULT_LEVEL_STYLES = {
    "critical": {"bold": True, "color": "red"},
    "debug": {"color": "green"},
    "error": {"color": "red"},
    "info": {"color": "white", "faint": True},
    "notice": {"color": "yellow", "faint": True},
    "spam": {"color": "green", "faint": True},
    "success": {"color": "green"},
    "verbose": {"color": "blue"},
    "warning": {"color": "yellow"},
}


def log_factory(name, level=logging.DEBUG):
    # create logger
    _logger = verboselogs.VerboseLogger(name)
    _logger.addHandler(logging.StreamHandler())
    _logger.setLevel(level)

    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    coloredlogs.install(level=logging.DEBUG, logger=_logger, fmt=fmt)
    return _logger


logger = log_factory("cli")

__all__ = ['logger', 'logging', 'log_factory']
