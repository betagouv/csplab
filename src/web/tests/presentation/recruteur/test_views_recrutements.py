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
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory

fake = Faker()

ORGANISME_UUID = fake.uuid4()
UNKNOWN_ORGANISME_UUID = fake.uuid4()

RECRUTEMENTS_ACTIFS_URL = reverse(
    "recruteur:organisme-recrutements-actifs",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
RECRUTEMENTS_ARCHIVES_URL = reverse(
    "recruteur:organisme-recrutements-archives",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)

# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"
UNKNOWN_RECRUTEMENT_UUID = fake.uuid4()

RECRUTEMENT_KANBAN_URL = reverse(
    "recruteur:organisme-recrutement-kanban",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
RECRUTEMENT_LISTE_URL = reverse(
    "recruteur:organisme-recrutement-liste",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
UNKNOWN_RECRUTEMENT_KANBAN_URL = reverse(
    "recruteur:organisme-recrutement-kanban",
    kwargs={
        "organisme_uuid": ORGANISME_UUID,
        "recrutement_uuid": UNKNOWN_RECRUTEMENT_UUID,
    },
)
UNKNOWN_RECRUTEMENT_LISTE_URL = reverse(
    "recruteur:organisme-recrutement-liste",
    kwargs={
        "organisme_uuid": ORGANISME_UUID,
        "recrutement_uuid": UNKNOWN_RECRUTEMENT_UUID,
    },
)


@pytest.fixture
def container():
    with patch("presentation.recruteur.views.recrutements.recruteur_container") as mock:
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

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL + "?size=2&page=2")
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

    @patch("presentation.recruteur.views.recrutements.recruteur_container")
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

    @patch("presentation.recruteur.views.recrutements.recruteur_container")
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
            RECRUTEMENTS_ARCHIVES_URL + "?size=2&page=1"
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

    @patch("presentation.recruteur.views.recrutements.recruteur_container")
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

    @patch("presentation.recruteur.views.recrutements.recruteur_container")
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


class TestRecrutementKanbanView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_200(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_response_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()
        assert "offer_id" in data
        assert "intitule" in data
        assert "date_publication" in data
        assert "localisation" in data
        assert "organisme_recruteur" in data
        assert "categorie_offre" in data
        assert "etapes" in data
        assert isinstance(data["etapes"], list)

    def test_localisation_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()
        localisation = data["localisation"]
        assert "zone_geographique" in localisation
        assert "pays" in localisation
        assert "region" in localisation
        assert "departement" in localisation

    def test_organisme_recruteur_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()
        organisme = data["organisme_recruteur"]
        assert "nom" in organisme
        assert "siret" in organisme

    def test_etape_structure(self, authenticated_client):
        etape = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()["etapes"][0]
        assert "etape_uuid" in etape
        assert "nom" in etape
        assert "categorie" in etape
        assert "candidatures" in etape
        assert isinstance(etape["candidatures"], list)

    def test_candidature_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()
        candidature = data["etapes"][0]["candidatures"][0]
        assert "uuid" in candidature
        assert "date_soumission" in candidature
        assert "candidat" in candidature
        assert "uuid" in candidature["candidat"]
        assert "nom" in candidature["candidat"]
        assert "prenom" in candidature["candidat"]

    def test_etapes_order(self, authenticated_client):
        etapes = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()["etapes"]
        assert etapes[0]["categorie"] == "ENTREE"
        assert etapes[-1]["categorie"] == "ACCEPTE"

    def test_etape_accepte_has_no_candidatures(self, authenticated_client):
        etape_accepte = authenticated_client.get(RECRUTEMENT_KANBAN_URL).json()[
            "etapes"
        ][-1]
        assert etape_accepte["categorie"] == "ACCEPTE"
        assert etape_accepte["candidatures"] == []

    def test_returns_404_for_unknown_recrutement(self, authenticated_client):
        response = authenticated_client.get(UNKNOWN_RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    @patch("presentation.recruteur.views.recrutements.RecrutementKanbanMapper")
    def test_returns_500_on_unexpected_error(self, mock_mapper, authenticated_client):
        mock_mapper.return_value.from_domain.side_effect = Exception("unexpected")

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestRecrutementListeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_200(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_pagination_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()
        assert "count" in data
        assert "next" in data
        assert "previous" in data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_total_count(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()
        assert data["count"] == 11  # noqa

    def test_candidature_structure(self, authenticated_client):
        candidature = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()["results"][
            0
        ]
        assert "uuid" in candidature
        assert "date_soumission" in candidature
        assert "candidat" in candidature
        assert "etape" in candidature

    def test_etape_structure(self, authenticated_client):
        etape = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()["results"][0][
            "etape"
        ]
        assert "etape_uuid" in etape
        assert "nom" in etape
        assert "categorie" in etape

    def test_candidat_structure(self, authenticated_client):
        candidat = authenticated_client.get(RECRUTEMENT_LISTE_URL).json()["results"][0][
            "candidat"
        ]
        assert "uuid" in candidat
        assert "nom" in candidat
        assert "prenom" in candidat

    def test_pagination_second_page(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENT_LISTE_URL + "?page=2&size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 5  # noqa
        assert data["next"] is not None
        assert data["previous"] is not None

    def test_no_next_on_last_page(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_LISTE_URL + "?size=20").json()
        assert data["next"] is None
        assert data["previous"] is None

    @patch("presentation.recruteur.views.recrutements.RecrutementListeMapper")
    def test_returns_500_on_unexpected_error(self, mock_mapper, authenticated_client):
        mock_mapper.return_value.from_domain.side_effect = Exception("unexpected")

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}
