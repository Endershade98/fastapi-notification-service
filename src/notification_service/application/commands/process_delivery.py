# src/notification_service/application/commands/process_delivery.py

from __future__ import annotations

from dataclasses import dataclass

from notification_service.domain.value_objects.notification_id import NotificationId


@dataclass(frozen=True)
class ProcessDeliveryCommand:
    """Input required to process a notification delivery."""

    notification_id: NotificationId