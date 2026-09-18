# tests/unit/application/test_get_status.py

from __future__ import annotations

import pytest

from notification_service.application.exceptions.application_exceptions import (
    NotificationNotFound,
)
from notification_service.application.ports.notification_repository import (
    NotificationRepository,
)
from notification_service.application.queries.get_notification_status import (
    GetNotificationStatusQuery,
)
from notification_service.application.use_cases.get_status import GetStatus
from notification_service.domain.entities.notification import Notification
from notification_service.domain.value_objects.notification_channel import (
    NotificationChannel,
)
from notification_service.domain.value_objects.notification_status import (
    NotificationStatus,
)
from notification_service.domain.value_objects.recipient import Recipient
from tests.unit.application.fakes.fake_notification_repository import (
    FakeNotificationRepository,
)


def create_notification() -> Notification:
    """Create a notification for status tests."""
    return Notification.create(
        recipient=Recipient("user@example.com"),
        channel=NotificationChannel.PUSH,
        content="Test notification",
    )


@pytest.mark.asyncio
async def test_get_status_returns_pending_status() -> None:
    repository = FakeNotificationRepository()
    notification = create_notification()

    await repository.add(notification)

    use_case = GetStatus(
        notification_repository=repository,
    )

    query = GetNotificationStatusQuery(
        notification_id=notification.id,
    )

    status = await use_case.execute(query)

    assert status == NotificationStatus.PENDING


@pytest.mark.asyncio
async def test_get_status_returns_sent_status() -> None:
    repository = FakeNotificationRepository()
    notification = create_notification()

    notification.mark_as_sent()
    await repository.add(notification)

    use_case = GetStatus(
        notification_repository=repository,
    )

    query = GetNotificationStatusQuery(
        notification_id=notification.id,
    )

    status = await use_case.execute(query)

    assert status == NotificationStatus.SENT


@pytest.mark.asyncio
async def test_get_status_returns_failed_status() -> None:
    repository = FakeNotificationRepository()
    notification = create_notification()

    notification.mark_as_failed("Provider unavailable")
    await repository.add(notification)

    use_case = GetStatus(
        notification_repository=repository,
    )

    query = GetNotificationStatusQuery(
        notification_id=notification.id,
    )

    status = await use_case.execute(query)

    assert status == NotificationStatus.FAILED


@pytest.mark.asyncio
async def test_get_status_raises_when_notification_does_not_exist() -> None:
    repository = FakeNotificationRepository()

    use_case = GetStatus(
        notification_repository=repository,
    )

    notification = create_notification()

    query = GetNotificationStatusQuery(
        notification_id=notification.id,
    )

    with pytest.raises(
        NotificationNotFound,
        match="was not found",
    ):
        await use_case.execute(query)