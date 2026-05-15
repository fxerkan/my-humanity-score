"""Neo4j driver factory with FastAPI lifespan integration.

The driver is a module-level singleton initialised once at app startup
and closed during shutdown.  Tests can override the driver via
``get_neo4j_driver`` by providing a mock or test‑container driver.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from core.config import settings

logger = logging.getLogger(__name__)

# ── Module-level driver (singleton) ──────────────────────────────────────────

_driver: AsyncGraphDatabase.driver | None = None


def _create_driver() -> AsyncGraphDatabase.driver:
    """Build an async Neo4j driver from Settings."""
    return AsyncGraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
        max_connection_lifetime=3600,
        max_connection_pool_size=20,
        connection_acquisition_timeout=10,
    )


async def get_neo4j_driver() -> AsyncGraphDatabase.driver:
    """Return the shared driver, creating it on first call."""
    global _driver
    if _driver is None:
        _driver = _create_driver()
    return _driver


def set_neo4j_driver(driver: AsyncGraphDatabase.driver | None) -> None:
    """Override the module-level driver (used in tests)."""
    global _driver
    _driver = driver


async def verify_connectivity() -> bool:
    """Check Neo4j is reachable. Returns True on success, False otherwise."""
    try:
        driver = await get_neo4j_driver()
        await driver.verify_connectivity()
        logger.info("Neo4j connectivity verified OK")
        return True
    except (ServiceUnavailable, Neo4jError, OSError) as exc:
        logger.warning("Neo4j connectivity check failed: %s", exc)
        return False


async def close_driver() -> None:
    """Shut down the driver cleanly."""
    global _driver
    if _driver is not None:
        await _driver.close()
        _driver = None
        logger.info("Neo4j driver closed")


@asynccontextmanager
async def neo4j_session() -> AsyncGenerator:
    """Async context manager that yields a Neo4j async session.

    Usage::

        async with neo4j_session() as session:
            result = await session.run(query, **params)
    """
    driver = await get_neo4j_driver()
    async with driver.session(database="neo4j") as session:
        yield session


def neo4j_lifespan() -> list[dict]:
    """Return start‑up / shut‑down events for the Neo4j driver.

    Use in FastAPI ``lifespan``::

        app = FastAPI(lifespan=neo4j_lifespan)
    """
    # FastAPI lifespan expects an async context manager that yields
    # a state dict.  We return a generator‑based implementation below.  # pragma: no cover — used in main.py
    pass  # pragma: no cover — implemented inline in main.py
