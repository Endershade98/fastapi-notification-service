# src/notification_service/application/use_cases/get_status.py

from __future__ import annotations

from notification_service.application.exceptions.application_exceptions import NotificationNotFound
from notification_service.application.ports.notification_repository import (
    NotificationRepository,
)
from notification_service.application.queries.get_notification_status import (
    GetNotificationStatusQuery,
)

from notification_service.domain.value_objects.notification_status import (
    NotificationStatus,
)


class GetStatus:
    """Retrieve the current status of a notification."""

    def __init__(
        self,
        notification_repository: NotificationRepository,
    ) -> None:
        self._notification_repository = notification_repository

    async def execute(
        self,
        query: GetNotificationStatusQuery,
    ) -> NotificationStatus:
        notification = await self._notification_repository.get_by_id(
            query.notification_id,
        )

        if notification is None:
            raise NotificationNotFound(
                notification_id=str(query.notification_id),
            )

        return notification.status