from unittest.mock import patch

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from referentiel.value_objects.verse import Verse
from rest_framework import status

from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeModel,
    OrganismeQuerySet,
)
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
VALID_SIRET = fake.siret().replace(" ", "")
INVALID_CHECKSUM_SIRET = VALID_SIRET[:-1] + str((int(VALID_SIRET[-1]) + 1) % 10)


@pytest.fixture
def staff_client(api_client):
    api_client.force_login(UtilisateurDjangoFactory(is_staff=True))
    return api_client


def _body(**overrides):
    return {
        "nom": fake.company(),
        "siret": VALID_SIRET,
        "versant": Verse.FPE.value,
        "gestion_ats": True,
        **overrides,
    }


def _post(client, body):
    return client.post(ORGANISME_URL, body, format="json")


class TestListOrganismes:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ORGANISME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_returns_organismes(self, staff_client):
        organisme = OrganismeDjangoFactory(gestion_ats=True)
        RecrutementDjangoFactory(organisme=organisme)
        superviseur = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.SUPERVISEUR.value
        )
        OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.SUPERVISEUR.value,
            date_revocation=timezone.now(),
        )
        OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.AGENT.value
        )

        response = staff_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_200_OK
        organisme.refresh_from_db()
        matching = next(o for o in response.json() if o["uuid"] == str(organisme.id))
        last_activity = max(
            organisme.updated_at,
            *organisme.agents_liaisons.values_list("updated_at", flat=True),
        )
        assert matching == {
            "uuid": str(organisme.id),
            "nom": organisme.nom,
            "versant": organisme.versant,
            "siret": organisme.siret,
            "superviseurs": (
                f"{superviseur.agent.utilisateur.last_name} "
                f"{superviseur.agent.utilisateur.first_name}"
            ),
            "gestion_ats": True,
            "date_creation": datetime_to_drf_representation(organisme.created_at),
            "date_derniere_activite": datetime_to_drf_representation(last_activity),
            "nombre_agents": 2,
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
        with patch.object(
            OrganismeQuerySet, "with_counts", side_effect=Exception("unexpected")
        ):
            response = staff_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestCreateOrganisme:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = _post(api_client, _body())

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_staff_creates_and_persists_the_organisme(self, staff_client):
        body = _body()

        response = _post(staff_client, body)

        assert response.status_code == status.HTTP_201_CREATED
        organisme = OrganismeModel.objects.get(siret=VALID_SIRET)
        assert response.json() == {
            "uuid": str(organisme.id),
            "nom": body["nom"],
            "versant": Verse.FPE.value,
            "siret": VALID_SIRET,
            "superviseurs": "",
            "gestion_ats": True,
            "date_derniere_activite": datetime_to_drf_representation(
                organisme.date_derniere_activite
            ),
            "date_creation": datetime_to_drf_representation(organisme.date_creation),
        }

    def test_refuses_non_staff(self, authenticated_client):
        response = _post(authenticated_client, _body())

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": OperationOrganismeRefusee().message}
        assert not OrganismeModel.objects.exists()

    def test_refuses_existing_siret(self, staff_client):
        OrganismeDjangoFactory(siret=VALID_SIRET)

        response = _post(staff_client, _body())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "error": OrganismeSiretExisteDeja(VALID_SIRET).message
        }
        assert OrganismeModel.objects.count() == 1

    def test_refuses_siret_with_invalid_checksum(self, staff_client):
        response = _post(staff_client, _body(siret=INVALID_CHECKSUM_SIRET))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid SIRET checksum" in response.json()["error"]
        assert not OrganismeModel.objects.exists()

    @pytest.mark.parametrize(
        ("overrides", "invalid_field"),
        [
            ({"nom": ""}, "nom"),
            ({"siret": "123"}, "siret"),
            ({"siret": "1" * 15}, "siret"),
            ({"versant": "UNKNOWN"}, "versant"),
            ({"gestion_ats": None}, "gestion_ats"),
        ],
    )
    def test_refuses_invalid_body(self, staff_client, overrides, invalid_field):
        response = _post(staff_client, _body(**overrides))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert list(response.json()) == [invalid_field]
        assert not OrganismeModel.objects.exists()

    @pytest.mark.parametrize(
        "missing_field", ["nom", "siret", "versant", "gestion_ats"]
    )
    def test_refuses_missing_field(self, staff_client, missing_field):
        body = _body()
        del body[missing_field]

        response = _post(staff_client, body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert list(response.json()) == [missing_field]
