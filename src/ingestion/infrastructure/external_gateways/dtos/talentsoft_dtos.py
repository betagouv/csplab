from __future__ import annotations

from datetime import datetime, timezone
from time import time
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


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


class TalentsoftLink(BaseModel):
    href: str
    rel: str


class TalentsoftCodedObject(BaseModel):
    code: int
    clientCode: str
    label: str
    active: bool
    parentCode: Optional[int] = None
    type: str
    parentType: str = ""
    hasChildren: bool = False
    links: List[TalentsoftLink] = Field(default=[], alias="_links")


class TalentsoftFormatFields(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    tooltip: Optional[str] = None


class TalentsoftMetadataField(BaseModel):
    fieldName: Optional[str] = None
    fieldLabel: Optional[str] = None
    fieldCustomTableCode: Optional[str] = None
    fieldOrder: Optional[int] = None
    path: Optional[str] = None


class TalentsoftMetadataBlock(BaseModel):
    blockIdentifier: Optional[str] = None
    blockLabel: Optional[str] = None
    blockOrder: Optional[int] = None
    customFields: List[TalentsoftMetadataField] = []


class TalentsoftMetadata(BaseModel):
    blocks: List[TalentsoftMetadataBlock] = []


class TalentsoftMultiLocationAddress(BaseModel):
    country: Optional[str] = None
    countryCode: Optional[str] = None
    countryCodeISO3: Optional[str] = None
    countrySecondarySubdivision: Optional[str] = None
    countrySubdivision: Optional[str] = None
    freeformAddress: Optional[str] = None
    municipality: Optional[str] = None


class TalentsoftMultiLocationPosition(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None


class TalentsoftMultiLocation(BaseModel):
    locationReferential: Optional[TalentsoftCodedObject] = None
    clientCode: Optional[str] = None
    displayedAddress: Optional[str] = None
    address: Optional[TalentsoftMultiLocationAddress] = None
    position: Optional[TalentsoftMultiLocationPosition] = None
    active: Optional[bool] = None


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
    links: List[TalentsoftLink] = Field(default=[], alias="_links")
    locations: List[TalentsoftMultiLocation] = []

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

    customFields: Optional[TalentsoftCustomFields] = None

    format: Optional[TalentsoftFormatFields] = Field(default=None, alias="_format")
    metadata: Optional[TalentsoftMetadata] = Field(default=None, alias="_metadata")

    @field_validator("modificationDate", mode="before")
    @classmethod
    def default_modification_date_to_now(cls, value: Optional[str]) -> str:
        if value is None:
            return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        return value


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


class TalentsoftOrganisationsReferentielResponse(BaseModel):
    data: List[TalentsoftCodedObject]
    pagination: Optional[TalentsoftPagination] = Field(
        default=None, alias="_pagination"
    )


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


class TalentsoftOrganisationPayload(TalentsoftOrganisation):
    code: int
    parentCode: Optional[int] = None
    hasChildren: bool = False

    @classmethod
    def from_referentiel_and_detail(
        cls,
        referentiel: TalentsoftCodedObject,
        detail: TalentsoftOrganisation,
    ) -> TalentsoftOrganisationPayload:
        return cls(
            code=referentiel.code,
            parentCode=referentiel.parentCode,
            hasChildren=referentiel.hasChildren,
            **detail.model_dump(),
        )


class TalentsoftOperationalManager(BaseModel):
    language: Optional[TalentsoftCodedObject] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None


class TalentsoftMainSupervisor(BaseModel):
    firstName: str
    lastName: str
    fullName: Optional[str] = None
    login: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None


class TalentsoftApplicationQuestion(BaseModel):
    question: Optional[TalentsoftCodedObject] = None
    answers: List[TalentsoftCodedObject] = []
    isRequired: bool = False


class TalentsoftFormMetadataField(BaseModel):
    name: Optional[str] = None
    controlType: Optional[str] = None
    dataType: Optional[str] = None
    label: Optional[str] = None
    isReadOnly: Optional[bool] = None
    isRequired: Optional[bool] = None
    isVisible: Optional[bool] = None
    order: Optional[int] = None
    referentialTypeName: Optional[str] = None
    isMultipleSelectionAllowed: Optional[bool] = None
    textValidationType: Optional[str] = None
    maxTextLength: Optional[int] = None
    textValidationRegularExpression: Optional[str] = None
    booleanTrueLabel: Optional[str] = None
    booleanFalseLabel: Optional[str] = None
    booleanNullLabel: Optional[str] = None


class TalentsoftFormMetadataBlock(BaseModel):
    blockIdentifier: Optional[str] = None
    blockLabel: Optional[str] = None
    blockOrder: Optional[int] = None
    fields: List[TalentsoftFormMetadataField] = []


class TalentsoftFileSettings(BaseModel):
    fileTypeId: Optional[int] = None
    label: Optional[str] = None
    maxRequired: Optional[int] = None
    minRequired: Optional[int] = None
    maxSizeInBytes: Optional[int] = None
    orderNumber: Optional[int] = None
    attachmentType: Optional[str] = None


class TalentsoftFormMetadata(BaseModel):
    blocks: List[TalentsoftFormMetadataBlock] = []
    attachmentSettings: List[TalentsoftFileSettings] = []


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
    links: List[TalentsoftLink] = Field(default=[], alias="_links")


class TalentsoftDynamicField(BaseModel):
    associatedObjectIdentifier: Optional[int] = None
    date1: Optional[str] = None
    date2: Optional[str] = None
    date3: Optional[str] = None
    shortText1: Optional[str] = None
    shortText2: Optional[str] = None
    shortText3: Optional[str] = None
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
    offer: Optional[TalentsoftDynamicField] = None
    description: Optional[TalentsoftDynamicField] = None
    location: Optional[TalentsoftDynamicField] = None
    applicantCriteria: Optional[TalentsoftDynamicField] = None
    origin: Optional[TalentsoftDynamicField] = None
    offerCustomBlock1: Optional[TalentsoftDynamicField] = None
    offerCustomBlock2: Optional[TalentsoftDynamicField] = None
    offerCustomBlock3: Optional[TalentsoftDynamicField] = None
    offerCustomBlock4: Optional[TalentsoftDynamicField] = None


class TalentsoftDetailOffer(TalentsoftOffer):
    applicationUrl: Optional[str] = None
    endPublicationDate: Optional[str] = None
    isAnonymousOrganisation: bool = False
    beginningDate: Optional[str] = None

    organisation: Optional[TalentsoftOrganisation] = None
    operationalManager: Optional[TalentsoftOperationalManager] = None
    mainSupervisor: Optional[TalentsoftMainSupervisor] = None
    usersInChargeOf: List[str] = []
    notificationCollection: List[str] = []
    applicationNotificationLevel: Optional[TalentsoftCodedObject] = None

    offerTime: Optional[TalentsoftCodedObject] = None
    numberOfVacancies: Optional[int] = None
    recruitingReason: Optional[TalentsoftCodedObject] = None

    educationLevel: Optional[TalentsoftCodedObject] = None
    diploma: Optional[TalentsoftCodedObject] = None
    experienceLevel: Optional[TalentsoftCodedObject] = None
    languages: List[TalentsoftLanguage] = []
    specialisations: List[TalentsoftCodedObject] = []
    profileCollection: List[TalentsoftCodedObject] = []
    skillCollection: List[TalentsoftCodedObject] = []
    freeCriteria1: Optional[str] = None
    freeCriteria2: Optional[str] = None
    freeCriteria1Formatted: Optional[str] = None
    freeCriteria2Formatted: Optional[str] = None
    applicationQuestions: List[TalentsoftApplicationQuestion] = []
    attachedFilesUrls: List[str] = []

    applicationFormMetadata: Optional[TalentsoftFormMetadata] = Field(
        default=None, alias="_applicationformmetadata"
    )

    geolocation: Optional[TalentsoftGeolocation] = None

    customFields: Optional[TalentsoftCustomFields] = None
