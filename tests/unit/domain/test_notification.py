# tests/unit/domain/test_notification.py

import pytest

from notification_service.domain.entities.notification import Notification
from notification_service.domain.events.notification_delivery_failed import (
    NotificationDeliveryFailed,
)
from notification_service.domain.events.notification_sent import NotificationSent
from notification_service.domain.exceptions.domain_exceptions import (
    InvalidNotificationStateTransition,
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
from notification_service.domain.value_objects.recipient import Recipient


def create_notification() -> Notification:
    return Notification(
        id=NotificationId.generate(),
        recipient=Recipient("+393331234567"),
        channel=NotificationChannel.SMS,
        content="Test notification",
    )


def test_notification_starts_as_pending() -> None:
    notification = create_notification()

    assert notification.status == NotificationStatus.PENDING


def test_notification_has_creation_audit_log() -> None:
    notification = create_notification()

    assert len(notification.delivery_logs) == 1
    assert notification.delivery_logs[0].status == NotificationStatus.PENDING
    assert notification.delivery_logs[0].message == "Notification created."


def test_notification_can_be_marked_as_sent() -> None:
    notification = create_notification()

    notification.mark_as_sent()

    assert notification.status == NotificationStatus.SENT


def test_notification_sent_creates_audit_log() -> None:
    notification = create_notification()

    notification.mark_as_sent()

    assert len(notification.delivery_logs) == 2
    assert notification.delivery_logs[-1].status == NotificationStatus.SENT


def test_notification_sent_creates_domain_event() -> None:
    notification = create_notification()

    notification.mark_as_sent()

    events = notification.pull_domain_events()

    assert len(events) == 1
    assert isinstance(events[0], NotificationSent)
    assert events[0].notification_id == notification.id


def test_notification_can_be_marked_as_failed() -> None:
    notification = create_notification()

    notification.mark_as_failed("Provider unavailable")

    assert notification.status == NotificationStatus.FAILED


def test_notification_failed_creates_audit_log() -> None:
    notification = create_notification()

    notification.mark_as_failed("Provider unavailable")

    assert len(notification.delivery_logs) == 2
    assert notification.delivery_logs[-1].status == NotificationStatus.FAILED
    assert notification.delivery_logs[-1].message == "Provider unavailable"


def test_notification_failed_creates_domain_event() -> None:
    notification = create_notification()

    notification.mark_as_failed("Provider unavailable")

    events = notification.pull_domain_events()

    assert len(events) == 1
    assert isinstance(events[0], NotificationDeliveryFailed)
    assert events[0].notification_id == notification.id
    assert events[0].reason == "Provider unavailable"


def test_pending_to_sent_is_valid() -> None:
    notification = create_notification()

    notification.mark_as_sent()

    assert notification.status == NotificationStatus.SENT


def test_pending_to_failed_is_valid() -> None:
    notification = create_notification()

    notification.mark_as_failed("Provider unavailable")

    assert notification.status == NotificationStatus.FAILED


def test_sent_to_failed_is_invalid() -> None:
    notification = create_notification()

    notification.mark_as_sent()

    with pytest.raises(InvalidNotificationStateTransition):
        notification.mark_as_failed("Another failure")


def test_failed_to_sent_is_invalid() -> None:
    notification = create_notification()

    notification.mark_as_failed("Provider unavailable")

    with pytest.raises(InvalidNotificationStateTransition):
        notification.mark_as_sent()


def test_sent_to_sent_is_invalid() -> None:
    notification = create_notification()

    notification.mark_as_sent()

    with pytest.raises(InvalidNotificationStateTransition):
        notification.mark_as_sent()


def test_failed_to_failed_is_invalid() -> None:
    notification = create_notification()

    notification.mark_as_failed("Provider unavailable")

    with pytest.raises(InvalidNotificationStateTransition):
        notification.mark_as_failed("Another failure")


def test_empty_content_is_invalid() -> None:
    with pytest.raises(ValueError):
        Notification(
            id=NotificationId.generate(),
            recipient=Recipient("+393331234567"),
            channel=NotificationChannel.SMS,
            content="",
        )


def test_empty_failure_reason_is_invalid() -> None:
    notification = create_notification()

    with pytest.raises(ValueError):
        notification.mark_as_failed("")


def test_pull_domain_events_returns_and_clears_events() -> None:
    notification = create_notification()

    notification.mark_as_sent()

    first_pull = notification.pull_domain_events()
    second_pull = notification.pull_domain_events()

    assert len(first_pull) == 1
    assert second_pull == []