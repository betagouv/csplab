from time import time
from typing import List, Optional

from pydantic import BaseModel, Field


class TalentsoftTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None


class CachedToken(BaseModel):
    access_token: str
    token_type: str
    expires_at_epoch: float
    refresh_token: Optional[str] = None

    def is_valid(self) -> bool:
        leeway_seconds = 30
        return (self.expires_at_epoch - leeway_seconds) > time()


class TalentsoftCodedObject(BaseModel):
    code: int
    clientCode: str
    label: str
    active: bool
    parentCode: Optional[int] = None
    type: str
    parentType: str = ""
    hasChildren: bool = False


class TalentsoftLink(BaseModel):
    href: str
    rel: str


class TalentsoftOffer(BaseModel):
    # Mandatory fields
    reference: str
    isTopOffer: bool
    title: str
    organisationName: str
    organisationDescription: str
    organisationLogoUrl: str
    modificationDate: str
    startPublicationDate: str
    offerUrl: str

    # Mandatory coded objects
    offerFamilyCategory: TalentsoftCodedObject
    contractTypeCountry: TalentsoftCodedObject

    # Mandatory arrays (can be empty)
    geographicalLocation: List[TalentsoftCodedObject] = []
    country: List[TalentsoftCodedObject] = []
    region: List[TalentsoftCodedObject] = []
    department: List[TalentsoftCodedObject] = []
    _links: List[TalentsoftLink] = []

    # Optional text fields
    location: Optional[str] = None
    description1: Optional[str] = None
    description2: Optional[str] = None
    description1Formatted: Optional[str] = None
    description2Formatted: Optional[str] = None
    beginningDate: Optional[str] = None
    contractDuration: Optional[str] = None

    # Optional coded objects
    contractType: Optional[TalentsoftCodedObject] = None
    salaryRange: Optional[TalentsoftCodedObject] = None
    professionalCategory: Optional[TalentsoftCodedObject] = None

    # Optional coordinates
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Optional redirect URLs
    urlRedirectionEmployee: Optional[str] = None
    urlRedirectionApplicant: Optional[str] = None


class TalentsoftPagination(BaseModel):
    start: int
    count: int
    total: int
    resultsPerPage: int
    hasMore: bool
    lastPage: int


class TalentsoftOffersResponse(BaseModel):
    data: List[TalentsoftOffer]
    pagination: TalentsoftPagination = Field(alias="_pagination")
