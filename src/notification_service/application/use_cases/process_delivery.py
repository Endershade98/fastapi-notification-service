# src/notification_service/application/use_cases/process_delivery.py

from __future__ import annotations

from notification_service.application.commands.process_delivery import (
    ProcessDeliveryCommand,
)
from notification_service.application.exceptions.application_exceptions import NotificationNotFound
from notification_service.application.ports.notification_provider import (
    NotificationProvider,
)
from notification_service.application.ports.notification_repository import (
    NotificationRepository,
)



class ProcessDelivery:
    """Process the delivery of a pending notification."""

    def __init__(
        self,
        notification_repository: NotificationRepository,
        notification_provider: NotificationProvider,
    ) -> None:
        self._notification_repository = notification_repository
        self._notification_provider = notification_provider

    async def execute(
        self,
        command: ProcessDeliveryCommand,
    ) -> None:
        notification = await self._notification_repository.get_by_id(
            command.notification_id,
        )

        if notification is None:
            raise NotificationNotFound(
                notification_id=str(command.notification_id),
            )

        try:
            await self._notification_provider.send(notification)
        except Exception as exc:
            reason = str(exc).strip() or "Notification delivery failed."

            notification.mark_as_failed(reason)
            await self._notification_repository.save(notification)

            return

        notification.mark_as_sent()
        await self._notification_repository.save(notification)