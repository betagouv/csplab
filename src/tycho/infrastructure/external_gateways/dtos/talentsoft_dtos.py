"""Pydantic models for FO Talentsoft API endpoints."""

from time import time
from typing import Optional

from pydantic import BaseModel, Field

from domain.types import JsonDataType


class TalentsoftTokenResponse(BaseModel):
    """Raw token response content."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None


class CachedToken(BaseModel):
    """Cached token with an absolute expiry timestamp."""

    access_token: str
    token_type: str
    expires_at_epoch: float
    refresh_token: Optional[str] = None

    def is_valid(self) -> bool:
        """True if token is valid (with leeway)."""
        leeway_seconds = 30
        return (self.expires_at_epoch - leeway_seconds) > time()


class TalentsoftPagination(BaseModel):
    """Pagination information from Talentsoft API."""

    start: int
    count: int
    total: int
    resultsPerPage: int
    hasMore: bool
    lastPage: int


class TalentsoftOffersResponse(BaseModel):
    """Offers response content."""

    data: JsonDataType
    pagination: TalentsoftPagination = Field(alias="_pagination")
