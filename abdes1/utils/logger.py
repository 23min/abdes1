"""
logger.py

Make console output more consistent during initial development.
"""
import logging
import os

from copy import copy
from logging import Logger
from typing import Any, TYPE_CHECKING, Tuple
from collections.abc import MutableMapping


if TYPE_CHECKING:
    _LoggerAdapter = logging.LoggerAdapter[logging.Logger]
else:
    _LoggerAdapter = logging.LoggerAdapter


loglevel = os.environ.get("LOGGING_LEVEL_DEFAULT") or "DEBUG"
logging.basicConfig(
    level=loglevel,
    format="%(asctime)s [%(levelname)-8s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("myapp.log"),
    ],
)


class Color:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    LIGHT_GRAY = "\033[37m"
    DARK_GRAY = "\033[90m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_MAGENTA = "\033[95m"
    LIGHT_CYAN = "\033[96m"
    WHITE = "\033[97m"


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # modify copy for console output and not affect log output
        record_copy = copy(record)
        if record_copy.levelno == logging.ERROR:
            record_copy.msg = f"{Color.RED}{record.msg}{Color.RESET}"
        elif record_copy.levelno == logging.INFO:
            record_copy.msg = f"{Color.LIGHT_GRAY}{record.msg}{Color.RESET}"
        elif record_copy.levelno == logging.DEBUG:
            record_copy.msg = f"{Color.DARK_GRAY}{record.msg}{Color.RESET}"
        return super().format(record_copy)


class LoggerAdapter(_LoggerAdapter):
    def __init__(self, logger: "Logger", extra: MutableMapping[str, str]):
        if "source" not in extra:
            extra["source"] = "unknown"
        super().__init__(logger, extra)

    def process(self, msg: str, kwargs: MutableMapping[str, Any]) -> Tuple[str, Any]:
        kwargs["extra"] = self.extra
        # return "[{}] {}".format(self.extra["source"], msg), kwargs
        return msg, kwargs


class ALogger:
    def __init__(self, source: str) -> None:
        self.source = source

        # Create logger for the specific source and set propagate to False to avoid double logging
        logger = logging.getLogger(f"{__name__}_{self.source}")
        logger.propagate = False
        logger.setLevel(self._get_logging_level())

        # Check if logger already has handlers to avoid adding them multiple times
        if not logger.hasHandlers():
            console_handler = logging.StreamHandler()
            console_format = "%(asctime)s [%(levelname)-8s] [%(source)-10s] %(message)s"
            console_handler.setFormatter(ColoredFormatter(console_format))
            logger.addHandler(console_handler)

            file_handler = logging.FileHandler("myapp.log")
            file_formatter = logging.Formatter("%(asctime)s [%(levelname)-8s] [%(source)-10s] %(message)s")
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        self.logger = LoggerAdapter(logger, {"source": source})

        self.warning(f"Loglevel for source '{self.source}' set to {loglevel}")

    def _get_logging_level(self) -> str:
        return os.environ.get(f"LOGGING_LEVEL_{self.source.upper().replace('-', '')}") or os.environ.get("LOGGING_LEVEL_DEFAULT") or "DEBUG"

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)
