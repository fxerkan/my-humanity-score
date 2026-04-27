"""Groups endpoints — stub, implemented in TASK-023."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/")
async def list_groups() -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.post("/")
async def create_group() -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.get("/{group_id}")
async def get_group(group_id: str) -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.post("/{group_id}/join")
async def join_group(group_id: str) -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})


@router.delete("/{group_id}/leave")
async def leave_group(group_id: str) -> JSONResponse:
    return JSONResponse(status_code=501, content={"message": "not implemented"})
