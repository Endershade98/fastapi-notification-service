# src/notification_service/application/ports/notification_repository.py

from __future__ import annotations

from abc import ABC, abstractmethod

from notification_service.domain.entities.notification import Notification
from notification_service.domain.value_objects.notification_id import NotificationId


class NotificationRepository(ABC):
    """Port for notification persistence."""

    @abstractmethod
    async def add(self, notification: Notification) -> None:
        """Persist a new notification."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        notification_id: NotificationId,
    ) -> Notification | None:
        """Retrieve a notification by its identifier."""
        raise NotImplementedError

    @abstractmethod
    async def save(self, notification: Notification) -> None:
        """Persist changes to an existing notification."""
        raise NotImplementedError