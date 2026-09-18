# tests/unit/application/test_process_delivery.py

from __future__ import annotations

import pytest

from notification_service.application.commands.process_delivery import (
    ProcessDeliveryCommand,
)
from notification_service.application.exceptions.application_exceptions import (
    NotificationNotFound,
)
from notification_service.application.use_cases.process_delivery import (
    ProcessDelivery,
)
from notification_service.domain.entities.notification import Notification
from notification_service.domain.value_objects.notification_channel import (
    NotificationChannel,
)
from notification_service.domain.value_objects.notification_status import (
    NotificationStatus,
)
from notification_service.domain.value_objects.recipient import Recipient
from notification_service.application.ports.notification_provider import (
    NotificationProvider,
)
from tests.unit.application.fakes.fake_notification_provider import (
    FakeNotificationProvider,
)
from tests.unit.application.fakes.fake_notification_repository import (
    FakeNotificationRepository,
)


def create_pending_notification() -> Notification:
    """Create a notification ready for delivery processing."""
    return Notification.create(
        recipient=Recipient("user@example.com"),
        channel=NotificationChannel.PUSH,
        content="Test notification",
    )


@pytest.mark.asyncio
async def test_process_delivery_marks_notification_as_sent() -> None:
    repository = FakeNotificationRepository()
    provider = FakeNotificationProvider()

    notification = create_pending_notification()
    await repository.add(notification)

    use_case = ProcessDelivery(
        notification_repository=repository,
        notification_provider=provider,
    )

    command = ProcessDeliveryCommand(
        notification_id=notification.id,
    )

    result = await use_case.execute(command)

    assert result is None
    assert notification.status == NotificationStatus.SENT

    assert len(provider.sent_notifications) == 1
    assert provider.sent_notifications[0] is notification

    assert len(repository.saved_notifications) == 1
    assert repository.saved_notifications[0] is notification


@pytest.mark.asyncio
async def test_process_delivery_marks_notification_as_failed_when_provider_fails() -> None:
    repository = FakeNotificationRepository()
    provider = FakeNotificationProvider(
        error=RuntimeError("Provider unavailable"),
    )

    notification = create_pending_notification()
    await repository.add(notification)

    use_case = ProcessDelivery(
        notification_repository=repository,
        notification_provider=provider,
    )

    command = ProcessDeliveryCommand(
        notification_id=notification.id,
    )

    result = await use_case.execute(command)

    assert result is None
    assert notification.status == NotificationStatus.FAILED

    assert provider.sent_notifications == []

    assert len(repository.saved_notifications) == 1
    assert repository.saved_notifications[0] is notification

    assert notification.delivery_logs[-1].status == NotificationStatus.FAILED
    assert notification.delivery_logs[-1].message == "Provider unavailable"


@pytest.mark.asyncio
async def test_process_delivery_raises_when_notification_does_not_exist() -> None:
    repository = FakeNotificationRepository()
    provider = FakeNotificationProvider()

    use_case = ProcessDelivery(
        notification_repository=repository,
        notification_provider=provider,
    )

    notification = create_pending_notification()

    command = ProcessDeliveryCommand(
        notification_id=notification.id,
    )

    with pytest.raises(
        NotificationNotFound,
        match="was not found",
    ):
        await use_case.execute(command)

    assert provider.sent_notifications == []
    assert repository.saved_notifications == []


@pytest.mark.asyncio
async def test_process_delivery_updates_persisted_notification_status() -> None:
    repository = FakeNotificationRepository()
    provider = FakeNotificationProvider()

    notification = create_pending_notification()
    await repository.add(notification)

    use_case = ProcessDelivery(
        notification_repository=repository,
        notification_provider=provider,
    )

    command = ProcessDeliveryCommand(
        notification_id=notification.id,
    )

    await use_case.execute(command)

    stored_notification = await repository.get_by_id(notification.id)

    assert stored_notification is notification
    assert stored_notification.status == NotificationStatus.SENT