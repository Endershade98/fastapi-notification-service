# src/notification_service/domain/events/notification_delivery_failed.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..value_objects.notification_id import NotificationId


@dataclass(frozen=True, slots=True)
class NotificationDeliveryFailed:
    """
    Domain event raised when notification delivery fails.
    """

    notification_id: NotificationId
    reason: str
    occurred_at: datetime

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise ValueError("Failure reason cannot be empty.")