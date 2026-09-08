from datetime import UTC, datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from django.urls import reverse
from pydantic import HttpUrl
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.offer_criteria import OfferCriteria, OfferLanguage
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from application.ingestion.interfaces.get_offers_by_source_input import (
    GetOffersBySourceInput,
)
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from infrastructure.factories.referentiel.offer_factory import OfferFactory

SOURCE_ID = UUID("12345678-1234-4234-b234-123456789abc")

URL = reverse("ingestion:offers_by_source", kwargs={"source_id": SOURCE_ID})

NOMBRE_REQUETES_ATTENDU = (
    1  # view JWT authentication
    + 1  # usecase: utilisateur_repository.get_by_username
    + 2  # usecase: get_allowed_source_ids (get user + filter sources M2M)
    + 2  # pagination: count + page
    + 1  # ApiRequestLoggerMiddleware re-decodes the JWT to log the request
    + 2  # logging: DJ tries an UPDATE (manually-assigned pk) then falls back to INSERT
)


@pytest.fixture
def use_case():
    return MagicMock()


@pytest.fixture(autouse=True)
def mock_container(mock_offers_container, use_case):
    mock_offers_container.get_offers_by_source_usecase.return_value = use_case


@pytest.fixture
def source():
    return SourceDjangoFactory(source_id=SOURCE_ID)


@pytest.fixture
def authenticated_client_with_source(api_client, test_user, source):
    test_user.sources.add(source)
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


def _make_paginated_mock(use_case, num_offers, offers_slice):
    mock_page = MagicMock()
    mock_page.count.return_value = num_offers
    mock_page.slice.return_value = iter(offers_slice)
    use_case.execute.return_value = mock_page
    return use_case


class TestOffersBySourceView:
    def test_unauthenticated_returns_401(self, api_client):
        response = api_client.get(URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_api_key_returns_401(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
        response = api_client.get(URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_api_key_authentication_returns_offers(self, api_key_client, use_case):
        offer = OfferFactory.create_entity(source_id=SOURCE_ID)
        _make_paginated_mock(use_case, num_offers=1, offers_slice=[offer])

        response = api_key_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
        use_case.execute.assert_called_once_with(
            GetOffersBySourceInput(source_id=SOURCE_ID, utilisateur_username=None)
        )

    def test_post_not_allowed(self, authenticated_client):
        response = authenticated_client.post(URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_jwt_authentication_returns_offers(
        self, authenticated_client_with_source, test_user, use_case
    ):
        offer = OfferFactory.create_entity(source_id=SOURCE_ID)
        _make_paginated_mock(use_case, num_offers=1, offers_slice=[offer])

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["external_id"] == offer.external_id
        assert data["results"][0]["source_id"] == str(SOURCE_ID)

        use_case.execute.assert_called_once_with(
            GetOffersBySourceInput(
                source_id=SOURCE_ID,
                utilisateur_username=test_user.username,
            )
        )

    def test_jwt_authentication_returns_offer_without_localisation(
        self, authenticated_client_with_source, use_case
    ):
        offer = OfferFactory.create_entity(source_id=SOURCE_ID)
        offer.localisation = None
        _make_paginated_mock(use_case, num_offers=1, offers_slice=[offer])

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["results"][0]["localisation"] is None

    def test_jwt_authentication_forbidden_source_returns_401(
        self, authenticated_client, use_case
    ):
        use_case.execute.side_effect = SourceAuthorizationError({SOURCE_ID})
        response = authenticated_client.get(URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_error_500(self, authenticated_client, use_case):
        use_case.execute.side_effect = Exception("db error")

        response = authenticated_client.get(URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


class TestOffersBySourceViewDbVerified:
    @pytest.fixture(autouse=True)
    def mock_container(self):
        return None

    def test_response_matches_db_record_field_by_field(
        self, authenticated_client_with_source, source
    ):
        offer = OfferDjangoFactory(
            source=source,
            offer_url=None,
            contract_type=None,
            area=None,
            country=None,
            region=None,
            department=None,
            beginning_date=None,
        )

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"] == [
            {
                "external_id": offer.external_id,
                "reference": offer.reference,
                "source_id": str(SOURCE_ID),
                "title": offer.title,
                "long_title": None,
                "organization": offer.organization,
                "employer": None,
                "profile": offer.profile,
                "mission": offer.mission,
                "complements": None,
                "verse": offer.verse,
                "category": offer.category,
                "contract_type": None,
                "contract_kind": None,
                "job_vacancy": None,
                "offer_url": None,
                "application_url": None,
                "localisation": None,
                "criteria": None,
                "conditions": None,
                "contacts": None,
                "publication_date": "2024-01-15T00:00:00Z",
                "beginning_date": None,
                "archived_at": None,
            }
        ]

    def test_response_matches_db_record_field_by_field_with_non_null_data(
        self, authenticated_client_with_source, source
    ):
        criteria = OfferCriteria(
            diploma_level=Diploma(5),
            diploma="Master",
            experience_level=ExperienceLevel.CONFIRME,
            specialisations=["informatique"],
            languages=[OfferLanguage(iso_code="en", level=LanguageLevel.B2)],
        )
        offer = OfferDjangoFactory(
            source=source,
            long_title="Développeur Backend Senior",
            employer="Ministère Test",
            complements="Poste à pourvoir immédiatement",
            contract_type=ContractType.TERRITORIAL.value,
            contract_kind=[ContractKind.CDI.name, ContractKind.CDD.name],
            job_vacancy="1",
            offer_url=HttpUrl("https://exemple.gouv.fr/offres/e2e-1"),
            application_url=HttpUrl("https://exemple.gouv.fr/candidature/e2e-1"),
            location_label="Paris",
            latitude=48.8566,
            longitude=2.3522,
            criteria=criteria.to_dict(),
            conditions={"salaire": "35000-45000"},
            contacts=[{"nom": "Jean Dupont", "email": "jean.dupont@example.gouv.fr"}],
            beginning_date=datetime(2024, 6, 1, tzinfo=UTC),
        )

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"] == [
            {
                "external_id": offer.external_id,
                "reference": offer.reference,
                "source_id": str(SOURCE_ID),
                "title": offer.title,
                "long_title": offer.long_title,
                "organization": offer.organization,
                "employer": offer.employer,
                "profile": offer.profile,
                "mission": offer.mission,
                "complements": offer.complements,
                "verse": offer.verse,
                "category": offer.category,
                "contract_type": offer.contract_type,
                "contract_kind": [ContractKind.CDI.value, ContractKind.CDD.value],
                "job_vacancy": offer.job_vacancy,
                "offer_url": "https://exemple.gouv.fr/offres/e2e-1",
                "application_url": "https://exemple.gouv.fr/candidature/e2e-1",
                "localisation": {
                    "zone_geographique": offer.area,
                    "pays": offer.country,
                    "region": offer.region,
                    "departement": offer.department,
                    "localisation_label": offer.location_label,
                    "latitude": offer.latitude,
                    "longitude": offer.longitude,
                },
                "criteria": criteria.to_dict(),
                "conditions": {"salaire": "35000-45000"},
                "contacts": [
                    {"nom": "Jean Dupont", "email": "jean.dupont@example.gouv.fr"}
                ],
                "publication_date": "2024-01-15T00:00:00Z",
                "beginning_date": "2024-06-01T00:00:00Z",
                "archived_at": None,
            }
        ]

    def test_does_not_trigger_n_plus_one_queries(
        self, authenticated_client_with_source, source, django_assert_num_queries
    ):
        OfferDjangoFactory.create_batch(5, source=source)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
