from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from abdes1.actors import Message

    ...


import datetime

# import logging
from abdes1.utils import ALogger
from dotenv import load_dotenv

load_dotenv()


# class Color:
#     RESET = "\033[0m"
#     BLACK = "\033[30m"
#     RED = "\033[31m"
#     GREEN = "\033[32m"
#     YELLOW = "\033[33m"
#     BLUE = "\033[34m"
#     MAGENTA = "\033[35m"
#     CYAN = "\033[36m"
#     LIGHT_GRAY = "\033[37m"
#     DARK_GRAY = "\033[90m"
#     LIGHT_RED = "\033[91m"
#     LIGHT_GREEN = "\033[92m"
#     LIGHT_YELLOW = "\033[93m"
#     LIGHT_BLUE = "\033[94m"
#     LIGHT_MAGENTA = "\033[95m"
#     LIGHT_CYAN = "\033[96m"
#     WHITE = "\033[97m"


# class ColoredFormatter(logging.Formatter):
#     def format(self, record: logging.LogRecord) -> str:
#         if record.levelno == logging.ERROR:
#             record.msg = f"{Color.YELLOW}{record.msg}{Color.RESET}"
#         elif record.levelno == logging.INFO:
#             record.msg = f"{Color.CYAN}{record.msg}{Color.RESET}"
#         elif record.levelno == logging.DEBUG:
#             record.msg = f"{Color.DARK_GRAY}{record.msg}{Color.RESET}"
#         return super().format(record)


class MessageLogger(ALogger):
    def __init__(self, source: str) -> None:
        self.source = source
        # logging.basicConfig(
        #     # level=os.getenv("LOGGING_LEVEL", "DEBUG"),
        #     level="INFO",
        #     format="%(asctime)s [%(levelname)s] %(message)s",
        #     handlers=[
        #         logging.StreamHandler(),
        #         logging.FileHandler("myapp.log"),
        #     ],
        # )
        # logging.getLogger().handlers[0].setFormatter(fmt=ColoredFormatter())  # Use the custom formatter for console output
        # logging.info(f"Message logger created for source '{source}'")

        super().__init__(source=source)

    def log_message(self, event_source: str, message: "Message") -> None:
        """
        Log a message in the actor system.

        Args:
            source (str): The source of the event.
            message (Message): The message to log.
        """
        wall_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Define the column names and widths
        columns = [
            # ("Wall Time", 10.2),
            # ("Time", 22.2),
            # ("Source", 12),
            ("Type", 20),
            ("From ID", 20),
            ("To ID", 20),
            ("Content", 20),
            ("Processed", None),
        ]

        # Construct the log message string
        log_message = ""
        for column, width in columns:
            value = getattr(message, column.lower().replace(" ", "_")) or ""
            if width is not None:
                value = f"{value:<{width}}"
            log_message += f"{value} | "

        # Remove the trailing " | " characters
        log_message = log_message[:-3]

        log_message = f"{wall_time:<12} | {message.time or 0.0:<12.2f} | {event_source:<12} | {log_message}"

        self.info(log_message)
