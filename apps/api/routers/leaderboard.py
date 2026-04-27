"""Leaderboard endpoints — stub, implemented in TASK-009."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/")
async def get_leaderboard() -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.get("/regional")
async def get_regional_leaderboard() -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.get("/category/{category}")
async def get_category_leaderboard(category: str) -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})
