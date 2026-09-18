# src/notification_service/domain/value_objects/notification_status.py

from enum import StrEnum


class NotificationStatus(StrEnum):
    """Lifecycle states of a Notification aggregate."""

    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

    @property
    def is_terminal(self) -> bool:
        """Return True when the notification cannot transition further."""
        return self in {
            NotificationStatus.SENT,
            NotificationStatus.FAILED,
        }