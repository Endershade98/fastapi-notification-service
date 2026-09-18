# src/notification_service/infrastructure/persistence/init_db.py

from __future__ import annotations

from notification_service.infrastructure.persistence.database import engine
from notification_service.infrastructure.persistence.models import Base


async def init_db() -> None:
    """Create database tables required by the application."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)