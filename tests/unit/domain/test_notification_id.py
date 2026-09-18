# tests/unit/domain/test_notification_id.py

from uuid import UUID

from notification_service.domain.value_objects.notification_id import (
    NotificationId,
)


def test_generate_creates_valid_uuid() -> None:
    notification_id = NotificationId.generate()

    assert isinstance(notification_id.value, UUID)


def test_generated_ids_are_unique() -> None:
    first = NotificationId.generate()
    second = NotificationId.generate()

    assert first != second


def test_notification_id_can_be_created_from_string() -> None:
    original = NotificationId.generate()

    restored = NotificationId.from_string(str(original))

    assert restored == original


def test_notification_id_is_immutable() -> None:
    notification_id = NotificationId.generate()

    try:
        notification_id.value = UUID(int=0)
    except AttributeError:
        pass
    else:
        raise AssertionError("NotificationId must be immutable.")