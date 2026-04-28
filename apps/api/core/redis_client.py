"""Redis async client singleton."""

from collections.abc import AsyncGenerator

import redis.asyncio as redis

from core.config import settings

_redis: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    """Return the global async Redis client, creating it on first call.

    Returns:
        A connected ``redis.asyncio.Redis`` instance with ``decode_responses=True``.
    """
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def close_redis() -> None:
    """Close and reset the global Redis client.

    Safe to call even if the client has not been initialised yet.
    """
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None


async def get_redis_dep() -> AsyncGenerator[redis.Redis, None]:
    """FastAPI dependency that yields the shared Redis client.

    Yields:
        A connected ``redis.asyncio.Redis`` instance.
    """
    r = await get_redis()
    yield r
