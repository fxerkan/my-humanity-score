"""Admin dashboard endpoints — stub, implemented in TASK-027."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def get_stats() -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.get("/users")
async def list_users() -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.patch("/users/{user_id}/suspend")
async def suspend_user(user_id: str) -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})
