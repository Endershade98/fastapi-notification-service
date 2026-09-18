# tests/integration/conftest.py

from __future__ import annotations

import pytest_asyncio

from notification_service.infrastructure.persistence.database import (
    dispose_engine,
)


@pytest_asyncio.fixture(autouse=True)
async def dispose_database_engine():
    """Dispose the global async engine after every integration test."""
    yield

    await dispose_engine()