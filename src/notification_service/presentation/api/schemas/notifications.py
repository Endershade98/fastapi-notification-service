# src/notification_service/presentation/api/schemas/notifications.py

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from notification_service.domain.value_objects.notification_channel import (
    NotificationChannel,
)
from notification_service.domain.value_objects.notification_status import (
    NotificationStatus,
)


class CreateNotificationRequest(BaseModel):
    """HTTP request for creating a notification."""

    recipient: str = Field(min_length=1)
    channel: NotificationChannel
    content: str = Field(min_length=1)


class CreateNotificationResponse(BaseModel):
    """HTTP response after accepting a notification."""

    model_config = ConfigDict(use_enum_values=True)

    notification_id: UUID
    status: NotificationStatus