# src/notification_service/application/use_cases/send_notification.py

from __future__ import annotations

from notification_service.application.commands.send_notification import (
    SendNotificationCommand,
)
from notification_service.application.ports.notification_repository import (
    NotificationRepository,
)
from notification_service.domain.entities.notification import Notification
from notification_service.domain.value_objects.notification_id import NotificationId
from notification_service.domain.value_objects.recipient import Recipient


class SendNotification:
    """Create and persist a new notification."""

    def __init__(
        self,
        notification_repository: NotificationRepository,
    ) -> None:
        self._notification_repository = notification_repository

    async def execute(
        self,
        command: SendNotificationCommand,
    ) -> NotificationId:
        notification = Notification.create(
            recipient=Recipient(command.recipient),
            channel=command.channel,
            content=command.content,
        )

        await self._notification_repository.add(notification)

        return notification.id