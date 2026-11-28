from datetime import UTC, datetime
from unittest.mock import patch
from uuid import UUID

import pytest
from django.urls import reverse
from pydantic import HttpUrl
from referentiel.value_objects.contract_kind import ContractKind
from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.offer_criteria import OfferCriteria, OfferLanguage
from referentiel.value_objects.offer_nature import OfferNature
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

SOURCE_ID = UUID("12345678-1234-4234-b234-123456789abc")

URL = reverse("ingestion:offers_by_source", kwargs={"source_id": SOURCE_ID})

NOMBRE_REQUETES_ATTENDU = (
    1  # view JWT authentication
    + 1  # JWT account's allowed networks
    + 1  # service: the user's access to the source
    + 2  # pagination: count + page
    + 1  # prefetch of the offers' localisations
    + 1  # ApiRequestLoggerMiddleware re-decodes the JWT to log the request
    + 2  # logging: DJ tries an UPDATE (manually-assigned pk) then falls back to INSERT
)


@pytest.fixture
def source():
    return SourceDjangoFactory(source_id=SOURCE_ID)


@pytest.fixture
def authenticated_client_with_source(api_client, test_user, source):
    test_user.sources.add(source)
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


def _localisation(department: str) -> dict:
    return {"area": "EU", "country": "FRA", "region": "28", "department": department}


class TestOffersBySourceView:
    def test_unauthenticated_returns_401(self, api_client):
        response = api_client.get(URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_api_key_returns_401(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
        response = api_client.get(URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_api_key_authentication_returns_offers(self, api_key_client, source):
        offer = OfferDjangoFactory(source=source)

        response = api_key_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
        assert [result["reference"] for result in response.json()["results"]] == [
            offer.reference
        ]

    def test_post_not_allowed(self, jwt_client):
        response = jwt_client.post(URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_jwt_authentication_returns_offers(
        self, authenticated_client_with_source, source
    ):
        offer = OfferDjangoFactory(source=source)
        OfferDjangoFactory()

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["reference"] == offer.reference
        assert data["results"][0]["source_id"] == str(SOURCE_ID)

    def test_jwt_authentication_returns_offer_without_localisation(
        self, authenticated_client_with_source, source
    ):
        OfferDjangoFactory(source=source, localisations=[])

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["results"][0]["localisation"] == []

    def test_returns_every_localisation_in_order(
        self, authenticated_client_with_source, source
    ):
        OfferDjangoFactory(
            source=source, localisations=[_localisation("14"), _localisation("50")]
        )

        response = authenticated_client_with_source.get(URL)

        assert [
            localisation["departement"]
            for localisation in response.json()["results"][0]["localisation"]
        ] == ["14", "50"]

    def test_jwt_authentication_forbidden_source_returns_403(self, jwt_client, source):
        response = jwt_client.get(URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_pagination_out_of_bounds_returns_404(
        self, authenticated_client_with_source, source
    ):
        OfferDjangoFactory.create_batch(3, source=source)

        response = authenticated_client_with_source.get(URL, {"page": 3, "taille": 2})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()

    def test_returns_error_500(self, jwt_client):
        with patch(
            "presentation.ingestion.views.offers.list_source_offers",
            side_effect=Exception("db error"),
        ):
            response = jwt_client.get(URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


class TestOffersBySourceViewDbVerified:
    def test_response_matches_db_record_field_by_field(
        self, authenticated_client_with_source, source
    ):
        offer = OfferDjangoFactory(
            source=source,
            offer_url=None,
            offer_nature=None,
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
                "reference": offer.reference,
                "source_id": str(SOURCE_ID),
                "titre": offer.title,
                "titre_long": None,
                "organisation": offer.organization,
                "employeur": None,
                "profil": offer.profile,
                "mission": offer.mission,
                "complements": None,
                "conditions_exercice": None,
                "descriptif_service": None,
                "versant": offer.verse,
                "categories": offer.categories,
                "nature_offre": None,
                "type_contrat": None,
                "vacance_poste": None,
                "url_offre": None,
                "url_candidature": None,
                "email_candidature": None,
                "localisation": [],
                "criteres": None,
                "conditions": None,
                "contacts": None,
                "debut_publication": "2024-01-15T00:00:00Z",
                "fin_publication": "2025-01-15T00:00:00Z",
                "debut_contrat": None,
                "fin_candidature": None,
                "debut_vacance_poste": None,
                "date_archivage": None,
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
            exercise_conditions="Télétravail possible",
            service_description="Service des ressources humaines",
            end_publication_date=datetime(2024, 12, 31, tzinfo=UTC),
            application_deadline=datetime(2024, 5, 15, tzinfo=UTC),
            job_vacancy_date=datetime(2024, 7, 1, tzinfo=UTC),
            offer_nature=OfferNature.TERRITORIAL.value,
            contract_kind=ContractKind.CDD_CDI.name,
            job_vacancy="1",
            offer_url=HttpUrl("https://exemple.gouv.fr/offres/e2e-1"),
            application_url=HttpUrl("https://exemple.gouv.fr/candidature/e2e-1"),
            location_label="Paris",
            latitude=48.8566,
            longitude=2.3522,
            criteria=criteria.to_dict(),
            conditions={"salaire": "35000-45000"},
            contacts=[
                {
                    "role": "principal",
                    "texte": "Jean Dupont : jean.dupont@example.gouv.fr",
                    "emails": ["jean.dupont@example.gouv.fr"],
                }
            ],
            beginning_date=datetime(2024, 6, 1, tzinfo=UTC),
        )

        response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"] == [
            {
                "reference": offer.reference,
                "source_id": str(SOURCE_ID),
                "titre": offer.title,
                "titre_long": offer.long_title,
                "organisation": offer.organization,
                "employeur": offer.employer,
                "profil": offer.profile,
                "mission": offer.mission,
                "complements": offer.complements,
                "conditions_exercice": offer.exercise_conditions,
                "descriptif_service": offer.service_description,
                "versant": offer.verse,
                "categories": offer.categories,
                "nature_offre": offer.offer_nature,
                "type_contrat": ContractKind.CDD_CDI.value,
                "vacance_poste": offer.job_vacancy,
                "url_offre": "https://exemple.gouv.fr/offres/e2e-1",
                "url_candidature": "https://exemple.gouv.fr/candidature/e2e-1",
                "email_candidature": None,
                "localisation": [
                    {
                        "zone_geographique": "EU",
                        "pays": "FRA",
                        "region": "11",
                        "departement": "75",
                        "localisation_label": "Paris",
                        "latitude": 48.8566,
                        "longitude": 2.3522,
                    }
                ],
                "criteres": criteria.to_dict(),
                "conditions": {"salaire": "35000-45000"},
                "contacts": [
                    {
                        "role": "principal",
                        "texte": "Jean Dupont : jean.dupont@example.gouv.fr",
                        "emails": ["jean.dupont@example.gouv.fr"],
                    }
                ],
                "debut_publication": "2024-01-15T00:00:00Z",
                "fin_publication": "2024-12-31T00:00:00Z",
                "debut_contrat": "2024-06-01T00:00:00Z",
                "fin_candidature": "2024-05-15T00:00:00Z",
                "debut_vacance_poste": "2024-07-01T00:00:00Z",
                "date_archivage": None,
            }
        ]

    def test_does_not_trigger_n_plus_one_queries(
        self, authenticated_client_with_source, source, django_assert_num_queries
    ):
        OfferDjangoFactory.create_batch(5, source=source)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = authenticated_client_with_source.get(URL)

        assert response.status_code == status.HTTP_200_OK
