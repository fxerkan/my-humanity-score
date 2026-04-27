"""Shared pagination and error schemas."""

from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list


class ErrorResponse(BaseModel):
    error: str
    code: str
    detail: str | None = None
