# tests/unit/application/fakes/fake_notification_provider.py

from __future__ import annotations

from notification_service.application.ports.notification_provider import (
    NotificationProvider,
)
from notification_service.domain.entities.notification import Notification


class FakeNotificationProvider(NotificationProvider):
    """In-memory notification provider for unit tests."""

    def __init__(
        self,
        *,
        error: Exception | None = None,
    ) -> None:
        self.error = error
        self.sent_notifications: list[Notification] = []

    async def send(self, notification: Notification) -> None:
        if self.error is not None:
            raise self.error

        self.sent_notifications.append(notification)

    def reset(self) -> None:
        """Clear the list of delivered notifications."""
        self.sent_notifications.clear()