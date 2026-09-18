# src/notification_service/domain/events/notification_sent.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..value_objects.notification_id import NotificationId


@dataclass(frozen=True, slots=True)
class NotificationSent:
    """
    Domain event raised when a notification is successfully delivered.
    """

    notification_id: NotificationId
    occurred_at: datetime