# src/notification_service/presentation/api/app.py

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from notification_service.infrastructure.persistence.database import (
    dispose_engine,
)
from notification_service.infrastructure.persistence.init_db import init_db
from notification_service.presentation.api.routes.notifications import router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize and clean up application infrastructure."""
    await init_db()

    try:
        yield
    finally:
        await dispose_engine()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Notification Service",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(router)

    return app


app = create_app()