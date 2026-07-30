from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.recruteur.dtos.recrutement_read_models import (
    AgentDto,
    CandidaturesCompteurDto,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory

fake = Faker()

ORGANISME_UUID = fake.uuid4()

RECRUTEMENTS_ACTIFS_URL = reverse(
    "recruteur:organisme-recrutements-actifs",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
RECRUTEMENTS_ARCHIVES_URL = reverse(
    "recruteur:organisme-recrutements-archives",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)


@pytest.fixture
def container():
    with patch(
        "presentation.recruteur.views.recrutement_listes.recruteur_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestRecrutementsActifsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pagination_second_page(self, container, authenticated_client):
        mock_usecase = container.lister_mes_recrutements_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_usecase.execute.return_value.count.return_value = 6
        mock_usecase.execute.return_value.slice.return_value = [
            RecrutementFactory.create_actif_read_model() for _ in range(2)
        ]

        response = authenticated_client.get(
            RECRUTEMENTS_ACTIFS_URL + "?taille=2&page=2"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 2  # noqa
        assert data["next"] is not None
        assert data["previous"] is not None

    def test_candidatures_structure(self, container, authenticated_client):
        mock_usecase = container.lister_mes_recrutements_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_usecase.execute.return_value.count.return_value = 1
        mock_usecase.execute.return_value.slice.return_value = [
            RecrutementFactory.create_actif_read_model(
                candidatures=CandidaturesCompteurDto(total=5, a_traiter=2, en_cours=1),
            )
        ]

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)
        data = response.json()
        candidatures = data["results"][0]["candidatures"]
        assert "total" in candidatures
        assert "a_traiter" in candidatures
        assert "en_cours" in candidatures

    def test_returns_actifs(self, container, authenticated_client):
        mock_usecase = container.lister_mes_recrutements_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_usecase.execute.return_value.count.return_value = 1
        mock_usecase.execute.return_value.slice.return_value = [
            RecrutementFactory.create_actif_read_model(
                intitule="Chargé de mission numérique",
                reference_csp="REF-2025-001",
                type_contrat="TITULAIRE_CONTRACTUEL",
                agents=[AgentDto(nom="Marie Dupont")],
            )
        ]

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        first = data["results"][0]
        assert "offer_id" in first
        assert "intitule" in first
        assert "reference_csp" in first
        assert "type_contrat" in first
        assert "date_publication" in first
        assert "responsables" in first
        assert "derniere_activite" in first
        assert "candidatures" in first

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")
        container.lister_mes_recrutements_usecase.return_value = mock_usecase

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    @patch("presentation.recruteur.views.recrutement_listes.recruteur_container")
    def test_returns_403_when_not_responsable(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = AccesOrganismeRefuse(UUID(fake.uuid4()))

        mock_container = MagicMock()
        mock_container.lister_mes_recrutements_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    @patch("presentation.recruteur.views.recrutement_listes.recruteur_container")
    def test_returns_500_on_unexpected_error(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.lister_mes_recrutements_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestRecrutementsArchivesView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENTS_ARCHIVES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pagination_second_page(self, container, authenticated_client):
        mock_usecase = container.lister_mes_recrutements_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_usecase.execute.return_value.count.return_value = 3
        mock_usecase.execute.return_value.slice.return_value = [
            RecrutementFactory.create_archive_read_model() for _ in range(2)
        ]

        response = authenticated_client.get(
            RECRUTEMENTS_ARCHIVES_URL + "?taille=2&page=1"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 2  # noqa
        assert data["next"] is not None
        assert data["previous"] is None

    def test_returns_archives(self, container, authenticated_client):
        mock_usecase = container.lister_mes_recrutements_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_usecase.execute.return_value.count.return_value = 1
        mock_usecase.execute.return_value.slice.return_value = [
            RecrutementFactory.create_archive_read_model(
                intitule="Directeur des systèmes d'information",
                reference_csp="REF-2024-A01",
                type_contrat="TITULAIRE_CONTRACTUEL",
                agents=[AgentDto(nom="Marie Dupont")],
                finalise=True,
                recrute="Sophie Leblanc",
            )
        ]

        response = authenticated_client.get(RECRUTEMENTS_ARCHIVES_URL)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        first = data["results"][0]
        assert "offer_id" in first
        assert "intitule" in first
        assert "reference_csp" in first
        assert "type_contrat" in first
        assert "date_archivage" in first
        assert "responsables" in first
        assert "finalise" in first
        assert "recrute" in first

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")
        container.lister_mes_recrutements_usecase.return_value = mock_usecase

        response = authenticated_client.get(RECRUTEMENTS_ARCHIVES_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    @patch("presentation.recruteur.views.recrutement_listes.recruteur_container")
    def test_returns_403_when_not_responsable(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = AccesOrganismeRefuse(UUID(fake.uuid4()))

        mock_container = MagicMock()
        mock_container.lister_mes_recrutements_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ARCHIVES_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    @patch("presentation.recruteur.views.recrutement_listes.recruteur_container")
    def test_returns_500_on_unexpected_error(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.lister_mes_recrutements_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ARCHIVES_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}
