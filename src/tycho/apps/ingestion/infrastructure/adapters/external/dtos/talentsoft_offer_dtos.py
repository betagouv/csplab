"""Pydantic models for TalentSoft API responses."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class TalentSoftOfferDocument(BaseModel):
    """TalentSoft offer document structure."""

    model_config = ConfigDict(extra="ignore")

    id: str
    verse: str
    title: str
    profile: str
    category: str
    region: Optional[str] = None
    department: Optional[str] = None
    limit_date: Optional[str] = None
