# src/notification_service/infrastructure/persistence/database.py

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from notification_service.config.settings import get_settings


settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=False,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide an async SQLAlchemy session."""
    async with async_session_factory() as session:
        yield session


async def dispose_engine() -> None:
    """Dispose the SQLAlchemy engine and its connection pool."""
    await engine.dispose()