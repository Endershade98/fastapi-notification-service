# src/notification_service/presentation/api/routes/notifications.py

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from notification_service.application.commands.send_notification import (
    SendNotificationCommand,
)
from notification_service.application.use_cases.send_notification import (
    SendNotification,
)
from notification_service.presentation.api.dependencies import (
    get_send_notification,
)
from notification_service.presentation.api.schemas.notifications import (
    CreateNotificationRequest,
    CreateNotificationResponse,
)


router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)


@router.post(
    "",
    response_model=CreateNotificationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_notification(
    request: CreateNotificationRequest,
    use_case: SendNotification = Depends(get_send_notification),
) -> CreateNotificationResponse:
    """Accept a notification for asynchronous delivery."""
    command = SendNotificationCommand(
        recipient=request.recipient,
        channel=request.channel,
        content=request.content,
    )

    notification_id = await use_case.execute(command)

    return CreateNotificationResponse(
        notification_id=notification_id.value,
        status="pending",
    )