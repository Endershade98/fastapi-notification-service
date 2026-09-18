# src/notification_service/application/ports/notification_provider.py

from __future__ import annotations

from abc import ABC, abstractmethod

from notification_service.domain.entities.notification import Notification


class NotificationProvider(ABC):
    """Port for external notification delivery providers."""

    @abstractmethod
    async def send(self, notification: Notification) -> None:
        """Deliver a notification through an external provider."""
        raise NotImplementedError