# tests/integration/test_notification_repository.py

from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy import delete

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
from notification_service.infrastructure.persistence.database import (
    async_session_factory,
)
from notification_service.infrastructure.persistence.models import (
    NotificationModel,
)
from notification_service.infrastructure.persistence.repositories import (
    SQLAlchemyNotificationRepository,
)


@pytest.mark.asyncio
async def test_notification_repository_persists_and_reads_notification() -> None:
    notification = Notification(
        id=NotificationId(uuid4()),
        recipient=Recipient("user@example.com"),
        channel=NotificationChannel.PUSH,
        content="Integration test",
    )

    async with async_session_factory() as session:
        repository = SQLAlchemyNotificationRepository(session)

        await repository.add(notification)

        persisted = await repository.get_by_id(notification.id)

        assert persisted is not None
        assert persisted.id == notification.id
        assert persisted.recipient == notification.recipient
        assert persisted.channel == notification.channel
        assert persisted.content == notification.content
        assert persisted.status == NotificationStatus.PENDING

        await session.execute(
            delete(NotificationModel).where(
                NotificationModel.id == notification.id.value,
            ),
        )
        await session.commit()


@pytest.mark.asyncio
async def test_notification_repository_preserves_persisted_status() -> None:
    notification = Notification(
        id=NotificationId(uuid4()),
        recipient=Recipient("user@example.com"),
        channel=NotificationChannel.PUSH,
        content="Integration test",
    )

    notification.mark_as_sent()

    async with async_session_factory() as session:
        repository = SQLAlchemyNotificationRepository(session)

        await repository.add(notification)

        persisted = await repository.get_by_id(notification.id)

        assert persisted is not None
        assert persisted.status == NotificationStatus.SENT

        await session.execute(
            delete(NotificationModel).where(
                NotificationModel.id == notification.id.value,
            ),
        )
        await session.commit()