# src/notification_service/presentation/api/dependencies/dependencies.py

from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from notification_service.application.ports.notification_repository import (
    NotificationRepository,
)
from notification_service.application.use_cases.send_notification import (
    SendNotification,
)
from notification_service.infrastructure.persistence.database import (
    get_session,
)
from notification_service.infrastructure.persistence.repositories import (
    SQLAlchemyNotificationRepository,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session to the request scope."""
    async for session in get_session():
        yield session


def get_notification_repository(
    session: AsyncSession = Depends(get_db_session),
) -> NotificationRepository:
    """Build the notification repository adapter."""
    return SQLAlchemyNotificationRepository(session)


def get_send_notification(
    repository: NotificationRepository = Depends(
        get_notification_repository,
    ),
) -> SendNotification:
    """Build the SendNotification application service."""
    return SendNotification(repository)