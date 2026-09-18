# src/notification_service/domain/value_objects/recipient.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Recipient:
    """
    Destination of a notification.

    The domain deliberately does not know whether the recipient
    will be reached through SMS, push, email, or another provider.
    """

    value: str

    def __post_init__(self) -> None:
        normalized_value = self.value.strip()

        if not normalized_value:
            raise ValueError("Recipient cannot be empty.")

        object.__setattr__(self, "value", normalized_value)

    def __str__(self) -> str:
        return self.value