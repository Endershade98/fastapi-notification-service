# tests/unit/domain/test_notification_channel.py

from notification_service.domain.value_objects.notification_channel import (
    NotificationChannel,
)


def test_push_channel() -> None:
    assert NotificationChannel.PUSH.value == "push"


def test_sms_channel() -> None:
    assert NotificationChannel.SMS.value == "sms"


def test_channel_is_string_compatible() -> None:
    assert str(NotificationChannel.PUSH) == "push"