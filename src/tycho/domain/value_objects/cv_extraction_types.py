"""Types for CV extraction results."""

from typing import List, Optional, TypedDict


class CVExperience(TypedDict):
    """Structure for a CV experience entry."""

    title: str
    company: str
    sector: Optional[str]
    description: str


class CVExtractionResult(TypedDict):
    """Structure for complete CV extraction result."""

    experiences: List[CVExperience]
    skills: List[str]
