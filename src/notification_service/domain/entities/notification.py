# src/notification_service/domain/entities/notification.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from ..events.notification_delivery_failed import NotificationDeliveryFailed
from ..events.notification_sent import NotificationSent
from ..exceptions.domain_exceptions import (
    InvalidNotificationStateTransition,
)
from ..value_objects.delivery_log import DeliveryLog
from ..value_objects.notification_channel import NotificationChannel
from ..value_objects.notification_id import NotificationId
from ..value_objects.notification_status import NotificationStatus
from ..value_objects.recipient import Recipient


@dataclass
class Notification:
    """
    Aggregate Root representing a notification delivery intention.

    The aggregate owns its lifecycle, audit log and domain events.
    """

    id: NotificationId
    recipient: Recipient
    channel: NotificationChannel
    content: str

    status: NotificationStatus = field(
        default=NotificationStatus.PENDING,
        init=False,
    )

    delivery_logs: list[DeliveryLog] = field(
        default_factory=list,
        init=False,
    )

    _domain_events: list[object] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise ValueError("Notification content cannot be empty.")

        self._append_delivery_log(
            status=NotificationStatus.PENDING,
            message="Notification created.",
        )

    @classmethod
    def create(
        cls,
        *,
        recipient: Recipient,
        channel: NotificationChannel,
        content: str,
    ) -> Notification:
        """
        Create a new Notification aggregate.

        The domain owns the generation of the NotificationId so that
        application services do not need to know how aggregate identity
        is created.
        """
        return cls(
            id=NotificationId.generate(),
            recipient=recipient,
            channel=channel,
            content=content,
        )

    def mark_as_sent(self) -> None:
        """
        Transition the notification from PENDING to SENT.

        Raises:
            InvalidNotificationStateTransition:
                if the notification is not currently PENDING.
        """
        self._transition_to(
            new_status=NotificationStatus.SENT,
            message="Notification delivered successfully.",
        )

        self._record_event(
            NotificationSent(
                notification_id=self.id,
                occurred_at=datetime.now(timezone.utc),
            )
        )

    def mark_as_failed(self, reason: str) -> None:
        """
        Transition the notification from PENDING to FAILED.

        Raises:
            InvalidNotificationStateTransition:
                if the notification is not currently PENDING.

            ValueError:
                if the failure reason is empty.
        """
        if not reason.strip():
            raise ValueError("Failure reason cannot be empty.")

        self._transition_to(
            new_status=NotificationStatus.FAILED,
            message=reason,
        )

        self._record_event(
            NotificationDeliveryFailed(
                notification_id=self.id,
                reason=reason,
                occurred_at=datetime.now(timezone.utc),
            )
        )

    def pull_domain_events(self) -> list[object]:
        """
        Return and clear the currently pending domain events.

        Events are intentionally kept inside the aggregate until explicitly
        pulled by the application layer.
        """
        events = list(self._domain_events)
        self._domain_events.clear()

        return events

    def _transition_to(
        self,
        *,
        new_status: NotificationStatus,
        message: str,
    ) -> None:
        if not self._is_valid_transition(new_status):
            raise InvalidNotificationStateTransition(
                current_status=self.status.value,
                requested_status=new_status.value,
            )

        self.status = new_status

        self._append_delivery_log(
            status=new_status,
            message=message,
        )

    def _is_valid_transition(
        self,
        new_status: NotificationStatus,
    ) -> bool:
        return (
            self.status == NotificationStatus.PENDING
            and new_status
            in {
                NotificationStatus.SENT,
                NotificationStatus.FAILED,
            }
        )

    def _append_delivery_log(
        self,
        *,
        status: NotificationStatus,
        message: str,
    ) -> None:
        self.delivery_logs.append(
            DeliveryLog.create(
                status=status,
                message=message,
            )
        )

    def _record_event(self, event: object) -> None:
        self._domain_events.append(event)