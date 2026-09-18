# src/notification_service/application/commands/send_notification.py

from __future__ import annotations

from dataclasses import dataclass

from notification_service.domain.value_objects.notification_channel import (
    NotificationChannel,
)


@dataclass(frozen=True)
class SendNotificationCommand:
    """Input required to create a new notification."""

    recipient: str
    channel: NotificationChannel
    content: str