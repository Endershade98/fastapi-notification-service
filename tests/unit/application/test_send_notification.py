# tests/unit/application/test_send_notification.py

from __future__ import annotations

import pytest

from notification_service.application.commands.send_notification import (
    SendNotificationCommand,
)
from notification_service.application.use_cases.send_notification import (
    SendNotification,
)
from notification_service.domain.value_objects.notification_channel import (
    NotificationChannel,
)
from notification_service.domain.value_objects.notification_id import (
    NotificationId,
)
from notification_service.domain.value_objects.notification_status import (
    NotificationStatus,
)
from tests.unit.application.fakes.fake_notification_repository import (
    FakeNotificationRepository,
)


@pytest.mark.asyncio
async def test_send_notification_creates_and_persists_notification() -> None:
    repository = FakeNotificationRepository()
    use_case = SendNotification(
        notification_repository=repository,
    )

    command = SendNotificationCommand(
        recipient="+393331234567",
        channel=NotificationChannel.SMS,
        content="Test notification",
    )

    notification_id = await use_case.execute(command)

    assert isinstance(notification_id, NotificationId)
    assert len(repository.added_notifications) == 1

    notification = repository.added_notifications[0]

    assert notification.id == notification_id
    assert notification.recipient.value == "+393331234567"
    assert notification.channel == NotificationChannel.SMS
    assert notification.content == "Test notification"
    assert notification.status == NotificationStatus.PENDING


@pytest.mark.asyncio
async def test_send_notification_persists_notification_by_id() -> None:
    repository = FakeNotificationRepository()
    use_case = SendNotification(
        notification_repository=repository,
    )

    command = SendNotificationCommand(
        recipient="user@example.com",
        channel=NotificationChannel.PUSH,
        content="Hello",
    )

    notification_id = await use_case.execute(command)

    stored_notification = await repository.get_by_id(notification_id)

    assert stored_notification is not None
    assert stored_notification.id == notification_id


@pytest.mark.asyncio
async def test_send_notification_creates_unique_ids() -> None:
    repository = FakeNotificationRepository()
    use_case = SendNotification(
        notification_repository=repository,
    )

    command = SendNotificationCommand(
        recipient="user@example.com",
        channel=NotificationChannel.PUSH,
        content="Hello",
    )

    first_id = await use_case.execute(command)
    second_id = await use_case.execute(command)

    assert first_id != second_id
    assert len(repository.notifications) == 2


@pytest.mark.asyncio
async def test_send_notification_rejects_empty_content() -> None:
    repository = FakeNotificationRepository()
    use_case = SendNotification(
        notification_repository=repository,
    )

    command = SendNotificationCommand(
        recipient="user@example.com",
        channel=NotificationChannel.PUSH,
        content="   ",
    )

    with pytest.raises(ValueError, match="Notification content cannot be empty"):
        await use_case.execute(command)

    assert repository.added_notifications == []
    assert repository.notifications == {}