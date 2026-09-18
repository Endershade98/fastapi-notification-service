# tests/unit/application/fakes/fake_notification_repository.py

from __future__ import annotations

from notification_service.application.ports.notification_repository import (
    NotificationRepository,
)
from notification_service.domain.entities.notification import Notification
from notification_service.domain.value_objects.notification_id import NotificationId


class FakeNotificationRepository(NotificationRepository):
    """In-memory notification repository for unit tests."""

    def __init__(self) -> None:
        self.notifications: dict[NotificationId, Notification] = {}
        self.added_notifications: list[Notification] = []
        self.saved_notifications: list[Notification] = []

    async def add(self, notification: Notification) -> None:
        self.notifications[notification.id] = notification
        self.added_notifications.append(notification)

    async def get_by_id(
        self,
        notification_id: NotificationId,
    ) -> Notification | None:
        return self.notifications.get(notification_id)

    async def save(self, notification: Notification) -> None:
        self.notifications[notification.id] = notification
        self.saved_notifications.append(notification)

    def clear(self) -> None:
        """Remove all stored notifications and tracking data."""
        self.notifications.clear()
        self.added_notifications.clear()
        self.saved_notifications.clear()