# src/notification_service/application/exceptions/application_exceptions.py

from __future__ import annotations


class ApplicationException(Exception):
    """Base exception for application-level errors."""


class NotificationNotFound(ApplicationException):
    """Raised when a notification cannot be found."""

    def __init__(self, *, notification_id: str) -> None:
        self.notification_id = notification_id

        super().__init__(
            f"Notification '{notification_id}' was not found.",
        )