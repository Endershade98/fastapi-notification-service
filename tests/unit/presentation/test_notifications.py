# tests/unit/presentation/test_notifications.py

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from notification_service.presentation.api.dependencies import (
    get_notification_repository,
)
from notification_service.presentation.api.routes.notifications import router
from tests.unit.application.fakes.fake_notification_repository import (
    FakeNotificationRepository,
)


def create_test_app(
    repository: FakeNotificationRepository,
) -> FastAPI:
    """Create a presentation-only application using a fake repository."""
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_notification_repository] = (
        lambda: repository
    )

    return app


def test_create_notification_returns_accepted_and_pending() -> None:
    repository = FakeNotificationRepository()
    app = create_test_app(repository)

    with TestClient(app) as client:
        response = client.post(
            "/notifications",
            json={
                "recipient": "user@example.com",
                "channel": "push",
                "content": "Hello",
            },
        )

    assert response.status_code == 202

    body = response.json()

    assert body["status"] == "pending"
    assert len(body["notification_id"]) == 36

    assert len(repository.added_notifications) == 1

    notification = repository.added_notifications[0]

    assert str(notification.id) == body["notification_id"]
    assert notification.recipient.value == "user@example.com"
    assert notification.channel.value == "push"
    assert notification.content == "Hello"
    assert notification.status.value == "pending"