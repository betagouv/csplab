from datetime import UTC, datetime
from unittest.mock import MagicMock

from django.urls import reverse
from pydantic import HttpUrl
from referentiel.exceptions.offer_errors import OfferDoesNotExist
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.offer_criteria import OfferCriteria, OfferLanguage
from referentiel.value_objects.region import Region
from rest_framework import status

from application.ingestion.interfaces.get_offer_by_reference_input import (
    GetOfferByReferenceInput,
)
from infrastructure.factories.referentiel.offer_factory import OfferFactory
from presentation.ingestion.serializers import (
    FakeTsCodedObjectSerializer,
    FakeTsOfferDetailSerializer,
    FakeTsOrganisationSerializer,
)
from tests.utils.openapi_test_utils import assert_matches_openapi_schema

URL = reverse("ingestion_fake_ts:offer_detail")


def _make_usecase(mock_container, offer=None, exception=None):
    mock_usecase = MagicMock()
    if exception:
        mock_usecase.execute.side_effect = exception
    else:
        mock_usecase.execute.return_value = offer
    mock_container.get_offer_by_reference_usecase.return_value = mock_usecase
    return mock_usecase


def test_unauthenticated_access(api_client):
    response = api_client.get(URL, {"reference": "REF-1"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_valid_api_key_no_longer_grants_access(api_key_client):
    response = api_key_client.get(URL, {"reference": "REF-1"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_allowed(authenticated_client):
    response = authenticated_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_missing_reference_returns_400(
    mock_offer_detail_container, authenticated_client
):
    _make_usecase(mock_offer_detail_container)

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_unknown_reference_returns_404(
    mock_offer_detail_container, authenticated_client
):
    _make_usecase(mock_offer_detail_container, exception=OfferDoesNotExist("REF-1"))

    response = authenticated_client.get(URL, {"reference": "REF-1"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_reference_is_forwarded_to_usecase(
    mock_offer_detail_container, authenticated_client
):
    offer = OfferFactory.create_entity(reference="REF-1")
    mock_usecase = _make_usecase(mock_offer_detail_container, offer=offer)

    authenticated_client.get(URL, {"reference": "REF-1"})

    mock_usecase.execute.assert_called_once_with(
        GetOfferByReferenceInput(reference="REF-1")
    )


def test_returns_offer_detail(mock_offer_detail_container, authenticated_client):
    offer = OfferFactory.create_entity()
    _make_usecase(mock_offer_detail_container, offer=offer)

    response = authenticated_client.get(URL, {"reference": offer.reference})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["reference"] == offer.reference
    assert data["title"] == offer.title
    assert data["organisation"]["name"] == offer.organization
    assert data["isAnonymousOrganisation"] is False


def test_response_matches_openapi_schema(
    mock_offer_detail_container, authenticated_client
):
    offer = OfferFactory.create_entity()
    _make_usecase(mock_offer_detail_container, offer=offer)

    response = authenticated_client.get(URL, {"reference": offer.reference})

    assert_matches_openapi_schema(
        response.json(), "/api/fake-ts/offers/getoffer", method="get"
    )


def test_response_has_no_undeclared_fields(
    mock_offer_detail_container, authenticated_client
):
    offer = OfferFactory.create_entity()
    _make_usecase(mock_offer_detail_container, offer=offer)

    response = authenticated_client.get(URL, {"reference": offer.reference})
    data = response.json()

    assert set(data.keys()) == set(FakeTsOfferDetailSerializer().fields.keys())
    assert set(data["organisation"].keys()) == set(
        FakeTsOrganisationSerializer().fields.keys()
    )
    assert set(data["offerFamilyCategory"].keys()) == set(
        FakeTsCodedObjectSerializer().fields.keys()
    )


def test_response_matches_db_record_field_by_field(authenticated_client):
    localisation = Localisation(
        area=GeographicalArea.EUROPE,
        country=Country("FRA"),
        region=Region(code="11"),
        department=Department(code="75"),
        label="Paris",
        latitude=48.8566,
        longitude=2.3522,
    )
    criteria = OfferCriteria(
        diploma_level=Diploma(5),
        diploma="Master",
        experience_level=ExperienceLevel.CONFIRME,
        specialisations=["informatique"],
        languages=[OfferLanguage(iso_code="en", level=LanguageLevel.B2)],
    )
    offer_model = OfferFactory.create_model(
        reference="REF-E2E-1",
        title="Développeur Backend",
        profile="Profil recherché",
        mission="Mission du poste",
        organization="Ministère Test",
        category=Category.A,
        contract_type=ContractType.TERRITORIAL,
        offer_url=HttpUrl("https://exemple.gouv.fr/offres/e2e-1"),
        localisation=localisation,
        publication_date=datetime(2024, 3, 1, 9, 0, tzinfo=UTC),
        beginning_date=LimitDate(datetime(2024, 6, 1, tzinfo=UTC)),
        criteria=criteria,
    )

    response = authenticated_client.get(URL, {"reference": offer_model.reference})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "reference": "REF-E2E-1",
        "isTopOffer": False,
        "title": "Développeur Backend",
        "location": "Paris",
        "modificationDate": "2024-03-01T09:00:00",
        "contractType": {
            "code": None,
            "clientCode": "TERRITORIAL",
            "label": "TERRITORIAL",
            "active": True,
            "parentCode": None,
            "type": "contractType",
            "parentType": "",
            "hasChildren": False,
        },
        "offerFamilyCategory": {
            "code": None,
            "clientCode": "A",
            "label": "A",
            "active": True,
            "parentCode": None,
            "type": "offerFamilyCategory",
            "parentType": "",
            "hasChildren": False,
        },
        "organisationName": "Ministère Test",
        "organisationDescription": None,
        "organisationLogoUrl": None,
        "contractDuration": None,
        "contractTypeCountry": None,
        "description1": "Mission du poste",
        "description2": "Profil recherché",
        "description1Formatted": None,
        "description2Formatted": None,
        "salaryRange": None,
        "geographicalLocation": [],
        "country": [
            {
                "code": None,
                "clientCode": "FRA",
                "label": "France",
                "active": True,
                "parentCode": None,
                "type": "country",
                "parentType": "",
                "hasChildren": False,
            }
        ],
        "region": [
            {
                "code": None,
                "clientCode": "11",
                "label": "Île-de-France",
                "active": True,
                "parentCode": None,
                "type": "region",
                "parentType": "",
                "hasChildren": False,
            }
        ],
        "department": [
            {
                "code": None,
                "clientCode": "75",
                "label": "Paris",
                "active": True,
                "parentCode": None,
                "type": "department",
                "parentType": "",
                "hasChildren": False,
            }
        ],
        "latitude": 48.8566,
        "longitude": 2.3522,
        "professionalCategory": None,
        "_links": [],
        "offerUrl": "https://exemple.gouv.fr/offres/e2e-1",
        "_format": None,
        "_metadata": None,
        "urlRedirectionEmployee": None,
        "urlRedirectionApplicant": None,
        "startPublicationDate": "2024-03-01T09:00:00",
        "beginningDate": "2024-06-01T00:00:00",
        "locations": [],
        "applicationUrl": None,
        "endPublicationDate": None,
        "isAnonymousOrganisation": False,
        "organisation": {
            "entityCode": "",
            "name": "Ministère Test",
            "description": None,
            "url": "https://exemple.gouv.fr/offres/e2e-1",
            "phoneNumber": None,
            "postCode": None,
            "geolocation": {"latitude": 48.8566, "longitude": 2.3522},
            "parentName": None,
            "logoUrl": None,
            "maxDelayForConsent": None,
            "retentionPeriod": None,
            "generalConditions": None,
            "personalDataConsent": None,
        },
        "operationalManager": None,
        "educationLevel": {
            "code": None,
            "clientCode": "5",
            "label": "5",
            "active": True,
            "parentCode": None,
            "type": "educationLevel",
            "parentType": "",
            "hasChildren": False,
        },
        "diploma": {
            "code": None,
            "clientCode": "Master",
            "label": "Master",
            "active": True,
            "parentCode": None,
            "type": "diploma",
            "parentType": "",
            "hasChildren": False,
        },
        "experienceLevel": {
            "code": None,
            "clientCode": "CONFIRME",
            "label": "Confirmé",
            "active": True,
            "parentCode": None,
            "type": "experienceLevel",
            "parentType": "",
            "hasChildren": False,
        },
        "languages": [
            {
                "languageName": {
                    "code": None,
                    "clientCode": "en",
                    "label": "en",
                    "active": True,
                    "parentCode": None,
                    "type": "language",
                    "parentType": "",
                    "hasChildren": False,
                },
                "languageLevel": {
                    "code": None,
                    "clientCode": "B2",
                    "label": "B2",
                    "active": True,
                    "parentCode": None,
                    "type": "languageLevel",
                    "parentType": "",
                    "hasChildren": False,
                },
            }
        ],
        "specialisations": [
            {
                "code": None,
                "clientCode": "informatique",
                "label": "informatique",
                "active": True,
                "parentCode": None,
                "type": "specialisation",
                "parentType": "",
                "hasChildren": False,
            }
        ],
        "applicationQuestions": [],
        "attachedFilesUrls": [],
        "geolocation": {"latitude": 48.8566, "longitude": 2.3522},
        "customFields": None,
    }


def test_returns_error_500(mock_offer_detail_container, authenticated_client):
    _make_usecase(mock_offer_detail_container, exception=Exception("db error"))

    response = authenticated_client.get(URL, {"reference": "REF-1"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
