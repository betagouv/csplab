"""Types for CV extraction results."""

from typing import List, Optional

from pydantic import BaseModel


class CVExperience(BaseModel):
    """Structure for a CV experience entry."""

    title: str
    company: str
    sector: Optional[str]
    description: str


class CVExtractionResult(BaseModel):
    """Structure for complete CV extraction result."""

    experiences: List[CVExperience]
    skills: List[str]
