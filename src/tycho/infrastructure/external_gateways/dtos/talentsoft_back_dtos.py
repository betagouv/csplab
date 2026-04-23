from typing import List, Optional

from pydantic import BaseModel, Field


class TalentsoftBackCodedObject(BaseModel):
    id: Optional[str] = None
    label: Optional[str] = None


class TalentsoftBackOrganisation(BaseModel):
    id: str
    label: str


class TalentsoftBackVacancy(BaseModel):
    reference: str
    title: str
    languageId: int
    status: TalentsoftBackCodedObject
    jobTime: TalentsoftBackCodedObject
    salaryRange: TalentsoftBackCodedObject
    contractType: TalentsoftBackCodedObject
    contractLength: Optional[str] = None
    primaryProfile: TalentsoftBackCodedObject
    geographicalArea: TalentsoftBackCodedObject
    country: TalentsoftBackCodedObject
    region: TalentsoftBackCodedObject
    department: TalentsoftBackCodedObject
    address: Optional[str] = None
    diploma: TalentsoftBackCodedObject
    educationLevel: TalentsoftBackCodedObject
    experienceLevel: TalentsoftBackCodedObject
    organisation: TalentsoftBackOrganisation
    modificationDate: str
    creationDate: str
    vacancyUrl: str


class TalentsoftBackVacanciesResponse(BaseModel):
    code: int
    status: str
    data: List[TalentsoftBackVacancy]
    content_range: str = Field(alias="contentRange")
