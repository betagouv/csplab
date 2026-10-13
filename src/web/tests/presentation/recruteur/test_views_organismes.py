from unittest.mock import MagicMock, patch

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from faker import Faker
from pydantic import ValidationError
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse
from rest_framework import status

from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from tests.utils.dates import datetime_to_drf_representation

fake = Faker("fr_FR")

ORGANISME_URL = reverse("recruteur:organismes")


def _invalid_siret_error() -> ValidationError:
    try:
        SIRET(code="not-a-siret")
    except ValidationError as err:
        return err
    raise AssertionError("expected SIRET validation to fail")


@pytest.fixture
def staff_client(api_client):
    api_client.force_login(UtilisateurDjangoFactory(is_staff=True))
    return api_client


@pytest.fixture
def container():
    with patch(
        "presentation.recruteur.views.organismes.create_identite_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


siret = fake.siret().replace(" ", "")


class TestOrganismesView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ORGANISME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_returns_organismes(self, staff_client):
        organisme = OrganismeDjangoFactory(gestion_ats=True)
        RecrutementDjangoFactory(organisme=organisme)

        response = staff_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_200_OK
        organisme.refresh_from_db()
        matching = next(o for o in response.json() if o["uuid"] == str(organisme.id))
        assert matching == {
            "uuid": str(organisme.id),
            "nom": organisme.nom,
            "versant": organisme.versant,
            "siret": organisme.siret,
            "gestionnaire": None,
            "gestion_ats": True,
            "date_creation": datetime_to_drf_representation(organisme.created_at),
            "date_derniere_activite": datetime_to_drf_representation(
                organisme.updated_at
            ),
            "nombre_agents": 0,
            "nombre_offres_publiees": 1,
        }

    def test_get_query_count_does_not_grow_with_organismes(self, staff_client):
        def count_queries() -> int:
            with CaptureQueriesContext(connection) as queries:
                staff_client.get(ORGANISME_URL)
            return len(queries)

        OrganismeDjangoFactory()
        baseline = count_queries()
        for organisme in OrganismeDjangoFactory.create_batch(3):
            OrganismeAgentDjangoFactory(organisme=organisme)
            RecrutementDjangoFactory(organisme=organisme)

        assert count_queries() == baseline

    def test_get_refuses_non_staff(self, authenticated_client):
        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": OperationOrganismeRefusee().message}

    def test_get_returns_500_on_unexpected_error(self, staff_client):
        with patch(
            "presentation.recruteur.views.organismes.list_organismes",
            side_effect=Exception("unexpected"),
        ):
            response = staff_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeSiretExisteDeja(siret),
                status.HTTP_400_BAD_REQUEST,
                {"error": OrganismeSiretExisteDeja(siret).message},
            ),
            (
                _invalid_siret_error(),
                status.HTTP_400_BAD_REQUEST,
                {"error": str(_invalid_siret_error())},
            ),
            (
                OperationOrganismeRefusee(),
                status.HTTP_403_FORBIDDEN,
                {"error": OperationOrganismeRefusee().message},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_post_returns_error_from_usecase(
        self,
        container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        container.create_organisme_usecase.return_value = mock_usecase
        body = {
            "nom": fake.name(),
            "siret": siret,
            "versant": fake.random_choices(
                [Verse.FPE.value, Verse.FPT.value, Verse.FPH.value]
            ),
            "gestion_ats": fake.boolean(),
        }
        response = authenticated_client.post(ORGANISME_URL, body)

        assert response.status_code == expected_status
        assert response.json() == expected_body


class TestOrganismesViewDbVerified:
    def test_post_creates_and_persists_the_organisme(self, staff_client):
        siret_code = fake.siret().replace(" ", "")
        body = {
            "nom": fake.company(),
            "siret": siret_code,
            "versant": Verse.FPE.value,
            "gestion_ats": True,
        }

        response = staff_client.post(ORGANISME_URL, body)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == body["nom"]
        assert data["siret"] == siret_code
        assert data["versant"] == Verse.FPE.value
        assert data["gestion_ats"] is True

        organisme = OrganismeModel.objects.get(siret=siret_code)
        assert str(organisme.id) == data["uuid"]
        assert organisme.nom == body["nom"]
