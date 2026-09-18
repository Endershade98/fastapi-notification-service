# src/notification_service/domain/value_objects/delivery_log.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .notification_status import NotificationStatus


@dataclass(frozen=True, slots=True)
class DeliveryLog:
    """
    Immutable audit entry describing a change in notification delivery state.
    """

    status: NotificationStatus
    message: str
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        status: NotificationStatus,
        message: str,
    ) -> DeliveryLog:
        """Create a delivery log entry using the current UTC time."""
        return cls(
            status=status,
            message=message,
            occurred_at=datetime.now(timezone.utc),
        )

    def __post_init__(self) -> None:
        if not self.message.strip():
            raise ValueError("Delivery log message cannot be empty.")

        if self.occurred_at.tzinfo is None:
            raise ValueError("Delivery log timestamp must be timezone-aware.")