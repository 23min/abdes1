"""
logger.py

Make console output more consistent during initial development.
"""
import logging
import os
from dotenv import load_dotenv


load_dotenv()


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
        if record.levelno == logging.ERROR:
            record.msg = f"{Color.RED}{record.msg}{Color.RESET}"
        elif record.levelno == logging.INFO:
            record.msg = f"{Color.LIGHT_GRAY}{record.msg}{Color.RESET}"
        elif record.levelno == logging.DEBUG:
            record.msg = f"{Color.DARK_GRAY}{record.msg}{Color.RESET}"
        return super().format(record)


class Logger:
    def __init__(self, source: str) -> None:
        self.source = source
        # Configure the logging system
        logging.basicConfig(
            level=os.getenv("LOGGING_LEVEL", "DEBUG"),
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("myapp.log"),
            ],
        )
        logging.getLogger().handlers[0].setFormatter(fmt=ColoredFormatter())  # Use the custom formatter for console output

    @staticmethod
    def _update_message(source: str, message: str) -> str:
        extra_space: str = " " if "-" in source else ""
        return f"[{source:10}] {extra_space}{message}"

    def debug(self, message: str) -> None:
        logging.debug(Logger._update_message(self.source, message))

    def info(self, message: str) -> None:
        logging.info(Logger._update_message(self.source, message))

    def warning(self, message: str) -> None:
        logging.warning(Logger._update_message(self.source, message))

    def error(self, message: str) -> None:
        logging.error(Logger._update_message(self.source, message))
