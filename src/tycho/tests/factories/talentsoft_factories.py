from typing import List, Optional

from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory

from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftCodedObject,
    TalentsoftCustomFields,
    TalentsoftDetailOffer,
    TalentsoftGeolocation,
    TalentsoftLink,
    TalentsoftOffer,
    TalentsoftOffersResponse,
    TalentsoftOrganisation,
    TalentsoftPagination,
)

_fake = Faker("fr_FR")


class TalentsoftCodedObjectFactory(ModelFactory[TalentsoftCodedObject]):
    __model__ = TalentsoftCodedObject
    __faker__ = _fake

    parentType = ""
    hasChildren = False


class TalentsoftLinkFactory(ModelFactory[TalentsoftLink]):
    __model__ = TalentsoftLink

    @classmethod
    def href(cls) -> str:
        ref = _fake.numerify("####-#######")
        return f"https://fake-ats.com/api/v2/offers/getoffer?reference={ref}"

    @classmethod
    def rel(cls) -> str:
        return "detail"


class TalentsoftOfferFactory(ModelFactory[TalentsoftOffer]):
    __model__ = TalentsoftOffer
    __faker__ = _fake

    salaryRange = None
    professionalCategory = None
    location = None
    urlRedirectionEmployee = None

    @classmethod
    def reference(cls) -> str:
        return _fake.numerify("20##-#######")

    @classmethod
    def title(cls) -> str:
        return _fake.job().upper()

    @classmethod
    def organisationName(cls) -> str:
        return _fake.company()

    @classmethod
    def organisationDescription(cls) -> str:
        return _fake.company()

    @classmethod
    def organisationLogoUrl(cls) -> str:
        entity_id = _fake.numerify("####")
        return f"https://fake-ats.com/Handlers/Image.ashx?imagetype=logo&entityid={entity_id}"

    @classmethod
    def modificationDate(cls) -> str:
        return _fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

    @classmethod
    def startPublicationDate(cls) -> str:
        return _fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    @classmethod
    def beginningDate(cls) -> Optional[str]:
        return _fake.future_date().strftime("%Y-%m-%dT00:00:00Z")

    @classmethod
    def offerUrl(cls) -> str:
        ref = _fake.numerify("20##-#######")
        return f"https://fake-csp.fr/offre-emploi/{ref}/?tracking=1&idOrigine=502"

    @classmethod
    def geographicalLocation(cls) -> List[TalentsoftCodedObject]:
        return TalentsoftCodedObjectFactory.batch(size=1)

    @classmethod
    def country(cls) -> List[TalentsoftCodedObject]:
        return [
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ]

    @classmethod
    def region(cls) -> List[TalentsoftCodedObject]:
        # R24 -> "24" (Centre-Val de Loire) after cleaner transformation
        return [
            TalentsoftCodedObjectFactory.build(clientCode="R24", type="offerRegion")
        ]

    @classmethod
    def department(cls) -> List[TalentsoftCodedObject]:
        # "41" -> Loir-et-Cher, valid INSEE department code
        return [
            TalentsoftCodedObjectFactory.build(clientCode="41", type="offerDepartment")
        ]

    @classmethod
    def _links(cls) -> List[TalentsoftLink]:
        return TalentsoftLinkFactory.batch(size=1)


class TalentsoftGeolocationFactory(ModelFactory[TalentsoftGeolocation]):
    __model__ = TalentsoftGeolocation
    __faker__ = _fake

    @classmethod
    def latitude(cls) -> float:
        return float(_fake.latitude())

    @classmethod
    def longitude(cls) -> float:
        return float(_fake.longitude())


class TalentsoftOrganisationFactory(ModelFactory[TalentsoftOrganisation]):
    __model__ = TalentsoftOrganisation
    __faker__ = _fake

    @classmethod
    def entityCode(cls) -> str:
        return _fake.numerify("###")

    @classmethod
    def name(cls) -> str:
        return _fake.company()

    @classmethod
    def logoUrl(cls) -> Optional[str]:
        entity_id = _fake.numerify("###")
        return f"https://fake-ats.com/Handlers/Image.ashx?imagetype=logo&entityid={entity_id}"


class TalentsoftCustomFieldsFactory(ModelFactory[TalentsoftCustomFields]):
    __model__ = TalentsoftCustomFields
    __faker__ = _fake


class TalentsoftDetailOfferFactory(ModelFactory[TalentsoftDetailOffer]):
    __model__ = TalentsoftDetailOffer
    __faker__ = _fake

    salaryRange = None
    professionalCategory = None
    location = None
    urlRedirectionEmployee = None
    urlRedirectionApplicant = None
    diploma = None
    operationalManager = None

    @classmethod
    def reference(cls) -> str:
        return _fake.numerify("20##-#######")

    @classmethod
    def title(cls) -> str:
        return _fake.job().upper()

    @classmethod
    def organisationName(cls) -> str:
        return _fake.company()

    @classmethod
    def organisationDescription(cls) -> str:
        return _fake.company()

    @classmethod
    def organisationLogoUrl(cls) -> str:
        entity_id = _fake.numerify("####")
        return f"https://fake-ats.com/Handlers/Image.ashx?imagetype=logo&entityid={entity_id}"

    @classmethod
    def modificationDate(cls) -> str:
        return _fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

    @classmethod
    def startPublicationDate(cls) -> str:
        return _fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    @classmethod
    def endPublicationDate(cls) -> Optional[str]:
        return _fake.future_date().strftime("%Y-%m-%dT%H:%M:%S")

    @classmethod
    def beginningDate(cls) -> Optional[str]:
        return _fake.future_date().strftime("%Y-%m-%dT00:00:00")

    @classmethod
    def offerUrl(cls) -> str:
        ref = _fake.numerify("20##-#######")
        return f"https://fake-csp.fr/offre-emploi/{ref}/?tracking=1&idOrigine=502"

    @classmethod
    def applicationUrl(cls) -> Optional[str]:
        return f"https://fake-ats.com/offre/{_fake.numerify('######')}.aspx"

    @classmethod
    def geographicalLocation(cls) -> List[TalentsoftCodedObject]:
        return TalentsoftCodedObjectFactory.batch(size=1)

    @classmethod
    def country(cls) -> List[TalentsoftCodedObject]:
        return [
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ]

    @classmethod
    def region(cls) -> List[TalentsoftCodedObject]:
        return [
            TalentsoftCodedObjectFactory.build(clientCode="R24", type="offerRegion")
        ]

    @classmethod
    def department(cls) -> List[TalentsoftCodedObject]:
        return [
            TalentsoftCodedObjectFactory.build(clientCode="41", type="offerDepartment")
        ]

    @classmethod
    def _links(cls) -> List[TalentsoftLink]:
        return TalentsoftLinkFactory.batch(size=1)

    @classmethod
    def organisation(cls) -> TalentsoftOrganisation:
        return TalentsoftOrganisationFactory.build()

    @classmethod
    def geolocation(cls) -> TalentsoftGeolocation:
        return TalentsoftGeolocationFactory.build()

    @classmethod
    def customFields(cls) -> TalentsoftCustomFields:
        return TalentsoftCustomFieldsFactory.build()

    @classmethod
    def languages(cls) -> list:
        return []

    @classmethod
    def specialisations(cls) -> list:
        return []

    @classmethod
    def applicationQuestions(cls) -> list:
        return []

    @classmethod
    def attachedFilesUrls(cls) -> list:
        return []


class TalentsoftPaginationFactory(ModelFactory[TalentsoftPagination]):
    __model__ = TalentsoftPagination

    hasMore = False
    start = 1
    lastPage = 1


class TalentsoftOffersResponseFactory(ModelFactory[TalentsoftOffersResponse]):
    __model__ = TalentsoftOffersResponse

    @classmethod
    def data(cls) -> List[TalentsoftOffer]:
        return TalentsoftOfferFactory.batch(size=2)

    @classmethod
    def pagination(cls) -> TalentsoftPagination:
        return TalentsoftPaginationFactory.build()
