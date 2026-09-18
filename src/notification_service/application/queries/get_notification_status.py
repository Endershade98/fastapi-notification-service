# src/notification_service/application/queries/get_notification_status.py

from __future__ import annotations

from dataclasses import dataclass

from notification_service.domain.value_objects.notification_id import NotificationId


@dataclass(frozen=True)
class GetNotificationStatusQuery:
    """Input required to retrieve a notification status."""

    notification_id: NotificationId