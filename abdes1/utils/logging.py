"""
logging.py

Mae console output ore consistent during initial development.
"""
import datetime


def log_event(source: str, event: str) -> None:
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    # if the source has '-' in it, then it is a system component. Add 2 spaces before the event
    # create a variable containing the extra space to use in the log message

    if "-" in source:
        extra_space = "  "
    else:
        extra_space = ""

    log_message = f"{timestamp} [{source:10}] {extra_space}{event}"
    print(log_message)


# def log_info(message: str) -> None:
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     log_message = f"{timestamp} - INFO: {message}"
#     print(log_message)


# def log_warning(message: str) -> None:
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     log_message = f"{timestamp} - WARNING: {message}"
#     print(log_message)


# def log_error(message: str) -> None:
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     log_message = f"{timestamp} - ERROR: {message}"
#     print(log_message)


# def log_critical(message: str) -> None:
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     log_message = f"{timestamp} - CRITICAL: {message}"
#     print(log_message)
