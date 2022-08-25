import logging
import verboselogs  # type: ignore
import coloredlogs  # type: ignore


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


def log_factory(name: str, level: int = logging.DEBUG):
    # create logger
    logger = verboselogs.VerboseLogger(name)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(level)
    logger.propagate = False

    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    coloredlogs.install(level=logging.DEBUG, logger=logger, fmt=fmt)  # type: ignore
    return logger


log = log_factory("cli")

__all__ = ["log", "logging", "log_factory"]
