# tests/unit/domain/test_recipient.py

import pytest

from notification_service.domain.value_objects.recipient import Recipient


def test_recipient_strips_surrounding_whitespace() -> None:
    recipient = Recipient("  +393331234567  ")

    assert recipient.value == "+393331234567"


def test_recipient_cannot_be_empty() -> None:
    with pytest.raises(ValueError):
        Recipient("")


def test_recipient_cannot_contain_only_whitespace() -> None:
    with pytest.raises(ValueError):
        Recipient("   ")


def test_equal_recipients_have_equal_value() -> None:
    first = Recipient("+393331234567")
    second = Recipient("+393331234567")

    assert first == second