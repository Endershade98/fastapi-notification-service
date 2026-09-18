# src/notification_service/domain/value_objects/notification_channel.py

from enum import StrEnum


class NotificationChannel(StrEnum):
    """Supported notification delivery channels."""

    PUSH = "push"
    SMS = "sms"