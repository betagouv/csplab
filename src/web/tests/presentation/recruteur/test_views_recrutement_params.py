from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
    RecrutementEtapeIncoherents,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementInexistant,
    SupressionEtapeImpossible,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from presentation.recruteur.views.recrutement_params import _etapes_to_serializer_data

fake = Faker()

ORGANISME_UUID = fake.uuid4()

# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"

RECRUTEMENT_ETAPES_URL = reverse(
    "recruteur:organisme-recrutement-etapes",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
RECRUTEMENT_ETAPES_INIT_URL = reverse(
    "recruteur:organisme-recrutement-etapes-init",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)

ETAPE_UUID = "aaaaaaaa-0002-0002-0002-000000000002"


@pytest.fixture
def container():
    with patch(
        "presentation.recruteur.views.recrutement_params.recruteur_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestRecrutementEtapeView:
    def test_anonymous_access_is_unauthorized_on_get(self, api_client):
        response = api_client.get(RECRUTEMENT_ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_access_is_unauthorized_on_patch(self, api_client):
        response = api_client.patch(RECRUTEMENT_ETAPES_URL, data=[], format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_returns_pipeline(self, container, authenticated_client):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        container.get_recrutement_etapes_usecase.return_value.execute.return_value = (
            etapes
        )

        response = authenticated_client.get(RECRUTEMENT_ETAPES_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == len(etapes)
        assert data[0]["nom"] == "Réception des candidatures"
        assert data[0]["categorie"] == "ENTREE"

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeRecrutementIncoherents(
                    UUID(ORGANISME_UUID), UUID(RECRUTEMENT_UUID)
                ),
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": OrganismeRecrutementIncoherents(
                        UUID(ORGANISME_UUID), UUID(RECRUTEMENT_UUID)
                    ).message
                },
            ),
            (
                AccesOrganismeRefuse(UUID(ORGANISME_UUID)),
                status.HTTP_403_FORBIDDEN,
                {"error": AccesOrganismeRefuse(UUID(ORGANISME_UUID)).message},
            ),
            (
                OrganismeNexistePas(ORGANISME_UUID),
                status.HTTP_404_NOT_FOUND,
                {"error": OrganismeNexistePas(ORGANISME_UUID).message},
            ),
            (
                RecrutementInexistant(UUID(RECRUTEMENT_UUID)),
                status.HTTP_404_NOT_FOUND,
                {"error": RecrutementInexistant(UUID(RECRUTEMENT_UUID)).message},
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
        container.get_recrutement_etapes_usecase.return_value.execute.side_effect = (
            exception
        )
        response = authenticated_client.get(
            RECRUTEMENT_ETAPES_URL,
        )

        assert response.status_code == expected_status
        assert response.json() == expected_body

    def test_patch_requires_valid_body(self, authenticated_client):
        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=[{"nom": "Réception"}],
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_201_with_updated_pipeline(self, container, authenticated_client):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        usecase = container.update_recrutement_etapes_usecase.return_value.execute
        usecase.return_value = etapes

        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=_etapes_to_serializer_data(etapes=etapes),
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == len(etapes)
        assert data[-1]["etape_uuid"] == str(etapes[-1].entity_id)
        assert data[-1]["nom"] == "Recrutement"
        assert data[-1]["categorie"] == "ACCEPTE"

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeRecrutementIncoherents(
                    UUID(ORGANISME_UUID), UUID(RECRUTEMENT_UUID)
                ),
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": OrganismeRecrutementIncoherents(
                        UUID(ORGANISME_UUID), UUID(RECRUTEMENT_UUID)
                    ).message
                },
            ),
            (
                RecrutementEtapeIncoherents(
                    recrutement_id=UUID(ORGANISME_UUID), etape_id=UUID(ETAPE_UUID)
                ),
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": f"L'étape {ETAPE_UUID} ne correspond pas au recrutement"
                    f" {ORGANISME_UUID}"
                },
            ),
            (
                ConfigurationEtapesInvalide(
                    "La première étape doit être de catégorie ENTREE"
                ),
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": ConfigurationEtapesInvalide(
                        "La première étape doit être de catégorie ENTREE"
                    ).message
                },
            ),
            (
                SupressionEtapeImpossible(UUID(ETAPE_UUID), 1),
                status.HTTP_400_BAD_REQUEST,
                {"error": SupressionEtapeImpossible(UUID(ETAPE_UUID), 1).message},
            ),
            (
                AccesOrganismeRefuse(UUID(ORGANISME_UUID)),
                status.HTTP_403_FORBIDDEN,
                {"error": AccesOrganismeRefuse(UUID(ORGANISME_UUID)).message},
            ),
            (
                OrganismeNexistePas(ORGANISME_UUID),
                status.HTTP_404_NOT_FOUND,
                {"error": OrganismeNexistePas(ORGANISME_UUID).message},
            ),
            (
                RecrutementInexistant(UUID(RECRUTEMENT_UUID)),
                status.HTTP_404_NOT_FOUND,
                {"error": RecrutementInexistant(UUID(RECRUTEMENT_UUID)).message},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_patch_returns_error_from_usecase(
        self,
        container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        container.update_recrutement_etapes_usecase.return_value.execute.side_effect = (
            exception
        )
        etapes = EtapeRecrutementFactory.create_entity_batch()
        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=_etapes_to_serializer_data(etapes=etapes),
            format="json",
        )

        assert response.status_code == expected_status
        assert response.json() == expected_body


class TestInitRecrutementEtapeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(RECRUTEMENT_ETAPES_INIT_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_201_with_default_pipeline(self, container, authenticated_client):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        container.init_recrutement_etapes_usecase.return_value.execute.return_value = (
            etapes
        )

        response = authenticated_client.post(RECRUTEMENT_ETAPES_INIT_URL)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert len(data) == len(etapes)
        assert data[-1]["nom"] == "Recrutement"
        assert data[-1]["categorie"] == "ACCEPTE"

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeRecrutementIncoherents(
                    UUID(ORGANISME_UUID), UUID(RECRUTEMENT_UUID)
                ),
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": OrganismeRecrutementIncoherents(
                        UUID(ORGANISME_UUID), UUID(RECRUTEMENT_UUID)
                    ).message
                },
            ),
            (
                SupressionEtapeImpossible(UUID(ETAPE_UUID), 1),
                status.HTTP_400_BAD_REQUEST,
                {"error": SupressionEtapeImpossible(UUID(ETAPE_UUID), 1).message},
            ),
            (
                AccesOrganismeRefuse(UUID(ORGANISME_UUID)),
                status.HTTP_403_FORBIDDEN,
                {"error": AccesOrganismeRefuse(UUID(ORGANISME_UUID)).message},
            ),
            (
                OrganismeNexistePas(ORGANISME_UUID),
                status.HTTP_404_NOT_FOUND,
                {"error": OrganismeNexistePas(ORGANISME_UUID).message},
            ),
            (
                RecrutementInexistant(UUID(RECRUTEMENT_UUID)),
                status.HTTP_404_NOT_FOUND,
                {"error": RecrutementInexistant(UUID(RECRUTEMENT_UUID)).message},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_returns_error_from_usecase(
        self,
        container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        container.init_recrutement_etapes_usecase.return_value.execute.side_effect = (
            exception
        )

        response = authenticated_client.post(RECRUTEMENT_ETAPES_INIT_URL)

        assert response.status_code == expected_status
        assert response.json() == expected_body


class TestRecrutementEtapeViewDbVerified:
    def test_returns_persisted_etapes(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        offer = OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
        recrutement = RecrutementDjangoFactory(organisme=organisme, offre=offer)

        response = authenticated_client.get(RECRUTEMENT_ETAPES_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == len(recrutement.ordre_etapes)
        assert data[0]["categorie"] == "ENTREE"
        assert data[-1]["categorie"] == "ACCEPTE"

    def test_patch_persists_the_etapes(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        offer = OfferDjangoFactory(id=UUID(RECRUTEMENT_UUID))
        RecrutementDjangoFactory(organisme=organisme, offre=offer)
        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL, data=payload, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert [{"nom": e["nom"], "categorie": e["categorie"]} for e in data] == payload

        recrutement_model = RecrutementModel.objects.get(
            offre_id=UUID(RECRUTEMENT_UUID)
        )
        assert [e["nom"] for e in recrutement_model.ordre_etapes] == [
            e["nom"] for e in payload
        ]
