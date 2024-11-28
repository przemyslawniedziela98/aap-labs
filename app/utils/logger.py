from ..models.logger import AppLog
from .. import db


class GlobalLogger:
    """
    Global logger class that logs events to the database.
    """

    @staticmethod
    def log_event(event_type: str, message: str) -> None:
        """
        Logs an event to the database.

        Args:
            event_type (str): The type of event (e.g., INFO, ERROR, LOGIN).
            message (str): The details of the event.
        """
        try:
            log_entry = AppLog(event_type=event_type, message=message)
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            print(f"Failed to log event: {e}")

    @staticmethod
    def log_info(message: str) -> None:
        """
        Logs an informational event.

        Args:
            message (str): The details of the event.
        """
        GlobalLogger.log_event("INFO", message)

    @staticmethod
    def log_error(message: str) -> None:
        """
        Logs an error event.

        Args:
            message (str): The details of the error.
        """
        GlobalLogger.log_event("ERROR", message)
