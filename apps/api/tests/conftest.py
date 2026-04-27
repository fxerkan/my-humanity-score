"""Pytest configuration and shared fixtures.

Integration tests require a running PostgreSQL instance.
Set DATABASE_URL / DATABASE_URL_SYNC env vars
(default: mhs:mhs@localhost:5432/mhs_test).

Teardown uses DROP SCHEMA … CASCADE to avoid FK dependency errors
when dropping tables that have cross-table foreign key constraints.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Import all ORM models so Base.metadata knows every table before create_all
import models.activity  # noqa: F401
import models.group  # noqa: F401
import models.score  # noqa: F401
import models.user  # noqa: F401
from core.database import Base, get_db
from main import app

# ── Test database URLs ────────────────────────────────────────────────────────
_TEST_DB_SYNC = os.getenv(
    "DATABASE_URL_SYNC",
    "postgresql://mhs:mhs@localhost:5432/mhs_test",
)
_TEST_DB_ASYNC = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://mhs:mhs@localhost:5432/mhs_test",
)


# ── Session-scoped: create schema once, tear down with CASCADE ───────────────
@pytest.fixture(scope="session", autouse=True)
def run_migrations() -> Generator[None, None, None]:
    """Create all tables before the test session.

    Teardown drops the entire public schema with CASCADE to avoid FK
    constraint errors (``psycopg2.errors.DependentObjectsStillExist``),
    then recreates an empty public schema for the next run.
    """
    sync_engine = create_engine(_TEST_DB_SYNC)
    Base.metadata.create_all(sync_engine)
    yield
    with sync_engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO mhs"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
    sync_engine.dispose()


# ── Function-scoped async session (SAVEPOINT rollback per test) ──────────────
@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Async DB session that rolls back via SAVEPOINT after each test.

    Uses a nested transaction (SAVEPOINT) so each test starts clean
    without committing anything to the database.
    """
    async_engine = create_async_engine(_TEST_DB_ASYNC)
    async with async_engine.connect() as conn:
        await conn.begin()
        # Nested SAVEPOINT — rolled back per-test, outer transaction never commits
        await conn.begin_nested()
        session_factory = async_sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with session_factory() as session:
            yield session
            await session.rollback()
    await async_engine.dispose()


# ── Async HTTP client with DB dependency override ────────────────────────────
@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """AsyncClient with FastAPI DB dependency replaced by the test session."""

    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


# ── Sync TestClient (no DB — health and unit-level tests) ─────────────────────
@pytest.fixture
def sync_client() -> TestClient:
    """Sync TestClient for endpoints that do not require a database."""
    return TestClient(app)
