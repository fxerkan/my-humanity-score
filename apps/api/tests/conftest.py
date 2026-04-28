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
from core.redis_client import get_redis_dep
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


# ── In-memory Redis mock for unit/integration tests ──────────────────────────

class FakeRedis:
    """Minimal in-memory Redis mock that supports setex, delete, and exists."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    async def setex(self, name: str, time: int, value: str) -> None:
        """Store a key with an ignored TTL (tests don't need real expiry)."""
        self._store[name] = value

    async def delete(self, *names: str) -> int:
        """Delete one or more keys; return count of deleted keys."""
        count = 0
        for name in names:
            if name in self._store:
                del self._store[name]
                count += 1
        return count

    async def exists(self, *names: str) -> int:
        """Return the number of requested keys that exist."""
        return sum(1 for name in names if name in self._store)

    async def eval(self, script: str, numkeys: int, *keys: str) -> int:
        """Minimal eval that handles only the consume-token Lua pattern."""
        key = keys[0] if keys else ""
        if key in self._store:
            del self._store[key]
            return 1
        return 0

    def clear(self) -> None:
        """Reset all stored keys (called between tests)."""
        self._store.clear()


@pytest_asyncio.fixture
async def fake_redis() -> AsyncGenerator[FakeRedis, None]:
    """Yield a fresh FakeRedis instance, cleared after the test."""
    fr = FakeRedis()
    yield fr
    fr.clear()


# ── Async HTTP client with DB + Redis dependency overrides ───────────────────
@pytest_asyncio.fixture
async def client(
    db_session: AsyncSession,
    fake_redis: FakeRedis,
) -> AsyncGenerator[AsyncClient, None]:
    """AsyncClient with FastAPI DB and Redis dependencies replaced by test fakes."""

    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    async def _override_get_redis() -> AsyncGenerator[FakeRedis, None]:
        yield fake_redis

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_redis_dep] = _override_get_redis
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
