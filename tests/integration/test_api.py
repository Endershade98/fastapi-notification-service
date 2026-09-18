# tests/integration/test_api.py

from __future__ import annotations

from fastapi.testclient import TestClient

from notification_service.presentation.api.app import app


def test_create_notification_e2e() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/notifications",
            json={
                "recipient": "user@example.com",
                "channel": "push",
                "content": "Hello from API",
            },
        )

    assert response.status_code == 202

    body = response.json()

    assert "notification_id" in body
    assert len(body["notification_id"]) == 36
    assert body["status"] == "pending"


def test_create_notification_rejects_empty_content() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/notifications",
            json={
                "recipient": "user@example.com",
                "channel": "push",
                "content": "",
            },
        )

    assert response.status_code == 422


def test_create_notification_rejects_invalid_channel() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/notifications",
            json={
                "recipient": "user@example.com",
                "channel": "email",
                "content": "Hello",
            },
        )

    assert response.status_code == 422


def test_create_notification_rejects_empty_recipient() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/notifications",
            json={
                "recipient": "",
                "channel": "push",
                "content": "Hello",
            },
        )

    assert response.status_code == 422