"""FastAPI dependency injection: auth, DB session."""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.security import decode_token

bearer = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> uuid.UUID:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise ValueError("Wrong token type")
        return uuid.UUID(payload["sub"])
    except (ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


async def get_optional_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> uuid.UUID | None:
    if not credentials:
        return None
    try:
        payload = decode_token(credentials.credentials)
        return uuid.UUID(payload["sub"])
    except Exception:
        return None
