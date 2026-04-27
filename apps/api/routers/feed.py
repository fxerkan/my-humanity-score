"""Feed / social timeline endpoints — stub, implemented in TASK-022."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("/")
async def get_feed() -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.get("/global")
async def get_global_feed() -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})
