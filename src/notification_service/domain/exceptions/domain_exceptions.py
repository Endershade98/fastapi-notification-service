# src/notification_service/domain/exceptions/domain_exceptions.py

from __future__ import annotations


class DomainException(Exception):
    """Base exception for domain-level rule violations."""


class InvalidNotificationStateTransition(DomainException):
    """Raised when a Notification performs an illegal state transition."""

    def __init__(
        self,
        *,
        current_status: str,
        requested_status: str,
    ) -> None:
        self.current_status = current_status
        self.requested_status = requested_status

        super().__init__(
            f"Invalid notification state transition: "
            f"{current_status} -> {requested_status}."
        )