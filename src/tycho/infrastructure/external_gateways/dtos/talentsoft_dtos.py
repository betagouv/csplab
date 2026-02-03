"""Pydantic models for FO Talentsoft API endpoints."""

from time import time
from typing import List, Optional

from pydantic import BaseModel, Field


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


class TalentsoftCodedObject(BaseModel):
    """Base class for all TalentSoft coded objects."""

    code: int
    clientCode: str
    label: str
    active: bool
    parentCode: Optional[int] = None
    type: str
    parentType: str = ""
    hasChildren: bool = False


class TalentsoftLink(BaseModel):
    """TalentSoft _links object."""

    href: str
    rel: str


class TalentsoftOffer(BaseModel):
    """Complete TalentSoft offer DTO with strict validation."""

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
    """Pagination information from Talentsoft API."""

    start: int
    count: int
    total: int
    resultsPerPage: int
    hasMore: bool
    lastPage: int


class TalentsoftOffersResponse(BaseModel):
    """TalentSoft offers API response with typed data."""

    data: List[TalentsoftOffer]
    pagination: TalentsoftPagination = Field(alias="_pagination")
