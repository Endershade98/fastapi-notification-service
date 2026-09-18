# src/notification_service/infrastructure/persistence/repositories/sqlalchemy_notification_repository.py

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from notification_service.application.ports.notification_repository import (
    NotificationRepository,
)
from notification_service.domain.entities.notification import Notification
from notification_service.domain.value_objects.notification_channel import (
    NotificationChannel,
)
from notification_service.domain.value_objects.notification_id import (
    NotificationId,
)
from notification_service.domain.value_objects.notification_status import (
    NotificationStatus,
)
from notification_service.domain.value_objects.recipient import Recipient
from notification_service.infrastructure.persistence.models.notification_model import (
    NotificationModel,
)


class SQLAlchemyNotificationRepository(NotificationRepository):
    """SQLAlchemy implementation of the notification repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, notification: Notification) -> None:
        now = datetime.now(timezone.utc)

        model = NotificationModel(
            id=notification.id.value,
            recipient=notification.recipient.value,
            channel=notification.channel.value,
            content=notification.content,
            status=notification.status.value,
            created_at=now,
            updated_at=now,
        )

        self._session.add(model)
        await self._session.commit()

    async def get_by_id(
        self,
        notification_id: NotificationId,
    ) -> Notification | None:
        statement = select(NotificationModel).where(
            NotificationModel.id == notification_id.value,
        )

        result = await self._session.execute(statement)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def save(self, notification: Notification) -> None:
        model = await self._session.get(
            NotificationModel,
            notification.id.value,
        )

        if model is None:
            raise ValueError(
                f"Notification '{notification.id}' does not exist.",
            )

        model.recipient = notification.recipient.value
        model.channel = notification.channel.value
        model.content = notification.content
        model.status = notification.status.value
        model.updated_at = datetime.now(timezone.utc)

        await self._session.commit()

    @staticmethod
    def _to_domain(model: NotificationModel) -> Notification:
        return Notification.reconstitute(
            id=NotificationId(model.id),
            recipient=Recipient(model.recipient),
            channel=NotificationChannel(model.channel),
            content=model.content,
            status=NotificationStatus(model.status),
        )