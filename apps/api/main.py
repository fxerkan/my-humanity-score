"""MHS API — FastAPI entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from core.config import settings
from core.exceptions import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    conflict_handler,
    forbidden_handler,
    not_found_handler,
    unauthorized_handler,
)
from routers import activities, admin, auth, feed, groups, leaderboard, scores, users

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="My Humanity Score API",
    description="Backend for the My Humanity Score / MHS platform.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(NotFoundError, not_found_handler)  # type: ignore[arg-type]
app.add_exception_handler(UnauthorizedError, unauthorized_handler)  # type: ignore[arg-type]
app.add_exception_handler(ForbiddenError, forbidden_handler)  # type: ignore[arg-type]
app.add_exception_handler(ConflictError, conflict_handler)  # type: ignore[arg-type]

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(scores.router)
app.include_router(activities.router)
app.include_router(leaderboard.router)
app.include_router(feed.router)
app.include_router(groups.router)
app.include_router(admin.router)


@app.get("/health", tags=["infra"])
async def health() -> dict[str, str]:
    """Health check endpoint used by Docker and CI."""
    return {"status": "ok", "version": "1.0.0"}
