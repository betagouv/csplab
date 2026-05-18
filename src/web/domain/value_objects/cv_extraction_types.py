from typing import List, Optional

from pydantic import BaseModel


class CVExperience(BaseModel):
    title: str
    company: Optional[str]
    sector: Optional[str]
    description: Optional[str]


class CVExtractionResult(BaseModel):
    experiences: List[CVExperience]
    skills: List[str]
