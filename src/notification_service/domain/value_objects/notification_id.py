# src/notification_service/domain/value_objects/notification_id.py

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class NotificationId:
    """
    Unique identifier of a Notification aggregate.

    The identifier is immutable and backed by UUID.
    """

    value: UUID

    @classmethod
    def generate(cls) -> NotificationId:
        """Generate a new unique notification identifier."""
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, value: str) -> NotificationId:
        """
        Create a NotificationId from its string representation.

        Raises:
            ValueError: if the value is not a valid UUID.
        """
        return cls(value=UUID(value))

    def __str__(self) -> str:
        return str(self.value)