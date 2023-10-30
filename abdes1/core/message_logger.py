from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abdes1.actors import Message

    ...


import datetime

# import logging
from abdes1.utils import ALogger
from dotenv import load_dotenv

load_dotenv()


class MessageLogger(ALogger):
    def __init__(self, source: str) -> None:
        self.source = source
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
