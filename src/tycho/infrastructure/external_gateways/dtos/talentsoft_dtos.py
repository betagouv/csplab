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


class TalentsoftGeolocation(BaseModel):
    latitude: float
    longitude: float


class TalentsoftOrganisation(BaseModel):
    entityCode: str
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    phoneNumber: Optional[str] = None
    postCode: Optional[str] = None
    geolocation: Optional[TalentsoftGeolocation] = None
    parentName: Optional[str] = None
    logoUrl: Optional[str] = None
    maxDelayForConsent: Optional[int] = None
    retentionPeriod: Optional[int] = None
    generalConditions: Optional[str] = None
    personalDataConsent: Optional[str] = None


class TalentsoftOperationalManager(BaseModel):
    language: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None


class TalentsoftLanguage(BaseModel):
    languageName: TalentsoftCodedObject
    languageLevel: TalentsoftCodedObject


class TalentsoftCustomCodeTable(BaseModel):
    code: int
    clientCode: str
    label: str
    active: bool
    parentCode: Optional[int] = None
    type: Optional[str] = None
    parentType: Optional[str] = None
    hasChildren: bool = False


class TalentsoftOfferCustomFields(BaseModel):
    date1: Optional[str] = None
    longText1: Optional[str] = None
    longText2: Optional[str] = None
    longText1Formatted: Optional[str] = None
    longText2Formatted: Optional[str] = None
    customCodeTable2: Optional[TalentsoftCustomCodeTable] = None


class TalentsoftDescriptionCustomFields(BaseModel):
    shortText2: Optional[str] = None
    shortText3: Optional[str] = None
    longText1: Optional[str] = None
    longText2: Optional[str] = None
    longText3: Optional[str] = None
    longText1Formatted: Optional[str] = None
    longText2Formatted: Optional[str] = None
    longText3Formatted: Optional[str] = None
    customCodeTable1: Optional[TalentsoftCustomCodeTable] = None
    customCodeTable3: Optional[TalentsoftCustomCodeTable] = None


class TalentsoftLocationCustomFields(BaseModel):
    shortText1: Optional[str] = None


class TalentsoftApplicantCriteriaCustomFields(BaseModel):
    longText1: Optional[str] = None
    longText1Formatted: Optional[str] = None
    customCodeTable1: Optional[TalentsoftCustomCodeTable] = None


class TalentsoftOriginCustomFields(BaseModel):
    shortText1: Optional[str] = None
    shortText2: Optional[str] = None
    shortText3: Optional[str] = None


class TalentsoftOfferCustomBlock(BaseModel):
    longText1: Optional[str] = None
    longText2: Optional[str] = None
    longText3: Optional[str] = None
    longText1Formatted: Optional[str] = None
    longText2Formatted: Optional[str] = None
    longText3Formatted: Optional[str] = None
    customCodeTable1: Optional[TalentsoftCustomCodeTable] = None
    customCodeTable2: Optional[TalentsoftCustomCodeTable] = None
    customCodeTable3: Optional[TalentsoftCustomCodeTable] = None


class TalentsoftCustomFields(BaseModel):
    offer: Optional[TalentsoftOfferCustomFields] = None
    description: Optional[TalentsoftDescriptionCustomFields] = None
    location: Optional[TalentsoftLocationCustomFields] = None
    applicantCriteria: Optional[TalentsoftApplicantCriteriaCustomFields] = None
    origin: Optional[TalentsoftOriginCustomFields] = None
    offerCustomBlock1: Optional[TalentsoftOfferCustomBlock] = None


class TalentsoftDetailOffer(TalentsoftOffer):
    applicationUrl: Optional[str] = None
    endPublicationDate: Optional[str] = None
    isAnonymousOrganisation: bool = False
    beginningDate: Optional[str] = None

    organisation: Optional[TalentsoftOrganisation] = None
    operationalManager: Optional[TalentsoftOperationalManager] = None

    educationLevel: Optional[TalentsoftCodedObject] = None
    diploma: Optional[TalentsoftCodedObject] = None
    experienceLevel: Optional[TalentsoftCodedObject] = None
    languages: List[TalentsoftLanguage] = []
    specialisations: List[TalentsoftCodedObject] = []
    applicationQuestions: List[str] = []
    attachedFilesUrls: List[str] = []

    geolocation: Optional[TalentsoftGeolocation] = None

    customFields: Optional[TalentsoftCustomFields] = None
