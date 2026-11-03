from unittest.mock import patch

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeQuerySet
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)

RECHERCHE_URL = reverse("recruteur:organismes_recherche")
TAILLE_PAR_DEFAUT = 25


@pytest.fixture
def staff_client(api_client):
    api_client.force_login(UtilisateurDjangoFactory(is_staff=True))
    return api_client


class TestRechercheOrganismes:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECHERCHE_URL, {"nom": "mairie"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refuses_non_staff(self, authenticated_client):
        response = authenticated_client.get(RECHERCHE_URL, {"nom": "mairie"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": OperationOrganismeRefusee().message}

    def test_returns_uuid_nom_siret(self, staff_client):
        organisme = OrganismeDjangoFactory(nom="Mairie de Lyon")

        response = staff_client.get(RECHERCHE_URL, {"nom": "mairie"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "uuid": str(organisme.id),
                "nom": "Mairie de Lyon",
                "siret": organisme.siret,
            }
        ]

    def test_ignores_case_and_accents(self, staff_client):
        organisme = OrganismeDjangoFactory(nom="École nationale")
        OrganismeDjangoFactory(nom="Préfecture")

        response = staff_client.get(RECHERCHE_URL, {"nom": "ECOLE"})

        assert [o["uuid"] for o in response.json()] == [str(organisme.id)]

    def test_orders_by_nom(self, staff_client):
        OrganismeDjangoFactory(nom="Mairie B")
        OrganismeDjangoFactory(nom="Mairie A")

        response = staff_client.get(RECHERCHE_URL, {"nom": "mairie"})

        assert [o["nom"] for o in response.json()] == ["Mairie A", "Mairie B"]

    def test_excludes_deleted_organismes(self, staff_client):
        OrganismeDjangoFactory(nom="Mairie supprimée", supprime_le=timezone.now())

        response = staff_client.get(RECHERCHE_URL, {"nom": "mairie"})

        assert response.json() == []

    def test_truncates_to_default_taille(self, staff_client):
        OrganismeDjangoFactory.create_batch(TAILLE_PAR_DEFAUT + 1, nom="Mairie")

        response = staff_client.get(RECHERCHE_URL, {"nom": "mairie"})

        assert len(response.json()) == TAILLE_PAR_DEFAUT

    def test_truncates_to_given_taille(self, staff_client):
        taille = 2
        OrganismeDjangoFactory.create_batch(taille + 1, nom="Mairie")

        response = staff_client.get(RECHERCHE_URL, {"nom": "mairie", "taille": taille})

        assert len(response.json()) == taille

    def test_query_count_does_not_grow_with_organismes(
        self, staff_client, django_assert_num_queries
    ):
        OrganismeDjangoFactory.create_batch(4, nom="Mairie")

        with django_assert_num_queries(
            1  # session lookup
            + 1  # user
            + 1  # organismes
        ):
            staff_client.get(RECHERCHE_URL, {"nom": "mairie"})

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"nom": ""},
            {"nom": "ab"},
            {"nom": "a" * 256},
            {"nom": "mairie", "taille": 0},
            {"nom": "mairie", "taille": 1_001},
            {"nom": "mairie", "taille": "abc"},
        ],
    )
    def test_invalid_query_is_rejected(self, staff_client, params):
        response = staff_client.get(RECHERCHE_URL, params)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert list(response.json()) == ["error"]

    @patch.object(OrganismeQuerySet, "search_name", side_effect=Exception("unexpected"))
    def test_returns_500_on_unexpected_error(self, _search_name, staff_client):
        response = staff_client.get(RECHERCHE_URL, {"nom": "mairie"})

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}
