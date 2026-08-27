from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from faker import Faker
from pydantic import ValidationError
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse
from rest_framework import status

from application.identite.usecases.list_organismes import ListOrganismesCommand
from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.seed_recruteur_datas import _ORGANISME_UUID

fake = Faker("fr_FR")

ORGANISME_UUID = fake.uuid4()
ORGANISME_URL = reverse("recruteur:organismes")


def _invalid_siret_error() -> ValidationError:
    try:
        SIRET(code="not-a-siret")
    except ValidationError as err:
        return err
    raise AssertionError("expected SIRET validation to fail")


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

    def test_get_returns_organismes(
        self,
        container,
        authenticated_client,
    ):
        mock_usecase = MagicMock()
        organismes = OrganismeFactory.create_entity_batch(3)

        mock_usecase.execute.return_value = organismes
        container.list_organismes_usecase.return_value = mock_usecase
        response = authenticated_client.get(ORGANISME_URL)

        mock_usecase.execute.assert_called_once()
        (called_command,), _ = mock_usecase.execute.call_args
        assert isinstance(called_command, ListOrganismesCommand)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "organisme_uuid": str(organisme.entity_id),
                "nom": organisme.nom,
                "versant": organisme.versant.value,
                "siret": organisme.siret.code,
                "gestionnaire": None,
                "gestion_ats": organisme.gestion_ats,
                "date_creation": organisme.date_creation,
                "date_derniere_activite": organisme.date_derniere_activite,
                "nombre_agents": 10,
                "nombre_offres_publiees": 20,
            }
            for organisme in organismes
        ]

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
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
    def test_get_returns_error_from_usecase(
        self,
        container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        container.list_organismes_usecase.return_value = mock_usecase
        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == expected_status
        assert response.json() == expected_body

    def test_post_create_organisme(
        self,
        container,
        authenticated_client,
    ):
        mock_usecase = MagicMock()
        organisme = OrganismeFactory.create_entity(entity_id=_ORGANISME_UUID)
        mock_usecase.execute.return_value = organisme
        container.create_organisme_usecase.return_value = mock_usecase
        body = {
            "nom": organisme.nom,
            "siret": organisme.siret.code,
            "versant": fake.random_choices(
                [Verse.FPE.value, Verse.FPT.value, Verse.FPH.value]
            ),
            "gestion_ats": organisme.gestion_ats,
        }
        response = authenticated_client.post(ORGANISME_URL, body)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["organisme_uuid"] == str(organisme.entity_id)
        assert response.json()["gestion_ats"] == organisme.gestion_ats

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
