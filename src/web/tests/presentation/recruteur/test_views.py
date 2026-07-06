from http import HTTPStatus
from unittest.mock import MagicMock, patch
from uuid import UUID

from django.test import Client
from django.urls import reverse
from faker import Faker
from rest_framework import status

from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.erreur_recrutement import (
    ConfigurationEtapesInvalide,
    ErreurRecruteur,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from tests.factories.recruteur.organisme_factory import (
    OrganismeRecruteurFactory,
)

fake = Faker()

ORGANISME_UUID = fake.uuid4()
ORGANISME_URL = reverse(
    "recruteur:organisme", kwargs={"organisme_uuid": ORGANISME_UUID}
)
ETAPES_URL = reverse(
    "recruteur:organisme-parametres-etapes",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
INIT_ETAPES_URL = reverse(
    "recruteur:organisme-parametres-etapes-init",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
UNKNOWN_ORGANISME_UUID = "ffffffff-ffff-4fff-bfff-ffffffffffff"

RECRUTEMENTS_ACTIFS_URL = reverse(
    "recruteur:organisme-recrutements-actifs",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
UNKNOWN_RECRUTEMENTS_ACTIFS_URL = reverse(
    "recruteur:organisme-recrutements-actifs",
    kwargs={"organisme_uuid": UNKNOWN_ORGANISME_UUID},
)
RECRUTEMENTS_ARCHIVES_URL = reverse(
    "recruteur:organisme-recrutements-archives",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
UNKNOWN_RECRUTEMENTS_ARCHIVES_URL = reverse(
    "recruteur:organisme-recrutements-archives",
    kwargs={"organisme_uuid": UNKNOWN_ORGANISME_UUID},
)


# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"
UNKNOWN_RECRUTEMENT_UUID = "ffffffff-ffff-4fff-bfff-ffffffffffff"

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


class TestOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ORGANISME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("presentation.recruteur.views.recruteur_container")
    def test_authenticated_access_is_ok(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_organisme = MagicMock()
        mock_organisme.nom = "COMMUNE DE BRIANCON"
        mock_organisme.siret = "21050023700354"

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = mock_organisme

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "nom": "COMMUNE DE BRIANCON",
            "siret": "21050023700354",
        }

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_404_when_organisme_not_found(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ErreurRecruteur("not found")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}


class TestEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_404_when_organisme_not_found(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"organisme_uuid": "Not found."}

    @patch("presentation.recruteur.views.recruteur_container")
    def test_authenticated_access_is_ok(
        self, mock_recruteur_container, authenticated_client
    ):
        organisme = OrganismeRecruteurFactory.create_entity()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_200_OK
        steps = []
        if organisme.etapes:
            steps = [
                {
                    "etape_uuid": str(etape.entity_id),
                    "nom": etape.nom,
                    "categorie": etape.categorie.name,
                }
                for etape in organisme.etapes
            ]

        assert response.json() == steps


class TestInitEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(INIT_ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_404_when_organisme_not_found(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"organisme_uuid": "Not found."}

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_500_on_unexpected_error(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    @patch("presentation.recruteur.views.recruteur_container")
    def test_authenticated_post_initialize_steps(
        self, mock_recruteur_container, authenticated_client
    ):
        organisme = OrganismeRecruteurFactory.create_entity()
        organisme.initialiser_etapes()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == [
            {
                "etape_uuid": str(etape.entity_id),
                "nom": etape.nom,
                "categorie": etape.categorie.name,
            }
            for etape in (organisme.etapes or ())
        ]


class TestPutEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.put(ETAPES_URL, [], format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_body_returns_400(self, authenticated_client):
        response = authenticated_client.put(
            ETAPES_URL,
            [{"nom": "Entretien", "categorie": "INVALIDE"}],
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_nom_returns_400(self, authenticated_client):
        response = authenticated_client.put(
            ETAPES_URL,
            [{"categorie": "EN_COURS"}],
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch("presentation.recruteur.views.recruteur_container")
    def test_put_mixed_existing_and_new_etapes(
        self, mock_recruteur_container, authenticated_client
    ):
        existing_uuid = fake.uuid4()
        new_uuid = fake.uuid4()
        other_uuid = fake.uuid4()

        organisme = OrganismeRecruteurFactory.create_entity()
        organisme._etapes = (
            EtapeRecrutement.build(
                entity_id=UUID(str(existing_uuid)),
                nom="Réception",
                categorie=CategorieEtapeRecrutement.ENTREE,
            ),
            EtapeRecrutement.build(
                entity_id=UUID(str(new_uuid)),
                nom="Nouvelle étape",
                categorie=CategorieEtapeRecrutement.EN_COURS,
            ),
            EtapeRecrutement.build(
                entity_id=UUID(str(other_uuid)),
                nom="Recrutement",
                categorie=CategorieEtapeRecrutement.ACCEPTE,
            ),
        )

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        payload = [
            {
                "etape_uuid": str(existing_uuid),
                "nom": "Réception",
                "categorie": "ENTREE",
            },
            {"nom": "Nouvelle étape", "categorie": "EN_COURS"},
            {
                "etape_uuid": str(other_uuid),
                "nom": "Recrutement",
                "categorie": "ACCEPTE",
            },
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3  # noqa
        assert data[0]["etape_uuid"] == str(existing_uuid)
        assert data[1]["etape_uuid"] == str(new_uuid)
        assert data[1]["nom"] == "Nouvelle étape"

    @patch("presentation.recruteur.views.recruteur_container")
    def test_put_returns_400_on_invalid_steps(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ConfigurationEtapesInvalide(
            "la première étape doit être de catégorie ENTREE"
        )

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        payload = [
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "error": "la première étape doit être de catégorie ENTREE"
        }

    @patch("presentation.recruteur.views.recruteur_container")
    def test_put_returns_404_when_organisme_not_found(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"organisme_uuid": "Not found."}

    @patch("presentation.recruteur.views.recruteur_container")
    def test_put_returns_500_on_unexpected_error(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestRecrutementsActifsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("presentation.recruteur.views.recruteur_container")
    def test_pagination_second_page(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_container = MagicMock()
        mock_usecase = mock_container.get_organisme_recruteur_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL + "?size=2&page=2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 2  # noqa
        assert data["next"] is not None
        assert data["previous"] is not None

    @patch("presentation.recruteur.views.recruteur_container")
    def test_candidatures_structure(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_container = MagicMock()
        mock_usecase = mock_container.get_organisme_recruteur_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)
        data = response.json()
        candidatures = data["results"][0]["candidatures"]
        assert "total" in candidatures
        assert "a_traiter" in candidatures
        assert "en_cours" in candidatures

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_actifs(self, mock_recruteur_container, authenticated_client):
        mock_container = MagicMock()
        mock_usecase = mock_container.get_organisme_recruteur_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 6  # noqa
        first = data["results"][0]
        assert "offer_id" in first
        assert "intitule" in first
        assert "reference_csp" in first
        assert "type_contrat" in first
        assert "date_publication" in first
        assert "responsables" in first
        assert "derniere_activite" in first
        assert "candidatures" in first

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_404_for_unknown_organisme(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(UNKNOWN_RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_500_on_unexpected_error(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ACTIFS_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestRecrutementsArchivesView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENTS_ARCHIVES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("presentation.recruteur.views.recruteur_container")
    def test_pagination_second_page(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_container = MagicMock()
        mock_usecase = mock_container.get_organisme_recruteur_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(
            RECRUTEMENTS_ARCHIVES_URL + "?size=2&page=1"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 2  # noqa
        assert data["next"] is not None
        assert data["previous"] is None

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_archives(self, mock_recruteur_container, authenticated_client):
        mock_container = MagicMock()
        mock_usecase = mock_container.get_organisme_recruteur_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(RECRUTEMENTS_ARCHIVES_URL)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 3  # noqa
        first = data["results"][0]
        assert "offer_id" in first
        assert "intitule" in first
        assert "reference_csp" in first
        assert "type_contrat" in first
        assert "date_archivage" in first
        assert "responsables" in first
        assert "finalise" in first
        assert "recrute" in first

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_404_for_unknown_organisme(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(UNKNOWN_RECRUTEMENTS_ARCHIVES_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    @patch("presentation.recruteur.views.recruteur_container")
    def test_returns_500_on_unexpected_error(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
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

    @patch("presentation.recruteur.views.RecrutementKanbanMapper")
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
        # 4 + 3 + 2 + 2 + 0 = 11 candidatures au total
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

    @patch("presentation.recruteur.views.RecrutementListeMapper")
    def test_returns_500_on_unexpected_error(self, mock_mapper, authenticated_client):
        mock_mapper.return_value.from_domain.side_effect = Exception("unexpected")

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestATSBase:
    def test_base_view_returns_200(self, db, client: Client):
        response = client.get("/ats/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_uses_correct_template(self, db, client: Client):
        response = client.get("/ats/")
        assert "ats/base.html" in [t.name for t in response.templates]

    def test_base_view_catches_subroutes(self, db, client: Client):
        response = client.get("/ats/candidates/123/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_sets_csrf_cookie(self, db, client: Client):
        response = client.get("/ats/")
        assert "csrftoken" in response.cookies
