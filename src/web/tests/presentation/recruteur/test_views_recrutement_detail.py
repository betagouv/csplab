from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.recruteur.dtos.recrutement_read_models import (
    CandidatDto,
    CandidatureKanbanDto,
    CandidatureListeReadModel,
    EtapeDto,
    EtapeKanbanReadModel,
    LocalisationDto,
    OrganismeRecruteurDto,
    RecrutementDetailReadModel,
    RecrutementKanbanReadModel,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse

fake = Faker()


def _candidature_liste_read_models(
    count: int = 11,
) -> list[CandidatureListeReadModel]:
    return [
        CandidatureListeReadModel(
            uuid=uuid4(),
            date_soumission=datetime.now(tz=timezone.utc),
            date_derniere_activite=datetime.now(tz=timezone.utc),
            candidat=CandidatDto(uuid=uuid4(), nom="Dupont", prenom="Alice"),
            etape=EtapeDto(etape_uuid=uuid4(), nom="Réception", categorie="ENTREE"),
        )
        for _ in range(count)
    ]


def _recrutement_detail_read_model() -> RecrutementDetailReadModel:
    return RecrutementDetailReadModel(
        offer_id=UUID(RECRUTEMENT_UUID),
        intitule="Chargé de mission numérique",
        archive=False,
        date_publication=datetime.now(tz=timezone.utc),
        localisation=LocalisationDto(
            zone_geographique="EU",
            pays="FRA",
            region="11",
            departement="75",
            localisation_label="Paris 8e arrondissement",
            latitude=48.8748,
            longitude=2.3070,
        ),
        organisme_recruteur=OrganismeRecruteurDto(
            nom="Mairie de Paris", siret="21750001600019"
        ),
        categorie_offre="A",
        etapes=[
            EtapeDto(etape_uuid=uuid4(), nom="Réception", categorie="ENTREE"),
            EtapeDto(etape_uuid=uuid4(), nom="Présélection", categorie="EN_COURS"),
        ],
    )


def _recrutement_kanban_read_model() -> RecrutementKanbanReadModel:
    return RecrutementKanbanReadModel(
        offer_id=UUID(RECRUTEMENT_UUID),
        intitule="Chargé de mission numérique",
        archive=False,
        date_publication=datetime.now(tz=timezone.utc),
        localisation=LocalisationDto(
            zone_geographique="EU",
            pays="FRA",
            region="11",
            departement="75",
            localisation_label="Paris 8e arrondissement",
            latitude=48.8748,
            longitude=2.3070,
        ),
        organisme_recruteur=OrganismeRecruteurDto(
            nom="Mairie de Paris", siret="21750001600019"
        ),
        categorie_offre="A",
        etapes=[
            EtapeKanbanReadModel(
                etape_uuid=uuid4(),
                nom="Réception des candidatures",
                categorie="ENTREE",
                candidatures=[
                    CandidatureKanbanDto(
                        uuid=uuid4(),
                        date_soumission=datetime.now(tz=timezone.utc),
                        date_derniere_activite=datetime.now(tz=timezone.utc),
                        candidat=CandidatDto(
                            uuid=uuid4(), nom="Dupont", prenom="Alice"
                        ),
                    )
                ],
            ),
            EtapeKanbanReadModel(
                etape_uuid=uuid4(),
                nom="Candidature acceptée",
                categorie="ACCEPTE",
                candidatures=[],
            ),
        ],
    )


ORGANISME_UUID = fake.uuid4()

# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"
UNKNOWN_RECRUTEMENT_UUID = fake.uuid4()

RECRUTEMENT_CANDIDATURES_ETAPE_URL = reverse(
    "recruteur:organisme-recrutement-candidatures-etape",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
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
RECRUTEMENT_DETAIL_URL = reverse(
    "recruteur:organisme-recrutement",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
UNKNOWN_RECRUTEMENT_DETAIL_URL = reverse(
    "recruteur:organisme-recrutement",
    kwargs={
        "organisme_uuid": ORGANISME_UUID,
        "recrutement_uuid": UNKNOWN_RECRUTEMENT_UUID,
    },
)


@pytest.fixture
def container():
    with patch(
        "presentation.recruteur.views.recrutement_detail.recruteur_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestRecrutementDetailView:
    @pytest.fixture(autouse=True)
    def _default_usecase(self, container):
        container.get_recrutement_detail_usecase.return_value.execute.return_value = (
            _recrutement_detail_read_model()
        )

    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENT_DETAIL_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_200(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENT_DETAIL_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_response_structure(self, authenticated_client):
        payload = authenticated_client.get(RECRUTEMENT_DETAIL_URL).json()
        assert set(payload) == {
            "offer_id",
            "intitule",
            "archive",
            "date_publication",
            "localisation",
            "organisme_recruteur",
            "categorie_offre",
            "etapes",
        }

    def test_localisation_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_DETAIL_URL).json()
        localisation = data["localisation"]
        assert "zone_geographique" in localisation
        assert "pays" in localisation
        assert "region" in localisation
        assert "departement" in localisation

    def test_organisme_recruteur_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_DETAIL_URL).json()
        organisme = data["organisme_recruteur"]
        assert "nom" in organisme
        assert "siret" in organisme

    def test_etape_structure(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_DETAIL_URL).json()
        etape = data["etapes"][0]
        assert "etape_uuid" in etape
        assert "nom" in etape
        assert "categorie" in etape

    def test_returns_404_for_unknown_recrutement(self, container, authenticated_client):
        container.get_recrutement_detail_usecase.return_value.execute.return_value = (
            None
        )

        response = authenticated_client.get(UNKNOWN_RECRUTEMENT_DETAIL_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_403_when_not_authorized(self, container, authenticated_client):
        container.get_recrutement_detail_usecase.return_value.execute.side_effect = (
            AccesOrganismeRefuse(UUID(fake.uuid4()))
        )

        response = authenticated_client.get(RECRUTEMENT_DETAIL_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        container.get_recrutement_detail_usecase.return_value.execute.side_effect = (
            OrganismeNexistePas("not found")
        )

        response = authenticated_client.get(RECRUTEMENT_DETAIL_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_500_on_unexpected_error(self, container, authenticated_client):
        container.get_recrutement_detail_usecase.return_value.execute.side_effect = (
            Exception("unexpected")
        )

        response = authenticated_client.get(RECRUTEMENT_DETAIL_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestRecrutementKanbanView:
    @pytest.fixture(autouse=True)
    def _default_usecase(self, container):
        container.get_recrutement_kanban_usecase.return_value.execute.return_value = (
            _recrutement_kanban_read_model()
        )

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

    def test_returns_404_for_unknown_recrutement(self, container, authenticated_client):
        container.get_recrutement_kanban_usecase.return_value.execute.return_value = (
            None
        )

        response = authenticated_client.get(UNKNOWN_RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_403_when_not_authorized(self, container, authenticated_client):
        container.get_recrutement_kanban_usecase.return_value.execute.side_effect = (
            AccesOrganismeRefuse(UUID(fake.uuid4()))
        )

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        container.get_recrutement_kanban_usecase.return_value.execute.side_effect = (
            OrganismeNexistePas("not found")
        )

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_500_on_unexpected_error(self, container, authenticated_client):
        container.get_recrutement_kanban_usecase.return_value.execute.side_effect = (
            Exception("unexpected")
        )

        response = authenticated_client.get(RECRUTEMENT_KANBAN_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestRecrutementListeView:
    @pytest.fixture(autouse=True)
    def _default_usecase(self, container):
        mock_usecase = container.get_recrutement_liste_usecase.return_value
        mock_usecase.execute.return_value = MagicMock()
        mock_usecase.execute.return_value.count.return_value = 11
        mock_usecase.execute.return_value.slice.return_value = (
            _candidature_liste_read_models()
        )

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

    def test_pagination_second_page(self, container, authenticated_client):
        mock_usecase = container.get_recrutement_liste_usecase.return_value
        mock_usecase.execute.return_value.slice.return_value = (
            _candidature_liste_read_models(5)
        )

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL + "?page=2&taille=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 5  # noqa
        assert data["next"] is not None
        assert data["previous"] is not None

    def test_no_next_on_last_page(self, authenticated_client):
        data = authenticated_client.get(RECRUTEMENT_LISTE_URL + "?taille=20").json()
        assert data["next"] is None
        assert data["previous"] is None

    def test_returns_404_for_unknown_recrutement(self, container, authenticated_client):
        container.get_recrutement_liste_usecase.return_value.execute.return_value = None

        response = authenticated_client.get(UNKNOWN_RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_403_when_not_authorized(self, container, authenticated_client):
        container.get_recrutement_liste_usecase.return_value.execute.side_effect = (
            AccesOrganismeRefuse(UUID(fake.uuid4()))
        )

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        container.get_recrutement_liste_usecase.return_value.execute.side_effect = (
            OrganismeNexistePas("not found")
        )

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_500_on_unexpected_error(self, container, authenticated_client):
        container.get_recrutement_liste_usecase.return_value.execute.side_effect = (
            Exception("unexpected")
        )

        response = authenticated_client.get(RECRUTEMENT_LISTE_URL)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestRecrutementCandidaturesEtapeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_echoes_candidatures_as_reussites(self, container, authenticated_client):
        candidature_uuid = str(uuid4())
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
        mock_usecase.execute.return_value = MagicMock(
            reussites=[UUID(candidature_uuid)], echecs=[]
        )

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={
                "etape_cible_uuid": fake.uuid4(),
                "candidatures": [
                    {
                        "candidature_uuid": candidature_uuid,
                        "etape_actuelle_uuid": fake.uuid4(),
                    }
                ],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reussites"] == [candidature_uuid]
        assert data["echecs"] == []

    def test_requires_etape_cible_uuid(self, authenticated_client):
        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_500_on_unexpected_error(self, container, authenticated_client):
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
        mock_usecase.execute.side_effect = Exception("unexpected")

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}
